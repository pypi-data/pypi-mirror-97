# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pmatcher']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0', 'python-Levenshtein>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'pmatcher',
    'version': '0.1.5',
    'description': 'Monadic election precinct matcher for gerrymandering data collection and research at MGGG',
    'long_description': '## (monadic) Precinct Matcher\nMatching election data to shapefiles is hard.\nIt is usually context-dependent and implemented on a project-by-project basis.\nIt also sometimes involves some manual labor.\nThis attempts to make life easier for everyone who has to deal with precinct matching.\n\n## Install\n\n``` bash\npip install pmatcher\n```\n## Benchmarks (on real data)\nVEST releases its precincts with VTD codes and county FIPS codes.\nTo validate this approach, I ran the matcher on known, good data.\n\nResults (in % accuracy):\n``` \nExact match 0.9444831591173054\nInsensitive match 0.9444831591173054\nInsensitive normalized match 0.9932636469221835\nAggressive insensitive normalized match 0.9983739837398374\n```\n\n## Implemented Methods\n- `matcher.default()`\nApplies exact, insensitive, normalized, and weighted_manual in that order.\nAll batteries included!\n\n- `matcher.exact()`\nMatches exact strings.\n\n- `matcher.insensitive()`\nMatches strings (case-insensitive).\n\n- `matcher.insensitive_normalized()`\nMatches strings with special characters removed (e.g.`()`, `#`, `-`).\n\n- `matcher.weighted_manual()`\nUses a weighted levenshtein algorithm.\nFirst looks for token-distance, followed by token word distance for tiebreaking.\n\n### Saving and loading progress\n- `matcher.save_progress("progress.json")`\nSaves progress/mapping to a json file.\n\n- `matcher.load_progress("progress.json")`\nLoads progress/mapping from a json file.\n\n## Example usage\n\n``` python\nfrom pmatcher import PrecinctMatcher\nmatcher = PrecinctMatcher(list_1, list_2)\nmapping = matcher.default()\n```\n\n``` python\nfrom pmatcher import PrecinctMatcher\nmatcher = PrecinctMatcher(list_1, list_2)\nmatcher.exact()\nmatcher.insensitive()\nmatcher.insensitive_normalized()\nmatcher.insensitive_normalized(aggressive=True)\nmapping = matcher.weighted_manual()\n```\n\n',
    'author': 'Max Fan',
    'author_email': 'theinnovativeinventor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
