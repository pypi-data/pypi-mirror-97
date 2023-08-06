# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyworks_medialibrary']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.17,<2.0.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'pytest>=6.2.2,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'pyworks-medialibrary',
    'version': '0.1.0',
    'description': 'Provide awsome tools for manage images and documents.',
    'long_description': '# PyWorks Medialibrary\n\nPyworks Medialibrary provide awsome tools for manage image and document files.\n\n## Pre-Requisites\n\n- Python 3+\n- Poetry 1.1.4+\n\nSetup environment\n\n```shell\npoetry init\n```\n\n## Test package locally\n\nTo run tests for project run this command:\n\n```\nmake test\nmake test-cov\n```\n\nResults\n\n====================== test session starts ==============================\nplatform linux -- Python 3.7.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1\nrootdir: *********/pyworks-medialibrary, configfile: pytest.ini\ncollected 10 items          \n\ntests/test_config.py .                                              [ 50%]\ntests/test_send_mail.py .                                           [100%]\n\n======================= 2 passed in 3.18s ================================',
    'author': 'PyWorks Asia Team',
    'author_email': 'opensource@pyworks.asia',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyworksasia/pyworks-medialibrary',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
