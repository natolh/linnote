#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Misceallenous security tools for the application.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

CSP_POLICY = {
    "default-src": [
        "'self'",
        "*.pythonanywhere.com",
        "'unsafe-inline'",
    ],
}
