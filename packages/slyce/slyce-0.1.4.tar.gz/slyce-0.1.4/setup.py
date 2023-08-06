from os import path
from setuptools import setup
from setuptools import find_packages

DIR = path.abspath(path.dirname(__file__))
with open(path.join(DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

__version__ = "0.1.4"


setup(
    name="slyce",
    version=__version__,
    description="Python library for calling Slyce API.",
    author='Slyce Dev',
    author_email='dev@slyce.it',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://slyce-inc.github.io/forgex.lib.slycepy/_build/html/index.html",
    license='MIT',
    platforms=["any"],
    python_requires='>=3.7',
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        'grpcio==1.32.0',
        'grpcio-tools==1.32.0',
        'grpclib==0.4.1',
        'googleapis-common-protos==1.51.0'
    ],
    tests_require=[],
    test_suite='pytest'
)
