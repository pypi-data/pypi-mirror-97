# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaclass', 'niaclass.tests']

package_data = \
{'': ['*'], 'niaclass.tests': ['test_files/*']}

install_requires = \
['NiaPy>=2.0.0rc12,<3.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'niaclass',
    'version': '0.1.0',
    'description': 'Python framework for building classifiers using nature-inspired algorithms.',
    'long_description': 'NiaClass\n========\n\nNiaClass is a framework for solving classification tasks using nature-inspired algorithms. The framework is written fully in Python. Its goal is to find the best possible set of classification rules for the input data using the `NiaPy framework <https://github.com/NiaOrg/NiaPy>`_, which is a popular Python collection of nature-inspired algorithms. The NiaClass classifier support numerical and categorical features.\n\nLicense\n-------\n\nThis package is distributed under the MIT License. This license can be\nfound online at http://www.opensource.org/licenses/MIT.\n\nDisclaimer\n----------\n\nThis framework is provided as-is, and there are no guarantees that it\nfits your purposes or that it is bug-free. Use it at your own risk!\n\nReferences\n----------\n\n[1] Iztok Fister Jr., Iztok Fister, Dušan Fister, Grega Vrbančič, Vili Podgorelec. On the potential of the nature-inspired algorithms for pure binary classification. In. Computational science - ICCS 2020 : 20th International Conference, Proceedings. Part V. Cham: Springer, pp. 18-28. Lecture notes in computer science, 12141, 2020',
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukapecnik/NiaClass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
