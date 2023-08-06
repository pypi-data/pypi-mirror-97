#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_i18n.generations main module

This module is checking for a registered I18n negotiator utility.
"""

from pyams_i18n.interfaces import INegotiator
from pyams_i18n.negotiator import Negotiator
from pyams_site.generations import check_required_utilities
from pyams_site.interfaces import ISiteGenerations
from pyams_utils.registry import utility_config


__docformat__ = 'restructuredtext'


REQUIRED_UTILITIES = ((INegotiator, '', Negotiator, 'Language negotiator'),)


@utility_config(name='PyAMS I18n', provides=ISiteGenerations)
class I18nGenerationsChecker:
    """I18n generations checker"""

    order = 20
    generation = 1

    def evolve(self, site, current=None):  # pylint: disable=unused-argument,no-self-use
        """Check for required utilities"""
        check_required_utilities(site, REQUIRED_UTILITIES)
