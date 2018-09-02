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
from typing import List
from sqlalchemy import Column
from sqlalchemy import Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from .user import Student
from .utils import BASE


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
    student_id = Column(Integer, ForeignKey('profiles__students.identifier'))
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

    def __lt__(self, other):
        if isinstance(other, Mark):
            return self.value < other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Mark):
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Mark):
            return self.value <= other.value
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Mark):
            return self.value >= other.value
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

    def __radd__(self, other):
        return self.__add__(other)

    def __copy__(self):
        return Mark(self.student, self.score, self.scale, bonus=self.bonus)

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


class Grader(ABC):
    """
    Abstract Base Class for graders.

    Automatically assign a grade based on student's score according to a
    formula. The formula can auto-adjust it's parameters or parameters can be
    defined by the user.

    About grading:
    - https://en.wikipedia.org/wiki/Grading_on_a_curve
    - https://www.wikihow.com/Curve-Grades
    - https://divisbyzero.com/2008/12/22/how-to-curve-an-exam-and-assign-grades
    - https://academia.stackexchange.com/questions/8261
    """

    @abstractmethod
    def __call__(self, mark):
        return mark

    def apply(self, sequence):
        """Apply the curve to a sequence of marks."""
        marks = map(self, sequence)
        return list(marks)

    @staticmethod
    def _set(mark: Mark, new: float) -> Mark:
        if new > mark.scale:
            mark.bonus = mark.scale - mark.score
        else:
            mark.bonus = new - mark.value
        return mark


class TopLinear(Grader):
    """
    Top-Linear grader.

    Transform the best mark of the assessment to reach the top of the scale.
    Transform following marks proportionnaly.
    """

    def __init__(self, marks):
        super().__init__()
        self.slope = marks[0].scale / max(marks).value

    def __call__(self, mark: Mark) -> Mark:
        score = self.slope * mark.value
        return self._set(mark, score)


class Assessment(BASE):
    """
    Evaluation of students knowledge.

    - identifier:   Integer. A unique number to identify the assessment.
    - title:        String. String for assessment identification by humans.
    - scale:        Integer. Maximal possible score.
    - precision:    Integer. Maximal number of decimals to keep for mark
                    computations.
    - results:      Collection of Mark. Students marks to the assessment.
    - reports:      Collection of Report.
    """

    __tablename__ = 'assessments'

    identifier = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False, index=True)
    scale = Column(Integer, nullable=False)
    precision = Column(Integer, nullable=False, default=3)
    creator_id = Column(Integer, ForeignKey('users.identifier'))
    creation_date = Column(
        DateTime, nullable=False, server_default=current_timestamp())

    creator = relationship('User', uselist=False)
    results = relationship('Mark', back_populates='assessment', cascade='all')
    rankings = relationship('Ranking', back_populates='assessment', cascade='all')

    def __init__(self, title: str, scale: int, **kwargs) -> None:
        super().__init__()
        self.title = title
        self.scale = scale
        self.precision = kwargs.get('precision', 3)
        self.creator = kwargs.get('creator', None)

    def __repr__(self) -> str:
        return '<Assessment #{}: {}>'.format(self.identifier, self.title)

    def __str__(self) -> str:
        return self.title

    def add_result(self, mark: Mark) -> None:
        """
        Add a new result to the assessment.

        - mark: Mark object. The mark to add.

        Ensure that there is not an assessment's result for the student, if so
        raise an AttributeError. If the mark scale is not equal to the
        assessment scale, the mark is automatically rescale before being
        added.
        """
        if mark.student not in self.attendees:
            if mark.scale is not self.scale:
                mark.rescale(self.scale)
            self.results.append(mark)
        raise AttributeError('a result is already known for this student')

    def add_results(self, marks: List[Mark]) -> None:
        """
        Add a collection of results to the assessment.

        - marks:    Collection of Mark objects. The marks to add.

        Ensure that there is not an assessment's result for the student. If
        the mark scale is not equal to the assessment scale, the mark is
        automatically rescale before being added.
        """
        attendees = self.attendees
        marks = [mark for mark in marks if mark.student not in attendees]
        if marks[0].scale is not self.scale:
            for mark in marks:
                mark.rescale(self.scale)
        self.results.extend(marks)

    @property
    def attendees(self) -> List[Student]:
        """
        Students that have taken the assessment.
        """
        get_student = attrgetter('student')
        attendees = map(get_student, self.results)
        return list(attendees)

    def grade(self, name: str) -> None:
        """Grade the assessment."""
        graders = {'top_linear': TopLinear}
        grader = getattr(graders, name, TopLinear)
        grader = grader(self.results)
        grader.apply(self.results)

    @property
    def expected(self) -> List[Student]:
        """
        Students called for the assessment.
        """
        raise NotImplementedError

    @classmethod
    def merge(cls, title: str, *assessments) -> 'Assessment':
        """
        Merge multiple assessments into one.

        Create a new Assessment with 'title' as title. Other attributes of the
        new Assessment are determined using this function accordingly to the
        set of assessments to merge.
        """
        # Merge.
        scales = [assessment.scale for assessment in assessments]
        scale = sum(scales)

        precision = min([assessment.precision for assessment in assessments])

        results = [assessment.results for assessment in assessments]
        results = Mark.merge(results)

        # Create the new assessment.
        assessment = cls(title, scale, precision=precision)
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

    def get_results(self, group=None):
        """
        Fetch assessment's results or a part of it.

        If group is provided, only results of group's members are returned.
        Else, all assessment's results are returned.
        """
        if group:
            res = filter(lambda m: m.student.identity in group, self.results)
            return list(res)
        return self.results
