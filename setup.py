import re
from pip.req import parse_requirements
from setuptools import setup, find_packages


def requirements(filename):
    reqs = parse_requirements(filename, session=False)
    return [str(r.req) for r in reqs]


def get_version():
    with open('flask_waypoint/__init__.py', 'r') as f:
        version_regex = r'^__version__\s*=\s*[\'"](.+)[\'"]'
        return re.search(version_regex, f.read(), re.MULTILINE).group(1)

setup(
    name='Flask-Waypoint',
    version=get_version(),
    url='https://github.com/wizeline/flask-waypoint',
    license='MIT',
    author='Wizeline',
    author_email='engineering@wizeline.com',
    description='Flask-Waypoint is an extension that handles database access for master-slave '
                'replicas for Flask applications using SQLAlchemy.',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python 2.7',
        'Programming Language :: Python 3',
    ],
    tests_require=requirements('requirements-dev.txt'),
    install_requires=requirements('requirements.txt'),
    extras_require={
        'dev': requirements('requirements-dev.txt')
    }
)
