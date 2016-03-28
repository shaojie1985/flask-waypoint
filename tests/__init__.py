import unittest

import sure  # noqa
import flask
from flask_sqlalchemy import SQLAlchemy

from flask_waypoint import FlaskWaypoint, db_master, db_slave, with_master, with_slave


def make_user_model(db):
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(60))

        def __init__(self, name):
            self.name = name

    return User


def create_data(db, model, username):
    obj = model(username)
    db.session.add(obj)
    db.session.commit()


class BasicAppTestCase(unittest.TestCase):

    def setUp(self):
        app = flask.Flask(__name__)
        app.config['DB_MASTER_URI'] = 'sqlite:///master.db'
        app.config['DB_SLAVE_URI'] = 'sqlite:///slave.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        db = SQLAlchemy(app)
        waypoint = FlaskWaypoint(app, db, raise_when_not_binding=self.__class__.__name__ == 'RaiseWhenNotBindingTestCase')  # noqa
        self.User = make_user_model(db)
        self.app = app
        self.db = db
        self.client = self.app.test_client()

        def get_users_count():
            return len(self.User.query.all())

        @app.route('/setup_master_database')
        def setup_master_database():
            with db_master():
                db.drop_all()
                db.create_all()
                create_data(db, self.User, 'foo')
            return 'ok'

        @app.route('/setup_slave_database')
        def setup_slave_database():
            with db_slave():
                db.drop_all()
                db.create_all()
                create_data(db, self.User, 'foo')
                create_data(db, self.User, 'bar')
            return 'ok'

        @app.route('/no_binding')
        def no_binding():
            try:
                return str(get_users_count())
            except Exception as e:
                return e.__class__.__name__

        @app.route('/nested_bindings')
        def nested_bindings():
            try:
                with db_master():
                    with db_slave():
                        return str(get_users_count())
            except Exception as e:
                return e.__class__.__name__

        @app.route('/consecutive_bindings')
        def consecutive_bindings():
            try:
                with db_master():
                    pass
                with db_slave():
                    return str(get_users_count())
            except Exception as e:
                return e.__class__.__name__

        @app.route('/db_master')
        def db_master_binding():
            with db_master():
                return str(get_users_count())

        @app.route('/db_slave')
        def db_slave_binding():
            with db_slave():
                return str(get_users_count())

        @app.route('/with_master')
        @with_master
        def with_master_binding():
            return str(get_users_count())

        @app.route('/with_slave')
        @with_slave
        def with_slave_binding():
            return str(get_users_count())

        """
        You usually don't need to do a db.create_all call on a slave since it's replicated from master,
        since we're faking it for the test we will do it with a flask call to have an app context where to call it
        """
        self.client.get('/setup_master_database')
        self.client.get('/setup_slave_database')


class CommonTestCase(BasicAppTestCase):

    def test_db_master(self):
        self.client.get('/db_master').data.should.equals(b'1')

    def test_db_slave(self):
        self.client.get('/db_slave').data.should.equals(b'2')

    def test_with_master(self):
        self.client.get('/with_master').data.should.equals(b'1')

    def test_with_slave(self):
        self.client.get('/with_slave').data.should.equals(b'2')

    def test_raise_when_multiple_bindings(self):
        self.client.get('/nested_bindings').data.should.equals(b'TwoBindingsOnSameRequestError')
        self.client.get('/consecutive_bindings').data.should.equals(b'TwoBindingsOnSameRequestError')


class DefaultsMasterWhenNotBindingTestCase(BasicAppTestCase):

    def test_no_binding_defaults_to_master(self):
        self.client.get('/no_binding').data.should.equals(b'1')


class RaiseWhenNotBindingTestCase(BasicAppTestCase):

    def test_raise_when_not_binding(self):
        self.client.get('/no_binding').data.should.equals(b'NoBindingActiveError')

    def test_should_work_with_binding(self):
        self.client.get('/with_master').data.should.equals(b'1')
        self.client.get('/with_slave').data.should.equals(b'2')
