from distutils.core import setup

setup(
    name = 'yahoo-finance-api',
    packages = ['yahoo_finance'],
    version = 'v0.2', 
    description = 'Package to source data from Yahoo Finance',
    author = 'Rakesh Bhat',
    author_email = 'rakeshbhat9@gmail.com',
    url = 'https://github.com/rakeshbhat9/yahoo-finance-api',
    download_url = 'https://github.com/rakeshbhat9/yahoo-finance-api/archive/v0.2.tar.gz',
    keywords = ['v0.1'],
    classifiers = [],
        install_requires=[
        'pandas==1.1.3',
        'requests==2.24.0',
        'bs4==4.9.3'
        'matplotlib==3.3.2']
)