import logging
import sys
import tarfile
from argparse import ArgumentParser
from getpass import getpass
from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory
from uuid import uuid4

import yaml
from paramiko.client import SSHClient
from paramiko.sftp_client import SFTPClient

from phantom_dev.app import App


logger = logging.getLogger(name=__name__)


DEFAULT_DATA = Path(__file__).absolute().parent.joinpath('default_data')
DEFAULT_CONNECTOR = DEFAULT_DATA.joinpath('connector.py')
DEFAULT_METADATA = DEFAULT_DATA.joinpath('metadata.yaml')


class RemoteTemporaryFolder:
	def __init__(self, ssh_client: SSHClient):
		self.client = ssh_client
		self.path = None

	def __enter__(self):
		path = Path('/').joinpath('tmp', str(uuid4()))
		self.client.exec_command(f'mkdir -p {path}')
		self.path = path
		logger.debug('Created remote temporary directory %r', self.path)
		return self.path

	def __exit__(self, exc_type, exc_info, traceback):
		self.client.exec_command(f'rm -rf {self.path}')
		self.path = None


def package(app_directory: Path, destination: Path = None):
	logger.debug('App directory: %r', app_directory)
	app = App(path=app_directory)
	with TemporaryDirectory() as tmp:
		temp_path = Path(tmp)
		build_path = app.build(temp_path)
		if destination is None:
			tar_path = Path().joinpath(f'{app.package_name}.tgz')
		elif destination.is_dir():
			tar_path = destination.joinpath(f'{app.package_name}.tgz')
		else:
			tar_path = destination

		logger.debug('Packaging to destination %r', tar_path)
		if tar_path.exists():
			raise FileExistsError(
				f'Destination {tar_path!r} already exists')

		with tarfile.open(tar_path, 'w:gz') as tar:
			tar.add(build_path, arcname=build_path.name)

	return tar_path


def create(app_name, destination: Path = None, metadata_file: Path = None):
	app_directory_name = '_'.join(x.lower() for x in app_name.split())
	if destination is None:
		destination = Path().joinpath(app_directory_name)
	elif destination.is_dir():
		destination = destination.joinpath(app_directory_name)

	if metadata_file is None:
		metadata = {'name': app_name, 'id': str(uuid4())}
	else:
		with metadata_file.open() as metadata_yaml:
			metadata = yaml.safe_load(metadata_yaml)

	product_metadata = metadata.setdefault('product', {})
	for product_key in ['vendor', 'name']:
		if product_key in product_metadata:
			continue

		value = input(f'Product {product_key.title()}: ').strip()
		product_metadata[product_key] = value

	for key in ['description', 'publisher', 'license']:
		if key not in metadata:
			metadata[key] = input(f'{key.title()}: ').strip()

	destination.mkdir(exist_ok=False)
	copy2(DEFAULT_CONNECTOR, destination)
	new_metadata = destination.joinpath('metadata.yaml')

	with new_metadata.open('w') as metadata_yaml:
		yaml.safe_dump(metadata, metadata_yaml)

	return destination


def deploy(package_path: Path, phantom_location: str):
	try:
		credentials, phantom_location = phantom_location.split('@')
	except ValueError:
		username = None
		password = None
	else:
		try:
			username, password = credentials.split(':')
		except ValueError:
			username = credentials
			password = getpass(f'SSH password for {username}:')
		else:
			password = None if not password else password

	with SSHClient() as ssh_client:
		ssh_client.load_system_host_keys()
		ssh_client.connect(
			phantom_location, username=username, password=password)

		with RemoteTemporaryFolder(ssh_client=ssh_client) as tmp:
			remote_path = tmp.joinpath(package_path.name)
			with SFTPClient.from_transport(ssh_client.get_transport()) as sftp:
				sftp.put(str(package_path), str(remote_path))

			commands = [
				f'cd {tmp}',
				f'tar -zxvf {package_path.name}',
				f'cd $(ls --ignore={package_path.name})',
				'phenv python3 /opt/phantom/bin/py3/compile_app.pyc -i',
			]

			command_text = ';\n'.join(x.strip() for x in commands)
			logger.debug('Running commands: %r', command_text)

			stdin, stdout, stderr = ssh_client.exec_command(command_text)
			for line in stdout.readlines():
				print(line, end='')


def push(app_directory: Path, phantom_location: str):
	with TemporaryDirectory() as tmp_str:
		tmp = Path(tmp_str).absolute()
		package_path = package(app_directory, tmp)
		return deploy(
			package_path=package_path, phantom_location=phantom_location)


def main():
	root_parser = ArgumentParser(
		description='A Splunk>Phantom app development utility')
	root_parser.add_argument('-l', '--log-level', default='INFO')

	subparsers = root_parser.add_subparsers(
		title='Sub-commands',
		description=(
			'For more information on a sub-command, invoke it with `--help`'),
	)

	# package command
	package_parser = subparsers.add_parser(
		name='package',
		description=(
			'Build an installable package from an app project directory'),
	)

	app_directory_help = 'App project directory path'
	package_parser.set_defaults(function=package)
	package_parser.add_argument(
		'app_directory', type=Path, help=app_directory_help)
	package_parser.add_argument(
		'-o', '--output',
		type=Path,
		dest='destination',
		help=(
			'Output package path. If this is an existing directory, the'
			' package will be placed inside.'
		)
	)

	# create command
	create_parser = subparsers.add_parser(
		'create', description='Create a new Splunk>Phantom app project')
	create_parser.set_defaults(function=create)
	create_parser.add_argument('app_name', help='The name of the new app')
	create_parser.add_argument(
		'-d', '--destination',
		type=Path,
		help=(
			'The path to the new project directory. If this is an existing'
			' directory, the app directory will be placed inside.'
		),
	)
	create_parser.add_argument(
		'-m', '--metadata',
		type=Path,
		dest='metadata_file',
		help=(
			'The path to a YAML file containing metadata values for the new'
			' app'
		),
	)

	# deploy command
	deploy_parser = subparsers.add_parser(
		'deploy',
		description=(
			'Install a local app package on a remote Splunk>Phantom instance'),
	)
	deploy_parser.set_defaults(function=deploy)
	deploy_parser.add_argument(
		'package_path', type=Path, help='Local package path')

	phantom_location_help = (
			'Splunk>Phantom server location taking the form'
			' [username[:password]@]host'
	)
	deploy_parser.add_argument('phantom_location', help=phantom_location_help)

	# push command
	push_parser = subparsers.add_parser(
		'push',
		description=(
			'Combine `package` and `deploy` operations to build a package from'
			' the specified app project directory and install it on a remote'
			' Splunk>Phantom instance'
		),
	)
	push_parser.set_defaults(function=push)
	push_parser.add_argument(
		'app_directory', type=Path, help=app_directory_help)
	push_parser.add_argument('phantom_location', help=phantom_location_help)

	namespace = root_parser.parse_args(sys.argv[1:])
	arguments = vars(namespace)

	log_level = arguments.pop('log_level')
	logging.basicConfig(level=log_level.upper())
	logger.debug('parsed args: %r', namespace)
	
	try:
		command_function = arguments.pop('function')
	except KeyError:
		root_parser.print_usage()
		return

	logger.debug(
		'Calling %r with keyword arguments %r', command_function, arguments)

	return command_function(**arguments)


if __name__ == '__main__':
	main()
