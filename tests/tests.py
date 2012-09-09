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
from pushnotify import pushover

try:
    imp.find_module('nmakeys', [os.path.dirname(__file__)])
except ImportError:
    NMA_API_KEYS = {}
    NMA_DEVELOPER_KEY = ''
else:
    from nmakeys import API_KEYS as NMA_API_KEYS
    from nmakeys import DEVELOPER_KEY as NMA_DEVELOPER_KEY

try:
    imp.find_module('pushoverkeys', [os.path.dirname(__file__)])
except ImportError:
    PUSHOVER_TOKEN = ''
    PUSHOVER_USER = ''
    PUSHOVER_DEVICE = ''
else:
    from pushoverkeys import TOKEN as PUSHOVER_TOKEN
    from pushoverkeys import USER as PUSHOVER_USER
    from pushoverkeys import DEVICE as PUSHOVER_DEVICE


class NMATest(unittest.TestCase):

    def setUp(self):

        self.client = nma.Client(NMA_API_KEYS, NMA_DEVELOPER_KEY)

        self.app = 'pushnotify unit tests'
        self.event = 'unit test: test_notify'
        self.desc = 'valid notification test for pushnotify'

    def test_notify_valid(self):
        """Test notify with valid notifications.

        """

        """valid notification"""

        self.client.notify(self.app, self.event, self.desc)

        """valid notification, extra arguments, html"""

        html_desc = '<h1>{0}</h1><p>{1}<br>{2}</p>'.format(
            self.app, self.event, self.desc)
        priority = 0
        url = nma.NOTIFY_URL

        self.client.notify(self.app, self.event, html_desc,
                           kwargs={'priority': priority, 'url': url,
                                   'content-type': 'text/html'})

    def test_notify_invalid(self):
        """Test notify with invalid notifications.

        """

        """invalid API key"""

        char = self.client.apikeys[0][0]
        apikey = self.client.apikeys[0].replace(char, '_')
        self.client.apikeys = [apikey, ]
        self.client.developerkey = ''

        self.assertRaises(exceptions.ApiKeyError,
                          self.client.notify, self.app, self.event, self.desc)

        self.client.apikeys = NMA_API_KEYS
        self.client.developerkey = NMA_DEVELOPER_KEY

        """invalid argument lengths"""

        bad_app = 'a' * 257
        self.assertRaises(exceptions.FormatError,
                          self.client.notify, bad_app, self.event, self.desc)

    def test_verify_valid(self):
        """Test verify with a valid API key.

        """

        self.assertTrue(self.client.verify(self.client.apikeys[0]))

    def test_verify_invalid(self):
        """Test verify with invalid API keys.

        """

        """invalid API key of incorrect length"""

        apikey = u'{0}{1}'.format(self.client.apikeys[0], '1')

        self.assertFalse(self.client.verify(apikey))

        """invalid API key of correct length"""

        char = self.client.apikeys[0][0]
        apikey = self.client.apikeys[0].replace(char, '_')

        self.assertFalse(self.client.verify(apikey))


class PushoverTest(unittest.TestCase):

    def setUp(self):

        self.client = pushover.Client(PUSHOVER_TOKEN)

    def test_verify_user_valid(self):
        """Test veriy_user with a valid user token.

        """

        self.assertTrue(self.client.verify_user(PUSHOVER_USER))

    def test_verify_user_invalid(self):
        """Test verify_user with an invalid user token.

        """

        self.assertFalse(self.client.verify_user('foo'))

    def test_verify_device_valid(self):
        """Test verify_device with a valid device string.

        """

        self.assertTrue(self.client.verify_device(PUSHOVER_USER,
                                                  PUSHOVER_DEVICE))

    def test_verify_device_invalid(self):
        """Test verify_device with an invalid device string.

        """

        self.assertFalse(self.client.verify_device(PUSHOVER_USER, 'foo'))

    def test_verify_device_invalid_user(self):
        """Test verify_device with an invalid user token.

        """

        self.assertRaises(exceptions.ApiKeyError, self.client.verify_device,
                          'foo', PUSHOVER_DEVICE)


if __name__ == '__main__':
    pass
