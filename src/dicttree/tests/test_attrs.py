from unittest import TestCase

from dicttree.aspects import attrs


class Adoption(TestCase):
    def runTest(self):
        @attrs
        class A(object):
            pass

        a = A()

        self.assertEquals(a.attrs.__name__, '__attrs__')
        self.assertIs(a.attrs.__parent__, a)
