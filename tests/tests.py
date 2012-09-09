#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""copyright: Copyright (c) Jeffrey Goettsch and other contributors.
license: BSD, see LICENSE for details.

"""


import imp
import os
import unittest

from pushnotify import exceptions
from pushnotify import nma
try:
    imp.find_module('nmakeys', [os.path.dirname(__file__)])
except ImportError:
    API_KEYS = {}
    DEVELOEPER_KEY = ''
else:
    from nmakeys import API_KEYS
    from nmakeys import DEVELOPER_KEY


class NMATest(unittest.TestCase):

    def setUp(self):

        self.client = nma.Client(API_KEYS, DEVELOPER_KEY)

    def test_notify(self):

        """valid notification"""

        app = 'pushnotify unit tests'
        event = 'unit test: test_notify'
        desc = 'valid notification test for pushnotify'

        self.client.notify(app, event, desc)

        """valid notification, extra arguments, html"""

        html_desc = '<h1>{0}</h1><p>{1}<br>{2}</p>'.format(app, event, desc)
        priority = 0
        url = nma.NOTIFY_URL

        self.client.notify(app, event, html_desc,
                           kwargs={'priority': priority, 'url': url,
                                   'content-type': 'text/html'})

        """invalid API key"""

        char = self.client.apikeys[0][0]
        apikey = self.client.apikeys[0].replace(char, '_')
        self.client.apikeys = [apikey, ]
        self.client.developerkey = ''

        self.assertRaises(exceptions.ApiKeyError,
                          self.client.notify, app, event, desc)

        self.client.apikeys = API_KEYS
        self.client.developerkey = DEVELOPER_KEY

        """invalid argument length"""

        bad_app = 'a' * 257

        self.assertRaises(exceptions.FormatError,
                          self.client.notify, bad_app, event, desc)

        bad_event = 'e' * 1001

        self.assertRaises(exceptions.FormatError,
                          self.client.notify, app, bad_event, desc)

        bad_desc = 'd' * 10001

        self.assertRaises(exceptions.FormatError,
                          self.client.notify, app, event, bad_desc)

    def test_verify(self):

        """valid API key"""

        self.assertTrue(self.client.verify(self.client.apikeys[0]))

        """invalid API key of incorrect length"""

        apikey = u'{0}{1}'.format(self.client.apikeys[0], '1')

        self.assertFalse(self.client.verify(apikey))

        """invalid API key of correct length"""

        char = self.client.apikeys[0][0]
        apikey = self.client.apikeys[0].replace(char, '_')

        self.assertFalse(self.client.verify(apikey))


if __name__ == '__main__':
    pass
