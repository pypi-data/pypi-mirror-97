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

"""PyAMS_i18n.interfaces module

This module provides all package interfaces and constants.
"""

from zope.interface import Interface, Invalid, invariant
from zope.schema import Bool, Choice, List, Set


__docformat__ = 'restructuredtext'

from pyams_i18n import _


LANGUAGE_POLICIES = (
    'server',
    'session',
    'browser',
    'browser --> session --> server',
    'browser --> server',
    'session --> browser --> server',
    'session --> server'
)

LANGUAGE_CACHE_KEY = 'pyams_i18n.language'

BASE_LANGUAGES_VOCABULARY_NAME = 'pyams_i18n.languages.base'
ISO_LANGUAGES_VOCABULARY_NAME = 'pyams_i18n.languages.iso'
OFFERED_LANGUAGES_VOCABULARY_NAME = 'pyams_i18n.languages.offered'
CONTENT_LANGUAGES_VOCABULARY_NAME = 'pyams_i18n.languages.content'


class INegotiator(Interface):
    """Local negotiator utility manager interface."""

    policy = Choice(title=_("Language lookup policy"),
                    description=_("Defines how the language lookup is working."),
                    values=LANGUAGE_POLICIES,
                    default='session --> browser --> server',
                    required=True)

    server_language = Choice(title=_("Server language"),
                             description=_("The language used for server policy."),
                             vocabulary=BASE_LANGUAGES_VOCABULARY_NAME,
                             default='en',
                             required=True)

    offered_languages = Set(title=_("Offered languages"),
                            description=_("A list of offered languages. Can be used to "
                                          "user select languages which are offered in "
                                          "a skin."""),
                            value_type=Choice(vocabulary=BASE_LANGUAGES_VOCABULARY_NAME),
                            default={'en'},
                            required=True)

    cache_enabled = Bool(title=_("Language caching enabled"),
                         description=_("Language caching enabled (per request)"),
                         required=True,
                         default=False)

    @invariant
    def check_policy(self):
        """Check against invalid policy"""
        if self.policy not in LANGUAGE_POLICIES:
            raise Invalid(_("Unsupported language policy"))

    def get_language(self, request):
        """Return the matching language to use.

        If 'lang' parameter is defined into request, this lang is returned.
        Otherwise, returned language is based on browser settings, user's session or
        server's language, depending on negotiator's settings.

        If no match is found, None is returned.
        """

    def clear_cache(self, request):
        """Clear cached language value"""


class II18nManager(Interface):
    """Context languages manager

    This interface is used to handle contents providing several languages
    """

    languages = List(title=_("Proposed languages"),
                     description=_("List of languages available for this content"),
                     required=False,
                     value_type=Choice(vocabulary=BASE_LANGUAGES_VOCABULARY_NAME))

    def get_languages(self):
        """Get full languages list"""


class IUserPreferredLanguage(Interface):
    """This interface provides language negotiation based on user preferences"""

    def get_language(self):
        """Return main user preferred language"""


class II18n(Interface):
    """I18n attribute interface"""

    def get_attribute(self, attribute, lang=None, request=None, default=None):
        """Get attribute in given language"""

    def query_attribute(self, attribute, lang=None, request=None, default=None):
        """Query attribute in given language"""
