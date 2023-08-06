# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_line']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['l = kt_line.cli:cli']}

setup_kwargs = {
    'name': 'kt-line',
    'version': '0.2.0',
    'description': 'Ferramenta de linha de comando para calcular linha de tendencia e linha de canal',
    'long_description': '# kt-line\nFerramenta de linha de comando para calcular linha de tendência e linha de canal.  \nEste pacote compõe o kit do trader.  \n\n## Instalação\npip install kt-line  \n\n## Uso\nl a b  \nonde:  \na = preço a  \nb = preço b  \n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-line',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
