# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbfcapi']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.4,<2.0']

extras_require = \
{'all': ['aiohttp[speedups]>=3.6,<4.0',
         'fastapi>=0.63.0,<0.64.0',
         'pyhumps>=1.3.1,<2.0.0',
         'requests>=2.24,<3.0',
         'uvicorn>=0.13.4,<0.14.0'],
 'api_async': ['aiohttp[speedups]>=3.6,<4.0', 'pyhumps>=1.3.1,<2.0.0'],
 'api_sync': ['pyhumps>=1.3.1,<2.0.0', 'requests>=2.24,<3.0'],
 'app': ['aiohttp[speedups]>=3.6,<4.0',
         'fastapi>=0.63.0,<0.64.0',
         'pyhumps>=1.3.1,<2.0.0',
         'uvicorn>=0.13.4,<0.14.0'],
 'client_async': ['aiohttp[speedups]>=3.6,<4.0'],
 'client_sync': ['requests>=2.24,<3.0'],
 'lib_async': ['aiohttp[speedups]>=3.6,<4.0'],
 'lib_sync': ['requests>=2.24,<3.0']}

setup_kwargs = {
    'name': 'bbfcapi',
    'version': '3.0.1',
    'description': 'API service, library and parser for BBFC',
    'long_description': '# BBFC API\n\n![PyPI](https://img.shields.io/pypi/v/bbfcapi)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bbfcapi)\n![PyPI - License](https://img.shields.io/pypi/l/bbfcapi)\n![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/fustra/bbfcapi)\n\nWeb API and Python library for [BBFC](https://bbfc.co.uk/).\n\n## Public REST API\n\n![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade-score/bbfcapi.fustra.uk?publish)\n![Security Headers](https://img.shields.io/security-headers?url=https%3A%2F%2Fbbfcapi.fustra.uk%2Fhealthz)\n<a href="https://uptime.statuscake.com/?TestID=SgEZQ2v2KF" title="bbfcapi uptime report">\n    <img src="https://app.statuscake.com/button/index.php?Track=K7juwHfXel&Days=7&Design=6"/>\n</a>\n\n* Hosted @ <https://bbfcapi.fustra.uk>\n* Documentation @ <https://bbfcapi.fustra.uk/redoc>\n* Alternative documentation @ <https://bbfcapi.fustra.uk/docs>\n\nTry it now:\n\n```console\n$ curl "https://bbfcapi.fustra.uk?title=interstellar"\n{"title":"Interstellar","ageRating":"12"}\n```\n\nUse the Python client:\n\n```console\n$ pip install bbfcapi[api_sync]\n```\n\n```py\n>>> from bbfcapi.api_sync import best_match\n>>> best_match("interstellar", 2014)\nFilm(title=\'INTERSTELLAR\', age_rating=<AgeRating.AGE_12: \'12\'>)\n```\n\n## Project Overview\n\nThe project is divided into:\n\n* "I want to self-host the REST API demoed above"\n    * BBFCAPI - Python REST Web API\n    * `pip install bbfcapi[app]`\n* "I want a Python library to talk to the REST API as demoed above"\n    * Python client for BBFCAPI\n    * `pip install bbfcapi[api_async]` (async variant)\n    * `pip install bbfcapi[api_sync]` (sync variant)\n* "I want a Python library to talk to the BBFC website"\n    * Python library for the BBFC website\n    * `pip install bbfcapi[lib_async]` (async variant)\n    * `pip install bbfcapi[lib_sync]` (sync variant)\n* "I want to download the raw HTML web pages from BBFC"\n    * Python network client for the BBFC website\n    * `pip install bbfcapi[client_async]` (async variant)\n    * `pip install bbfcapi[client_sync]` (sync variant)\n* "I want to parse the downloaded web pages from BBFC"\n    * Python HMTL parser for the BBFC web pages\n    * `pip install bbfcapi`\n\nSync versions use the `requests` library, while async variants use `aiohttp`.\n\n## High-Level REST Web API\n\nInstall `pip install bbfcapi[app]`.\n\nTo use the REST API to query BBFC, first run the web server:\n\n```console\n$ uvicorn bbfcapi.app:app\n```\n\nThen, to query the API using the Python library *synchronously*:\n\n```py\nfrom bbfcapi.api_sync import best_match\nbest_match("interstellar", base_url="http://127.0.0.1:8000")\n```\n\nOr, to query the API using the Python library *asynchronously*:\n\n```py\nfrom bbfcapi.api_async import best_match\nprint(await best_match("interstellar", base_url="http://127.0.0.1:8000"))\n```\n\n```py\nimport asyncio\nfrom bbfcapi.api_async import best_match\nprint(asyncio.run(best_match("interstellar", base_url="http://127.0.0.1:8000")))\n```\n\nOr, to query the API using `curl`:\n\n```console\n$ curl "127.0.0.1:8000?title=interstellar"\n{"title":"Interstellar",age_rating":"12"}\n```\n\nOr, to query the API from another web page:\n\n```js\nasync function call()\n{\n    const response = await fetch(\'http://127.0.0.1:8000/?title=interstellar\');\n    const responseJson = await response.json();\n    console.log(JSON.stringify(responseJson));\n}\ncall();\n```\n\nAdditional notes:\n\n* HTTP 404 Not Found is returned when there is no film found.\n* Browse documentation @ <http://127.0.0.1:8000/redoc>.\n* Or, browse documentation @ <http://127.0.0.1:8000/docs>.\n* Samples on hosting this web application are available in the repository\'s [/docs](/docs) folder.\n\n## High-Level Python Library\n\nTo use the library to get results from BBFC *synchronously*:\n\n```py\nfrom bbfcapi.lib_async import best_match\nprint(best_match(title="interstellar"))\n```\n\nTo use the library to get results from BBFC *asynchronously*:\n\n```py\nfrom bbfcapi.lib_async import best_match\nprint(await best_match(title="interstellar"))\n```\n\n```py\nimport asyncio\nfrom bbfcapi.lib_async import best_match\nprint(asyncio.run(best_match(title="interstellar")))\n```\n\n## Low-Level BBFC Network Client & Parser\n\nTo use the library to get raw HTML pages from BBFC *synchronously*:\n\n```console\n$ pip install bbfcapi[client_sync]`\n```\n\n```py\nfrom bbfcapi.client_sync import search\nprint(search(title="interstellar"))\n```\n\nTo use the library to get raw HTML pages from BBFC *asynchronously*:\n\n```console\n$ pip install bbfcapi[client_async]`\n```\n\n```py\nfrom bbfcapi.client_async import search\nprint(await search(title="interstellar"))\n```\n\n```py\nimport asyncio\nfrom bbfcapi.client_async import search\nprint(asyncio.run(search(title="interstellar")))\n```\n\nTo use the library to parse results from BBFC\'s GraphQL API:\n\n```console\n$ pip install bbfcapi[parser]`\n```\n\n```py\nfrom bbfcapi import parser\nprint(parser.best_autocomplete_match({"BBFC": "...graphql json..."}))\n```\n\n## Development\n\n1. `poetry install -E all` to set up the virtualenv (one-off)\n2. `poetry run uvicorn bbfcapi.apiweb:app --reload` to run the web server\n3. `make fix`, `make check`, and `make test` before committing\n\nThere is also `make test-live` which will run live integration tests against\nthe BBFC website.\n\n### Contributing\n\nPull requests are welcome :)\n\n### Publishing\n\nThis application is published on PyPi.\n\n1. Ensure you have configured the PyPi repository with Poetry (one-off)\n2. Run `make release` to execute the check-list\n\nTo publish to the test repository:\n\n1. Ensure you have configured the Test PyPi repository with Poetry (one-off)\n2. `poetry publish --build -r testpypi` to upload to the test repository\n\n## Changelog\n\n### Unpublished\n\n...\n\n### v3.0.1 - 2021-03-04\n\n- Change primary host to bbfcapi.fustra.uk\n- [Security] Upgrade dependencies\n\n### v3.0.0 - 2020-11-08\n\n- IMPORTANT: Major changes for compatibility with BBFC\'s new website\n- Update various dependencies\n\n### v2.0.2 - 2020-03-22\n\n- Fix another missing dependency\n\n### v2.0.1 - 2020-03-22\n\n- Fix missing dependencies\n\n### v2.0.0 - 2020-03-22\n\n- Add Python client library for the BBFCAPI REST Web API\n- Use camelCasing for JSON fields in the web API\n- Reorganise entire package\n\n### v1.0.1 - 2020-01-19\n\n- Fix parsing 12A age ratings\n\n### v1.0.0 - 2020-01-19\n\n- First release of bbfcapi\n',
    'author': 'QasimK',
    'author_email': 'noreply@QasimK.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fustra/bbfcapi/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
