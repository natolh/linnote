#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement assessments and related tools.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from functools import reduce
from itertools import groupby
from operator import add, attrgetter
from pandas import read_excel
from sqlalchemy import Column
from sqlalchemy import Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from .student import Student
from .utils.database import Base


class Mark(Base):
    """Student's mark to an assessment."""

    __tablename__ = 'marks'

    identifier = Column(Integer, primary_key=True)
    student = relationship('Student')
    student_id = Column(Integer, ForeignKey('students.identifier'))
    coefficient = Column(Integer, nullable=False)
    _raw = Column(Float)
    _bonus = Column(Float)

    assessment_id = Column(Integer, ForeignKey('assessments.identifier'))

    def __init__(self, student, coefficient, score, scale=1, bonus=0):
        """Initialize a new mark."""
        super().__init__()
        self.student = student
        self.coefficient = coefficient
        self._raw = score / scale
        self._bonus = bonus / scale

    def __repr__(self):
        return '<Mark of {}: {}>'.format(self.student, self.value)

    def __eq__(self, other):
        if isinstance(other, Mark):
            return self.value == other.value

        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, Mark):
            return self.value > other.value

        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Mark):
            return self.value < other.value

        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Mark):
            return self.value >= other.value

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Mark):
            return self.value <= other.value

        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Mark) and self.student == other.student:
            score = self.raw + other.raw
            bonus = self.bonus + other.bonus
            coefficient = self.coefficient + other.coefficient
            return Mark(self.student, coefficient, score, coefficient, bonus)

        return NotImplemented

    def __hash__(self):
        return hash(self.identifier)

    @property
    def raw(self):
        """Mark raw value."""
        return self._raw * self.coefficient

    @property
    def bonus(self):
        """Mark bonus value."""
        return self._bonus * self.coefficient

    @property
    def value(self):
        """The processed mark, including bonus points."""
        return (self._raw + self._bonus) * self.coefficient


class Assessment(Base):
    """
    Evaluation of students knowledge.

    - scale:        Float. Actual scale in results file.
    - coefficient:  Integer. Desired scale for output.
    - precision:    Integer. Number of decimals for outputing marks.
    """

    __tablename__ = 'assessments'

    identifier = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False, unique=True, index=True)
    scale = Column(Float, nullable=False)
    coefficient = Column(Integer, nullable=False)
    precision = Column(Integer, nullable=False, default=3)
    results = relationship('Mark')

    def __init__(self, title, scale, coefficient, precision, results=None):
        """
        Initialize a new assessment.
        - scale:        Float. Actual scale in results file.
        - coefficient:  Float. Desired scale for output.
        - precision:    Integer. Number of decimals for outputing marks.
        - results:      Path-like object. Path pointing to the results file.

        Return: None.
        """
        super().__init__()
        self.title = title
        self.scale = scale
        self.coefficient = coefficient
        self.precision = precision
        self.results = self.load(results) if results else list()

    def __repr__(self):
        return '<Assessment>'

    def load(self, file):
        """
        Load students results from an excel file.

        - file: A path-like object. Path poiting to the file holding the
                results.

        Return: A list of 'Mark' objects.
        """
        results = read_excel(file, names=['anonymat', 'note'], usecols=1)

        stack = list()
        for result in results.to_dict('records'):
            student = Student(identifier=int(result['anonymat']))
            mark = Mark(student, self.coefficient, float(result['note']), self.scale)
            stack.append(mark)

        return stack

    def rescale(self):
        """Rescale assessment's results."""
        maximum = max(self.results)._raw
        for mark in self.results:
            mark._bonus = (mark._raw / maximum) - mark._raw

    def aggregate(self, tests):
        """Aggregate students results to assessments."""
        by_student = attrgetter('student.identifier')

        results = [mark for test in tests for mark in test.results]
        results.sort(key=by_student)

        for _, marks in groupby(results, by_student):
            marks = list(marks)

            if len(marks) == len(tests):
                mark = reduce(add, marks)
                self.results.append(mark)
