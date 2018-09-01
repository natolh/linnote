# linnote

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c9d4a74280bb4613963a53bfe1b80576)](https://www.codacy.com/app/natolh/linnote?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=natolh/linnote&amp;utm_campaign=Badge_Grade)
![GitHub release](https://img.shields.io/github/release/natolh/linnote.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/natolh/linnote.svg)
![Python Badge](https://img.shields.io/badge/python-3.6-brightgreen.svg)
![license](https://img.shields.io/github/license/natolh/linnote.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/natolh/linnote.svg)

## Introduction

`linnote` is a web application to manage assessments marks and create rankings. It has been developped by and for the [Tutorat Santé Lyon Sud](https://twitter.com/tutsantels) in order to ease the process of creating assessments' rankings. Mock assessments are organized at least each week during the year, and rankings should be issued for a number of specific students groups to mimic the official examinations of the university.

The Tutorat Santé Lyon Sud has used `linnote` since 2016. Until november 2017 it was a mere command tool line. Now it is a web application, freely available here on GitHub, and distributed under a permissive license.

## What it does ?

Not a lot, but it still saves a lot of time at the Tutorat Santé Lyon Sud. Below is a quick look at what the application can do currently.

- Importation of marks (Excel files), with an option to rescale marks during the process.
- Apply transformation to marks. This has been implemented to match the processing of marks at the university. Currently only one algorithm is availabe. This feature is opt-in.
- Creation of assessment's ranking reports that displays univariate statistics about marks, a distribution of marks and ranks. All this information can be issued on a per-group basis.
- Merging of several assessments into one *virtual* assessment.

## Technical informations

`linnote` is a web application coded in [Python3](https://python.org) using the [Flask](http://flask.pocoo.org/) framework. You can consult the project dependancies in the available Pipfile or directly on Github in the [insights section](https://github.com/natolh/linnote/network/dependencies).

The code is maintained by me. I mainly wrote it using the [VSCode editor](https://code.visualstudio.com/) and the official Python extension that goes with it. I use [PyLint](https://www.pylint.org/) to check code quality and for potential errors.

# Installation

## Requirements

Server should be equipped with at least Python 3.6.5, MySQL and NGINX.

# Usage

Refer to the [wiki section](https://github.com/natolh/linnote/wiki) for documentation on how to use the application.
