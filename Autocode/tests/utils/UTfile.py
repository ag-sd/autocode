import unittest
from Autocode.utils import file


class UTfile(unittest.TestCase):

    def testNonExistentPath(self):
        self.assertEqual(file.find_files("XYS"), [])

