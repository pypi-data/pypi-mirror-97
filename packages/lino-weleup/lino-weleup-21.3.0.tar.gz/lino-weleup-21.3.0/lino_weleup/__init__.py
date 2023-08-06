# -*- coding: UTF-8 -*-
# Copyright 2002-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The main package for :ref:`weleup`.

.. autosummary::
   :toctree:

   lib
   settings



"""

from .setup_info import SETUP_INFO

doc_trees = ['docs', 'dedocs']
intersphinx_urls = dict(
    docs="http://weleup.lino-framework.org",
    dedocs="http://de.welfare.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/weleup/blob/master/%s'
