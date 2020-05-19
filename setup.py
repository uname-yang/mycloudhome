import sys
import codecs

from setuptools import setup, find_packages

import mycloudhome

install_requires = [
    'requests',
    'click',
    'progress'
]

def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()

setup(
    name='mycloudhome',
    version=mycloudhome.__version__,
    description=mycloudhome.__doc__.strip(),
    long_description=long_description(),
    author=mycloudhome.__author__,
    author_email='yang.lights@hotmail.com',
    license=mycloudhome.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mycloudhome = mycloudhome.main:cli',
        ],
    },
    python_requires='>=3.6',
    install_requires=install_requires,
    keywords=['WD My Cloud Home','western digital','cli','file management'],
)