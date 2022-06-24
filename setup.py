from setuptools import setup

setup(
    name='zacks-scraper',
    url='https://github.com/igalci/zacks-scraper',
    author='Igal',
    author_email='igal8k@gmail.com',
    packages=['zacks-scraper'],
    install_requires=['requests','json','beautifulsoup4','setuptools'],
    version='0.1',
    license='Apache',
    )