import os
import string
from os import path
from setuptools import find_packages, setup


def get_version(version_list):
    return '.'.join(map(str, version_list))


init = os.path.join(os.path.dirname(__file__), 'pararamio', 'constants.py')
version_line = list(filter(lambda l: l.startswith('VERSION'), open(init)))[0]
VERSION = get_version(''.join(list(filter(lambda c: c in string.digits + '.', version_line.split('=')[-1]))).split('.'))
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='pararamio',
    version=VERSION,
    description='Pararam Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/pararam-public/py-pararamio',
    author='Ilya Volnistov',
    author_email='i.volnistov@gaijin.team',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    zip_safe=False
)
