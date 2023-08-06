import codecs
import os.path
from setuptools import setup, find_packages

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='complycube',
    version=get_version("complycube/__init__.py"),
    author='Complycube',
    author_email='tech@complycube.com',
    license='MIT',
    url='https://docs.complycube.com/api-reference/',
    install_requires=[
        'requests >= 2.20.0',
        'pyhumps>=1.2.0',
    ],
    python_requires=">=3.6.0",
    tests_require=[
        "dotenv >= 1.0.0",
        "pytest >= 4.6.2, < 4.7",
    ],
    description='Official Python client for the ComplyCube API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    keywords=['complycube','aml','kyc','client', 'api', 'wrapper','PEP','identity verification','identity checks','document verification'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ],
)