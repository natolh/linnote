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
    group = Group(name=name)

    students = read_excel(
        file, names=['identifier', 'first_name', 'last_name', 'email'])
    students = students.to_dict('records')
    for student in students:
        user = User(student['first_name'], student['last_name'], student['email'])
        student = Student(identity=user, aid=int(student['identifier']))
        group.append(user)
    return group
