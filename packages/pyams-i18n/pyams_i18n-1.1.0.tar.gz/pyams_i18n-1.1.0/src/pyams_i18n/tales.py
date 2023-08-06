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

"""PyAMS_i18n.tales module

This module provides a TALES "i18n" expression, as well as a PyAMS TALES extension also called
"i18n"; the first one is the default one used to get a translated attribute value into a chameleon
template, while the second one can be used when you have to handle possible mising attributes
by providing a default value.
"""

from chameleon.astutil import Symbol
from chameleon.tales import StringExpr
from zope.interface import Interface

from pyams_i18n.interfaces import II18n
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.tales import ContextExprMixin


__docformat__ = 'restructuredtext'


def render_i18n_expression(econtext, name):
    """Render an I18n expression

    Value can be given as a single attribute name (for example: "i18n:title"), in which case value
    is extracted from current "context".

    Value can also be given as a dotted name, for example "i18n:local_var.property.title".
    """
    name = name.strip()  # pylint: disable=redefined-argument-from-local
    if '.' in name:
        names = name.split('.')
        context = econtext.get(names[0])
        for name in names[1:-1]: # pylint: disable=redefined-argument-from-local
            context = getattr(context, name)
        attr = names[-1]
    else:
        context = econtext.get('context')
        attr = name
    request = econtext.get('request')
    return II18n(context).query_attribute(attr, request=request)


class I18nExpr(ContextExprMixin, StringExpr):
    """i18n:context.attribute TALES expression"""

    transform = Symbol(render_i18n_expression)


@adapter_config(name='i18n',
                required=(Interface, Interface, Interface),
                provides=ITALESExtension)
class I18NTalesExtension(ContextRequestViewAdapter):
    """tales:i18n(context, attribute, default=None) TALES extension

    Similar to standard i18n: TALES expression, but provides a default value for missing
    attributes.
    Please note that this extension returns default value when applied on a non-existent
    attribute, not on an attribute with an empty value for selected language!
    """

    def render(self, context, attribute, default=None):
        """Render TALES extension"""
        try:
            # pylint: disable=assignment-from-no-return
            value = II18n(context).query_attribute(attribute, request=self.request)
        except AttributeError:
            value = default
        return value
