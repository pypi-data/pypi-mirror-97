# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextcloud_notes_api']

package_data = \
{'': ['*']}

install_requires = \
['requests-mock>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'nextcloud-notes-api',
    'version': '1.0.0',
    'description': 'A Nextcloud Notes app API wrapper',
    'long_description': "# nextcloud-notes-api\n\n[![Test](https://github.com/coma64/nextcloud-notes-api/workflows/Test/badge.svg)](https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ATest)\n[![Super-Linter](https://github.com/coma64/nextcloud-notes-api/workflows/Super-Linter/badge.svg)](https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ASuper-Linter)\n[![Coverage](https://img.shields.io/codecov/c/github/coma64/nextcloud-notes-api?color=%2334D058)](https://codecov.io/gh/coma64/nextcloud-notes-api)\n\nA [Nextcloud Notes app](https://github.com/nextcloud/notes) API wrapper.\n\n```py\nfrom nextcloud_notes_api import NotesApi, Note\n\napi = NotesApi('username', 'pass', 'hostname')\n\nnote = Note('Shopping List', 'Spam', favorite=True)\napi.create_note(note)\n```\n\n_*nextcloud-notes-api is not supported nor endorsed by Nextcloud.*_\n\n## Installation\n\n```sh\npip install nextcloud-notes-api\n```\n\n## Documentation\n\nThe docs are available on [Github Pages](https://coma64.github.io/nextcloud-notes-api/).\n\n## Contributing\n\nPull requests are welcome. For major changes,\nplease open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests and documentation as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'coma64',
    'author_email': 'coma64@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coma64/nextcloud-notes-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
