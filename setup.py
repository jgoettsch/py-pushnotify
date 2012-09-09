#!/usr/bin/env python
# vim: set fileencoding=utf-8

from distutils.core import setup


version = '0.1p'


setup(
    name='pushnotify',
    version=version,
    author='Jeffrey Goettsch and other contributors',
    author_email='jgoettsch@gmail.com',
    url='https://bitbucket.org/jgoettsch/py-pushnotify/',
    description=('A package for sending push notifications to Android '
                 'devices.'),
    long_description=('A package for sending push notifications to '
                      'Android devices. It requires Notify My Android '
                      'be installed on each device.'),
    download_url=('https://bitbucket.org/jgoettsch/py-pushnotify/get/'
                  '{0}.tar.gz').format(version),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'])
