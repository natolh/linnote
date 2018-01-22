#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Script to build the SECRET_KEY needed in the config.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from binascii import hexlify
from os import urandom as random


def make_secret(size=40):
    """Compute a random string to use as SECRET_KEY for the app."""
    secret = random(size)
    secret = hexlify(secret)
    return secret.decode('utf8')


if __name__ == '__main__':
    SIZE = input('Size for secret key: ')
    SECRET = make_secret(int(SIZE))
    print(SECRET)
