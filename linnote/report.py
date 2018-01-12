#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reporting tools.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from io import StringIO
from operator import attrgetter
from pickle import dump, load
from statistics import mean, median
from re import sub
from matplotlib import pyplot
from linnote import APP_DIR
from linnote.ranking import Ranking


class Report(object):
    """Report for an assessment."""

    composers = {'statistics', 'histogram', 'ranking'}

    def __init__(self, title, assessment, groups=None, **kwargs):
        """
        Prepare the new report object.

        - title:        String. The report's title.
        - assessment:   An 'assessment.Assessment' object. The object of the
                        report.
        - groups:       A list of 'student.Group' objects. If provided,
                        analysis will run for each group independently.
        - kwargs:       A dictionnary. Optionnal static arguments to display in
                        the report.

        Return: None.
        """
        self.title = title
        self.assessment = assessment
        self.groups = groups
        self.kwargs = kwargs
        self.data = list()

    def __repr__(self):
        return '<Report: {}>'.format(self.title)

    def build(self):
        """Build the report."""
        # Compute data.
        general_data = dict(group_name='Général')
        for composer in self.composers:
            compose = getattr(self, composer)
            general_data.update({composer: compose()})

        self.data.append(general_data)

        for group in self.groups:
            group_data = dict(group_name=group.name)

            for composer in self.composers:
                compose = getattr(self, composer)
                group_data.update({composer: compose(group)})

            self.data.append(group_data)

    def save(self, path=APP_DIR.joinpath('ressources', 'private', 'rankings')):
        """Save the report to the filesystem."""
        filename = self.sanitize_filename(self.title)
        dump(self, path.joinpath(filename).open('wb'), -1)

    @staticmethod
    def load(name, path=APP_DIR.joinpath('ressources', 'private', 'rankings')):
        """Load a report from the filesystem."""
        return load(path.joinpath(name).open('rb'))

    @staticmethod
    def sanitize_filename(filename, substitute='-'):
        """
        Sanitize filename so it would be valid on multiple platforms.

        REGEXP is build to sanitize filenames on macOS, windows and UNIX.
        Unallowed characters have been defined using the following references :
        https://msdn.microsoft.com/en-us/library/aa365247#naming_conventions,
        https://en.wikipedia.org/wiki/Filename.

        - filename:     String. The filename to sanitize.
        - substitute:   String. Character or string for replacing unallowed
                        characters in the filename.

        Return: String. The sanitized filename.
        """
        return sub(r'[/\.\\\?<>\|\*:]+', substitute, filename)

    def marks(self, group=None):
        """
        Get assessment marks.

        - group:    A 'Group' object. If provided, only assessment marks of
                    students in the group will be fetched. If not provided, all
                    marks of the assessment will be fetched.

        Return: A list of 'Mark' objects.
        """
        if not group:
            return self.assessment.results

        marks = list()
        for mark in self.assessment.results:
            if mark.student in group:
                marks.append(mark)

        return marks

    # Methods for composing the report.
    def statistics(self, group=None):
        """Descriptive statistics of the group's marks."""
        value = attrgetter('value')
        marks = [value(mark) for mark in self.marks(group)]
        return {
            "size": len(marks),
            "maximum": max(marks, default=0),
            "minimum": min(marks, default=0),
            "mean": mean(marks) if marks else 0,
            "median": median(marks) if marks else 0
        }

    def histogram(self, group=None):
        """Distribution of the group's marks as an histogram."""
        value = attrgetter('value')
        document = StringIO()
        coefficient = self.assessment.coefficient
        marks = [value(mark) for mark in self.marks(group)]

        pyplot.figure(figsize=(6, 4))
        pyplot.hist(marks, bins=coefficient, range=(0, coefficient),
                    color=(0.80, 0.80, 0.80), histtype="stepfilled")
        pyplot.title("Répartition des notes")
        pyplot.savefig(document, format="svg")
        document.seek(0)
        return "\n".join(document.readlines()[5:-1])

    def ranking(self, group=None):
        """Ranking of the group's marks."""
        value = attrgetter('value')
        return Ranking(self.marks(group), key=value)
