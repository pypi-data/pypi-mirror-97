import pip
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile


logger = getLogger(name=__name__)


def download_requirements(requirements_file: Path, destination: Path):
	with TemporaryDirectory() as tmp:
		pip_args = [
			'download',
			'--platform', 'manylinux1_x86_64',
			'--python-version', '3.6',
			'--implementation', 'cp',
			'--abi', 'cp36m',
			'--prefer-binary',
			'--only-binary', ':all:',
			'--requirement', str(requirements_file),
			'--dest', tmp,
		]
		logger.debug('Running pip.main with args %r', pip_args)
		result = pip.main(pip_args)
		logger.debug('pip result: %r', result)
		if result != 0:
			raise RuntimeError(f'pip failed with code {result!r}')

		for tmp_wheel in Path(tmp).iterdir():
			wheel_path = destination.joinpath(tmp_wheel.name)
			yield tmp_wheel.rename(wheel_path)


def wheel_package_name(wheel: Path):
	with ZipFile(wheel) as wheel_zip:
		metadata_items = []
		for item_info in wheel_zip.infolist():
			item_path = Path(item_info.filename)
			try:
				parent_name, name = item_path.parts
			except ValueError:
				continue

			if name != 'METADATA':
				continue

			if not parent_name.endswith('.dist-info'):
				continue

			metadata_items.append(item_info.filename)

		try:
			metadata_path, = metadata_items
		except ValueError:
			raise ValueError(
				'Unable to resolve metadata file from candidates'
				f' {metadata_items}'
			)

		with wheel_zip.open(metadata_path) as metadata:
			for line in metadata.readlines():
				if line.startswith(b'Name: '):
					_, package_name = line.strip().split(b': ')
					return package_name.decode()
			else:
				raise KeyError("No 'Name' entry in wheel metadata")


if __name__ == '__main__':
	import sys
	print(wheel_package_name(sys.argv[1]))