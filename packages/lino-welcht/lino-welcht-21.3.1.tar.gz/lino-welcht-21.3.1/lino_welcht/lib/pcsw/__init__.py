# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino_welfare.modlib.pcsw`
"""

from lino_welfare.modlib.pcsw import Plugin


class Plugin(Plugin):

    def setup_config_menu(config, site, user_type, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('pcsw.UnemploymentRights')
