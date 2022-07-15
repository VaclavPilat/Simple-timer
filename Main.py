#!/usr/bin/env python3
from core.Timer import *
import sys


indent = "    "


def prints(text: str):
    """Prints text with an indent

    Args:
        text (str): Text to print
    """
    print(indent + text)


def help():
    """Prints out all usable commands
    """
    maxLength = len(max(commandList, key = len))
    for command, description in commandList.items():
        prints(command.ljust(maxLength) + " : " + description)


def exit():
    """Exits the application
    """
    sys.exit()


# List of all commands (with description and a pointer to a function)
commandList = {
    "help": "Prints all usable commands",
    "exit": "Exits the application"
}


def execute(command: str):
    """Attempts to execute the specified command

    Args:
        command (str): Command to run
    """
    if command in commandList:
        getattr(sys.modules[__name__], command)()
    else:
        prints("Command not found")
    print()


def main(args: list):
    """Running timer as a console app

    Args:
        args (list): List of arguments
    """
    try:
        if len(args) > 1:
            # Executes arguments (if exist)
            for command in sys.argv[1:]:
                execute(command)
        else:
            # Asking for commands
            print("Usable commands:")
            execute('help')
            while True:
                execute(input('Enter command: '))
    except (SystemExit, KeyboardInterrupt):
        prints("Exitting...")


if __name__ == '__main__':
    main(sys.argv)