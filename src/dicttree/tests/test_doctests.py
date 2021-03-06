import doctest
import unittest
from pprint import pprint

optionflags = doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    '../tests.rst',
    '../tools.rst',
#    'view.rst',
]

TESTMODULES = [
    'dicttree.aspects',
    'dicttree.tools',
# there is a test declared in INode, but it does not work
#    'dicttree.interfaces',
#    'dicttree.view',
]

def test_suite():
    return unittest.TestSuite([
        doctest.DocTestSuite(
            module,
            optionflags=optionflags,
            ) for module in TESTMODULES
        ]+[
        doctest.DocFileSuite(
            file,
            optionflags=optionflags,
            globs={'pprint': pprint},
            ) for file in TESTFILES
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')  #pragma NO COVERAGE
