# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd.
# License: BSD (see file COPYING for details)

"""
How to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.PackagesTests

"""
from unipath import Path

import lino_welcht
from lino.utils.pythontest import TestCase


class BaseTestCase(TestCase):
    project_root = Path(__file__).parent.parent


class PackagesTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(lino_welcht.SETUP_INFO['packages'])
