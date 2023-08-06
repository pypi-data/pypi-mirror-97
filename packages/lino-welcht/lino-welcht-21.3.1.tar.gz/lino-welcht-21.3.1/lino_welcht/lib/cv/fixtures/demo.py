# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
"""

from builtins import range
from lino.utils import Cycler
from lino.api import rt

from lino_xl.lib.clients.choicelists import ClientStates

def objects():

    Obstacle = rt.models.cv.Obstacle
    ObstacleType = rt.models.cv.ObstacleType
    Client = rt.models.pcsw.Client

    CLIENTS = Cycler(Client.objects.filter(
        client_state=ClientStates.coached)[10:15])

    TYPES = Cycler(ObstacleType.objects.all())

    for i in range(20):
        yield Obstacle(person=CLIENTS.pop(), type=TYPES.pop())
