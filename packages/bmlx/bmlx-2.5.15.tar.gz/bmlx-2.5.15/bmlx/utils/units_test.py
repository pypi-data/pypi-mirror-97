from bmlx.utils import unit_utils
import unittest


class Unittest(unittest.TestCase):
    def testTranslate(self):
        s = unit_utils.StorageUnit("20Gi")
        self.assertAlmostEquals(s.to_mega(), 21474, delta=1)
        self.assertEqual(s.to_mega_i(), 20 * 1024)

    def testAdd(self):
        left = unit_utils.StorageUnit("20Gi")
        right = unit_utils.StorageUnit("30Gi")
        left += right
        self.assertEqual(left.to_mega_i(), 50 * 1024)

        left += unit_utils.StorageUnit("20Mi")
        self.assertEqual(left.to_mega_i(), 50 * 1024 + 20)
