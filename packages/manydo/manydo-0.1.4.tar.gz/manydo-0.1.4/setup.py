# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manydo']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0.0,<2.0.0', 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'manydo',
    'version': '0.1.4',
    'description': 'Dead-simple parallel execution.',
    'long_description': "# manydo\n\nDead-simple parallel execution with a loading bar sprinkled on top.\n\n## Installation\n\n`pip install manydo`. Or, better for you, use [Poetry](python-poetry.org/): `poetry add manydo`.\n\n## Usage\n\n`manydo` is simple. All you need is `map`:\n\n```python\nfrom manydo import map\n\nmap(lambda x: x + 3, [1, 2, 3]) # [4, 5, 6]\nmap(function, iterable, num_jobs=16) # try not to burn your CPU\nmap(function, iterable, loading_bar=False)\nmap(function, iterable, desc='Passes arguments to tqdm')\n```\n\n## Related projects\n\n[pqdm](https://github.com/niedakh/pqdm) is very similar, but didn't work for me ¯\\\\\\_(ツ)\\_/¯\n",
    'author': 'malyvsen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/malyvsen/manydo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
