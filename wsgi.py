#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WSGI connector.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from linnote import account, assessments, services, users
from linnote.core import create_app


BLUEPRINTS = [account, assessments, services, users]
APPLICATION = create_app('linnote', config_path='configuration.ini',
                         blueprints=BLUEPRINTS)
