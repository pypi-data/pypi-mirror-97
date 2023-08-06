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

"""PyAMS_i18n.vocabulary module

This module provides named vocabularies for offered and selected content languages.
"""

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_i18n.interfaces import CONTENT_LANGUAGES_VOCABULARY_NAME, II18nManager, INegotiator, \
    OFFERED_LANGUAGES_VOCABULARY_NAME
from pyams_i18n.language import BASE_LANGUAGES
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'

from pyams_i18n import _  # pylint: disable=ungrouped-imports


@vocabulary_config(name=OFFERED_LANGUAGES_VOCABULARY_NAME)
class I18nOfferedLanguages(SimpleVocabulary):
    """I18n offered languages vocabulary"""

    def __init__(self, context=None):  # pylint: disable=unused-argument
        terms = []
        negotiator = query_utility(INegotiator)
        if negotiator is not None:
            translate = check_request().localizer.translate
            for lang in negotiator.offered_languages:
                terms.append(SimpleTerm(lang,
                                        title=translate(
                                            BASE_LANGUAGES.get(lang) or _("<unknown>"))))
        super(I18nOfferedLanguages, self).__init__(terms)


@vocabulary_config(name=CONTENT_LANGUAGES_VOCABULARY_NAME)
class I18nContentLanguages(SimpleVocabulary):
    """I18n content languages vocabulary"""

    def __init__(self, context):
        terms = []
        translate = check_request().localizer.translate
        negotiator = query_utility(INegotiator)
        if negotiator is not None:
            terms.append(SimpleTerm(negotiator.server_language,
                                    title=translate(
                                        BASE_LANGUAGES.get(negotiator.server_language))))
        manager = get_parent(context, II18nManager)
        if manager is not None:
            for lang in manager.languages:  # pylint: disable=not-an-iterable
                if (negotiator is None) or (lang != negotiator.server_language):
                    terms.append(SimpleTerm(lang,
                                            title=translate(
                                                BASE_LANGUAGES.get(lang) or _("<unknown>"))))
        super(I18nContentLanguages, self).__init__(terms)
