#!/usr/bin/env python3
import os


class Timer(object):
    """Singleton for timer functions
    """


    folderName = "timestamps"


    def __new__(cls):
        """Creating class instance

        Returns:
            Timer: Timer class instance
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Timer, cls).__new__(cls)
        return cls.instance
    

    def getFolderPath(cls) -> str:
        """Returns path to folder for timestamps

        Returns:
            str: _description_
        """
        return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, cls.folderName))