try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'PAUL: Python Actions Using Language',
    'author': 'Aaron Stockdill',
    'url': 'http://aaronstockdill.github.io/paul.html',
    'download_url': 'https://github.com/aaronstockdill/PAUL/archive/master.zip',
    'author_email': 'aaronstockdill@me.com',
    'version': '0.2',
    'install_requires': [],
    'packages': ['PAUL'],
    'scripts': ['bin/PAUL'],
    'name': 'PAUL'
}

setup(**config)