try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'PAUL: Python Actions Using Language',
    'author': 'Aaron Stockdill',
    'url': 'https://github.com/aaronstockdill/PAUL',
    'download_url': 'https://github.com/aaronstockdill/PAUL/archive/master.zip',
    'author_email': 'aaronstockdill@me.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['PAUL'],
    'scripts': ['bin/brain.py', 'bin/paul.py'],
    'name': 'PAUL'
}

setup(**config)