# a control panel for the web app. When someone uses this file, they can do important 
# tasks like managing the database or starting the website. 
# It makes it easy to keep the web app running smoothly and perform 
# important operations with just a few commands.

from flask_migrate import MigrateCommand
from flask_script import Manager
from app import app

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()