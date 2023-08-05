# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydent',
 'pydent.aql',
 'pydent.marshaller',
 'pydent.models',
 'pydent.planner',
 'pydent.utils',
 'pydent.utils.loggable']

package_data = \
{'': ['*'],
 'pydent': ['.idea/*', '.idea/inspectionProfiles/*', '.idea/libraries/*']}

install_requires = \
['colorlog>=4.0,<5.0',
 'inflection>=0.3.1,<0.4.0',
 'jsonschema>=3.2.0,<4.0.0',
 'nest-asyncio>=1.0,<2.0',
 'networkx>=2.3,<3.0',
 'requests>=2.22,<3.0',
 'retry>=0.9.2,<0.10.0',
 'tqdm>=4.32,<5.0']

setup_kwargs = {
    'name': 'pydent',
    'version': '1.0.7',
    'description': "Aquarium's Python API for planning, executing, and analyzing scientific experiments.",
    'long_description': '# Pydent: Aquarium API Scripting\n\n[![CircleCI](https://circleci.com/gh/klavinslab/trident/tree/master.svg?style=svg&circle-token=88677c59698d55a127a080cba9ca025cf8072f6c)](https://circleci.com/gh/klavinslab/trident/tree/master)\n[![PyPI version](https://badge.fury.io/py/pydent.svg)](https://badge.fury.io/py/pydent)\n\nPydent is the python API for Aquarium.\n\n## Documentation\n\n[API documentation can be found here at http://aquariumbio.github.io/pydent](http://aquariumbio.github.io/pydent/)\n\n## Requirements\n\n* Python > 3.4\n* An Aquarium login\n\n## Quick installation\n\nPydent can be installed using `pip3`.\n\n```\n    pip3 install pydent\n```\n\nor upgraded using\n\n```\n    pip3 install pydent --upgrade\n```\n\n## Basic Usage\n\n### Logging in\n\n```python\nfrom pydent import AqSession\n\n# open a session\nmysession = AqSession("username", "password", "www.aquarium_nursery.url")\n\n# find a user\nu = mysession.User.find(1)\n\n# print the user data\nprint(u)\n```\n\n### Models\n\n```python\nprint(mysession.models)\n```\n\n#### Finding models\n\n* By name: `nursery.SampleType.find_by_name("Primer")`\n\n* By ID: `nursery.SampleType.find(1)`\n\n* By property: `nursery.SampleType.where({\'name\': \'Primer\'})`\n\n* All models: `nursery.SampleType.all()`\n\n#### Getting nested data\n\n```python\n# samples are linked to sample_type\nprimer_type = mysession.SampleType.find_by_name("Primer")\nprimers = primer_type.samples\n\n# and sample type is linked to sample\np = primers[0]\nprint(p.sample_type)\n```\n\n#### Listing Available nested relationships\n\n```python\nprimer_type = mysession.SampleType.find(1)\nprint(primer_type.get_relationships())\n```\n\n## making a release\n\n```bash\npoetry build\npoetry publish\n```\n\nTo use a pypi token, the user name should be `__token__` and the password should be the token including the `pypi-` prefix.\n\n',
    'author': 'jvrana',
    'author_email': 'justin.vrana@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/aquariumbio/trident',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
