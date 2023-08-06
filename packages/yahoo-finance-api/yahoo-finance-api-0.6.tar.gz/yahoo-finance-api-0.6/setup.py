from setuptools import setup, find_packages

setup(
    name = 'yahoo-finance-api',
    version = 'v0.6', 
    description = 'Package to source data from Yahoo Finance',
    author = 'Rakesh Bhat',
    author_email = 'rakeshbhat9@gmail.com',
    url = 'https://github.com/rakeshbhat9/yahoo-finance-api',
    download_url = 'https://github.com/rakeshbhat9/yahoo-finance-api/archive/v0.2.tar.gz',
    keywords = ['v0.6'],
    classifiers = [],
    packages=find_packages(),
    install_requires=[
    'pandas==1.1.3',
    'requests==2.24.0',
    'beautifulsoup4==4.9.3',
    'matplotlib==3.3.2']
)
# python setup.py sdist upload -r pypi