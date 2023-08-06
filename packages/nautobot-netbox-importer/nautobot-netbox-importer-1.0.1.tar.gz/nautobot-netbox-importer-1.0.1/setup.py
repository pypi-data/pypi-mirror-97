# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_netbox_importer',
 'nautobot_netbox_importer.diffsync',
 'nautobot_netbox_importer.diffsync.adapters',
 'nautobot_netbox_importer.diffsync.models',
 'nautobot_netbox_importer.management.commands',
 'nautobot_netbox_importer.tests']

package_data = \
{'': ['*'], 'nautobot_netbox_importer.tests': ['fixtures/*']}

install_requires = \
['diffsync>=1.2.0,<2.0.0', 'nautobot']

setup_kwargs = {
    'name': 'nautobot-netbox-importer',
    'version': '1.0.1',
    'description': 'Data importer from NetBox 2.10.x to Nautobot',
    'long_description': '# Nautobot NetBox Importer\n\nA plugin for [Nautobot](https://github.com/nautobot/nautobot).\n\n## Installation\n\nThe plugin is available as a Python package in PyPI and can be installed with pip:\n\n```shell\npip install nautobot-netbox-importer\n```\n\n> The plugin is compatible with Nautobot 1.0 and can handle JSON data exported from NetBox 2.10.3 through 2.10.5 at present.\n\nOnce installed, the plugin needs to be enabled in your `nautobot_config.py`:\n\n```python\nPLUGINS = ["nautobot_netbox_importer"]\n```\n\n## Usage\n\n### Getting a data export from NetBox\n\nFrom the NetBox root directory, run the following command:\n\n```shell\npython netbox/manage.py dumpdata \\\n    --traceback --format=json \\\n    --exclude admin.logentry --exclude sessions.session \\\n    --exclude extras.ObjectChange --exclude extras.Script --exclude extras.Report \\\n    > /tmp/netbox_data.json\n```\n\n### Importing the data into Nautobot\n\nFrom the Nautobot root directory, run `nautobot-server import_netbox_json <json_file> <netbox_version>`, for example `nautobot-server import_netbox_json /tmp/netbox_data.json 2.10.3`.\n\n## Contributing\n\nMost of the internal logic of this plugin is based on the [DiffSync](https://github.com/networktocode/diffsync) library, which in turn is built atop [Pydantic](https://github.com/samuelcolvin/pydantic/).\nA basic understanding of these two libraries will be helpful to those wishing to contribute to this project.\n\nPull requests are welcomed and automatically built and tested against multiple version of Python and multiple versions of Nautobot through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.\n\nThe project is following Network to Code software development guideline and is leveraging:\n- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n- Poetry for packaging and dependency management.\n\n### CLI Helper Commands\n\nThe project includes a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`.\n\nEach command can be executed with `invoke <command>`. All commands support the argument `--python-ver` if you want to manually define the version of Python to use. Each command also has its own help `invoke <command> --help`\n\n#### Local dev environment\n```\n  build            Build all docker images.\n  debug            Start Nautobot and its dependencies in debug mode.\n  destroy          Destroy all containers and volumes.\n  restart          Restart Nautobot and its dependencies.\n  start            Start Nautobot and its dependencies in detached mode.\n  stop             Stop Nautobot and its dependencies.\n```\n\n#### Utility\n```\n  cli              Launch a bash shell inside the running Nautobot container.\n  create-user      Create a new user in django (default: admin), will prompt for password.\n  makemigrations   Run Make Migration in Django.\n  nbshell          Launch a nbshell session.\n```\n#### Testing\n\n```\n  bandit           Run bandit to validate basic static code security analysis.\n  black            Run black to check that Python files adhere to its style standards.\n  flake8           This will run flake8 for the specified name and Python version.\n  pydocstyle       Run pydocstyle to validate docstring formatting adheres to standards.\n  pylint           Run pylint code analysis.\n  tests            Run all tests for this plugin.\n  unittest         Run Django unit tests for the plugin.\n```\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [#nautobot slack channel](https://networktocode.slack.com/).\nSign up [here](http://slack.networktocode.com/)\n\n## Screenshots\n\n![Screenshot of the start of synchronization](https://raw.githubusercontent.com/nautobot/nautobot-plugin-netbox-importer/develop/media/screenshot1.png "Beginning synchronization")\n\n![Screenshot of the completed process](https://raw.githubusercontent.com/nautobot/nautobot-plugin-netbox-importer/develop/media/screenshot2.png "Synchronization complete!")\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-plugin-netbox-importer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
