# -*- coding: utf-8 -*-

"""
Users module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import GroupsController as Groups
from .controllers import GroupSettingsController as GroupSettings
from .controllers import GroupMembersController as GroupMembers
from .controllers import GroupCreationController as GroupCreation
from .controllers import UsersController as Users
from .controllers import UserController as User
from .controllers import UserCreationController as UserCreation


# Build controllers functions.
GROUPS = Groups.as_view('groups')
GROUP_SETTINGS = GroupSettings.as_view('group')
GROUP_MEMBERS = GroupMembers.as_view('group_members')
GROUP_CREATION = GroupCreation.as_view('group_creation')
USERS = Users.as_view('users')
USER = User.as_view('user')
USER_CREATION = UserCreation.as_view('user_creation')

# Register routes to controllers.
BLUEPRINT = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')


BLUEPRINT.add_url_rule('/groups', view_func=GROUPS)
BLUEPRINT.add_url_rule('/groups/', view_func=GROUP_CREATION)
BLUEPRINT.add_url_rule('/groups/<int:identifier>', view_func=GROUP_SETTINGS)
BLUEPRINT.add_url_rule('/groups/<int:identifier>/members', view_func=GROUP_MEMBERS)
BLUEPRINT.add_url_rule('', view_func=USERS)
BLUEPRINT.add_url_rule('/', view_func=USER_CREATION)
BLUEPRINT.add_url_rule('/<int:identifier>', view_func=USER)
