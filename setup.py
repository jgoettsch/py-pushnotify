#!/usr/bin/env python
# vim: set fileencoding=utf-8

import re
from setuptools import setup


def parse_requirements():

    requirements = []

    with open('requirements.txt') as fh:
        for line in fh.read().split('\n'):
            if re.match(r'(\s*#)|(\s*$)', line):
                continue
            if re.match(r'\s*-e\s+', line):
                requirements.append(
                    re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
            elif re.match(r'\s*-f\s+', line):
                pass
            else:
                requirements.append(line)

    return requirements

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
    install_requires=parse_requirements(),
    version=version,
    author='Jeffrey Goettsch',
    author_email='jgoettsch+pypushnotify@gmail.com',
    url='https://bitbucket.org/jgoettsch/py-pushnotify/',
    description=(
        'A package for sending push notifications to '
        'Android and iOS devices.'),
    long_description=long_description,
    download_url=('https://bitbucket.org/jgoettsch/py-pushnotify/get/'
                  '{0}.tar.gz').format(version),
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
        'Topic :: System :: Systems Administration'])
