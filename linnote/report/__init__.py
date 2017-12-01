#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reporting tools.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pathlib import Path
from re import sub
from jinja2 import Environment, PackageLoader
from linnote import APP_DIR


ENV = Environment(loader=PackageLoader("linnote"))


class MetaReport(type):
    """Metaclass for creating Report classes."""

    def __new__(cls, name, template, composers={}):
        """Create a new report class."""
        bases = (Report, )
        attrs = dict()
        return super().__new__(cls, name, bases, attrs)

    def __init__(self, name, template, composers={}):
        """Initialize the new report class."""
        self.template = ENV.get_template(template)
        self.composers = composers


class Report(object):
    """Common method for Report classes."""

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

            for ref, composer in self.composers.items():
                group_data.update({ref: composer(self.assessment, group)})

            self.data.append(group_data)

        # Fill the report.
        report = self.template.render(rep=self)

        return report.encode('utf8')

    def write(self, path=APP_DIR.joinpath('rankings'), format="html"):
        """
        Build and export the report to the filesystem.

        - path:     A path-like object. Directory where the application should
                    write the report.
        - format:   A string. Document format in which to provide the report,
                    specify as the extension of this format. Currently, only
                    HTML output is supported.

        Return: None.
        """
        report = self.build()

        folder = Path(path).resolve()
        filename = self.sanitize_filename(self.title) + '.' + format
        document = folder.joinpath(filename)
        document.write_bytes(report)

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
