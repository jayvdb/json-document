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

"""Unit tests for bridge decorators."""

from unittest2 import TestCase

from json_document import bridge
from json_document.document import Document, DocumentFragment


class DecoratorHyphenTests(TestCase):
    """Test automatic hyphen to underscore translation."""

    class TestDocument(Document):

        @bridge.fragment('foo-bar-fragment')
        def foo_bar_fragment(self):
            """Fragment."""
            pass

        @bridge.readonly('foo-bar-readonly')
        def foo_bar_readonly(self):
            """Read-only fragment."""
            pass

        @bridge.readwrite('foo-bar-readwrite')
        def foo_bar_readwrite(self):
            """Read-write fragment."""
            pass

    def setUp(self):
        super(DecoratorHyphenTests, self).setUp()
        self.doc = self.TestDocument({})

    def test_hyphen_fragment(self):
        obj = object()
        self.doc['foo-bar-fragment'] = obj
        self.assertIsInstance(self.doc.foo_bar_fragment, DocumentFragment)
        self.assertIs(self.doc.foo_bar_fragment.value, obj)
        self.assertEqual(self.TestDocument.foo_bar_fragment.__doc__, 'Fragment.')

    def test_hyphen_readonly(self):
        obj = object()
        self.doc['foo-bar-readonly'] = obj
        self.assertIs(self.doc.foo_bar_readonly, obj)
        self.assertEqual(self.TestDocument.foo_bar_readonly.__doc__,
                         'Read-only fragment.')

    def test_hyphen_readwrite(self):
        obj = object()
        self.doc['foo-bar-readwrite'] = obj
        self.assertIs(self.doc.foo_bar_readwrite, obj)
        self.assertEqual(self.TestDocument.foo_bar_readwrite.__doc__,
                         'Read-write fragment.')
