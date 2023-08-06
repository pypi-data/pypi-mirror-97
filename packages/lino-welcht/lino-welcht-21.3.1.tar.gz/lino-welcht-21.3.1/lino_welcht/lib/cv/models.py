# -*- coding: UTF-8 -*-
# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from lino.api import dd

from lino_xl.lib.cv.models import *
from lino.core.signals import pre_ui_save

from lino_xl.lib.clients.choicelists import ClientEvents, ObservedEvent

from lino_welfare.modlib.integ.roles import IntegrationStaff, IntegUser

# from lino.core.utils import range_filter


def is_learning_filter(prefix, a, b):
    if a is None:
        flt = Q(**{prefix+'start_date__isnull': False})
    else:
        flt = Q(**{prefix+'start_date__lte': a})
    if b is not None:
        flt &= Q(**{prefix+'end_date__isnull': True}) \
            | Q(**{prefix+'end_date__gte': b})
    return flt


class ClientIsLearning(ObservedEvent):
    """Select only clients who are "learning" during the given date.
    That is, who have an active :class:`Study`, :class:`Training` or
    :class:`Experience`.
    Only the `start_date` is used, `end_date` has no effect when
    this criteria.

    """
    text = _("Learning")

    def add_filter(self, qs, pv):
        p = (pv.start_date, pv.end_date)
        flt = is_learning_filter('training__', *p)
        flt |= is_learning_filter('study__', *p)
        flt |= is_learning_filter('experience__', *p)
        qs = qs.filter(flt)
        # logger.info("20150522 %s", qs.query)
        return qs

        # if pv.start_date:
        #     flt = range_filter(
        #         pv.start_date, 'training__start_date', 'training__end_date')
        #     flt |= range_filter(
        #         pv.start_date, 'study__start_date', 'study__end_date')
        #     flt |= range_filter(
        #         pv.start_date, 'experience__start_date',
        #         'experience__end_date')
        #     # flt = Q(training__start_date__gte=pv.start_date)
        #     # flt |= Q(study__start_date__gte=pv.start_date)
        #     # flt |= Q(experience__start_date__gte=pv.start_date)
        #     qs = qs.filter(flt)
        # else:
        #     flt = Q(training__start_date__isnull=False)
        #     flt |= Q(study__start_date__isnull=False)
        #     flt |= Q(experience__start_date__isnull=False)
        #     qs = qs.filter(flt)

        # if pv.end_date:
        #     flt = Q(training__end_date__lte=pv.end_date)
        #     flt |= Q(study__end_date__lte=pv.end_date)
        #     flt |= Q(experience__end_date__lte=pv.end_date)
        #     qs = qs.filter(flt)
        return qs

ClientEvents.add_item_instance(ClientIsLearning("learning"))


LanguageKnowledgesByPerson.column_names = "language native spoken \
written spoken_passively written_passively *"


class Proof(mixins.BabelNamed):
    """A **proof** is some document which certifies that a given person
    has a given skill."""
    class Meta:
        app_label = 'cv'
        verbose_name = _("Skill proof")
        verbose_name_plural = _("Skill proofs")


class Proofs(dd.Table):
    model = 'cv.Proof'
    required_roles = dd.login_required(IntegrationStaff)

class PersonProperty(dd.Model):
    """Abstract base for :class:`Skill`, :class:`SoftSkill` and
    :class:`Obstacle`.

    """
    class Meta:
        abstract = True

    allow_cascaded_delete = ['person']

    person = dd.ForeignKey(config.person_model)
    remark = models.CharField(max_length=200,
                              blank=True,  # null=True,
                              verbose_name=_("Remark"))


class PropsByPerson(dd.Table):
    master_key = 'person'
    auto_fit_column_widths = True
    required_roles = dd.login_required(IntegUser)


##
## SKILLS
##

class Skill(PersonProperty, SectorFunction):

    class Meta:
        app_label = 'cv'
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    proof = dd.ForeignKey('cv.Proof', blank=True, null=True)

dd.update_field(Skill, 'remark', verbose_name=_("Competences"))


class Skills(dd.Table):
    model = 'cv.Skill'
    required_roles = dd.login_required(IntegrationStaff)


class SkillsByPerson(PropsByPerson, Skills):
    column_names = 'sector function remark proof *'
    required_roles = dd.login_required(IntegUser)


##
## SOFTSKILLS
##


class SoftSkillType(mixins.BabelNamed):
    class Meta:
        app_label = 'cv'
        verbose_name = _("Soft skill type")
        verbose_name_plural = _("Soft skill types")


class SoftSkillTypes(dd.Table):
    model = 'cv.SoftSkillType'
    required_roles = dd.login_required(IntegrationStaff)

    
class SoftSkill(PersonProperty):
    class Meta:
        app_label = 'cv'
        verbose_name = _("Soft skill")
        verbose_name_plural = _("Soft skills")
    type = dd.ForeignKey('cv.SoftSkillType', verbose_name=_("Type"))
    proof = dd.ForeignKey('cv.Proof', blank=True, null=True)


class SoftSkills(dd.Table):
    model = 'cv.SoftSkill'
    required_roles = dd.login_required(IntegrationStaff)


class SoftSkillsByPerson(PropsByPerson, SoftSkills):
    column_names = 'type remark'
    required_roles = dd.login_required(IntegUser)

##
## OBSTACLES
##


class ObstacleType(mixins.BabelNamed):
    class Meta:
        app_label = 'cv'
        verbose_name = _("Obstacle type")
        verbose_name_plural = _("Obstacle types")


class ObstacleTypes(dd.Table):
    required_roles = dd.login_required(IntegrationStaff)
    model = 'cv.ObstacleType'


class Obstacle(PersonProperty):
    """An **obstacle** is an observed fact or characteristic of a client
    which might be reason to not get a given job.

    .. attribute:: type

        A pointer to :class:`ObstacleType`.

    .. attribute:: user

        The agent who observed this obstacle.

    .. attribute:: detected_date

        The date when the agent observed this obstacle.

    """
    class Meta:
        app_label = 'cv'
        verbose_name = _("Obstacle")
        verbose_name_plural = _("Obstacles")
    type = dd.ForeignKey('cv.ObstacleType', verbose_name=_("Type"))
    user = dd.ForeignKey(
        settings.SITE.user_model,
        related_name='obstacles_detected',
        verbose_name=_("Detected by"),
        blank=True, null=True)
    detected_date = models.DateField(
        _("Date"), blank=True, null=True, default=dd.today)


@dd.receiver(pre_ui_save, sender=Obstacle)
def on_create(sender, instance=None, ar=None, **kwargs):
    instance.user = ar.get_user()


class Obstacles(dd.Table):
    required_roles = dd.login_required(IntegrationStaff)
    model = 'cv.Obstacle'


class ObstaclesByPerson(PropsByPerson, Obstacles):
    required_roles = dd.login_required(IntegUser)
    column_names = 'type user detected_date remark  *'


dd.inject_field('system.SiteConfig', 'propgroup_skills', dd.DummyField())
dd.inject_field('system.SiteConfig', 'propgroup_softskills', dd.DummyField())
dd.inject_field('system.SiteConfig', 'propgroup_obstacles', dd.DummyField())

# print(StudiesByPerson.column_names)
# print(TrainingsByPerson.column_names)
# print(ExperiencesByPerson.column_names)

StudiesByPerson.column_names = "type content start_date end_date duration_text school country state education_level remarks *"
TrainingsByPerson.column_names = "type sector function start_date end_date duration_text school country state certificates remarks *"
ExperiencesByPerson.column_names = "company country start_date end_date duration_text function status duration termination_reason remarks *"
