# -*- coding: UTF-8 -*-
# Copyright 2002-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The main package for :ref:`welcht`.

.. autosummary::
   :toctree:

   lib


.. autosummary::
   :toctree:

   settings


.. convert to prosa:
   layouts
   workflows
   migrate



"""

from .setup_info import SETUP_INFO

# doc_trees = ['docs', 'dedocs', 'frdocs']
# doc_trees = ['dedocs', 'frdocs']
doc_trees = ['docs', 'frdocs']
intersphinx_urls = dict(
    docs="http://welcht.lino-framework.org",
    frdocs="http://fr.welfare.lino-framework.org")
# intersphinx_urls = dict()
# intersphinx_urls.update(dedocs="http://de.welfare.lino-framework.org")
# intersphinx_urls.update(frdocs="http://fr.welfare.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/welcht/blob/master/%s'
