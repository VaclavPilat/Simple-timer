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
    # Getting length of the longest key
    maxLength = 0
    for commands in list(commandList.keys()):
        if len(commands[0]) > maxLength:
            maxLength = len(commands[0])
    # Printing commands
    for commands, description in commandList.items():
        prints(commands[0].ljust(maxLength) + " - " + description)


def exit():
    """Exits the application
    """
    sys.exit()


def start():
    """Adding new START timestamp to file
    """
    if Timer().startTimestamp():
        prints("New START timestamp added. Calculations will use current time as end of this term.")
    else:
        prints("New START timestamp could not be added. Make sure that timestamp types alternate.")


def stop():
    """Adding new STOP timestamp to file
    """
    if Timer().stopTimestamp():
        prints("New STOP timestamp added.")
    else:
        prints("New STOP timestamp could not be added. Make sure that timestamp types alternate.")


# List of all commands (with description and a pointer to a function)
commandList = {
    ("help", "cmd", "command", "commands"): "Prints list of usable commands",
    ("start", "begin"): "Adds new START timestamp",
    ("stop", "end"): "Adds new STOP timestamp",
    ("exit", "quit"): "Exits the application"
}


def execute(command: str):
    """Attempts to execute the specified command

    Args:
        command (str): Command to run
    """
    # Searcing list of commands
    for commands in list(commandList.keys()):
        if command in commands:
            getattr(sys.modules[__name__], commands[0])()
            print()
            return
    # Message in case the command is not found
    prints("Command not found, use '" + list(commandList.keys())[0][0] + "' to list all usable commands.")
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