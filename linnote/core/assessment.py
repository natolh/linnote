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
from sqlalchemy import Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from werkzeug.datastructures import FileStorage
from linnote.core.user import Student
from linnote.core.utils.database import BASE


class Mark(BASE):
    """Student's mark to an assessment."""

    __tablename__ = 'marks'

    identifier = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('assessments.identifier'))
    student_id = Column(Integer, ForeignKey('students.identifier'))
    _score = Column(Float, nullable=False)
    _bonus = Column(Float)
    _scale = Column(Integer, nullable=False)

    assessment = relationship('Assessment', back_populates='results')
    student = relationship('Student', back_populates='results', cascade='all')

    def __init__(self, student, score, scale, **kwargs):
        """
        Create a new mark.

        - student:      <Student> object. The student that has obtain the mark.
        - score:        Float. Student's score for the assessment.
        - scale:        Numeric. Maximal possible score for the assessment.
        * bonus:        Float. Student's bonus points for the assessment.

        Return: None.
        """
        super().__init__()
        self.student = student
        self._scale = scale
        self._score = score
        self._bonus = kwargs.get('bonus', 0)

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
            return Mark(self.student,
                        self.score + other.score,
                        self.scale + other.scale,
                        bonus=self.bonus + other.bonus)

        return NotImplemented

    def __radd__(self, other):
        if other is 0:
            return self

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.identifier)

    @property
    def bonus(self):
        """Mark bonus value."""
        return self._bonus

    @bonus.setter
    def bonus(self, value):
        """Change the score bonus."""
        self._bonus = value

    def rescale(self, scale):
        """
        Rescale the mark.

        - scale:    Integer. The new desired scale.

        Return: None.
        """
        self._score = (self._score / self._scale) * scale
        self._bonus = (self._bonus / self._scale) * scale
        self._scale = scale

    @property
    def scale(self):
        """Mark scale."""
        return self._scale

    @property
    def score(self):
        """Mark raw value."""
        return self._score

    @score.setter
    def score(self, value):
        """Change the score value."""
        self._score = value

    @property
    def value(self):
        """The processed mark, including bonus points."""
        return self._score + self._bonus


class Assessment(BASE):
    """
    Evaluation of students knowledge.

    - identifier:   Integer. A unique number to identify the assessment.
    - title:        String. String for assessment identification by humans.
    - coefficient:  Integer. Maximal possible score.
    - precision:    Integer. Maximal number of decimals to keep for mark
                    computations.
    - results:      Collection of Mark. Students marks to the assessment.
    - reports:      Collection of Report.
    """

    # Change name of 'coefficient' attribute to 'scale'. Make this
    # attribute private (_scale) and make a setter that automatically call the
    # 'rescale' method on modification.

    __tablename__ = 'assessments'

    identifier = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False, index=True)
    coefficient = Column(Integer, nullable=False)
    precision = Column(Integer, nullable=False, default=3)
    creator_id = Column(Integer, ForeignKey('users.identifier'))
    creation_date = Column(
        DateTime, nullable=False, server_default=current_timestamp())

    creator = relationship('User', uselist=False)
    results = relationship('Mark', back_populates='assessment', cascade='all')
    reports = relationship('Report', back_populates='assessment')

    def __init__(self, title: str, coefficient: int, **kwargs) -> None:
        super().__init__()
        self.title = title
        self.coefficient = coefficient
        self.precision = kwargs.get('precision', 3)
        self.creator = kwargs.get('creator', None)

        if isinstance(kwargs.get('results'), FileStorage):
            self.load(kwargs.get('results'), scale=kwargs.get('scale'))

        if isinstance(kwargs.get('results'), list):
            self.results = kwargs.get('results')

    def __repr__(self) -> str:
        return '<Assessment #{}: {}>'.format(self.identifier, self.title)

    def __str__(self) -> str:
        return self.title

    def __add__(self, other):

        def merge_results(*args):
            """
            Merge students results of multiple assessments.

            - args: <Assessment> objects. Assessments to merge.

            Return: List of <Mark> objects. Merged marks for each student.
            """
            by_student = attrgetter('student.identifier')
            results = [i for assessment in args for i in assessment.results]
            results.sort(key=by_student)
            return [sum(marks) for _, marks in groupby(results, by_student)]

        if isinstance(other, Assessment):
            return Assessment(title='[{} {}]'.format(self.title, other.title),
                              coefficient=self.coefficient + other.coefficient,
                              precision=min([self.precision, other.precision]),
                              results=merge_results(self, other))

        return NotImplemented

    def __radd__(self, other):
        if other is 0:
            return self

        return NotImplemented

    def load(self, path, scale):
        """
        Load assessment's results from a tabular file.

        - path:     Path-like object. Path to the file holding the results.
        - scale:    Integer. Scale for marks in the result file.

        Return: None.
        """
        results = read_excel(path, names=['anonymat', 'note'], usecols=1)

        for result in results.to_dict('records'):
            student = Student(identifier=int(result['anonymat']))
            mark = Mark(student, float(result['note']), scale)

            if not scale == self.coefficient:
                mark.rescale(self.coefficient)

            self.results.append(mark)

    def rescale(self, new_scale: int) -> None:
        """
        Rescale assessment's results.

        Change the assessment 'scale' and recompute students scores for the
        new 'scale'.

        - new_scale: Integer. The desired scale.
        """
        for mark in self.results:
            mark.rescale(new_scale)

    def transform(self) -> None:
        """Mark post-process function."""
        maximum = max(self.results).value

        for mark in self.results:
            bonus = (mark.value / maximum) * (mark.scale - maximum)

            if not mark.value + bonus > mark.scale:
                mark.bonus += bonus
            else:
                mark.bonus = mark.scale - mark.value
