from flask import Flask
from .app_routes import *
from .app_config import *
from .blueprints.auth.signin import signin
from .blueprints.auth.signup import signup
from .blueprints.home.home import home
from .blueprints.admin.admin import admin
from .blueprints.logout.logout import logout
from .database.database import database
from .modules.time_management import starts_on_time

class app:
    def __init__(self):
        self = Flask(__name__)
        self.config.from_object(dev_config)
        self.before_first_request(before_first_request)
        self.before_request(before_request)
        self.after_request(after_request)
        self.errorhandler(404)(errorhandler_404)
        self.add_url_rule('/','index', index)
        self.register_blueprint(blueprint=signin, url_prefix='/signin')
        self.register_blueprint(blueprint=signup, url_prefix='/signup')
        self.register_blueprint(blueprint=logout, url_prefix='/logout')
        self.register_blueprint(blueprint=home, url_prefix='/home')
        self.register_blueprint(blueprint=admin, url_prefix='/admin')
        
        #starts_on_time()

        with database() as db:
            db.create_tables()

        self.run(host='0.0.0.0', port=10000)