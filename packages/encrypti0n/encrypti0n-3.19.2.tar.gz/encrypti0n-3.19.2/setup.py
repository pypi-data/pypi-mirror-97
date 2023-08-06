# source: https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup, find_packages
name='encrypti0n'
setup(
	name=name,
	version='3.19.2',
	description='Easily encrypt & decrypt files with python / through the CLI.',
	url=f'http://github.com/vandenberghinc/{name}',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
            'certifi>=2020.6.20',
            'chardet>=3.0.4',
            'idna>=2.10',
            'pycryptodome>=3.9.9',
            'requests>=2.24.0',
            'urllib3>=1.25.11',
            'fil3s>=2.13.2',
            'r3sponse>=2.8.9',
            'cl1>=1.12.1',
            'netw0rk>=1.7.8',
            'syst3m>=2.14.7',
        ])