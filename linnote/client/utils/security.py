#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Misceallenous security tools for the application.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import current_app, request, redirect


class StrictTransport(object):
    """Enforce HSTS policy and redirect insecure requests."""

    def __init__(self, max_age=31536000, app=None, **kwargs):
        super().__init__()
        self.max_age = max_age
        self.include_subdomains = kwargs.get('include_subdomains', True)
        self.preload = kwargs.get('preload', False)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register hooks to handle requests."""
        app.before_request(self._check_request)
        app.after_request(self._set_policy)

    def _check_request(self):
        """Check if URL was requested using a secure scheme."""
        if not any([request.is_secure, current_app.debug]):
            return self._upgrade_request(request.url)

        return None

    @staticmethod
    def _upgrade_request(url, code=301):
        """Upgrade scheme of the requested URL and redirect to it."""
        return redirect(url.replace('http', 'https', 1), code)

    @property
    def policy(self):
        """Strict Transport Policy."""
        policy = 'max-age={}'.format(self.max_age)

        if self.include_subdomains:
            policy += ' ; includeSubDomains'

        if self.preload:
            policy += ' ; preload'

        return policy

    def _set_policy(self, response):
        """Set HSTS policy header."""
        if request.is_secure:
            response.headers.setdefault(
                'Strict-Transport-Security',
                self.policy)

        return response


STRICT_TRANSPORT = StrictTransport()
