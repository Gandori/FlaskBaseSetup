from flask import Blueprint, render_template
from src.database.database import database

admin = Blueprint('admin',__name__,template_folder='../',static_folder='/')


def get_all_users():
    with database() as db:
        db.cursor.execute(f"select name, status, img from users")
        return db.cursor.fetchall()

@admin.route('/')
def index():
    return render_template('admin/admin.html', title='admin', users=get_all_users())
