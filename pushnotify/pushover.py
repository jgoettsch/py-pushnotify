#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""Module for sending push notificiations to Android and iOS devices
that have Pushover installed. See https://pushover.net/ for more
information.

copyright: Copyright (c) Jeffrey Goettsch and other contributors.
license: BSD, see LICENSE for details.

"""


import json
import urllib
import urllib2

from pushnotify import exceptions


PUBLIC_API_URL = u'https://api.pushover.net/1'
VERIFY_URL = u'/'.join([PUBLIC_API_URL, u'users/validate.json'])
NOTIFY_URL = u'/'.join([PUBLIC_API_URL, u'messages.json'])


class Client(object):
    """Client for sending push notifications to Android and iOS devices
    with the Pushover application installed.

    Member Vars:
        token: A string containing a valid API token.

    """

    def __init__(self, token):
        """Initialize the Pushover client.

        Args:
            token: A string containing a valid API token.

        """

        self._browser = urllib2.build_opener(urllib2.HTTPSHandler())

        self.token = token

    def _parse_response(self, stream, verify=False):

        response = json.loads(stream.read())

        self._last_code = stream.code
        if 'user' in response.keys():
            self._last_user = response['user']
        else:
            self._last_user = None
        if 'status' in response.keys():
            self._last_status = response['status']
        else:
            self._last_status = None
        if 'device' in response.keys():
            self._last_device = response['device']
        else:
            self._last_device = None

    def _post(self, url, data):

        request = urllib2.Request(url, data)
        try:
            response_stream = self._browser.open(request)
        except urllib2.HTTPError, exc:
            return exc
        else:
            return response_stream

    def verify_user(self, user):
        """Verify a user token.

        Args:
            user: A string containing a valid user token.

        Returns:
            A boolean containing True if the user token is valid, and
            False if it is not.

        """

        data = {'token': self.token, 'user': user}

        data = urllib.urlencode(data)
        response_stream = self._post(VERIFY_URL, data)

        self._parse_response(response_stream, True)

        return self._last_status

    def verify_device(self, user, device):
        """Verify a device for a user.

        Args:
            user: A string containing a valid user token.
            device: A string containing a device name.

        Raises:
            pushnotify.exceptions.ApiKeyError

        Returns:
            A boolean containing True if the device is valid, and
            False if it is not.

        """

        data = {'token': self.token, 'user': user, 'device': device}

        data = urllib.urlencode(data)
        response_stream = self._post(VERIFY_URL, data)

        self._parse_response(response_stream, True)

        if self._last_user and 'invalid' in self._last_user.lower():
            raise exceptions.ApiKeyError(self._last_user, self._last_code)

        return self._last_status


if __name__ == '__main__':
    pass
