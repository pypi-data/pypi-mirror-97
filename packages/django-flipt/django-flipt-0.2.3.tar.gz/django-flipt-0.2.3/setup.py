# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flipt', 'flipt.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.0,<4.0.0', 'flipt-grpc-python>=0.2.0,<0.3.0']

extras_require = \
{'rest': ['djangorestframework>=3.12.2,<4.0.0']}

setup_kwargs = {
    'name': 'django-flipt',
    'version': '0.2.3',
    'description': 'Flipt Integration for Django and Django REST Framework',
    'long_description': '# django-flipt\n\n<p>\n<img src="https://img.shields.io/pypi/v/django-flipt">\n<img src="https://img.shields.io/pypi/l/django-flipt">\n<img src="https://img.shields.io/pypi/pyversions/django-flipt">\n<img src="https://img.shields.io/pypi/dm/django-flipt">\n<img src="https://img.shields.io/github/workflow/status/earthpyy/django-flipt/CI/main">\n<img src="https://img.shields.io/github/workflow/status/earthpyy/django-flipt/CodeQL/main?label=CodeQL">\n</p>\n\n<p>Flipt Integration for Django and Django REST Framework</p>\n\n## Installation\n\n```shell\npip install django-flipt\n```\n\n## Usage\n\n1. Add `flipt` into `INSTALLED_APPS`\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'flipt\',\n]\n```\n\n2. Define Flipt gRPC endpoint in `settings.py`\n\n```python\nFLIPT_GRPC_HOST = \'flipt:9000\'\n```\n\n3. Ready to go!\n\n### Overriding Flags\n\nYou can override any flag by defining your flag key and overriding value\n\n```python\nFLIPT_FLAG_OVERRIDDEN = {\n    \'some-flag-key\': True\n}\n```\n\n### Available Classes/Functions\n\n- `flag_enabled`\n- `flag_disabled`\n- `FlaggedRouter`\n- `@flag_check`\n- `@override_flags`\n- `{% featureflag %} ... {% endfeatureflag %}`\n- `FeatureFlagListView`\n\n## Development\n\n### Requirements\n\n- Docker\n\n### Run Project\n\n```shell\n$ make\n```\n\n### Linting/Test Project\n\n```shell\n$ make lint\n$ make test\n```\n\n## Credits\n\n- [Flipt](https://flipt.io)\n- Inspired by [django-flags](https://github.com/cfpb/django-flags)\n',
    'author': 'Preeti Yuankrathok',
    'author_email': 'preetisatit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/earthpyy/django-flipt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
