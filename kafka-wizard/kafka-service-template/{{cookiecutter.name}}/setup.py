# Copyright {% now 'local', '%Y' %} {{ cookiecutter.author }}
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
    name='{{ cookiecutter.name }}',
    version='1.0',
    packages=find_packages(),
    url="https://www.github.com/default/{{ cookiecutter.name }}",
    download_url='https://github.com/default/{{ cookiecutter.name }}/archive/1.0.tar.gz',
    license='LICENSE.md',
    author='{{ cookiecutter.author }}',
    author_email='{{ cookiecutter.email }}',
    description='',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(filename='requirements.txt'),
    data_files=[],
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.name }}={{ cookiecutter.name }}.main:run'
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers"
    ],
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://github.com/default/{{ cookiecutter.name }}/issues',
        'Source': 'https://github.com/default/{{ cookiecutter.name }}'
    },
)
