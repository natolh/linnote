from flask import Blueprint
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from linnote.core.user import User
from .database import session
from .forms import LoginForm


AUTH = Blueprint('auth', __name__, url_prefix='/auth')


@AUTH.route('/login', methods=['GET', 'POST'])
def login():
    """Login endpoint for the application."""
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        user = session.query(User).filter(User.name == form.identifier.data).one_or_none()

        if user and user.is_authentic(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('admin.home'))

    return render_template('authentification/login.html', form=form)

@AUTH.route('/logout')
def logout():
    """Logout endpoint for the application."""
    logout_user()
    return redirect(url_for('auth.login'))
