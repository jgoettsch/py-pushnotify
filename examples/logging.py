#!/usr/bin/env python
# vim: set fileencoding=utf-8

"""A simple example of how to make use of logging.

For more information about logging in Python,
see: http://docs.python.org/library/logging.html

copyright: Copyright (c) Jeffrey Goettsch and other contributors.
license: BSD, see LICENSE for details.

"""

import logging
import pushnotify
from pushnotify import get_client


def main():
    """The output should be something like:

    pushnotify.nma.Client-DEBUG: _post sending data: \
        application=pushnotify+examples&apikey=0123456789012345678901234\
        56789012345678901234567&event=logging+example&description=\
        testing+the+logging+capabilities+of+the+pushnotify+package
    pushnotify.nma.Client-DEBUG: _post sending to url: \
        https://www.notifymyandroid.com/publicapi/notify
    pushnotify.nma.Client-INFO: _post received response: \
        <?xml version="1.0" encoding="UTF-8"?><nma><error code="401" >\
        None of the API keys provided were valid.</error></nma>

    """

    logger = logging.getLogger('pushnotify')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s-%(levelname)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # an obviously invalid API Key

    apikey = '012345678901234567890123456789012345678901234567'

    client = get_client('nma', application='pushnotify examples')
    client.add_key(apikey)

    event = 'logging example'
    desc = 'testing the logging capabilities of the pushnotify package'

    # this will raise an exception because the API Key is invalid

    try:
        client.notify(desc, event, split=True)
    except pushnotify.exceptions.ApiKeyError:
        pass


if __name__ == '__main__':
    main()
