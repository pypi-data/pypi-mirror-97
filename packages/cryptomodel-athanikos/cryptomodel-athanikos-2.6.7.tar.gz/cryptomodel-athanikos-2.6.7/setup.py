import setuptools

from distutils.core import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cryptomodel-athanikos',
    version="2.6.7",
    license='MIT License',
    author='Nikos Athanasakis',
    packages=setuptools.find_packages(),
    author_email='athanikos@gmail.com',
    description='Model for CryptoStore and CoinMarketCap Collections for Mongo db',
    tests_require=['pytest'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
