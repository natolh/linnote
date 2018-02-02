from sys import path
from pathlib import Path

CWD = Path().resolve().parent
path.append(str(CWD))

from linnote.core.database import Session
from linnote.core.user import User

session = Session()

username = input('Identifiant : ')
email = input('Email : ')
password = input('Mot de passe : ')

user = User(username=username, email=email)
user.set_password(password)

session.add(user)
session.commit()
