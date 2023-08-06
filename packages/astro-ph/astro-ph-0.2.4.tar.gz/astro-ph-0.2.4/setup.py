# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astro_ph']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4.0',
 'feedparser>=6.0,<7.0',
 'fire>=0.4,<0.5',
 'pyppeteer>=0.2,<0.3',
 'typing-extensions>=3.7,<4.0']

entry_points = \
{'console_scripts': ['astro-ph = astro_ph.cli:cli']}

setup_kwargs = {
    'name': 'astro-ph',
    'version': '0.2.4',
    'description': 'Translate and post arXiv articles to various apps',
    'long_description': '# astro-ph\n\n[![PyPI](https://img.shields.io/pypi/v/astro-ph.svg?label=PyPI&style=flat-square)](https://pypi.org/project/astro-ph/)\n[![Python](https://img.shields.io/pypi/pyversions/astro-ph.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/astro-ph/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/astro-ph/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/astro-ph/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nTranslate and post arXiv articles to various apps\n\n## Installation\n\nUse pip or other package manager to install the Python package.\n\n```shell\n$ pip install astro-ph\n```\n\n## Usage\n\nAfter installation, command line interface, `astro-ph`, is available, with which you can translate and post arXiv articles to various apps.\nNote that only `slack` app is currently available.\nIn this case, you need to [create a custom Slack app to get an URL of incoming webhook](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack).\n\n```shell\n$ astro-ph slack --keywords galaxy,galaxies \\\n                 --categories astro-ph.GA,astro-ph.IM \\\n                 --lang_to ja \\\n                 --webhook_url https://hooks.slack.com/services/***/***\n```\n\nThe posted article looks like this.\n\n![astro-ph-slack.png](https://raw.githubusercontent.com/astropenguin/astro-ph/master/docs/_static/astro-ph-slack.png)\n\nFor detailed information, see the built-in help by the following command.\n\n```shell\n$ astro-ph slack --help\n```\n\n## Example\n\nIt would be nice to regularly run the command by GitHub Actions.\nHere is a live example in which daily (2 days ago) arXiv articles in [astro-ph.GA](https://arxiv.org/list/astro-ph.GA/new) and [astro-ph.IM](https://arxiv.org/list/astro-ph.IM/new) are posted to different channels of a Slack workspace.\n\n- [a-lab-nagoya/astro-ph-slack: Translate and post arXiv articles to Slack](https://github.com/a-lab-nagoya/astro-ph-slack)\n\n## References\n\n- [fkubota/Carrier-Owl: arxiv--> DeepL --> Slack](https://github.com/fkubota/Carrier-Owl)\n    - The astro-ph package is highly inspired by their work\n- [a-lab-nagoya/astro-ph-slack: Translate and post arXiv articles to Slack](https://github.com/a-lab-nagoya/astro-ph-slack)\n    - A live example using the astro-ph package\n- [pyppeteer/pyppeteer: Headless chrome/chromium automation library (unofficial port of puppeteer)](https://github.com/pyppeteer/pyppeteer)\n    - Used for async Chromium operation\n- [aio-libs/aiohttp: Asynchronous HTTP client/server framework for asyncio and Python](https://github.com/aio-libs/aiohttp)\n    - Used for async article posts to Slack\n- [google/python-fire: Python Fire is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object.](https://github.com/google/python-fire)\n    - Used for creating command line interface\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/astro-ph/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
