from flask import session

def create_session(name):
    session['name'] = name

def get_session():
    if 'name' in session:
        return session['name']

def delete_session():
    if 'name' in session:
        del session['name']

def clear_all_session():
    session.clear()