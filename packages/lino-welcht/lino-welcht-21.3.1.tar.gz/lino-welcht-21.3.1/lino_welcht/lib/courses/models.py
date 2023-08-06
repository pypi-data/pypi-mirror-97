# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Does some adaptions.
"""

from lino.api import dd, _

from lino_xl.lib.courses.models import *

ActivityLayouts.clear()
add = ActivityLayouts.add_item
# add('S', _("Integration workshops"), 'integ')  # no longer used
add('B', _("Integration workshops"), 'default')  # , 'courses.BasicCourses')
add('J', _("Job search workshops"), 'job', 'courses.JobCourses')
# add('B', _("Social integration"), 'default')
# add('J', _("Socio-professional integration"), 'job')

# requested #564
# Dans l'onglet O.I., remplacer "Ateliers" par "Ateliers d'Insertion
# sociale" et "Module de détermination d'un projet socioprofessionnel"
# par "Ateliers d'Insertion socioprofessionnelle".

# What follows is still the old approach for redefining a
# workflow. One day we should convert this to the new approach using
# the workflows_module.

# We add three enrolment states and remove "trying":
add = EnrolmentStates.add_item
EnrolmentStates.trying.text = _("Never came")
# EnrolmentStates.trying.remove()
add('40', _("Started"), 'started', invoiceable=False, uses_a_place=True)
add('50', _("Finished"), 'finished', invoiceable=False, uses_a_place=False)
# add('60', _("Never came"), 'never', invoiceable=False, uses_a_place=False)


@dd.receiver(dd.pre_analyze)
def my_enrolment_workflows(sender=None, **kw):

    EnrolmentStates.requested.add_transition(
        required_states="confirmed")
    EnrolmentStates.confirmed.add_transition(
        required_states="requested")
    EnrolmentStates.started.add_transition(
        required_states="confirmed requested")
    EnrolmentStates.finished.add_transition(
        required_states="started")
    EnrolmentStates.trying.add_transition(
        required_states="requested confirmed")
    # EnrolmentStates.trying.add_transition(
    #     required_states="requested confirmed")

    CourseStates.active.add_transition(required_states="draft inactive")
    CourseStates.inactive.add_transition(required_states="draft active")
    CourseStates.draft.add_transition(required_states="active inactive")


class Course(Course):
    class Meta:
        verbose_name = _("Workshop")
        verbose_name_plural = _('Workshops')
        abstract = dd.is_abstract_model(__name__, 'Course')


# GUEST_ENROLMENT_STATES = set([
#     EnrolmentStates.confirmed,
#     EnrolmentStates.started])


class Enrolment(Enrolment):
    """Adds two text fields :attr:`motivation` and :attr:`problems`.

    """
    motivation = dd.RichTextField(
        _("Motif de l'orientation"),
        blank=True, format="html")
    problems = dd.RichTextField(
        _("Difficultés à l'origine de la demande / "
          "Problématiques repérées"),
        blank=True, format="html")

    # def suggest_guest_for(self, event):
    #     return self.state in GUEST_ENROLMENT_STATES

    # default state is always "requested". In Welfare we do not want
    # to automatically confirm enrolments, so we deactivate
    # ConfirmedSubmitInsert set by `lino_xl.lib.courses`
    submit_insert = dd.SubmitInsert()


class Line(Line):
    class Meta:
        app_label = 'courses'
        verbose_name = _("Workshop series")
        verbose_name_plural = _('Workshop lines')
        abstract = dd.is_abstract_model(__name__, 'Line')
