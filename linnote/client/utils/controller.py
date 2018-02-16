#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Customized MethodView for the application.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask.views import MethodView


class Controller(MethodView):
    """Custom flask.MethodView with usefull functions for the application."""

    @classmethod
    def register_to(cls, blueprint, **kwargs):
        """Register the view to the blueprint."""
        name = kwargs.get('name', cls.__name__.lower())
        url = kwargs.get('url', '/{}'.format(name))
        view = cls.as_view(name)
        blueprint.add_url_rule(url, view_func=view)
