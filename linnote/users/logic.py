#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Forms for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pathlib import Path
from pandas import read_excel
from linnote.core.user import Group, Student, User


def load_group(file: Path, name: str = None) -> Group:
    """
    Load a student group from an excel file.

    - file: A path-like object. The path to the file.
    - name: String. The group's name.

    Return: A 'Group' object.
    """
    fields = ['identifier', 'firstname', 'lastname', 'email']
    types = {'identifier': int}

    records = read_excel(file, names=fields, dtypes=types)
    records = records.to_dict('records')

    group = Group(name=name)
    for record in records:
        user = User(record['firstname'], record['lastname'], record['email'])
        Student(identity=user, aid=record['identifier'])
        group.append(user)
    return group
