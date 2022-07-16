#!/usr/bin/env python3
import os, shutil


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
    

    def createFolder(cls):
        """Attempts to create a folder for timestamps
        """
        if not cls.folderExists():
            os.mkdir(cls.getFolderPath())
    

    def deleteFolder(cls):
        """Attempts to delete timestamp folder with files inside
        """
        if cls.folderExists():
            shutil.rmtree(cls.getFolderPath())
    

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