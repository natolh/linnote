#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Misceallenous tools for report package.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from re import sub


def sanitize_filename(filename, rep='-'):
    """Return a cross-plateform valid filename."""
    return sub(r'[/\.\\\?<>\|\*:]+', rep, filename)
