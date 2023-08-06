import unittest

from cbm_files.tokenset_basic_v2 import TokenSet_BASICv2


class TestBasicV2(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_BASICv2()
        self.assertEqual(tokenset.tokenize('SYS', 'ascii'), b'\x9e')
        self.assertEqual(tokenset.tokenize('GOTO', 'ascii'), b'\x89')
        self.assertEqual(tokenset.tokenize('GO TO', 'ascii'), b'\xcb \xa4')
        self.assertEqual(tokenset.tokenize('A=RND(1)', 'ascii'), b'A\xb2\xbb(1)')
        self.assertEqual(tokenset.tokenize('3↑2', 'ascii'), b'3\xae2')
        self.assertEqual(tokenset.tokenize('3^2', 'ascii'), b'3\xae2')

    def test_expand(self):
        tokenset = TokenSet_BASICv2()
        self.assertEqual(tokenset.expand(b'\x9e', 'ascii'), 'SYS')
        self.assertEqual(tokenset.expand(b'A\xb2\xbb(1)', 'ascii'), 'A=RND(1)')
        self.assertEqual(tokenset.expand(b'3\xae2', 'ascii'), '3^2')
