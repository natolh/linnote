#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Buisness logic for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pathlib import Path
from typing import List
from pandas import read_excel
from linnote.core.assessment import Mark
from linnote.core.user import Student
from linnote.core.utils import DATA


def load_results(file: Path, scale: int) -> List['Mark']:
    """
    Load marks from a tabular file.

    Currently, only Excel files are supported. The file should follow a
    predefined, non customizable layout: (1) student identifier, (2) score.
    Further columns are ignored.

    - filepath: Path pointing to the file to load.
    - scale:    Scale used to compute marks from scores.
    """
    records = read_excel(
        file, names=['student_id', 'score'], usecols=[0, 1],
        converters={'student_id': int, 'score': float})
    records = records.to_dict(orient='list')

    results = list()
    for student_id, score in zip(records['student_id'], records['score']):
        student = DATA.query(Student).filter_by(aid=student_id).first()
        if student is not None:
            mark = Mark(student, score, scale)
            results.append(mark)
    return results
