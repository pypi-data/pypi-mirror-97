from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)"""
    lineiter = (line.strip() for line in open(filename))
    reqs = [line for line in lineiter if line and not line.startswith("#")]
    return reqs


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='auto_util',
    packages=find_packages(),
    version='0.1',
    license='Apache License 2.0',
    install_requires=parse_requirements('requirements.txt'),
    url="https://github.com/auto-flutter/auto_util",
    description="A command line tool for image matching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points="""
    [console_scripts]
    auto_util = cli.cli:main
    """,
    python_requires=">=3.4,<3.8",
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
