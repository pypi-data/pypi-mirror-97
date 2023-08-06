# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.api import dd, rt, _


def objects():

    ExcerptType = rt.models.excerpts.ExcerptType
    Enrolment = rt.models.courses.Enrolment
    # ContentType = rt.models.contenttypes.ContentType
    kw = dict(
        # template='Default.odt',
        body_template='enrolment.body.html',
        print_recipient=False, certifying=True)
    kw.update(dd.str2kw('name', _("Enrolment")))
    yield ExcerptType.update_for_model(Enrolment, **kw)

    # kw = dict(
    #     body_template='intervention.body.html',
    #     print_recipient=False, certifying=True)
    # kw.update(dd.str2kw('name', _("Intervention request")))
    # kw.update(content_type=ContentType.objects.get_for_model(Enrolment))
    # yield ExcerptType(**kw)

