#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement assessment and related objects.

Assessment evaluates students knowledge. The performance of a student to an
assessment is rated as a mark.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from abc import ABC, abstractmethod
from copy import copy
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import List
from pandas import read_excel
from sqlalchemy import Column
from sqlalchemy import Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from linnote.core.user import Student
from linnote.core.utils.database import BASE


class Mark(BASE):
    """
    A mark.

    A mark is composed of a 'score' which represent the performance and a
    'scale' which represent the maximal performance achievable. The score
    never exceed the scale. Sometimes bonus points can be given.
    """

    __tablename__ = 'marks'

    identifier = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('assessments.identifier'))
    student_id = Column(Integer, ForeignKey('students.identifier'))
    _score = Column(Float, nullable=False)
    _bonus = Column(Float)
    _scale = Column(Integer, nullable=False)

    assessment = relationship('Assessment', back_populates='results')
    student = relationship('Student', back_populates='results')

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
            result = copy(self)
            result._score += other.score
            result._bonus += other.bonus
            result._scale += other.scale
            return result

        if other is None or other == 0:
            result = copy(self)
            return result

        return NotImplemented

    def __copy__(self):
        # Reimplement copy to copy the object, not the record.
        return Mark(self.student, self.score, self.scale, bonus=self.bonus)

    def __radd__(self, other):
        return self.__add__(other)

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

    @classmethod
    def load(cls, filepath: Path, scale: int) -> List['Mark']:
        """
        Load results from tabular file.

        Currently, only Excel files are supported. The file should follow a
        predefined, non customizable layout: (1) student identifier, (2)
        score. Further columns are ignored.

        - filepath: Path object. Path pointing to the file to load.
        - scale:    Integer. Scale used to compute marks from scores.
        """
        records = read_excel(
            filepath, names=['student_id', 'score'],
            usecols=[0, 1], converters={'student_id': int, 'score': float})
        records = records.to_dict(orient='list')

        results = list()
        for student_id, score in zip(records['student_id'], records['score']):
            student = Student(student_id)
            mark = cls(student, score, scale)
            results.append(mark)
        return results

    @staticmethod
    def merge(*args: List['Mark']) -> List['Mark']:
        """
        Merge student results for each students.

        - args: List of Mark list. Results list to merge.
        """
        student = attrgetter('student.identifier')

        results = [result for results in args for result in results]
        results.sort(key=student)
        results = [sum(marks) for _, marks in groupby(results, student)]

        return results

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


class Curve(ABC):
    """
    Abstract Base Class for curves.

    A curve transforms marks by applying a function to them. Parameters of the
    function can be either defined by the user or auto-defined?

    About curving:
    - en.wikipedia.org/wiki/Grading_on_a_curve
    - www.wikihow.com/Curve-Grades
    - divisbyzero.com/2008/12/22/how-to-curve-an-exam-and-assign-grades
    - academia.stackexchange.com/questions/8261
    """

    @abstractmethod
    def __call__(self, mark):
        return mark

    def apply(self, sequence):
        marks = map(self, sequence)
        return list(marks)

    @staticmethod
    def _set(mark, new):
        if new > mark.scale:
            mark.bonus = mark.scale - mark.score
        else:
            mark.bonus = new - mark.value
        return mark


class TopLinear(Curve):

    def __init__(self, marks):
        super().__init__()
        self.slope = marks[0].scale / max(marks).value

    def __call__(self, mark):
        new_score = self.slope * mark.value
        return self._set(mark, new_score)


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

    def __repr__(self) -> str:
        return '<Assessment #{}: {}>'.format(self.identifier, self.title)

    def __str__(self) -> str:
        return self.title

    # Should disappear in favor of a merge method (more customizable).
    def __add__(self, other):
        if isinstance(other, Assessment):
            title = f'{self.title} & {other.title}'
            coefficient = self.coefficient + other.coefficient
            precision = min([self.precision, other.precision])

            assessment = Assessment(title, coefficient, precision=precision)
            results = Mark.merge(self.results, other.results)
            assessment.add_results(results)

            return assessment
        return NotImplemented

    def __radd__(self, other):
        if other is 0:
            return self
        return NotImplemented

    def add_result(self, mark: Mark) -> None:
        """
        Add a new result to the assessment.

        - mark: Mark object. The mark to add.

        Ensure that there is not an assessment's result for the student, if so
        raise an AttributeError. If the mark scale is not equal to the
        assessment coefficient, the mark is automatically rescale before being
        added.
        """
        if mark.student not in self.attendees:
            if mark.scale is not self.coefficient:
                mark.rescale(self.coefficient)
            self.results.append(mark)
        raise AttributeError('a result is already known for this student')

    def add_results(self, marks: List[Mark]) -> None:
        """
        Add a collection of results to the assessment.

        - marks:    Collection of Mark objects. The marks to add.

        Ensure that there is not an assessment's result for the student. If
        the mark scale is not equal to the assessment coefficient, the mark is
        automatically rescale before being added.
        """
        attendees = self.attendees
        marks = [mark for mark in marks if mark.student not in attendees]
        if marks[0].scale is not self.coefficient:
            for mark in marks:
                mark.rescale(self.coefficient)
        self.results.extend(marks)

    @property
    def attendees(self) -> List[Student]:
        """
        Students that have taken the assessment.
        """
        get_student = attrgetter('student')
        attendees = map(get_student, self.results)
        return list(attendees)

    def curve(self, name: str) -> None:
        """
        Curve assessment's marks.

        Apply a curve to assessment's marks. The adequate curve is selected by
        it's name.
        To learn about curving read the Curve documentation.
        """
        curves = {'top_linear': TopLinear}
        curve = getattr(curves, name, TopLinear)
        curve = curve(self.results)
        curve.apply(self.results)

    @property
    def expected(self) -> List[Student]:
        """
        Students called for the assessment.
        """
        raise NotImplementedError

    @classmethod
    def merge(cls, title: str, *args) -> 'Assessment':
        """
        Merge assessments into one assessment.

        The product of merging multiple assessments is a new assessment with
        'title' as title. Assessments involved in the merge are preserved.
        """
        # Merge data of assessments.
        coefficient = sum(attrgetter('coefficient'), args)
        precision = min(map(attrgetter('precision'), args))
        results = Mark.merge(*list(map(attrgetter('results'), args)))
        # Create the assessment.
        assessment = cls(title, coefficient, precision=precision)
        assessment.add_results(results)
        return assessment

    def rescale(self, scale: int) -> None:
        """
        Rescale assessment's marks.

        Change the assessment scale to 'scale' and recompute students' marks
        accordingly.
        """
        for mark in self.results:
            mark.rescale(scale)
