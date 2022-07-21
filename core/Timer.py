#!/usr/bin/env python3
import os, shutil, json, time


class Timer(object):
    """Singleton for timer functions
    """


    folderName = "timestamps"
    fileName = "timestamps.json"
    

    #########################################################################################


    def __new__(cls):
        """Creating class instance

        Returns:
            Timer: Timer class instance
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Timer, cls).__new__(cls)
        return cls.instance
    

    #########################################################################################
    

    def getFolderPath(cls) -> str:
        """Returns path to folder for timestamps

        Returns:
            str: Folder path
        """
        return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, cls.folderName))
    

    def folderExists(cls) -> bool:
        """Checks if folder for timestamps exists

        Returns:
            bool: Does folder exist?
        """
        return os.path.isdir(cls.getFolderPath())
    

    def createFolder(cls) -> bool:
        """Attempts to create a folder for timestamps

        Returns:
            bool: Success?
        """
        if not cls.folderExists():
            os.mkdir(cls.getFolderPath())
            return True
        return False
    

    def deleteFolder(cls) -> bool:
        """Attempts to delete timestamp folder with files inside

        Returns:
            bool: Success?
        """
        if cls.folderExists():
            shutil.rmtree(cls.getFolderPath())
            return True
        return False
    

    #########################################################################################
    

    def getFilePath(cls) -> str:
        """Returns path to timestamps file

        Returns:
            str: Absolute file path
        """
        return os.path.join(cls.getFolderPath(), cls.fileName)
    

    def fileExists(cls) -> bool:
        """Checks if there is a file for timestamps

        Returns:
            bool: Does the file exist?
        """
        return os.path.isfile(cls.getFilePath())
    

    def createFile(cls) -> bool:
        """Create a file for timestamps

        Returns:
            bool: Success?
        """
        if not cls.folderExists():
            cls.createFolder()
        if not cls.fileExists():
            with open(cls.getFilePath(), 'w'):
                pass
            return True
        return False
    

    def deleteFile(cls) -> bool:
        """Removing timestamp file

        Returns:
            bool: Success?
        """
        if not cls.folderExists():
            return False
        if cls.fileExists():
            os.remove(cls.getFilePath())
            return True
        else:
            return False
    

    #########################################################################################


    def loadTimestamps(cls) -> list:
        """Attempts to load list of timestamps

        Returns:
            list: List of timestamps
        """
        if not cls.folderExists():
            cls.createFolder()
        if cls.fileExists():
            return json.load(open(cls.getFilePath(), "r"))
        else:
            timestamps = []
            cls.saveTimestamps(timestamps)
            return timestamps


    def saveTimestamps(cls, timestamps: list) -> bool:
        """Attempts to save list of timestamps

        Args:
            timestamps (list): List of timestamps to save

        Returns:
            bool: Success?
        """
        if not cls.folderExists():
            cls.createFolder()
        json.dump(timestamps, open(cls.getFilePath(), "w"), indent=4, sort_keys=False)
        return True
    

    #########################################################################################


    def startTimestamp(cls) -> bool:
        """Attempts to add a start timestamp

        Returns:
            bool: Success?
        """
        timestamps = cls.loadTimestamps()
        if len(timestamps) % 2 == 0:
            timestamps.append({"id": len(timestamps) + 1, "type": "start", "timestamp": time.time()})
            Timer().saveTimestamps(timestamps)
            return True
        else:
            return False


    def stopTimestamp(cls) -> bool:
        """Attempts to add a stop timestamp

        Returns:
            bool: Success?
        """
        timestamps = cls.loadTimestamps()
        if len(timestamps) % 2 == 1:
            timestamps.append({"id": len(timestamps) + 1, "type": "stop", "timestamp": time.time()})
            Timer().saveTimestamps(timestamps)
            return True
        else:
            return False
    

    #########################################################################################


    def calculateTerms(cls, timestamps: list) -> tuple:
        """Calculates time spent between timestamps
        List of timestamps should start with a START timestamp.

        Args:
            timestamps (list): List of timestamps

        Returns:
            tuple: Data for output, total time spent
        """
        data = []
        total = 0
        first = None
        last = None
        for i in range(0, len(timestamps), 2):
            start = timestamps[i]["timestamp"]
            if first is None:
                first = start
            # Checking if timestamp list ends with a STOP timestamp, otherwise making a new one
            if (i + 1) < len(timestamps):
                stop = timestamps[i+1]["timestamp"]
            else:
                stop = time.time()
            last = stop
            # Calculating time
            delta = stop - start
            total += delta
            data.append({"id": int(i/2 + 1), "start": start, "stop": stop, "time": delta, "hours": delta / 3600})
        return data, {"id": "TOTAL", "start": first, "stop": last, "time": total, "hours": total / 3600}