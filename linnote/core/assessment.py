#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Assessments models and related.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from itertools import groupby
from operator import attrgetter
from pandas import read_excel
from sqlalchemy import Column
from sqlalchemy import Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from werkzeug.datastructures import FileStorage
from linnote.core.user import Student
from linnote.core.utils.database import Base


class Mark(Base):
    """Student's mark to an assessment."""

    __tablename__ = 'marks'
    identifier = Column(Integer, primary_key=True)
    student = relationship('Student')
    coefficient = Column(Integer, nullable=False)
    _raw = Column(Float)
    _bonus = Column(Float)

    student_id = Column(Integer, ForeignKey('students.identifier'))
    assessment_id = Column(Integer, ForeignKey('assessments.identifier'))

    def __init__(self, student, score, scale, **kwargs):
        """
        Create a new mark.
        
        - student:      <Student> object. The student that has obtain the mark.
        - score:        Float. Student's score for the assessment.
        - scale:        Numeric. Maximal possible score for the assessment.
        * bonus:        Float. Student's bonus points for the assessment.
        * coefficient:  Numeric. Coefficient of the assessment.

        Return: None.
        """
        super().__init__()
        self.student = student
        self.coefficient = kwargs.get('coefficient', scale)
        self._raw = score / scale
        self._bonus = kwargs.get('bonus', 0) / scale

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
            return Mark(self.student, self._raw + other._raw, 2,
                        coefficient=self.coefficient + other.coefficient,
                        bonus=self._bonus + other._bonus)

        return NotImplemented

    def __radd__(self, other):
        if other is 0:
            return self

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
    """Evaluation of students knowledge."""

    __tablename__ = 'assessments'
    identifier = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False, unique=True, index=True)
    coefficient = Column(Integer, nullable=False)
    precision = Column(Integer, nullable=False, default=3)
    results = relationship('Mark')

    def __init__(self, title, coefficient, **kwargs):
        """
        Create a new assessment.

        - title:        String. Assessment's title.
        - coefficient:  Float. Output scale.
        * precision:    Integer. Number of decimal places for displaying marks.
        * results:      Path-like object. Path to the file holding results to 
                        import.
        * scale:        Integer. Scale used in 'results'.

        Return: None.
        """
        super().__init__()
        self.title = title
        self.coefficient = coefficient
        self.precision = kwargs.get('precision', 3)

        if isinstance(kwargs.get('results'), FileStorage):
            self.load(kwargs.get('results'), scale=kwargs.get('scale'))

    def __repr__(self):
        return '<Assessment #{}: {}>'.format(self.identifier, self.title)

    def __add__(self, other):
        if isinstance(other, Assessment):
            assessments = [self, other]
            assessment = Assessment(
                title=None,
                coefficient=self.coefficient + other.coefficient,
                precision=min([self.precision, other.precision]))
            assessment.results = list(self._aggregate(assessments))
            return assessment

        return NotImplemented

    def __radd__(self, other):
        if other is 0:
            return self

        return NotImplemented

    @staticmethod
    def _aggregate(assessments):
        """Aggregate students results of multiple assessments."""
        by_student = attrgetter('student.identifier')
        results = [mark for a in assessments for mark in a.results]
        results.sort(key=by_student)

        for _, marks in groupby(results, by_student):
            marks = list(marks)
            yield sum(marks)

    def load(self, path, scale):
        """
        Load assessment's results from a tabular file.

        - path: Path-like object. Path to the file holding the results.

        Return: None.
        """
        results = read_excel(path, names=['anonymat', 'note'], usecols=1)

        for result in results.to_dict('records'):
            student = Student(identifier=int(result['anonymat']))
            mark = Mark(student, float(result['note']), scale,
                        coefficient=self.coefficient)
            self.results.append(mark)

    def rescale(self):
        """Rescale assessment's results."""
        maximum = max(self.results)._raw
        for mark in self.results:
            mark._bonus = (mark._raw / maximum) - mark._raw
