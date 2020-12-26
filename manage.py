# manage.py
import os
import sys
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app.models import User, Email
basedir = os.path.abspath(os.path.dirname(__file__))


# app.config['APP_SETTINGS']="DevelopmentConfig"
app.config['SECRET_KEY'] = 'yo'
app.config['BCRYPT_LOG_ROUNDS'] = 13
app.config['DEBUG'] = False
app.config['WTF_CSRF_ENABLED'] = False
# app.config['WTF_CSRF_SECRET_KEY']="a csrf secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'lushtech.sqlite')
app.config['DEBUG_TB_ENABLED'] = False
    
# app.config.from_object(os.environ['APP_SETTINGS'])



migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test(test_name=None):
    """Runs the unit tests without test coverage."""
    if not test_name:
        tests = unittest.TestLoader().discover('tests')
    else:
        tests = unittest.TestLoader().loadTestsFromName('tests.' + test_name)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='app/*',
        omit="*/__init__.py"
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email="spuliz@admin.com", password="spuliz", admin=True))
    db.session.commit()


@manager.command
def create_data():
    """Adds data to the email model."""
    db.session.add(Email(email="test@test.com"))
    db.session.add(Email(email="foo@foo.com"))
    db.session.add(Email(email="bar@bar.com"))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
