from html import escape
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.modules.session import get_session, create_session
from src.database.database import database

signin = Blueprint('signin',__name__)
signin.template_folder = 'templates'
signin.static_folder = 'static'

def redirect_home():
    return redirect(url_for("home.index"))

def render():
    return render_template('signin.html', TITLE='signin')

@signin.route('/', methods=['GET', 'POST'])
def index():
    username = get_session()

    if username: return redirect_home()

    if request.method == 'GET':return render()

    if request.method == 'POST':

        username = escape(request.form['username'])
        pwd = escape(request.form['pwd'])

        msg = 'Die Angaben stimmen nicht'

        if not database.is_user_in_database(username):
            flash(msg)
            return render()

        if not database.valid_password(username, pwd):
            flash(msg)
            return render()

        flash('Du hast dich Erfolgreich Eingeloggt')
        create_session(username)
        database.set_user_online(username)
        return redirect_home()