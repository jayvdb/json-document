# Copyright (C) 2010, 2011 Linaro Limited
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@linaro.org>
#
# This file is part of json-document
#
# json-document is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation
#
# json-document is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with json-document.  If not, see <http://www.gnu.org/licenses/>.

import copy
import decimal
import os

from json_schema_validator.errors import SchemaError, ValidationError
from json_schema_validator.schema  import Schema
from json_schema_validator.validator import Validator
import simplejson

class DocumentIO(object):
    """
    DocumentIO encapsulates loading and saving JSON objects.
    """

    @classmethod
    def _get_dict_impl(cls, retain_order):
        if retain_order:
            object_pairs_hook = simplejson.OrderedDict
        else:
            object_pairs_hook = None
        return object_pairs_hook

    @classmethod
    def _get_indent_and_separators(cls, human_readable):
        if human_readable:
            indent = ' ' * 2
            separators = (', ', ': ')
        else:
            indent = None
            separators = (',', ':')
        return indent, separators

    @classmethod
    def load(cls, stream, retain_order=True):
        """
        Load and check a JSON document from the specified stream

        :Discussion:
            The document is read from the stream and parsed as JSON text.

        :Return value:
            The document loaded from the stream. If retain_order is True then
            the resulting objects are composed of ordered dictionaries. This
            mode is slightly slower and consumes more memory.

        :Exceptions:
            ValueError
                When the text does not represent a correct JSON document.
        """
        object_pairs_hook = cls._get_dict_impl(retain_order)
        return simplejson.load(stream, parse_float=decimal.Decimal,
                         object_pairs_hook=object_pairs_hook)

    @classmethod
    def loads(cls, text, retain_order=True):
        """
        Same as load() but reads data from a string
        """
        object_pairs_hook = cls._get_dict_impl(retain_order)
        return simplejson.loads(text, parse_float=decimal.Decimal,
                          object_pairs_hook=object_pairs_hook)

    @classmethod
    def dump(cls, stream, doc, human_readable=True, sort_keys=False):
        """
        Save a JSON document to the specified stream

        :Discussion:
            If human_readable is True the serialized stream is meant to be
            read by humans, it will have newlines, proper indentation and
            spaces after commas and colons. This option is enabled by default.

            If sort_keys is True then resulting JSON object will have sorted
            keys in all objects. This is useful for predictable format but is
            not recommended if you want to load-modify-save an existing
            document without altering it's general structure. This option is
            not enabled by default.

        :Return value:
            None
        """
        indent, separators = cls._get_indent_and_separators(human_readable)
        simplejson.dump(doc, stream, use_decimal=True, indent=indent,
                  separators=separators, sort_keys=sort_keys)

    @classmethod
    def dumps(cls, doc, human_readable=True, sort_keys=False):
        """
        Save a JSON document as string

        :Discussion:
            If human_readable is True the serialized value is meant to be read
            by humans, it will have newlines, proper indentation and spaces
            after commas and colons. This option is enabled by default.

            If sort_keys is True then resulting JSON object will have sorted
            keys in all objects. This is useful for predictable format but is
            not recommended if you want to load-modify-save an existing
            document without altering it's general structure. This option is
            not enabled by default.

        :Return value:
            JSON document as string
        """
        indent, separators = cls._get_indent_and_separators(human_readable)
        return simplejson.dumps(doc, use_decimal=True, indent=indent,
                          separators=separators, sort_keys=sort_keys)
