from os import path

dir = path.dirname(path.abspath(__file__))

class config:
    SECRET_KEY = 'secret_key'
    SESSION_COOKIE_NAME = 'session_cookie'

class productive_config(config):
    SERVER_NAME = ''
    DEBUG = False
    TESTING = False

class dev_config(config):
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    TESTING = True

