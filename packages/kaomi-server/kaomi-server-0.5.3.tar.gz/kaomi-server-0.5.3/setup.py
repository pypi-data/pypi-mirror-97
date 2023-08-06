import setuptools
import os

with open("README-package.md", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).split('\n'):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1].strip()
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="kaomi-server",
    version=get_version('kaomi_server/__init__.py'),
    author="Linkspirit Team",
    author_email="tecnici@linkspirit.it",
    description="This package contains the server endpoint for the Kaomi deployer. Kaomi server has to be run on the system where you want to deploy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.linkspirit.it/linkspirit/kaomi-deployer.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cherrypy>=18.0.0',
    ],
    python_requires='>=3',
)
