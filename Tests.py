#!/usr/bin/env python3
from core.Timer import *
import unittest


class Tests(unittest.TestCase):


    def test_singletion(self):
        """Tests if the Timer class is a singleton
        """
        self.assertEqual(Timer(), Timer())


    def test_changeFolderName(self):
        """Try to change default folder name
        """
        Timer().folderName = "test"
        self.assertEqual(Timer().folderName, "test")


    def test_checkFolderPath(self):
        """Checking if folder path to timestamp directory is correct
        """
        self.assertEqual(Timer().getFolderPath(), os.path.join(os.path.dirname(__file__), "test"))


if __name__ == '__main__':
    unittest.main()