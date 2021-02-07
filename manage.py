import os

from flask_script import Manager
from flask_migrate import MigrateCommand

from app import create_app

manager = Manager(create_app)

manager.add_command('db', MigrateCommand)


if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

if __name__ == '__main__':
    manager.run()
