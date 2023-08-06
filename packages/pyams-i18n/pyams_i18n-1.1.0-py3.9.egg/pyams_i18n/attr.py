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

"""PyAMS_i18n.attr module

This module provides the main II18n adapter, which is used to get value of translated properties.
"""

from pyramid.exceptions import NotFound
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable

from pyams_i18n.interfaces import II18n, INegotiator
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request


__docformat__ = 'restructuredtext'


@adapter_config(name='i18n', required=Interface, provides=ITraversable)
class I18nAttributeTraverser(ContextAdapter):
    """++i18n++attr:lang namespace traverser

    This traverser is used, for example, by I18n file fields (see :py:mod:pyams_file).
    """

    def traverse(self, name, furtherpath=None):  # pylint: disable=unused-argument
        """Traverse to selected attribute"""
        try:
            attr, lang = name.split(':')
            return getattr(self.context, attr, {}).get(lang)
        except (AttributeError, ValueError):
            raise NotFound


@adapter_config(required=Interface, provides=II18n)
class I18nAttributeAdapter(ContextAdapter):
    """I18n attribute adapter"""

    def get_attribute(self, attribute, lang=None, request=None, default=None):
        """Extract attribute value for given language or request"""
        result = getattr(self.context, attribute)
        if not isinstance(result, dict):
            return default
        if lang is None:
            if request is None:
                request = check_request()
            lang = request.params.get('lang') or request.locale_name
        return result.get(lang, default)

    def query_attribute(self, attribute, lang=None, request=None, default=None):
        """Extract attribute value for given language or request

        If value is empty or None, value associated to server language is returned.
        """
        result = getattr(self.context, attribute)
        if not isinstance(result, dict):
            return result
        if lang is None:
            if request is None:
                request = check_request()
            lang = request.params.get('lang') or request.locale_name
        value = result.get(lang)
        if not value:
            if default:
                value = default.get(lang)
        if not value:
            negotiator = query_utility(INegotiator)
            if (negotiator is not None) and (negotiator.server_language != lang):
                value = result.get(negotiator.server_language)
        return value
