#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import find_packages, setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='django-js-reverse',
    version=get_version("django_js_reverse/__init__.py"),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    license='MIT',
    description='Javascript url handling for Django that doesn\'t hurt.',
    long_description=read('README.rst') + '\n\n' + read('CHANGELOG.rst'),
    long_description_content_type='text/x-rst',
    author='Bernhard Janetzki',
    author_email='boerni@gmail.com',
    maintainer='Vinta Software',
    maintainer_email='contact@vinta.com.br',
    url='https://github.com/vintasoftware/django-js-reverse',
    project_urls={
        'Source': 'https://github.com/vintasoftware/django-js-reverse',
        'Tracker': 'https://github.com/vintasoftware/django-js-reverse/issues',
        'PyPI': 'https://pypi.org/project/django-js-reverse/',
    },
    packages=find_packages(),
    package_data={
        'django_js_reverse': [
            'templates/django_js_reverse/*',
        ]
    },
    python_requires='>=3.10',
    install_requires=[
        'Django>=5.2,<6.1',
    ],
)
