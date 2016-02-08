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

"""
json_document.bridge
--------------------

Collection of decorator methods for accessing document fragments

You want to use those decorators if you are not interested in raw JSON or
high-level DocumentFragments (which would require you to access each value via
the .value property) but want to offer a pythonic API instead.
"""


def fragment(func):
    """
    Bridge to a document fragment.

    The name of the fragment is identical to to the name of the decorated
    function. The function is never called, it is only used to obtain the
    docstring.

    This is equivalent to::

        @property
        def foo(self):
            return self['foo']
    """
    name = func.__name__ if callable(func) else func

    def _get(self):
        return self[name]

    def wrapper(func):
        return property(_get, None, None, func.__doc__)

    if callable(func):
        return property(_get, None, None, func.__doc__)
    else:
        return wrapper


def readonly(func):
    """
    Read-only bridge to the value of a document fragment.

    The name of the fragment is identical to to the name of the decorated
    function.  The function is never called, it is only used to obtain the
    docstring.

    This is equivalent to::

        @property
        def foo(self):
            return self['foo'].value
    """
    name = func.__name__ if callable(func) else func

    def _get(self):
        return self[name].value

    def wrapper(func):
        return property(_get, None, None, func.__doc__)

    if callable(func):
        return property(_get, None, None, func.__doc__)
    else:
        return wrapper


def readwrite(func):
    """
    Read-write bridge to the value of a document fragment.

    The name of the fragment is identical to to the name of the decorated
    function.  The function is never called, it is only used to obtain the
    docstring.

    This is equivalent to::

        @property
        def foo(self):
            return self['foo'].value

    Followed by::

        @foo.setter
        def foo(self, new_value):
            return self['foo'] = new_value
    """
    name = func.__name__ if callable(func) else func

    def _get(self):
        return self[name].value

    def _set(self, new_value):
        # XXX: Dear reader, see what __setitem__ does to understand why we
        # don't assign to .value
        self[name] = new_value

    def _del(self):
        del self[name]

    def wrapper(func):
        return property(_get, _set, _del, func.__doc__)

    if callable(func):
        return property(_get, _set, _del, func.__doc__)
    else:
        return wrapper
