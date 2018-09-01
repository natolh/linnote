#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement database related tools.

Define a 'Base' class that sould be inherited by every class to persist in the
database. Define a 'web_session' object to be used in the client to perform
actions on the database. Define a 'configure' function for binding the
'web_session' to the client.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from functools import partial
from jwt import encode, decode
from .configuration import load as load_configuration


CONFIG = load_configuration('configuration.ini')
SECRET = CONFIG['FLASK']['SECRET_KEY']


# pylint: disable=C0103
encode = partial(encode, key=SECRET, algorithm='HS256', headers=None,
                 json_encoder=None)
decode = partial(decode, key=SECRET)
