#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""Module for sending push notifications to Android devices that have
Notify My Android installed. See www.notifymyandroid.com/ for more
information.

"""


import urllib
import urllib2
try:
    from xml.etree import cElementTree
    ElementTree = cElementTree
except ImportError:
    from xml.etree import ElementTree


PUBLIC_API_URL = u'https://www.notifymyandroid.com/publicapi'
VERIFY_URL = u'/'.join([PUBLIC_API_URL, 'verify'])
NOTIFY_URL = u'/'.join([PUBLIC_API_URL, 'notify'])

LIMITS = {
    u'apikey': 48,
    u'application': 256,
    u'event': 1000,
    u'description': 10000,
    u'developerkey': 48,
    u'url': 2000}


class Client(object):
    """Client for the Notify My Android applications.

    Member Vars:
        apikeys: A list of strings, each containing a valid api key.
        developerkey: A string containing a valid developer key.

    """

    def __init__(self, apikeys=None, developerkey=None):
        """Initialize the Notify My Android client.

        Args:
            apikeys:  A list of strings, each containing a valid api
                key.
            developerkey: A string containing a valid developer key.

        """

        self._browser = urllib2.build_opener(urllib2.HTTPSHandler())
        self._last_type = None
        self._last_code = None
        self._last_message = None
        self._last_remaining = None
        self._last_resettimer = None

        self.apikeys = [] if apikeys is None else apikeys
        self.developerkey = developerkey

    def _get(self, url):

        request = urllib2.Request(url)
        response_stream = self._browser.open(request)
        response = response_stream.read()

        return response

    def _parse_response(self, xmlresp):

        root = ElementTree.fromstring(xmlresp)

        self._last_type = root[0].tag.lower()
        self._last_code = root[0].attrib['code']

        if self._last_type == 'success':
            self._last_message = None
            self._last_remaining = root[0].attrib['remaining']
            self._last_resettimer = root[0].attrib['resettimer']
        elif self._last_type == 'error':
            self._last_message = root[0].text
            self._last_remaining = None
            self._last_resettimer = None
        else:
            pass
            # TODO: throw an UnrecognizedResponse exception or something

        return root

    def _post(self, url, data):

        request = urllib2.Request(url, data)
        response_stream = self._browser.open(request)
        response = response_stream.read()

        return response

    def notify(self, app, event, desc, kwargs=None):
        """Send a notification to each apikey in self.apikeys.

        Args:
            app: A string containing the name of the application sending
                the notification.
            event: A string containing the event that is being notified
                (subject or brief description.)
            desc: A string containing the notification text.
            kwargs: A dictionary with any of the following strings as
                    keys:
                priority: An integer between -2 and 2, indicating the
                    priority of the notification. -2 is the lowest, 2 is
                    the highest, and 0 is normal.
                url: A string containing a URL to attach to the
                    notification.
                content_type: A string containing "text/html" (without
                    the quotes) that then allows some basic HTML to be
                    used while displaying the notification.
                (default: None)

        Returns:
            A boolean containing True of the notifications were sent
            successfully, and False if they were not. For multiple API
            keys, only return False if they all failed.

        """

        data = {'apikey': ','.join(self.apikeys),
                'application': app,
                'event': event,
                'description': desc}

        if self.developerkey:
            data['developerkey'] = self.developerkey

        if kwargs:
            data.update(kwargs)

        data = urllib.urlencode(data)

        response = self._post(NOTIFY_URL, data)
        self._parse_response(response)

        return self._last_code == '200'

    def verify(self, apikey):
        """Verify an API key.

        Args:
            apikey: A string containing a valid API key.

        Raises:
            urllib2.HTTPError
            urllib2.URLError

        Returns:
            A boolean containing True if the API key is valid, and False
            if it is not.

        """

        querystring = urllib.urlencode({'apikey': apikey})
        url = '?'.join([VERIFY_URL, querystring])

        response = self._get(url)
        self._parse_response(response)

        return self._last_code == '200'

if __name__ == '__main__':
    pass
