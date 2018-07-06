#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WSGI connector.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from linnote.core import create_app
from linnote import accounts, assessments, reports, services, users


BLUEPRINTS = [accounts, assessments, reports, services, users]
APPLICATION = create_app('linnote', config_path='configuration.ini',
                         blueprints=BLUEPRINTS)
