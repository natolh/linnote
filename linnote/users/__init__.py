# -*- coding: utf-8 -*-

"""
Users module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import GroupsController as Groups
from .controllers import GroupController as Group
from .controllers import UsersController as Users
from .controllers import UserController as User
from .controllers import UserCreationController as UserCreation


# Build controllers functions.
GROUPS = Groups.as_view('groups')
GROUP = Group.as_view('group')
USERS = Users.as_view('users')
USER = User.as_view('user')
USER_CREATION = UserCreation.as_view('user_creation')

# Register routes to controllers.
BLUEPRINT = Blueprint('users', __name__, url_prefix='/admin', template_folder='templates')


BLUEPRINT.add_url_rule('/users/groups', view_func=GROUPS)
BLUEPRINT.add_url_rule('/users/group', view_func=GROUP)
BLUEPRINT.add_url_rule('/users', view_func=USERS)
BLUEPRINT.add_url_rule('/user', view_func=USER_CREATION)
BLUEPRINT.add_url_rule('/user/<int:identifier>', view_func=USER)
