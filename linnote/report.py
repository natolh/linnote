#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reporting tools.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from io import StringIO
from operator import attrgetter
from pathlib import Path
from statistics import mean, median
from re import sub
from jinja2 import Environment, PackageLoader
from matplotlib import pyplot
from linnote import APP_DIR
from linnote.ranking import Ranking


ENV = Environment(loader=PackageLoader("linnote"))


class Report(object):
    """Common method for Report classes."""

    template = ENV.get_template('ranking.html')
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
        for group in self.groups:
            group_data = dict(group=group)

            for composer in self.composers:
                compose = getattr(self, composer)
                group_data.update({composer: compose(group)})

            self.data.append(group_data)

        # Fill the report.
        report = self.template.render(rep=self)

        return report.encode('utf8')

    def write(self, path=APP_DIR.joinpath('rankings'), doctype="html"):
        """
        Build and export the report to the filesystem.

        - path:     A path-like object. Directory where the application should
                    write the report.
        - doctype:  A string. Document format in which to provide the report,
                    specify as the extension of this format. Currently, only
                    HTML output is supported.

        Return: None.
        """
        report = self.build()

        folder = Path(path).resolve()
        filename = self.sanitize_filename(self.title) + '.' + doctype
        document = folder.joinpath(filename)

        document.write_bytes(report) # pylint: disable=E1101

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

    def statistics(self, group):
        """Descriptive statistics of the group's marks."""
        value = attrgetter('value')
        marks = [value(m) for m in self.assessment.results if m.student in group]
        return {
            "size": len(marks),
            "maximum": max(marks, default=0),
            "minimum": min(marks, default=0),
            "mean": mean(marks) if marks else 0,
            "median": median(marks) if marks else 0
        }

    def histogram(self, group):
        """Distribution of the group's marks as an histogram."""
        value = attrgetter('value')
        document = StringIO()
        coefficient = self.assessment.coefficient
        marks = [value(m) for m in self.assessment.results if m.student in group]

        pyplot.figure(figsize=(6, 4))
        pyplot.hist(marks, bins=coefficient, range=(0, coefficient),
                    color=(0.80, 0.80, 0.80), histtype="stepfilled")
        pyplot.title("Répartition des notes")
        pyplot.savefig(document, format="svg")
        document.seek(0)
        return "\n".join(document.readlines()[5:-1])

    def ranking(self, group):
        """Ranking of the group's marks."""
        value = attrgetter('value')
        marks = [mark for mark in self.assessment.results if mark.student in group]
        return Ranking(marks, key=value)
