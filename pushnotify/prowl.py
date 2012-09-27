#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""Module for sending push notifications to iOS devices that have
Prowl installed. See http://www.prowlapp.com/ for more
information.

copyright: Copyright (c) Jeffrey Goettsch and other contributors.
license: BSD, see LICENSE for details.

"""


try:
    from xml.etree import cElementTree
    ElementTree = cElementTree
except ImportError:
    from xml.etree import ElementTree

from pushnotify import abstract
from pushnotify import exceptions


PUBLIC_API_URL = u'https://api.prowlapp.com/publicapi'
VERIFY_URL = u'/'.join([PUBLIC_API_URL, 'verify'])
NOTIFY_URL = u'/'.join([PUBLIC_API_URL, 'add'])
RETRIEVE_TOKEN_URL = u'/'.join([PUBLIC_API_URL, 'retrieve', 'token'])
RETRIEVE_APIKEY_URL = u'/'.join([PUBLIC_API_URL, 'retrieve', 'apikey'])

DESC_LIMIT = 10000


class Client(abstract.AbstractClient):
    """Client for sending push notificiations to iOS devices with
    the Prowl application installed.

    Member Vars:
        developerkey: A string containing a valid developer key for the
            given type_ of client.
        application: A string containing the name of the application on
            behalf of whom the client will be sending messages.
        apikeys: A dictionary where the keys are strings containing
            valid user API keys, and the values are lists of strings,
            each containing a valid user device key.

    """

    def __init__(self, developerkey='', application=''):
        """Initialize the Prowl client.

        Args:
            developerkey: A string containing a valid provider key for
                the client.
            application: A string containing the name of the application
                on behalf of whom the client will be sending messages.

        """

        super(self.__class__, self).__init__(developerkey, application)

        self._type = 'prowl'
        self._urls = {'notify': NOTIFY_URL, 'verify': VERIFY_URL,
                      'retrieve_token': RETRIEVE_TOKEN_URL,
                      'retrieve_apikey': RETRIEVE_APIKEY_URL}

    def _parse_response_stream(self, response_stream, verify=False):

        xmlresp = response_stream.read()
        self.logger.info('received response: {0}'.format(xmlresp))

        root = ElementTree.fromstring(xmlresp)

        self._last_type = root[0].tag.lower()
        self._last_code = root[0].attrib['code']

        if self._last_type == 'success':
            self._last_message = None
            self._last_remaining = root[0].attrib['remaining']
            self._last_resetdate = root[0].attrib['resetdate']
        elif self._last_type == 'error':
            self._last_message = root[0].text
            self._last_remaining = None
            self._last_resetdate = None

            if (not verify or
                    (self._last_code != '400' and self._last_code != '401')):
                self._raise_exception()
        else:
            raise exceptions.UnrecognizedResponseError(xmlresp, -1)

        if len(root) > 1:
            if root[1].tag.lower() == 'retrieve':
                if 'token' in root[1].attrib:
                    self._last_token = root[1].attrib['token']
                    self._last_token_url = root[1].attrib['url']
                    self._last_apikey = None
                elif 'apikey' in root[1].attrib:
                    self._last_token = None
                    self.last_token_url = None
                    self._last_apikey = root[1].attrib['apikey']
                else:
                    raise exceptions.UnrecognizedResponseError(xmlresp, -1)
            else:
                raise exceptions.UnrecognizedResponseError(xmlresp, -1)

        return root

    def _raise_exception(self):

        if self._last_code == '400':
            raise exceptions.FormatError(self._last_message,
                                         int(self._last_code))
        elif self._last_code == '401':
            if 'provider' not in self._last_message.lower():
                raise exceptions.ApiKeyError(self._last_message,
                                             int(self._last_code))
            else:
                raise exceptions.ProviderKeyError(self._last_message,
                                                  int(self._last_code))
        elif self._last_code == '406':
            raise exceptions.RateLimitExceeded(self._last_message,
                                               int(self._last_code))
        elif self._last_code == '409':
            raise exceptions.PermissionDenied(self._last_message,
                                              int(self._last_code))
        elif self._last_code == '500':
            raise exceptions.ServerError(self._last_message,
                                         int(self._last_code))
        else:
            raise exceptions.UnknownError(self._last_message,
                                          int(self._last_code))

    def notify(self, description, event, split=True, kwargs=None):
        """Send a notification to each apikey in self.apikeys.

        Args:
            description: A string of up to DESC_LIMIT characters
                containing the notification text.
            event: A string of up to 1024 characters containing the
                event that is being notified (i.e. subject or brief
                description.)
            split: A boolean indicating whether to split long
                descriptions among multiple notifications (True) or to
                possibly raise an exception (False). (default True)
            kwargs: A dictionary with any of the following strings as
                    keys:
                priority: An integer between -2 and 2, indicating the
                    priority of the notification. -2 is the lowest, 2 is
                    the highest, and 0 is normal.
                url: A string of up to 512 characters containing a URL
                    to attach to the notification.
                (default: None)

        Raises:
            pushnotify.exceptions.FormatError
            pushnotify.exceptions.ApiKeyError
            pushnotify.exceptions.RateLimitExceeded
            pushnotify.exceptions.ServerError
            pushnotify.exceptions.UnknownError
            pushnotify.exceptions.UnrecognizedResponseError

        """

        def send_notify(description, event, kwargs):
            data = {'apikey': ','.join(self.apikeys),
                    'application': self.application,
                    'event': event,
                    'description': description}

            if self.developerkey:
                data['providerkey'] = self.developerkey

            if kwargs:
                data.update(kwargs)

            response_stream = self._post(self._urls['notify'], data)
            self._parse_response_stream(response_stream)

        if split:
            while description:
                this_desc = description[0:DESC_LIMIT]
                description = description[DESC_LIMIT:]
                send_notify(this_desc, event, kwargs)
        else:
            send_notify(description, event, kwargs)

    def retrieve_apikey(self, token):
        """Get an API key for a given token.

        Once a user has approved you sending them push notifications,
        you can supply the returned token here and get an API key.

        Args:
            token: A string containing a registration token returned
                from the retrieve_token method.

        Raises:
            pushnotify.exceptions.ProviderKeyError

        Returns:
            A string containing the API key.

        """

        data = {'providerkey': self.developerkey,
                'token': token}

        response_stream = self._get(self._urls['retrieve_apikey'], data)
        self._parse_response_stream(response_stream)

        return self._last_apikey

    def retrieve_token(self):
        """Get a registration token and approval URL.

        A user follows the URL and logs in to the Prowl website to
        approve you sending them push notifications. If you've
        associated a 'Retrieve success URL' with your provider key, they
        will be redirected there.

        Raises:
            pushnotify.exceptions.ProviderKeyError

        Returns:
            A two-item tuple where the first item is a string containing
            a registration token, and the second item is a string
            containing the associated URL.
        """

        data = {'providerkey': self.developerkey}

        response_stream = self._get(self._urls['retrieve_token'], data)
        self._parse_response_stream(response_stream)

        return self._last_token, self._last_token_url

    def verify_user(self, apikey):
        """Verify a user's API key.

        Args:
            apikey: A string of 40 characters containing a user's API
                key.

        Raises:
            pushnotify.exceptions.RateLimitExceeded
            pushnotify.exceptions.ServerError
            pushnotify.exceptions.UnknownError
            pushnotify.exceptions.UnrecognizedResponseError

        Returns:
            A boolean containing True if the user's API key is valid,
            and False if it is not.

        """

        data = {'apikey': apikey}

        if self.developerkey:
            data['providerkey'] = self.developerkey

        response_stream = self._get(self._urls['verify'], data)
        self._parse_response_stream(response_stream, True)

        return self._last_code == '200'

if __name__ == '__main__':
    pass
