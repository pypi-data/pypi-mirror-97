# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import _
from lino_xl.lib.courses.desktop import *

Enrolments.detail_layout = """
request_date user
course pupil
remark workflow_buttons printed
motivation problems
"""


EnrolmentsByPupil.column_names = 'request_date course workflow_buttons *'
EnrolmentsByPupil.insert_layout = """
course_area
course
places option
remark
request_date user
"""


# class BasicCourses(Activities):
#     activity_layout = 'default'


class JobCourses(ActivitiesByLayout):
    activity_layout = 'job'


# class IntegEnrolmentsByPupil(EnrolmentsByPupil):
#     _activity_layout = ActivityLayouts.integ


class BasicEnrolmentsByPupil(EnrolmentsByPupil):
    activity_layout = 'default'


class JobEnrolmentsByPupil(EnrolmentsByPupil):
    activity_layout = 'job'


class ActiveActivities(ActiveActivities):
    label = _("Active workshops")
    column_names = 'detail_link enrolments free_places room description *'
    hide_sums = True


class DraftActivities(DraftActivities):
    label = _("Draft workshops")
    column_names = 'detail_link room description *'


class InactiveActivities(InactiveActivities):
    label = _("Inactive workshops")


class ClosedActivities(ClosedActivities):
    label = _("Closed workshops")
