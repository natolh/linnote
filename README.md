# linnote

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c9d4a74280bb4613963a53bfe1b80576)](https://www.codacy.com/app/natolh/linnote?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=natolh/linnote&amp;utm_campaign=Badge_Grade)
![GitHub release](https://img.shields.io/github/release/natolh/linnote.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/natolh/linnote.svg)
![Python Badge](https://img.shields.io/badge/python-3.5%2C%203.6-brightgreen.svg)
![license](https://img.shields.io/github/license/natolh/linnote.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/natolh/linnote.svg)

## Introduction

`linnote`is a web application to manage assessments marks and rankings. It has been developped for the Tutorat Santé Lyon Sud in order to ease the process of making ranking reports of mock examinations organized by the association.

The Tutorat Santé Lyon Sud has used `linnote` in production since 2016 at [natolh.pythonanywhere.com](natolh.pythonanywhere.com). Until november 2017 it was not really an application but a mere command tool line. Since version 1.5.0, `linnote` is now a web application and is freely available here on GitHub.

## What it does ?

Not as much as we expect, but still save us a lot of time at the Tutorat Santé Lyon Sud.

### Core
- Importation of marks files (Excel), with an option to rescale marks at importation.
- Mark curving (post-treatment). Algorithm is not customizable in the user interface.
- Creation of report on single assessment or multiple assessments displaying:
  - Univariate statistics on assessment's marks (or on marks of merged assessments), if needed can be performed on sub-groups of students. Computed statistics are not customizable in the user interface.
  - Marks distribution plot, if needed can be performed on sub-groups of students.
  - Students marks (raw and adjusted).
  - Students ranking, if needed ranking can be performed by sub-groups of students. The ranking algorithm is currently not customizable in the user interface.

### Additional
- Manage admin accounts (creation, deletion).
- User account management (firstname, lastname, email adress, password).
- Manage students group (creation (importation), deletion).

## Technical informations

`linnote` is a web application coded in [Python3](https://python.org) using the [Flask](http://flask.pocoo.org/) framework. You can consult the project dependancies in the available Pipfile but for short, it uses:

- [SQLAlchemy](http://www.sqlalchemy.org/): ORM to link with the database.
- [alembic](http://alembic.zzzcomputing.com/en/latest/): for migrating database schema.
- [pandas](https://pandas.pydata.org/) avec [xlrd](https://github.com/python-excel/xlrd): for importing tabular files (xlrd is for Excel ones).
- [matplotlib](https://matplotlib.org/): for plotting some graphics.
- [flask-login](https://flask-login.readthedocs.io/en/latest/): to login users.
- [flask-wtf](https://flask-wtf.readthedocs.io/en/stable/): to write forms.

## Development

The code has been written using [VSCode](https://code.visualstudio.com/) with the official Python extension. [PyLint](https://www.pylint.org/) is used to check code quality and potential errors.

# Installation
Coming soon.

# Usage
Coming soon.
