from flask_script import Manager
import os

from flask.ext.migrate import Migrate, MigrateCommand

from project import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
