# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydebuginfod']

package_data = \
{'': ['*']}

install_requires = \
['bison>=0.1.2,<0.2.0',
 'boto3>=1.17.22,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'xdgappdirs>=1.4.5,<2.0.0']

setup_kwargs = {
    'name': 'pydebuginfod',
    'version': '0.2.0',
    'description': 'A python client for the debuginfod server',
    'long_description': '# pydebuginfod\n\npydebuginfod is a Python client implementation of the [debuginfod\nspec](https://www.mankier.com/8/debuginfod).\n\n![PyPI](https://img.shields.io/pypi/v/pydebuginfod)\n![Build](https://github.com/schultetwin1/pydebuginfod/workflows/CI/badge.svg)\n\n```python\nimport pydebuginfod\n\nclient = pydebuginfod.Client()\ndbginfo = client.get_debuginfo("c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b")\ndbginfo\n>>> \'/home/matt/.cache/debuginfod/buildid/c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b/debuginfo\'\n\nclient = pydebuginfod.Client()\nexecutable = client.get_executable("c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b")\ndbginfo\n>>> \'/home/matt/.cache/debuginfod/buildid/c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b/executable\'\n```\n\npydebuginfod allows you to easily get started with debuginfod.\n\n## Configurations\n\npydebuginfod allows configurations to passed in via:\n\n* A configuration file\n* ENV variables\n* Member variables\n\nConfigurations are set in that order (config file < env vars < direct).\n\nThe following items can be configured:\n\n* URLs: The URLs of the servers you are querying\n* Cache-Path: The cache location to store the downloaded artifacts\n* Verbose: Sets the logging level to verbose\n* Timeout: How long to wait on a connection before giving up\n* Progress: Show download progress via stdout during download?\n\n### Configuration File\n\nThe configuraton file follows the\n[XDG](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)\nspecification. pydebuginfod will look for a file named `pydebuginfo.yml`\nunder the `XDG_CONFIG_HOME` directory.\n\nThe structure of the yaml file is as follows\n\n```yml\ncache-path: /opt/cache\nverbose: false\ntimeout: 90\nprogress: true\nurls:\n    - "https://server1.com"\n    - "https://server2/com"\n```\n\n### Environment Variables\n\n* DEBUGINFOD_CACHE_PATH\n* DEBUGINFOD_VERBOSE\n* DEBUGINFOD_TIMEOUT\n* DEBUGINFOD_PROGRESS\n* DEBUGINFOD_URLS\n\n### Member variables\n\n```python\nclient = pydebuginfod.Client()\nclient.cache = "/opt/cache"\nclient.verbose = False\nclient.timeout = 90\nclient.progress = True\nclient.urls = ["https://server1.com"]\n```',
    'author': 'Matt Schulte',
    'author_email': 'schultetwin1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
