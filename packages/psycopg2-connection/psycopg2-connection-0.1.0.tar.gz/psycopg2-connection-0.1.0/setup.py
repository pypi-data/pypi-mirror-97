import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='psycopg2-connection',
    version='0.1.0',
    description='Abstract away common patterns you might use in psycopg2.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ethancarlsson/psycopg2-mini-abstractions",
    author="Ethan Carlsson",
    author_email="ethanmcarlsson@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["db_connections"],
    include_package_data=True,
    install_requires=["psycopg2"]
)