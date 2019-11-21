import unittest
import os

import click
import coverage
from flask import current_app
from flask.cli import with_appcontext

@click.command('test')
def run_tests_command():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@click.command('coverage')
@with_appcontext
def coverage_command():
    """ Run Tests with coverage """
    print(current_app.instance_path)
    cov = coverage.coverage(branch=True, include="project/*", omit='*/__init__.py')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    #basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = current_app.instance_path
    covedir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covedir)
    cov.erase()
