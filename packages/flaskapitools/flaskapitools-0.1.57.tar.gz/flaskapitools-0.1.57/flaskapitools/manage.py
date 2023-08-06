import os
from flask_script import Manager

application = None

class ApiManager():
    def __init__(self, app):
        application = app
        application.app_context().push()
        manager = Manager(application)

        @manager.command
        def start():
            application.run(host="0.0.0.0")
        
        manager.run()
