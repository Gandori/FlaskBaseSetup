from flask import Blueprint, render_template, request, redirect, url_for,flash
from src.database.database import database
from src.modules.session import *
from src.database.database import database


signin = Blueprint('signin',__name__)
signin.template_folder = 'templates'
signin.static_folder = 'static'

PAGE = 'signin.html'
TITLE = 'signin'
MESSAGES = [
    'Die Angaben stimmen nicht',
    'Du hast dich Erfolgreich Eingeloggt',
]

def is_session():
    if get_session():
        if database.is_user_in_database(get_session()):
            return True

def is_admin(username, pwd):
    with database() as db:
        db.cursor.execute(f"select password from admin where name = '{username}' and password='{pwd}'")
        return db.cursor.fetchone()

def render(PAGE, TITLE):
    return render_template(PAGE, TITLE=TITLE)

def set_user_online(username):
    with database() as db:
        db.cursor.execute(f"update users set status = 'online' where name = '{username}'")

def is_username_valid(username):
    with database() as db:
        db.cursor.execute(f"select name from users where name='{username}'")
        return db.cursor.fetchone()

def valid_password(username, pwd):
    with database() as db:
        db.cursor.execute(f"select password from users where name='{username}' and password='{pwd}'")
        return db.cursor.fetchone()

@signin.route('/', methods=['GET', 'POST'])
def index():

    if is_session(): return redirect(url_for("home.index"))

    if request.method == 'POST':
        #form daten
        username = request.form['username']
        pwd = request.form['pwd']

        #ist username in der datenbank
        if not is_username_valid(username):
            flash(MESSAGES[0])
            return render(PAGE, TITLE)

        #ist passwort das selbe
        if valid_password(username, pwd):
            flash(MESSAGES[1])
            create_session(username)
            set_user_online(username)
            return redirect(url_for('home.index'))

        #passwort ist nicht das selbe
        flash(MESSAGES[0])
        return render(PAGE, TITLE)

    return render(PAGE, TITLE)