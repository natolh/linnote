#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Miscellaneaous tools.

Currently contains tools for connecting to the database and tools for loading
configuration file.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from .configuration import load as load_configuration
from .database import configure, SESSION, WEBSESSION
from .security import CSP_POLICY
