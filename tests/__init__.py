import os
import sys
import unittest

import coverage


def run():
    os.environ['DATABASE_URL'] = 'sqlite://'

    # start coverage engine
    cov = coverage.Coverage(branch=True)
    cov.start()

    # run tests
    tests = unittest.TestLoader().discover('.')
    ok = unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()

    # print coverage report
    cov.stop()
    print('')
    omit = ['manage.py', 'tests/*', 'venv/*']
    cov.report(omit=omit, show_missing=True)
    cov.html_report(omit=omit)

    sys.exit(0 if ok else 1)
