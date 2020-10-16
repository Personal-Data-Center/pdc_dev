from setuptools import find_packages, setup

setup(
    name='pdc_dev',
    packages=find_packages(include=['django']),
    version='0.1.0',
    description='library with pdc funcionalities',
    author='Lucas Coraça Silva',
    install_requires=['django-cas-ng','Django'],
    license='GPL',
)
