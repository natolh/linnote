#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
WSGI connector.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from linnote.client import create_app
from linnote.client import api, admin, site, accounts, assessments, users


BLUEPRINTS = [api, admin, site, accounts, assessments, users]
APPLICATION = create_app('linnote', config_path='configuration.ini',
                         blueprints=BLUEPRINTS)
