#!/usr/bin/env python3


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