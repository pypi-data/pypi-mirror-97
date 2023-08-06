# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ukrdc_sqla']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.23,<2.0.0']

setup_kwargs = {
    'name': 'ukrdc-sqla',
    'version': '1.0.0',
    'description': 'SQLAlchemy models for the UKRDC',
    'long_description': '# UKRDC-SQLA\n\nSQLAlchemy models for the UKRDC and related databases.\n\n## Developer notes\n\n### Publish updates\n\n- Iterate the version number (`poetry version major/minor/patch`)\n- Push to GitHub repo\n- Create a GitHub release\n  - GitHub Actions will automatically publish the release to PyPI\n',
    'author': 'Joel Collins',
    'author_email': 'joel.collins@renalregistry.nhs.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
