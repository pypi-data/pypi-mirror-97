import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from .api import database as db

application = None
migrate = None

class ApiManager():
    def __init__(self, app):
        application = app
        application.app_context().push()
        manager = Manager(application)

        migrate = Migrate(application, db, directory="./database/migrations")
        manager.add_command('db', MigrateCommand)

        with application.app_context():
            from .models import imports

        @manager.command
        def start():
            application.run(host="0.0.0.0")
        
        manager.run()