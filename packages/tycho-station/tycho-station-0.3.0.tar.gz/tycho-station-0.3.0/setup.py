# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tychoreg', 'tychoreg.backends']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0', 'typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.8,<0.9'],
 's3': ['boto3>=1.16.62,<2.0.0']}

entry_points = \
{'console_scripts': ['tychoreg = tychoreg.cli:app']}

setup_kwargs = {
    'name': 'tycho-station',
    'version': '0.3.0',
    'description': 'A simple registry for storing versioned packages and archives',
    'long_description': '# Tycho Station\n\nA simple registry for storing versioned packages and archives.\n\n## Installation\n\nPython 3.6+ required\n\n`pip install tycho-station[s3]`\n\n## Usage\n\n```bash\n# initialize package on remote storage\n# pkgname = Name of package\n# filename =  Filename you would like package downloaded to when it\'s pulled\ntychoreg init pkgname filename\n\n# Push new version to remote storage\ntychoreg push pkgname 1.0 path_to/local/file --promote-latest\n\n# Pull latest package\ntychoreg pull pkgname\n# Outputs to tycho_packages/{filename} by default\n\n# Pull specific version\ntychoreg pull pkgname --version 1.0\n# Outputs to tycho_packages/{filename} by default\n\n# Pull multiple packages at latest\ntychoreg pull-list pkgname1 pkgname2 pkgname3\n\n# More help\ntychoreg {command} --help\n```\n## Configuration\n\nThe default configuration file is `.tychoreg.json`. You can use the `--config` option to change this path.\n\n**Example Configuration**\n\n```json\n{\n  "tycho": {\n    "backend": "s3",\n    "outdir": "tycho_packages"\n  },\n  "s3": {\n    "bucket": "my-registry",\n    "region_name": "us-east-1",\n    "aws_access_key_id": "KEYHERE",\n    "aws_secret_access_key": "SECRETHERE"\n  }\n}\n```\n\nNote: s3 attributes can be anything that is accepted by `boto3.client(\'s3\', **kwargs)` except for `bucket` which is passed in later.\n\n**Example Configuration Using Environment Variables**\n\nFor this example, a Read only key is set for pulling packages by everyone and users with escalated privileges can use a Write key.\n\n```json\n{\n  "s3": {\n    "bucket": "my-registry",\n    "region_name": "us-east-1",\n    "aws_access_key_id": {\n        "env": "REG_WRITE_KEY",\n        "default": "KEYHERE"\n    },\n    "aws_secret_access_key": {\n        "env": "REG_WRITE_SECRET",\n        "default": "SECRETHERE"\n    }\n  }\n}\n```\n\n**Loading a DotEnv file**\n```json\n    ...\n    "tycho": {\n        "dotenv": "/home/paul/cspace/tycho-station/.env"\n    },\n    ...\n```\n\n\n## Motivations\n\nDuring the course of development you often need to store versioned packages that don\'t nicely fit into any packaging ecosystem. And even when they do fit into an ecosystem such as NPM, PyPi, Conan, etc sometimes you do not want to maintain the infrastructure behind those packaging systems. I wanted a simple way to store files on a private remote storage and pull down versions as needed. Thus Tycho Station was conceived.\n\nTycho Station lets you store archives such as tarballs and zip files but also really anything on a remote storage system in a versioned fashion and then pull them down as needed.\n\n## Architecture\n\nTycho Station is designed to work with multiple storage systems but right now the first and default system is Amazon S3 storage. Packages are organized like shown below.\n\n```\nbucket\n│\n└───package_name_1\n│   │   tycho.json\n│   │   tycho_1.0.pkg\n│   │   tycho_1.1.pkg\n│   │   tycho_2.0.pkg\n│\n└───package_name_2\n    │   tycho.json\n    │   tycho_1.0.pkg\n    │   tycho_1.1.pkg\n    │   tycho_2.0.pkg\n```\n\n**tycho.json**\n\nThis file is what tracks the package meta data.\n\n```json\n{\n  "localname": "narf.tar.gz",\n  "latest": "1.0"\n}\n```\n\n**tycho.json Attributes**\n| Name           | Description  | Command(s)  |\n| :------------- | :----------- | :---------- |\n| localname      | Filename used when downloading the package. | Set by `init` command |\n| latest         | Version that is downloaded when `latest` is requested. | Updated when `promote` command is used or `--promote-latest` flag is used with the `push` command. |\n',
    'author': 'Paul Bailey',
    'author_email': 'paul@cognitivespace.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cognitive-space/tycho-station',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
