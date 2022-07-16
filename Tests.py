#!/usr/bin/env python3
from core.Timer import *
import unittest


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
    

    def test_createAndDeleteFile(self):
        """Attempts to create and delete a timestamp file
        """
        Timer().createFile()
        Timer().deleteFile()


if __name__ == '__main__':
    Timer().folderName = "testfolder"
    print("Folder: " + Timer().getFolderPath())
    Timer().fileName = "testfile.json"
    print("File: " + Timer().getFilePath())
    unittest.main()