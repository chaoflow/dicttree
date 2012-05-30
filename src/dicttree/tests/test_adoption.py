from unittest import TestCase

from dicttree.aspects.adoption import adopting
from dicttree.aspects.adoption import adoptable


class Adoption(TestCase):
    def runTest(self):
        class A(object):
            pass

        child = adoptable(A)(name=1, parent=2)
        self.assertEqual(child.name, 1)
        self.assertEqual(child.parent, 2)

        parent = adopting(dict())
        def setchild():
            parent['luke'] = child
        self.assertRaises(ValueError, setchild)

        child.__parent__ = None
        parent['leia'] = child
        self.assertEqual(child.name, 'leia')
        self.assertIs(child.parent, parent)

        del parent['leia']
        self.assertEqual(child.name, 'leia')
        self.assertIs(child.parent, None)

        @adopting
        class Fail(object):
            def __delitem__(self, key):
                pass
            def __setitem__(self, key, val):
                raise Exception
        parent = Fail()
        self.assertRaises(Exception, setchild)
        self.assertEqual(child.name, 'leia')
        self.assertIs(child.parent, None)
