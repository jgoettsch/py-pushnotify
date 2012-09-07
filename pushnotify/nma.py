#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""Module for sending push notifications to Android devices that have
Notify My Android installed. See www.notifymyandroid.com/ for more
information.

"""


import urllib
import urllib2


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

        self.apikeys = [] if apikeys is None else apikeys
        self.developerkey = developerkey

    def _get(self, url):

        request = urllib2.Request(url)
        response_stream = self._browser.open(request)
        response = response_stream.read()

        return response

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

        return self._post(NOTIFY_URL, data)

    def verify(self, apikey):
        """Verify an API key.

        Args:
            apikey: A string containing a valid API key.

        Raises:
            urllib2.HTTPError
            urllib2.URLError

        Returns:
            A string containing the XML from the verify call.

        """

        querystring = urllib.urlencode({'apikey': apikey})
        url = '?'.join([VERIFY_URL, querystring])

        return self._get(url)

if __name__ == '__main__':
    pass
