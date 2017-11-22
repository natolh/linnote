#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Miscellaneous tools for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from io import StringIO
from statistics import mean as get_mean, median as get_median
from jinja2 import Environment, PackageLoader
from matplotlib import pyplot as plot
from linnote.configuration import CHARSET


def make_stats(sample):
    """Basic statistics about an assessment's marks."""
    # Return statistics.
    return {
        "size": len(sample),
        "maximum": max(sample) if sample else 0,
        "minimum": min(sample) if sample else 0,
        "mean": get_mean(sample) if sample else 0,
        "median": get_median(sample) if sample else 0
    }


def make_histogram(sample, coefficient):
    """Distribution of marks to an assessment."""
    document = StringIO()
    plot.figure(figsize=(6, 4))
    plot.hist(x=sample, bins=coefficient, range=(0, coefficient),
              color=(0.80, 0.80, 0.80), histtype="stepfilled")
    plot.title("Répartition des notes")
    plot.savefig(document, format="svg")
    document.seek(0)
    return "\n".join(document.readlines()[5:-1])


def render_template(template, **kwargs):
    """
    Load a template and render it.

    - template: A string. Name of the template.
    - kwargs:   Dictionnary. Arguments to fill the template.

    Return: An HTML document.
    """
    # Load Jinja2 environnement and load the template.
    env = Environment(loader=PackageLoader("linnote"))
    template = env.get_template(template)

    # Render, encode and return the template.
    return template.render(**kwargs).encode(CHARSET)
