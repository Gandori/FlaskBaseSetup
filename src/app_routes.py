from flask import redirect, url_for

def index():
    return redirect(url_for('signin.index'))

def errorhandler_404(*args):
    return 'Page not Found'

def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-control', 'no-cache, no-store, must-revalidate')
    return response