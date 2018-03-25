"""
The management module of the application.
Contains the essential commands to set up
the environment to run the application.
Currently, it supports the database commands
(init, migrate, upgrade, etc.).
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
