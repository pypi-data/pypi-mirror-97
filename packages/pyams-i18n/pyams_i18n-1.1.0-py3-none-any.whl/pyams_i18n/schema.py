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

"""PyAMS_i18n.schema module

This module provides custom schema fields to support contents internationalization.
"""

from persistent.mapping import PersistentMapping
from zope.interface import implementer
from zope.schema import Dict, Text, TextLine
from zope.schema.interfaces import IDict, RequiredMissing

from pyams_utils.schema import HTMLField


__docformat__ = 'restructuredtext'


_MARKER = object()


class DefaultValueMapping(PersistentMapping):
    """Persistent mapping with default value"""

    def __init__(self, default=None, *args, **kwargs):
        # pylint: disable=keyword-arg-before-vararg
        super(DefaultValueMapping, self).__init__(*args, **kwargs)
        self._default = default

    def __missing__(self, key):
        if self._default is not None:
            return self._default
        raise KeyError(key)

    def get(self, key, default=None):
        result = super(DefaultValueMapping, self).get(key, _MARKER)
        if result is _MARKER:
            if default is not None:
                return default
            return self._default
        return result

    def copy(self):
        return DefaultValueMapping(default=self._default, **self)


#
# I18n fields
#

class II18nField(IDict):
    """I18n field marker interface"""


@implementer(II18nField)
class I18nField(Dict):
    """I18n base field class"""

    def __init__(self, key_type=None, value_type=None, **kwargs):
        default = kwargs.get('default')
        if default is not None:
            del kwargs['default']
        Dict.__init__(self, key_type=TextLine(), value_type=value_type, **kwargs)
        self.default = default

    def _validate(self, value):
        super(I18nField, self)._validate(value)
        if self.required:
            if self.default:
                return
            if not value:
                raise RequiredMissing
            for lang in value.values():
                if lang:
                    return
            raise RequiredMissing


class II18nTextLineField(II18nField):
    """I18n text line field marker interface"""


@implementer(II18nTextLineField)
class I18nTextLineField(I18nField):
    """I18n text line field"""

    def __init__(self, key_type=None, value_type=None, default=None,
                 value_constraint=None, value_min_length=0, value_max_length=None, **kwargs):
        # pylint: disable=too-many-arguments
        super(I18nTextLineField, self).__init__(value_type=TextLine(constraint=value_constraint,
                                                                    min_length=value_min_length,
                                                                    max_length=value_max_length,
                                                                    required=False),
                                                default=default,
                                                **kwargs)


class II18nTextField(II18nField):
    """I18n text field marker interface"""


@implementer(II18nTextField)
class I18nTextField(I18nField):
    """I18n text field"""

    def __init__(self, key_type=None, value_type=None, default=None,
                 value_constraint=None, value_min_length=0, value_max_length=None, **kwargs):
        # pylint: disable=too-many-arguments
        super(I18nTextField, self).__init__(value_type=Text(constraint=value_constraint,
                                                            min_length=value_min_length,
                                                            max_length=value_max_length,
                                                            required=False),
                                            default=default,
                                            **kwargs)


class II18nHTMLField(II18nField):
    """I18n HTML field marker interface"""


@implementer(II18nHTMLField)
class I18nHTMLField(I18nField):
    """I18n HTML field"""

    def __init__(self, key_type=None, value_type=None, default=None,
                 value_constraint=None, value_min_length=0, value_max_length=None, **kwargs):
        # pylint: disable=too-many-arguments
        super(I18nHTMLField, self).__init__(value_type=HTMLField(constraint=value_constraint,
                                                                 min_length=value_min_length,
                                                                 max_length=value_max_length,
                                                                 required=False),
                                            default=default,
                                            **kwargs)
