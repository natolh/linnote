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


# Create the module.
BLUEPRINT = Blueprint('users', __name__)
BLUEPRINT.url_prefix = '/users'
BLUEPRINT.template_folder = 'templates'

# Build views' controllers.
GROUPS = Groups.as_view('groups')
GROUP_CREATION = GroupCreation.as_view('group_creation')
GROUP = GroupMembers.as_view('group')
GROUP_MEMBERS = GroupMembers.as_view('group_members')
GROUP_SETTINGS = GroupSettings.as_view('group_settings')
USERS = Users.as_view('users')
USER_CREATION = UserCreation.as_view('user_creation')
USER = User.as_view('user')

# Register views' controllers routes.
BLUEPRINT.add_url_rule('/groups', view_func=GROUPS)
BLUEPRINT.add_url_rule('/groups/', view_func=GROUP_CREATION)
BLUEPRINT.add_url_rule('/groups/<int:identifier>', view_func=GROUP)
BLUEPRINT.add_url_rule('/groups/<int:identifier>/members', view_func=GROUP_MEMBERS)
BLUEPRINT.add_url_rule('/groups/<int:identifier>/settings', view_func=GROUP_SETTINGS)
BLUEPRINT.add_url_rule('', view_func=USERS)
BLUEPRINT.add_url_rule('/', view_func=USER_CREATION)
BLUEPRINT.add_url_rule('/<int:identifier>', view_func=USER)
