# -*- coding: utf-8 -*-

"""
Users module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import GroupCollection, GroupRessource, UserCollection, UserRessource


# Build controllers functions.
GROUPS = GroupCollection.as_view('groups')
GROUP = GroupRessource.as_view('group')
USERS = UserCollection.as_view('users')
USER = UserRessource.as_view('user')


# Register routes to controllers.
BLUEPRINT = Blueprint('users', __name__, url_prefix='/admin', template_folder='templates')


BLUEPRINT.add_url_rule('/users/groups', view_func=GROUPS)
BLUEPRINT.add_url_rule('/users/group', view_func=GROUP)
BLUEPRINT.add_url_rule('/users', view_func=USERS)
BLUEPRINT.add_url_rule('/user', defaults={'identifier': None}, view_func=USER)
BLUEPRINT.add_url_rule('/user/<int:identifier>', view_func=USER)
