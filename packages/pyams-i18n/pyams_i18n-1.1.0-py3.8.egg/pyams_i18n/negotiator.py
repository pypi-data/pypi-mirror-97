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

"""PyAMS_i18n.negotiator module

This module defines a I18n negotiator utility, which is responsible of decoding browser
settings to extract preferred languages.

It also provides Pyramid request properties to set locale.
"""

from persistent import Persistent
from pyramid.interfaces import IRequest
from zope.container.contained import Contained
from zope.i18n.interfaces import INegotiator as IZopeNegotiator
from zope.i18n.locales import locales
from zope.interface import Interface, implementer
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_i18n.interfaces import INegotiator, LANGUAGE_CACHE_KEY
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.i18n import get_browser_language
from pyams_utils.registry import query_utility, utility_config


__docformat__ = 'restructuredtext'


@implementer(INegotiator)
class Negotiator(Persistent, Contained):
    """Language negotiator utility"""

    policy = FieldProperty(INegotiator['policy'])
    server_language = FieldProperty(INegotiator['server_language'])
    offered_languages = FieldProperty(INegotiator['offered_languages'])
    cache_enabled = FieldProperty(INegotiator['cache_enabled'])

    def __init__(self):
        self.server_language = 'en'

    def get_language(self, request):
        # pylint: disable=too-many-branches,too-many-return-statements
        """See :intf:`INegotiator`"""

        # lang parameter, if defined, is of higher priority
        if 'lang' in request.params:
            return request.params['lang']

        policies = self.policy.split(' --> ')
        for policy in policies:

            # check server policy
            if policy == 'server':
                if self.server_language:
                    return self.server_language

            # check session policy
            elif policy == 'session':
                if self.cache_enabled:
                    try:
                        cached = request.annotations[LANGUAGE_CACHE_KEY]
                        return cached
                    except AttributeError:
                        return self.server_language
                    except KeyError:
                        try:
                            session = request.session
                            lang = session.get('language')
                            if lang is not None:
                                request.annotations[LANGUAGE_CACHE_KEY] = lang
                                return lang
                        except (AttributeError, KeyError):
                            return self.server_language
                else:
                    try:
                        session = request.session
                        lang = session.get('language')
                        if lang is not None:
                            return lang
                    except AttributeError:
                        return self.server_language

            # check browser policy
            elif policy == 'browser':
                lang = get_browser_language(request)
                if lang is not None:
                    return lang

        return self.server_language

    @staticmethod
    def clear_cache(request):
        """Clear cached language value"""
        try:
            del request.annotations[LANGUAGE_CACHE_KEY]
        except (AttributeError, KeyError):
            pass


@adapter_config(name='lang', required=(Interface, IRequest), provides=ITraversable)
class LangNamespaceTraverser(ContextRequestAdapter):
    """++lang++ namespace traverser

    This traverser is mainly used for backward compatibility with previous Zope 3 websites.
    """

    def traverse(self, name, furtherpath=None):  # pylint: disable=unused-argument
        """Traverse to set request parameter to given language attribute"""
        if name != '*':
            self.request.GET['lang'] = name
        return self.context


def locale_negotiator(request):
    """Negotiate language based on server, browser, request and user settings

    Locale is extracted from request's "lang" parameter, from browser settings or from
    negotiator utility
    """
    negotiator = query_utility(INegotiator)
    if negotiator is not None:
        locale_name = negotiator.get_language(request)
    else:
        locale_name = get_browser_language(request)
    if not locale_name:
        registry = request.registry
        locale_name = registry.settings.get('pyramid.default_locale_name', 'en')
    if '-' in locale_name:
        # remove 'sub-locale' to prevent Babel and Zope exceptions for unknown locales
        locale_name = locale_name.split('-')[0]
    return locale_name


def get_locale(request):
    """Get zope.i18n "locale" attribute"""
    return locales.getLocale(request.locale_name)


@utility_config(provides=IZopeNegotiator)
class ZopeNegotiator:
    """Zope language negotiator"""

    def getLanguage(self, langs, env):  # pylint: disable=invalid-name,unused-argument,no-self-use
        """Get current language negotiator"""
        return locale_negotiator(env)
