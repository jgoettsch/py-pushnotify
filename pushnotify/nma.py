#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""Module for sending push notifications to Android devices that have
Notify My Android installed. See www.notifymyandroid.com/ for more
information.

"""

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

        self.apikeys = [] if apikeys is None else apikeys
        self.developerkey = developerkey

    def notify(self, app, event, desc, kwargs=None):
        """Send a notification.

        Args:
            app:
            event:
            desc:
            kwargs:

        """

        pass

    def verify(self, apikey):
        """Verify an API key.

        Args:
            apikey: A string containing a valid API key.

        """

        pass


if __name__ == '__main__':
    pass
