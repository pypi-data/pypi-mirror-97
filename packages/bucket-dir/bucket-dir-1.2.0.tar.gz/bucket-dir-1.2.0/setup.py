# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bucket_dir']

package_data = \
{'': ['*'], 'bucket_dir': ['templates/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'boto3>=1.17.11,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'humanize>=3.2.0,<4.0.0',
 'rich>=9.11.0,<10.0.0']

entry_points = \
{'console_scripts': ['bucket-dir = bucket_dir:run_cli']}

setup_kwargs = {
    'name': 'bucket-dir',
    'version': '1.2.0',
    'description': 'Generate directory listings for S3 statically hosted content.',
    'long_description': '# bucket-dir\n\n<a href="https://github.com/hmrc"><img alt="PyPI" src="https://img.shields.io/badge/HMRC-Digital-FFA500?style=flat&labelColor=000000&logo=gov.uk"></a>\n<a href="https://pypi.org/project/bucket-dir/"><img alt="PyPI" src="https://img.shields.io/pypi/v/bucket-dir"></a>\n<img alt="PyPI" src="https://img.shields.io/pypi/pyversions/bucket-dir">\n<a href="https://github.com/hmrc/bucket-dir/blob/master/LICENSE"><img alt="License: Apache 2.0" src="https://img.shields.io/github/license/hmrc/bucket-dir"></a>\n<a href="https://github.com/hmrc/bucket-dir"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n**bucket-dir** is a utility for generating a browsable directory tree for an AWS S3 bucket.\n\n!["Sample image"](/docs/sample.png "A sample of bucket-dir output.")\n\nIt was built in order to host Maven and Ivy repositories in S3 and serve them via CloudFront, but it could meet other needs too.\n\n## Installation\n\n```\npip install bucket-dir\n```\n## Usage\n\nRun `bucket-dir` with the name of the bucket you wish to index as a parameter:\n\n```\nbucket-dir foo-bucket\n```\n\nUse `bucket-dir --help` for all arguments.\n\nBe sure to provide the command with credentials that allow it to perform ListBucket and PutObject calls against the bucket. E.g. with [aws-vault](https://github.com/99designs/aws-vault):\n\n```\naws-vault exec foo-profile -- bucket-dir foo-bucket\n```\n\n### Character support\n\n`bucket-dir` supports objects using any of the _Safe characters_ listed in the S3 [object key naming guidelines](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-guidelines).\n\nThe exception to the above rule is using forward slashes consecutively (e.g. `my-folder//my-object`). This results in a folder called `/`, which breaks hyperlinks.\n\nUse of characters in the _Characters that might require special handling_ list is currently unsupported but is theoretically ok.\n\nSome characters in _Characters to avoid_ may also work, but you\'re on your own.\n\n## Development\n\nStart with `make init`. This will install prerequisties and set up a poetry managed virtual environment containing all the required runtime and development dependencies.\n\nUnit testing can be performed with `make test`. If you want to run pytest with other options, use `poetry run pytest ...`.\n\nYou can execute the source code directly with `poetry run bucket-dir`.\n\nFinally, you can build with `make build`. This will update dependencies, run security checks and analysis and finally package the code into a wheel and archive.\n\nPublishing can be performed with `make publish`, but this is only intended to run in CI on commit to the main branch. If running locally, you need to have PyPI credentials set as env vars.\n\nFor other rules, see the [Makefile](Makefile).\n\nIf you are a collaborator, feel free to make changes directly to the main branch. Otherwise, please raise a PR. Don\'t forget to bump the version in [pyproject.toml](pyproject.toml).\n\n## License\n\nThis code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").\n',
    'author': 'Dave Randall',
    'author_email': '19395688+daveygit2050@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hmrc/bucket-dir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
