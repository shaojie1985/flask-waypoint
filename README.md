# Flask-Waypoint

[![Build Status](https://travis-ci.com/wizeline/flask-waypoint.svg?branch=master)](https://travis-ci.com/wizeline/flask-waypoint)


## Contents

1. [About](#about)
2. [Install](#install)
3. [Set up for development](#setup-for-development)
4. [Testing](#testing)
5. [Coding conventions](#coding-conventions)


## About

Flask-Waypoint is an extension that handles database access for master-slave replicas for Flask applications using SQLAlchemy.

## Using it

When defining your application:

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_waypoint import FlaskWaypoint

app = Flask(__name__)
db = SQLAlchemy(app)
waypoint = FlaskWaypoint(app, db)
```

Flask-Waypoint will use the config keys `DB_MASTER_URI` and `DB_SLAVE_URI` to create the engines to connect to master and slave as needed, you can also use your own config keys and set them with the constructor kwargs `master_config_key`, and `slave_config_key`.

When trying to access the database without specifying a binding it will default to `master` unless you initialize Flask-Waypoint with `raise_when_not_binding=True`, in which case it will raise `flask_waypoint.NoBindingActiveError`.

### Context manager

```python
    from flask_waypoint import db_master, db_slave

    with db_master():
        pass

    with db_slave():
        pass 
```

### Decorator

```python
    from flask_waypoint import with_slave, with_master

    @app.route('/users')
    @with_slave
    def get_users():
        pass # TODO: Return user list

    @app.route('/users', methods=['POST'])
    @with_master
    def create_user():
        pass # TODO: Create user
```


### Limitations

Due to the way Flask-SqlAlchemy works it's not possible to change across databases on the same request.


## Hacking

First install Python 3 from [Homebrew](http://brew.sh/) and virtualenvwrapper:

```
brew install python3
pip3 install virtualenv virtualenvwrapper
```

After installing virtualenvwrapper please add the following line to your shell startup file (e.g. ~/.zshrc):

```
source /usr/local/bin/virtualenvwrapper.sh
```

Then reset your terminal.

Clone this respository and create the virtual environment:

```
$ git clone https://github.com/wizeline/flask-waypoint
$ cd flask-waypoint
$ mkvirtualenv flask-waypoint
$ workon flask-waypoint
$ pip install -r requirements-dev.txt
$ pip install tox
```


### Testing

To run the tests, you just do:

```
$ tox
```


### Coding conventions

We use `editorconfig` to define our coding style. Please [add editorconfig](http://editorconfig.org/#download)
to your editor of choice.

When running `tox` linting will also be run along with the tests. You can also run linting only by doing:

```
$ tox -e flake8
```
