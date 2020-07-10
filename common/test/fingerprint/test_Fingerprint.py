# -*- coding: utf-8 -*-
import unittest
from common.fingerprint.Fingerprint import Fingerprint


class FingerprintTest(unittest.TestCase):
    f = Fingerprint()

    def test_unicode_case1(self):
        input = u"Gesù"
        expected = "gesu"
        actual = self.f.ontorefine_fingeprint_key(input)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

