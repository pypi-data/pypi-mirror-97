"""
A python module to support analytic cycling with a power meter.
"""
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

config = {
    'name': 'velopy',
    'version': '0.1.4',
    'license': 'BSD New License',
    'description': 'Library for simple calculations with respect to road cycling and training',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'keywords': ['cycling', 'training with power', 'training zones', 'TSS', 'PMC', 'CTL', 'ATL', 'power model'],
    'author': 'Christoph Ernst',
    'url': 'https://gitlab.com/ce72/velo/-/tree/master',
    'packages': find_packages(),
    'include_package_data': True,
    'py_modules': ['velopy'],
    'python_requires': '>3.6'
}

setup(**config)
