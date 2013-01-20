#!/usr/bin/env python
# vim: set fileencoding=utf-8

import re
from setuptools import setup


def parse_requirements(file_name):

    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*))$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):

    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


version = '0.5p'

with open('README.rst') as fh:
    long_description = fh.read()

with open('INSTALL.rst') as fh:
    long_description = '\n\n'.join([long_description, fh.read()])

with open('CHANGELOG.rst') as fh:
    long_description = '\n\n'.join([long_description, fh.read()])

setup(
    name='pushnotify',
    packages=['pushnotify', 'pushnotify.tests'],
    version=version,
    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),

    # PyPI metadata
    author='Jeffrey Goettsch',
    author_email='jgoettsch+pypushnotify@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration'],
    description=('A package for sending push notifications to Android and '
                 'iOS devices.'),
    download_url=('https://bitbucket.org/jgoettsch/py-pushnotify/get/'
                  '{0}.tar.gz').format(version),
    long_description=long_description,
    url='https://bitbucket.org/jgoettsch/py-pushnotify/',)
