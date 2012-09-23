#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""Module for abstract class.

copyright: Copyright (c) Jeffrey Goettsch and other contributors.
license: BSD, see LICENSE for details.

"""

import logging
import urllib
import urllib2


class AbstractClient(object):
    """Abstract client for sending push notifications. Inherit from this
    class but don't call it directly.

    """

    def __init__(self, type_, developerkey, application=''):
        """Initialize the client.

        """

        self.logger = logging.getLogger('{0}.{1}'.format(
            self.__module__, self.__class__.__name__))

        self.type = type_
        self.developerkey = developerkey
        self.application = application
        self.apikeys = {}

        self._browser = urllib2.build_opener(urllib2.HTTPSHandler())
        self._last = {}
        self._urls = {'notify': '', 'verify': ''}

    def _get(self, url, data):

        querystring = urllib.urlencode(data)
        url = '?'.join([url, querystring])

        self.logger.debug('_get requesting url: {0}'.format(url))

        request = urllib2.Request(url)
        try:
            response_stream = self._browser.open(request)
        except urllib2.HTTPError, exc:
            return exc
        else:
            return response_stream

    def _post(self, url, data):

        self.logger.debug('_post sending data: {0}'.format(data))
        self.logger.debug('_post sending to url: {0}'.format(url))

        request = urllib2.Request(url, data)
        try:
            response_stream = self._browser.open(request)
        except urllib2.HTTPError, exc:
            return exc
        else:
            return response_stream

    def add_key(self, apikey, device_key=''):

        if apikey not in self.apikeys:
            self.apikeys[apikey] = []

        if device_key and device_key not in self.apikeys[apikey]:
            self.apikeys[apikey].append(device_key)

    def del_key(self, apikey, device_key=''):

        if device_key:
            self.apikeys[apikey] = [value for value in self.apikeys[apikey]
                                    if value != device_key]
        else:
            del(self.apikeys[apikey])

    def notify(self, description, event, split=True, kwargs=None):

        raise NotImplementedError

    def retrieve_apikey(self, reg_token):

        raise NotImplementedError

    def retrieve_token(self):

        raise NotImplementedError

    def verify_device(self, apikey, device_key):

        raise NotImplementedError

    def verify_user(self, apikey):

        raise NotImplementedError
