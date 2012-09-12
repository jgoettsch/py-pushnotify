#!/usr/bin/env python
# vim: set fileencoding=utf-8

from distutils.core import setup


version = '0.2.1p'


setup(
    name='pushnotify',
    packages=['pushnotify', 'pushnotify.tests'],
    version=version,
    author='Jeffrey Goettsch',
    author_email='jgoettsch@gmail.com',
    url='https://bitbucket.org/jgoettsch/py-pushnotify/',
    description=('A package for sending push notifications to Android '
                 'and iOS devices.'),
    long_description=('A package for sending push notifications to '
                      'Android and iOS devices. It requires Notify My '
                      'Android, Prowl, or Pushover to be installed on '
                      'each device.'),
    download_url=('https://bitbucket.org/jgoettsch/py-pushnotify/get/'
                  '{0}.tar.gz').format(version),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration'])
