# flask-waypoint

[![Build Status](https://travis-ci.com/wizeline/flask-waypoint.svg?branch=master)](https://travis-ci.com/wizeline/flask-waypoint)


## Contents

1. [About](#about)
2. [Install](#install)
3. [Set up for development](#setup-for-development)
4. [Testing](#testing)
5. [Coding conventions](#coding-conventions)


## About

Flask-Waypoint is an extension that handles database access for master-slave replicas for Flask applications using SQLAlchemy.


## Install

Just do:

```
$ pip install git+ssh://git@github.com/wizeline/flask-waypoint.git
```


## Setup

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


## Testing

To run the tests, you just do:

```
$ tox
```


## Coding conventions

We use `editorconfig` to define our coding style. Please [add editorconfig](http://editorconfig.org/#download)
to your editor of choice.

When running `tox` linting will also be run along with the tests. You can also run linting only by doing:

```
$ tox -e flake8
```
