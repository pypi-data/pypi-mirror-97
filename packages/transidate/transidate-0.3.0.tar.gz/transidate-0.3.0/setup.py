# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transidate']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'cryptography>=3.3.2,<4.0.0',
 'lxml>=4.6.2,<5.0.0',
 'prettytable>=2.0.0,<3.0.0',
 'pydantic>=1.8,<2.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=9.12.4,<10.0.0']

entry_points = \
{'console_scripts': ['transidate = transidate.cli:validate']}

setup_kwargs = {
    'name': 'transidate',
    'version': '0.3.0',
    'description': 'Commandline tool for XML transit data validation.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/transidate.svg)](https://badge.fury.io/py/transidate)\n[![Build Status](https://github.com/ciaranmccormick/transidate/workflows/test/badge.svg?branch=master&event=push)](https://github.com/ciaranmccormick/transidate/actions?query=workflow%3Atest)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/ciaranmccormick/transidate/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n[![codecov](https://codecov.io/gh/ciaranmccormick/transidate/branch/develop/graph/badge.svg?token=I3693DR0S9)](https://codecov.io/gh/ciaranmccormick/transidate)\n\n\n# Transidate\n\nTransidate is a commandline tool for validating transit data files such as TransXChange\nNeTEx and SIRI.\n\nTransidate can validate several transit data formats out of the box.\n\n## Compatibility\n\nTransidate requires Python 3.7 or later.\n\n\n## Installing\n\nInstall transidate using `pip` or any other PyPi package manager.\n\n```sh\npip install transidate\n```\n\n## Using Transidate\n\nTransidate comes with a help guide to get you started. This will list all the options as\nwell as the transit data formats that are supported.\n\n```sh\ntransidate --help\n```\n\nTo validate a data source just specify the path to the data and the schema to validate\nthe data against. If the `--version` is not specified the data is automatically\nvalidated again TransXChange v2.4.\n\n\n```sh\ntransidate circular.xml --version TXC2.4\n```\n\n![No Errors](imgs/no-errors.png)\n\nIf transidate finds any schema violations it will print the details of the violation\nsuch as the file it occurred in, the line number of the violation and details.\n\nYou can also use transidate to validate a archived collection of files.\n\n```sh\ntransidate all_uk_txc_2_4.zip --version TXC2.4\n```\n\nThis is iterate over each XML file contained within the zip and collate all the\nviolations.\n\n![Errors](imgs/errors.png)\n\nTransidate also allows you to export any violations to CSV using the `--csv` flag.\n\n```sh\ntransidate all_uk_txc_2_4.zip --version TXC2.4 --csv\n```\n',
    'author': 'Ciaran McCormick',
    'author_email': 'ciaran@ciaranmccormick.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
