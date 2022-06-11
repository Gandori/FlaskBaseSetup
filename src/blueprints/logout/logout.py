from flask import Blueprint, redirect, url_for, flash
from src.database.database import database
from src.modules.session import get_session
from src.modules.session import delete_session

logout = Blueprint('logout',__name__)

def set_user_offline(username):
    with database() as db:
        db.cursor.execute(f"update users set status = 'offline' where name = '{username}'")

@logout.route('/', methods=['GET'])
def index():
    username = get_session()
    if username:
        set_user_offline(username)
        delete_session()
        flash('Du hast dich Erfolgreich ausgelogt')
    return redirect(url_for('signin.index'))