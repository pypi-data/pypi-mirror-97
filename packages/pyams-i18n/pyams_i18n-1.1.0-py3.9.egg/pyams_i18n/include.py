#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_i18n.include module

This module is used for Pyramid integration.
"""

from chameleon import PageTemplateFile

from pyams_i18n.tales import I18nExpr


__docformat__ = 'restructuredtext'


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_i18n:locales')

    # add custom locale negotiator
    from .negotiator import get_locale, locale_negotiator  # pylint: disable=import-outside-toplevel
    config.add_request_method(get_locale, 'locale', reify=True)
    config.set_locale_negotiator(locale_negotiator)

    config.scan()

    PageTemplateFile.expression_types['i18n'] = I18nExpr
