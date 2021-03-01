#!usr/bin/python

# Copyright 2021Francisco Pinto-Santos @ GandalFran in GitHub
# See LICENSE for details.


import io
from setuptools import setup, find_packages


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


def requirements(filename):
    reqs = list()
    with io.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs


setup(
    name='kafka_wizard',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/GandalFran/kafka-wizard',
    download_url='https://github.com/GandalFran/kafka-wizard/archive/master.zip',
    license='Copyright',
    author='Francisco Pinto-Santos',
    author_email='franpintosantos@usal.es',
    description='Utility to generate kafka components using draw.io diagrams.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(filename='requirements.txt'),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ],
    entry_points={
        'console_scripts': [
            'kafkawizard=kafka_wizard.cli:main'
        ],
    },
    python_requires='>=3',
    extras_require={
        "tests": requirements(filename='tests/requirements.txt'),
    },
    keywords=', '.join([
        'Apache Kafka', 'Kafka', 'Code Generation', 'cookiecutter'
    ]),
    project_urls={
        'Bug Reports': 'https://github.com/GandalFran/kafka-wizard/issues',
        'Source': 'https://github.com/GandalFran/kafka-wizard',
        'Documentation': 'https://github.com/GandalFran/kafka-wizard'
    }
)