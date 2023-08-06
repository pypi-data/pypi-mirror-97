# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ambra_sdk',
 'ambra_sdk.addon',
 'ambra_sdk.exceptions',
 'ambra_sdk.models',
 'ambra_sdk.service',
 'ambra_sdk.service.entrypoints',
 'ambra_sdk.service.entrypoints.generated',
 'ambra_sdk.storage']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'pydicom>=2.0.0,<3.0.0',
 'python-box>=5.1.1,<6.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['bump_release = release:bump_release',
                     'bump_release_candidate = release:bump_release_candidate',
                     'start_release = release:start_release']}

setup_kwargs = {
    'name': 'ambra-sdk',
    'version': '3.21.2.0.post1',
    'description': 'Ambrahealth python SDK',
    'long_description': "# Ambra-SDK\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![PyPI version](https://badge.fury.io/py/ambra-sdk.svg)](https://badge.fury.io/py/ambra-sdk)\n\n\n\n---\n\nWelcome to ambra-sdk library for intract with ambrahealth service and storage api. \n\n\n## Quickstart\n\n```bash\npip install ambra-sdk\n```\n\n## Running\n\n```python\nfrom ambra_sdk.api import Api\nfrom ambra_sdk.models import Study\nfrom ambra_sdk.service.filtering import Filter, FilterCondition\nfrom ambra_sdk.service.sorting import Sorter, SortingOrder\n\n# Usually, URL has a form:\n# url = https://ambrahealth_host/api/v3\n# username and password - ambrahealth credentials.\napi = Api.with_creds(url, username, password)\nuser_info = api.Session.user().get()\n\nstudies = api \\\n    .Study \\\n    .list() \\\n    .filter_by(\n        Filter(\n            'phi_namespace',\n            FilterCondition.equals,\n            user_info.namespace_id,\n        ),\n    ) \\\n    .only([Study.study_uid, Study.image_count]) \\\n    .sort_by(\n        Sorter(\n            'created',\n            SortingOrder.ascending,\n        ),\n    ) \\\n    .all()\n\nfor study in studies:\n    print(study.study_uid, study.image_count)\n \n```\n\n## License\n\nAmbra-SDK is licensed under the terms of the Apache-2.0 License (see the file LICENSE).\n\n## Read the docs\n\nDocumentation: https://dicomgrid.github.io/sdk-python/index.html\n",
    'author': 'Ambrahealth AI team',
    'author_email': 'python-sdk@ambrahealth.com',
    'maintainer': 'Alexander Kapustin',
    'maintainer_email': 'akapustin@ambrahealth.com',
    'url': 'https://github.com/dicomgrid/sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
