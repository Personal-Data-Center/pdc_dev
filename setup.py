import setuptools

setuptools.setup(
    name='pdc_dev',
    packages=setuptools.find_packages(),
    version='0.1.7',
    description='library with pdc funcionalities',
    author='Lucas Coraça Silva',
    url='https://github.com/Personal-Data-Center/pdc_dev',
    install_requires=['django-cas-ng'],
    license='GPL',
)
