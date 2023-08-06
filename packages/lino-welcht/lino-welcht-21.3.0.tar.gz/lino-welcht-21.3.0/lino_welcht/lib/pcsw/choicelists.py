# -*- coding: UTF-8 -*-
# Copyright 2008-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Choicelists for `lino_welcht.lib.pcsw`.

"""

from __future__ import print_function
from __future__ import unicode_literals

from lino.api import dd, _


class FollowedFORem(dd.ChoiceList):
    verbose_name = _("Followed by FORem")


add = FollowedFORem.add_item
add('0', _("No"), 'no')
add('1', _("Yes"), 'yes')
