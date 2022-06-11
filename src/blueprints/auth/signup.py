from flask import Blueprint, request, render_template, redirect, url_for,flash
from src.database.database import database
from src.modules.session import *

signup = Blueprint('signup',__name__)
signup.template_folder = 'templates'
signup.static_folder = 'static'

def render():
    return render_template('auth/templates/signup.html', TITLE='signup')

def is_username_valid(username):
    with database() as db:
        db.cursor.execute(f"select name from users where name='{username}'")
        return db.cursor.fetchone()

def add_user_in_database(username, pwd):
    with database() as db:
        db.cursor.execute(f"insert into users values('{username}', '{pwd}', 'offline', 'None')")

@signup.route('/', methods=['GET', 'POST'])
def index():

    return 'test'

    #wenn user online ist
    if get_session(): return redirect(url_for("home.index"))

    if request.method == 'POST':
        #form daten
        username = request.form['username']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']

        #ist username zu kurz
        if len(username) < 4:
            flash('Der Benutzername muss mindestens 4 zeichen enthalten')
            return render()

        #ist username zu lang
        if len(username) > 8:
            flash('Der Benutzername darf maximal 8 zeichen enthalten')
            return render()

        #ist username vorhanden
        if is_username_valid(username):
            flash('Username Ist Bereits Vergeben')
            return render()

        #sind eingegebene passwords gleich
        if pwd2 != pwd: 
            flash('Das Passwort muss gleich sein')
            return render()

        #ist passwort lang genug
        if len(pwd) < 5:
            flash('Das Passwort muss mindestens 5 Zeichten Enthalten')
            return render()

        #passwords sind gleich
        add_user_in_database(username, pwd)
        flash('Du hast dich Erfolgreich Registriert')
        return redirect(url_for('signin.index'))

    return render()
