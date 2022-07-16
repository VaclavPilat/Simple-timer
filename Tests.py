#!/usr/bin/env python3
from core.Timer import *
import unittest, random


class Tests(unittest.TestCase):


    def setUp(self):
        """Called before each test
        """
        Timer().createFolder()


    def tearDown(self):
        """Called after a test ends
        """
        Timer().deleteFolder()


    def test_singletion(self):
        """Tests if the Timer class is a singleton
        """
        self.assertEqual(Timer(), Timer())
    

    def test_createDelete(self):
        """Attempts to create and delete a timestamp file and folder
        """
        cases = [
            lambda: self.assertEqual(not Timer().folderExists(), Timer().createFolder()),
            lambda: self.assertEqual(Timer().folderExists(), Timer().deleteFolder()),
            lambda: self.assertEqual(not Timer().fileExists(), Timer().createFile()),
            lambda: self.assertEqual(Timer().fileExists(), Timer().deleteFile())
        ]
        for i in range(100):
            random.choice(cases)()


if __name__ == '__main__':
    Timer().folderName = "testfolder"
    print("Folder: " + Timer().getFolderPath())
    Timer().fileName = "testfile.json"
    print("File: " + Timer().getFilePath())
    unittest.main()