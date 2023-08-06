#can not be executed directly. Execute top-level test.py instead
from texbrix.texbrik import brikFromDoc
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath('src')))

testdoc = Path(__file__).resolve().parent.joinpath(
    'input_files/testinput1.brik')
mbrik_testdoc = Path(__file__).resolve().parent.joinpath(
    'input_files/testinput4.mbrik')
complete_testdoc = Path(__file__).resolve().parent.joinpath(
    'input_files/testinput0.brik')


class TestTexBrik(unittest.TestCase):

    def test_packages(self):
        tb = brikFromDoc(testdoc)
        self.assertEqual(set(['amssymb']), tb.packages)

    def test_content(self):
        tb = brikFromDoc(testdoc)
        self.assertTrue(tb.content)
    
    def test_mbrik(self):
        tb = brikFromDoc(mbrik_testdoc)
        self.assertTrue(tb.content)

    def test_expand_brikinserts(self):
        tb = brikFromDoc(testdoc)
        tb.expand()
        self.assertNotEqual(tb.content.find('in2'), -1)
    
    def test_expand_mbrik(self):
        tb = brikFromDoc(complete_testdoc)
        tb.expand()
        self.assertNotEqual(tb.content.find('in2'), -1)

    def test_expand_packages(self):
        tb = brikFromDoc(testdoc)
        tb.expand()
        self.assertNotEqual([i for i in tb.packages if i != 'amssymb'], {})

    def test_expand_content(self):
        tb = brikFromDoc(testdoc)
        tb.expand()
        self.assertNotEqual(tb.content.find('in3'), -1)


if __name__ == '__main__':
    unittest.main()
