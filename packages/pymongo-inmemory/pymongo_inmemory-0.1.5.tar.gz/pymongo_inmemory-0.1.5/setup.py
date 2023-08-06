# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymongo_inmemory']

package_data = \
{'': ['*']}

install_requires = \
['pymongo']

setup_kwargs = {
    'name': 'pymongo-inmemory',
    'version': '0.1.5',
    'description': 'A mongo mocking library with an ephemeral MongoDB running in memory.',
    'long_description': "[![PyPI\nversion](https://badge.fury.io/py/pymongo-inmemory.svg)](https://badge.fury.io/py/pymongo-inmemory)\n\n# pymongo_inmemory\nA mongo mocking library with an ephemeral MongoDB running in memory.\n\n## Installation\n```bash\npip install pymongo-inmemory\n```\n\n## Configuration\n| Config param     | Description                                                          | Optional? | Default                                          |\n|------------------|----------------------------------------------------------------------|-----------|--------------------------------------------------|\n| mongo_version    | Which MongoD version to download and use.                            | Yes       | 4.0.10                                           |\n| mongod_port      | Override port preference.                                            | Yes       | Automatically determined between 27017 and 28000 |\n| operating_system | This makes sense for Linux setting, where there are several flavours | Yes       | Automatically determined (Generic for Linux)     |\n\n\n## Usage\n### Configure\nThere are several ways you can configure `pymongo_inmemory`.\n\n1. Insert a new section to your project's `setup.cfg` for the operating system and mongo\nversion you want to spin up:\n    ```ini\n    [pymongo_inmemory]\n    mongo_version = 4.0.10\n    mongod_port = 27019\n    ```\n2. Define an ALL_CAPS environment variable with prefix `PYMONGOIM__` (attention to trailing double\n   underscores.) For instance, to override the port, set up an environment variable\n   `PYMONGOIM__MONGOD_PORT`.\n\n### Import and use\n`pymongo_inmemory` wraps the client that comes from `pymongo` and configures and ephemeral server.\nThen you can import `MongoClient` from `pymongo_inmemory` instead of `pymongo` and use it:\n\n```python\nfrom pymongo_inmemory import MongoClient\n\nclient = MongoClient()  # No need to provide host\ndb = client['testdb']\ncollection = db['test-collection']\n# etc., etc.\nclient.close()\n\n# Also usable with context manager\nwith MongoClient() as client:\n    # do stuff\n```\n\n## Supported Python versions\nSince `pytest` uses [`LocalPath`](https://py.readthedocs.io/en/latest/path.html) for path related\noperations and on python versions older than 3.6 `LocalPath` does not behave well with all path\nrelated operations, we are setting **Python 3.6.10** in our development.\n\nTechnically, this also limits the minimum Python version of tested features. However theer shouldn't\nbe a hard limitation to use Python 3.5. We recommend upgrading older Python versions than that.\n\n## Development\nProject is set up to develop with [poetry](https://python-poetry.org/). We rely on\n[pyenv](https://github.com/pyenv/pyenv#installation) to maintain the minimum supported\nPython version.\n\nAfter installing `pyenv`, `poetry`, and cloning the repo, create the shell and install\nall package requirements:\n\n```bash\npyenv install --skip-existing\npoetry install --no-root\npoetry shell\n```\n\nRun the tests:\n```bash\npytest\n```\n\nIf on NIX systems you can run further tests:\n```bash\nbash tests/integrity/test_integrity.sh\n```\n\n**See how you can wet your feet,** check out [good first\nissues](https://github.com/kaizendorks/pymongo_inmemory/contribute).\n",
    'author': 'Kaizen Dorks',
    'author_email': 'kaizendorks@gmail.com',
    'maintainer': 'Ertugrul Karademir',
    'maintainer_email': 'ekarademir@gmail.com',
    'url': 'https://github.com/kaizendorks/pymongo_inmemory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
