import json
import importlib.util
import shutil
import sys
from copy import deepcopy
from logging import getLogger
from inspect import Signature
from pathlib import Path

from docstring_parser import parse as parse_docstring
import yaml
from roboversion import get_version

try:
	import phantom
except ImportError:
	from phantom_dev import dummy_phantom
	sys.modules['phantom'] = dummy_phantom

from phantom_dev import action_handler
from .requirements import download_requirements, wheel_package_name


logger = getLogger(name=__name__)


class App:
	ANNOTATION_MAP = {
		bool: 'boolean',  # Check bool before int as bool is an int subclass
		str: 'string',
		int: 'numeric',
		float: 'numeric',
	}

	REQUIRED_ACTION_KEYS = {
		'name',
		'description',
		'parameters',
	}

	REQUIRED_PARAMETER_KEYS = [
		'description',
		'data_type',
	]

	DEFAULT_APP_TYPE = 'prototype'
	DEFAULT_ACTION_TYPE = 'prototype'

	DEFAULT_LOGO_PATH = Path(__file__).absolute().parent.joinpath(
		'default_logo.svg')

	def __init__(self, path):
		self.path = Path(path).absolute()
		logger.debug('Initialising app with path %r', self.path)
		metadata_path, = path.glob('metadata.yaml')
		with metadata_path.open() as metadata_file:
			self.metadata = yaml.safe_load(metadata_file)

	@property
	def id(self):
		return self.metadata['id']

	@property
	def name(self):
		return self.metadata.get('name', self.path.name)

	@property
	def main_module(self):
		try:
			return self.metadata['main_module']
		except KeyError:
			pass

		module_path, = self.path.glob('connector.py')
		return module_path.name

	@property
	def package_name(self):
		try:
			return self.metadata['package_name']
		except KeyError:
			pass

		compact_name = self.name.lower()
		for separator in [None, '_']:
			name_tokens = compact_name.split(sep=separator)
			compact_name = ''.join(name_tokens)

		return compact_name

	@property
	def type(self):
		try:
			return self.metadata['type']
		except KeyError:
			pass

		logger.warning(
			'No app type specified; using default type %r',
			self.DEFAULT_APP_TYPE,
		)

		return self.DEFAULT_APP_TYPE

	def get_version(self, *args, **kwargs):
		try:
			return self.metadata['version']
		except KeyError:
			pass

		try:
			version = get_version(*args, project_path=self.path, **kwargs)
		except Exception:
			raise RuntimeError(
				'Unable to infer app version from project git repository;'
				' configure the repository or specify "version" in metadata'
			)

		return str(version)

	def get_connector(self):
		connector_path = self.path.joinpath(self.main_module)
		module_name = f'{connector_path.stem}_{self.id}'
		try:
			module = sys.modules[module_name]
		except KeyError:
			spec = importlib.util.spec_from_file_location(
				name=module_name, location=connector_path)
			
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			sys.modules[module_name] = module

		registered_connectors = action_handler.registered_connectors
		try:
			all_connectors = registered_connectors[module.__name__]
		except KeyError:
			logger.error(
				'module %r not found in registered connectors map %r',
				module,
				action_handler.registered_connectors,
			)

			raise

		try:
			connector_class, = all_connectors
		except ValueError:
			logger.error('Too many connectors')
			for connector in all_connectors:
				logger.error(
					'%r from module %r', connector, connector.__module__)
			raise

		return connector_class

	def get_logo_metadata(self):
		try:
			data = self.metadata['logo']
		except KeyError:
			try:
				logo_light_path, = self.path.glob('logo_light.*')
			except ValueError:
				try:
					logo_path, = self.path.glob('logo.*')
				except ValueError:
					logo_path = self.path.joinpath(
						f'logo{self.DEFAULT_LOGO_PATH.suffix}')

					shutil.copy2(self.DEFAULT_LOGO_PATH, logo_path)

				logo = logo_path.name
				return {'logo': logo}

			logo_light = logo_light_path.name
			logo_dark_path, = self.path.glob('logo_dark.*')
			logo_dark = logo_dark_path.name
			return {'logo': logo_light, 'logo_dark': logo_dark}

		if isinstance(data, str):
			return {'logo': data}

		return {'logo': data['light'], 'logo_dark': data['dark']}

	def get_configuration_metadata(self):
		data = self.metadata.get('configuration', {})
		output = {}
		for index, (name, item) in enumerate(data.items()):
			output[name] = item.copy()
			output[name]['order'] = index

		return output

	def get_pip_dependencies(self):
		pip_data = self.metadata.get('pip_dependencies', {})

		data = {}
		try:
			pypi_data = pip_data['pypi']
		except KeyError:
			pass
		else:
			data['pypi'] = [{'module': x} for x in pypi_data]

		try:
			wheel_data = pip_data['wheels']
		except KeyError:
			pass
		else:
			data['wheel'] = [
				{'module': x, 'input_file': f'wheels/{y}'}
				for x, y in wheel_data.items()
			]
		
		return data

	def get_consolidate_widgets_metadata(self):
		try:
			consolidate_widgets = self.metadata['consolidate_widgets']
		except KeyError:
			return {}

		return {'consolidate_widgets': consolidate_widgets}

	def get_url_metadata(self):
		try:
			url = self.metadata['url']
		except KeyError:
			return {}

		return {'url': url}


	def get_action_metadata(self):
		for identifier, action_data, parameter_items in (
				self._get_merged_action_metadata()
		):

			action_parameters = {}
			action_data['parameters'] = action_parameters
			action_output = action_data.setdefault('output', {})
			for name, parameter_data in parameter_items:
				for key in self.REQUIRED_PARAMETER_KEYS:
					try:
						parameter_data[key]
					except KeyError as error:
						message = (
							f'Parameter {name!r} for action {identifier!r}'
							f' is missing a value for {key!r}'
						)
						
						raise KeyError(message) from error

				action_parameters[name] = parameter_data
				datapath = f'action_result.parameter.{name}'
				parameter_output = action_output.setdefault(datapath, {})
				data_type = parameter_data['data_type']
				parameter_output.setdefault('data_type', data_type)
				try:
					contains = parameter_data['contains']
				except KeyError:
					pass
				else:
					parameter_output.setdefault('contains', contains)

			action_data.setdefault('read_only', False)
			action_data.setdefault('versions', 'EQ(*)')
			try:
				action_data['type']
			except KeyError:
				logger.warning(
					f'Missing type for action {identifier!r};'
					f' setting type to {self.DEFAULT_ACTION_TYPE!r}'
				)

				action_data['type'] = self.DEFAULT_ACTION_TYPE

			action_data['action'] = action_data.pop('name')
			output = action_data.get('output', {})
			new_output = []
			for data_path, output_data in output.items():
				output_item = {**output_data, 'data_path': data_path}
				new_output.append(output_item)
			
			action_data['output'] = new_output

			yield {'identifier':identifier, **action_data}


	def get_json(self):
		json_data = {
			'appid': self.id,
			'name': self.name,
			'description': self.metadata['description'],
			'type': self.type,
			'main_module': self.main_module,
			'app_version': self.get_version(),
			'pip_dependencies': self.get_pip_dependencies(),
			'min_phantom_version': self.metadata.get(
				'min_phantom_version', '4.8.0'),
			'product_vendor': self.metadata['product']['vendor'],
			'product_name': self.metadata['product']['name'],
			'product_version_regex': self.metadata['product'].get(
				'version_regex', '.*'),
			'publisher': self.metadata['publisher'],
			'package_name': f'phantom_{self.package_name}',
			'license': self.metadata['license'],
			'configuration': self.get_configuration_metadata(),
			**self.get_url_metadata(),
			**self.get_logo_metadata(),
			'actions': list(self.get_action_metadata()),
			'python_version': '3',
		}

		return json_data

	def build(self, directory: Path):
		package_name = f'ph{self.package_name}'
		package_path = directory.joinpath(package_name)
		if package_path.exists():
			shutil.rmtree(package_path)

		copy_tree(self.path, package_path)

		action_handler_path_string, = action_handler.__path__
		action_handler_path = Path(action_handler_path_string).absolute()
		top_package_name = action_handler_path.parent.name
		dependency_destination = package_path.joinpath(
			'dependencies', top_package_name)

		dependency_destination.mkdir(exist_ok=True, parents=True)
		dependency_path = dependency_destination.joinpath(
			action_handler_path.name)

		copy_tree(action_handler_path, dependency_path)

		app_json = self.get_json()

		requirements_file = package_path.joinpath('requirements.txt')
		if requirements_file.exists():
			wheels = package_path.joinpath('wheels')
			wheels.mkdir(exist_ok=True)
			for wheel in download_requirements(requirements_file, wheels):
				name = wheel_package_name(wheel)
				data = {
					'module': name,
					'input_file': str(wheel.relative_to(package_path)),
				}
				wheels_data = app_json['pip_dependencies'].setdefault(
					'wheel', [])

				wheels_data.append(data)

		json_path = package_path.joinpath(f'autogenerated.json')
		with json_path.open('w') as json_file:
			json.dump(app_json, json_file, indent='\t')

		logger.debug('Wrote app JSON to %r', json_path)

		return package_path

	def _get_merged_action_metadata(self):
		try:
			data = self.metadata['actions']
		except KeyError:
			actions_metadata = {}
		else:
			actions_metadata = deepcopy(data)

		connector_class = self.get_connector()
		for handler in connector_class.get_handlers():
			identifier = handler.action_identifier
			action_data = actions_metadata.setdefault(identifier, {})
			handler_method = handler.handler_method
			name_tokens = handler_method.__name__.split('_')
			action_data.setdefault('name', ' '.join(name_tokens))
			docstring = handler_method.__doc__
			if docstring is not None:
				method_doc = parse_docstring(docstring)
				description_components = [
					method_doc.short_description, method_doc.long_description]

				description = '\n\n'.join(
					x for x in description_components if x is not None)

				action_data.setdefault('description', description)

			if handler.data_contains_map is not None:
				output = action_data.setdefault('output', {})
				for key, type_obj in handler.data_contains_map.items():
					result_data = output.setdefault(
						f'action_result.data.*.{key}', {})
					contains = action_handler.contains_map[type_obj]
					result_data.setdefault('contains', contains)
					data_type = self._get_data_type(type_obj)
					result_data.setdefault('data_type', data_type)

			if handler.summary_contains_map is not None:
				output = action_data.setdefault('output', {})
				for key, type_obj in handler.summary_contains_map.items():
					summary_data = output.setdefault(
						f'action_result.summary.{key}', {})
					try:
						contains = action_handler.contains_map[type_obj]
					except KeyError:
						logger.debug(
							'Summary type %r has no contains', type_obj)

						contains = []

					summary_data.setdefault('contains', contains)
					data_type = self._get_data_type(type_obj)
					summary_data.setdefault('data_type', data_type)

			parameters_data = action_data.pop('parameters', {})
			parameter_items = self._populate_parameter_defaults(
				method=handler_method,
				parameters_data=parameters_data,
				method_doc=method_doc,
			)
			yield identifier, action_data, parameter_items

	def _populate_parameter_defaults(
			self, method, parameters_data, method_doc):

		signature = Signature.from_callable(method)
		for name, method_parameter in signature.parameters.items():
			if name in ['self', 'context']:
					continue

			if method_parameter.kind in [
					method_parameter.VAR_POSITIONAL,
					method_parameter.VAR_KEYWORD,
			]:
				continue
			
			try:
				parameter_data = parameters_data[name]
			except KeyError:
				data = {}
			else:
				data = deepcopy(parameter_data)

			if data:
				logger.debug('Specified parameter %r metadata: %r', name, data)
			else:
				logger.warning(
					'Specified parameter %r metadata: %r', name, data)
				

			if method_parameter.default is method_parameter.empty:
				data.setdefault('required', True)
			else:
				data.setdefault('required', False)
				data.setdefault('default', method_parameter.default)

			for doc_param in method_doc.params:
				if doc_param.arg_name == name:
					data.setdefault('description', doc_param.description)
					break

			annotation = method_parameter.annotation
			if annotation is method_parameter.empty:
				continue

			try:
				data_type = data['data_type']
			except KeyError:
				data['data_type'] = self._get_data_type(annotation)

			try:
				contains = data['contains']
			except KeyError:
				try:
					contains = action_handler.contains_map[annotation]
				except KeyError:
					logger.error(
						f'Unable to infer parameter {name!r} contains data from'
						f' annotation {annotation!r}'
					)

				else:
					data['contains'] = contains

			yield name, data

	@classmethod
	def _get_data_type(cls, type_obj):
		logger.debug('Getting data_type for %r', type_obj)
		for base_type, data_type in cls.ANNOTATION_MAP.items():
			if issubclass(type_obj, base_type):
				return data_type

		raise KeyError(f'{type_obj} not in {cls.ANNOTATION_MAP}')


def copy_tree(source: Path, destination: Path):
	shutil.copytree(source, destination, ignore=lambda x, y: ['__pycache__'])
