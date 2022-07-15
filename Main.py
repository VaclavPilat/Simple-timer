#!/usr/bin/env python3
from core.Timer import *
import sys


def commands():
    print("List of commands:")


# List of all commands (with description and a pointer to a function)
commandList = {
    "commands": "Prints all usable commands"
}


def execute(command: str):
    """Attempts to execute the specified command

    Args:
        command (str): Command to run
    """
    if command in commandList:
        getattr(sys.modules[__name__], command)()
    else:
        print("Command not found")


def main(args: list):
    """Running timer as a console app

    Args:
        args (list): List of arguments
    """
    try:
        if len(args) > 1:
            # Executes arguments (if exist)
            for command in sys.argv[1:]:
                print(command)
        else:
            # Asking for commands
            execute('commands')
            while True:
                execute(input('Enter command: '))
    except (SystemExit, KeyboardInterrupt):
        pass


if __name__ == '__main__':
    main(sys.argv)