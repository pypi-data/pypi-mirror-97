# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['signal_cli_rest_api',
 'signal_cli_rest_api.app',
 'signal_cli_rest_api.app.api',
 'signal_cli_rest_api.app.api.api_v1',
 'signal_cli_rest_api.app.api.api_v1.endpoints',
 'signal_cli_rest_api.app.schemas']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'fastapi>=0.58.0,<0.59.0',
 'httpx>=0.16.1,<0.17.0',
 'pypng>=0.0.20,<0.0.21',
 'pyqrcode>=1.2.1,<2.0.0',
 'python-jose>=3.1.0,<4.0.0',
 'uvicorn>=0.11.5,<0.12.0']

setup_kwargs = {
    'name': 'signal-cli-rest-api',
    'version': '0.1.99',
    'description': '',
    'long_description': "# signal-cli-rest-api\nsignal-cli-rest-api is a wrapper around [signal-cli](https://github.com/AsamK/signal-cli) and allows you to interact with it through http requests.\n\n## Features\n* register/verify/unregister a number\n* send messages to multiple users/a group with one or multiple attachments\n* receive messages (with attachments)\n* block/unblock users and groups\n* link to existing device\n* list/create/update/leave groups\n* update profile (name/avatar)\n\n## To-Do\n* integrate dbus daemon for faster sending\n* authentication\n\n## Installation\n\n### pip\n\nIf you install signal-cli-rest-api through pip you need to manually install [signal-cli](https://github.com/AsamK/signal-cli) on your system.\n\n```console\n# by default the app will look for the signal config files in ~/.local/share/signal-cli\n# you can change the directory by setting the SIGNAL_CONFIG_PATH env var to the desired path\n# e.g. export SIGNAL_CONFIG_PATH=/opt/signal\npip install signal-cli-rest-api\nuvicorn signal_cli_rest_api.app.main:app --host 0.0.0.0 --port 8000\n```\n\n### Docker\n\n```console\nexport SIGNAL_DATA_DIR=~/signal/\ndocker run --name signal --restart unless-stopped -p 8000:8000 -v $SIGNAL_DATA_DIR:/root/.local/share/signal-cli sebastiannoelluebke/signal-cli-rest-api\n```\n\n### docker-compose\n```console\ngit clone https://github.com/SebastianLuebke/signal-cli-rest-api.git\ncd signal-cli-rest-api\n# docker-compose build\ndocker-compose up -d\n```\n\n## Security Notice\nsignal-cli-rest-api doesn't have any authentication for now. Everyone who knows the service address+port and the number is able to get your messages and send messages. So only use it a trusted environment and block external access.\n\n## Interactive Documentation\n\nAfter installing signal-cli-rest-api start it and open the following page [http://localhost:8000/docs](http://localhost:8000/docs)\n\n",
    'author': 'Sebastian Noel Lübke',
    'author_email': 'sebastian@luebke.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebastianLuebke/signal-cli-rest-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
