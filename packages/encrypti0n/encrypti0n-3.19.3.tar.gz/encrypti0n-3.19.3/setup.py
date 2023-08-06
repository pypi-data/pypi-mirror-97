# source: https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup, find_packages
name='encrypti0n'
setup(
	name=name,
	version='3.19.3',
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
            'fil3s>=2.13.3',
            'r3sponse>=2.9.0',
            'cl1>=1.12.2',
            'netw0rk>=1.7.9',
            'syst3m>=2.14.8',
        ])