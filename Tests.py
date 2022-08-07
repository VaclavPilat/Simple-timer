#!/usr/bin/env python3
from core.Timer import *
import unittest, random


class Tests(unittest.TestCase):


    def generateTimestamps(self, count: int) -> list:
        """Generating a bunch of timestamps with random intervals

        Args:
            count (int): Timestamp count

        Returns:
            list: List of created timestamps
        """
        timestamps = []
        timestamp = round(time.time())
        for i in range(count, 0, -1):
            timestamp -= random.randrange(100_000)
            if i % 2 == 1:
                type = "start"
            else:
                type = "stop"
            timestamps.append({
                "id": i,
                "type": type,
                "timestamp": timestamp
            })
        timestamps.reverse()
        return timestamps
    

    #########################################################################################


    def setUp(self):
        """Called before each test
        """
        Timer().createFolder()


    def tearDown(self):
        """Called after a test ends
        """
        Timer().deleteFolder()
    

    #########################################################################################


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
    

    def test_calculationCorrectness(self):
        """Checks correctness for each calculation method on a lot of timestamps
        """
        functions = [
            Timer().calculateTerms,
            Timer().calculateDays,
            Timer().calculateMonths,
            Timer().calculateWeeks,
            Timer().calculateYears
        ]
        timestamps = self.generateTimestamps(2000)
        for i in range(0, len(timestamps), 2):
            lastTime = None
            for function in functions:
                data, result = function(timestamps[:i])
                currentTime = result["time"]
                if lastTime is not None:
                    try:
                        self.assertEqual(currentTime, lastTime)
                    except AssertionError as e:
                        print("#"*50)
                        print("Function: " + function.__name__)
                        print("Timestamps (" + str(len(timestamps[:i])) + "): " + str(timestamps[:i]))
                        raise e
                lastTime = currentTime


if __name__ == '__main__':
    Timer().folderName = "testfolder"
    print("Folder: " + Timer().getFolderPath())
    Timer().fileName = "testfile.json"
    print("File: " + Timer().getFilePath())
    unittest.main()