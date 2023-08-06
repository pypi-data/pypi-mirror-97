# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyworks_orm',
 'pyworks_orm.orator',
 'pyworks_orm.orator.commands',
 'pyworks_orm.orator.commands.migrations',
 'pyworks_orm.orator.commands.models',
 'pyworks_orm.orator.commands.seeds',
 'pyworks_orm.orator.connections',
 'pyworks_orm.orator.connectors',
 'pyworks_orm.orator.dbal',
 'pyworks_orm.orator.dbal.exceptions',
 'pyworks_orm.orator.dbal.platforms',
 'pyworks_orm.orator.dbal.platforms.keywords',
 'pyworks_orm.orator.dbal.types',
 'pyworks_orm.orator.events',
 'pyworks_orm.orator.exceptions',
 'pyworks_orm.orator.migrations',
 'pyworks_orm.orator.orm',
 'pyworks_orm.orator.orm.mixins',
 'pyworks_orm.orator.orm.relations',
 'pyworks_orm.orator.orm.scopes',
 'pyworks_orm.orator.pagination',
 'pyworks_orm.orator.query',
 'pyworks_orm.orator.query.grammars',
 'pyworks_orm.orator.query.processors',
 'pyworks_orm.orator.schema',
 'pyworks_orm.orator.schema.grammars',
 'pyworks_orm.orator.seeds',
 'pyworks_orm.orator.support',
 'pyworks_orm.orator.utils']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=0.8,<0.9',
 'Pygments>=2.2,<3.0',
 'backpack>=0.1,<0.2',
 'blinker>=1.4,<2.0',
 'cleo>=0.6,<0.7',
 'inflection>=0.3,<0.4',
 'lazy-object-proxy>=1.2,<2.0',
 'pendulum>=1.4,<2.0',
 'pyaml>=16.12,<17.0',
 'pyyaml>=5.1,<6.0',
 'simplejson>=3.10,<4.0',
 'six>=1.10,<2.0',
 'wrapt>=1.10,<2.0']

extras_require = \
{'mysql': ['mysqlclient>=1.3,<2.0'],
 'mysql-python': ['PyMySQL>=0.7,<0.8'],
 'pgsql': ['psycopg2>=2.7,<3.0']}

entry_points = \
{'console_scripts': ['orator = orator.commands.application:application.run']}

setup_kwargs = {
    'name': 'pyworks-orm',
    'version': '1.0.0a1',
    'description': 'Pyworks ORM is a wrapper and other branch based on Orator ORM.',
    'long_description': 'Pyworks ORM\n######\n\nPyworks is an open source framework for fast-up release the products for python developers. It is inspired by the laravel framework. \n\nPyworks ORM is a branch based on Orator which is an awesome python orm with modern thinking. \n\n',
    'author': 'PyWorks Asia Team',
    'author_email': 'opensource@pyworks.asia',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyworksasia/pyworks-orm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
