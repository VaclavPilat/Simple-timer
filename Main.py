#!/usr/bin/env python3
from core.Timer import *
import sys, datetime


indent = "    "
dateFormat = "%d.%m.%Y"
timeFormat = "%H:%M:%S"


def datetimeFormat() -> str:
    """Returns a combination of date and time formats

    Returns:
        str: Datetime format
    """
    return dateFormat + " " + timeFormat


#########################################################################################


def timeToReadableString(time: float) -> str:
    """Converts timestamp to readable datetime string

    Args:
        time (float): Timestamp

    Returns:
        str: Timestamp converted to readable datetime
    """
    return datetime.datetime.fromtimestamp(time).strftime(datetimeFormat())


#########################################################################################


def prints(text: str):
    """Prints text with an indent

    Args:
        text (str): Text to print
    """
    print(indent + text)


def printTable(data: list):
    """Prettyprints data in a table

    Args:
        data (list): List of objects
    """
    if len(data) == 0:
        prints("No data found.")
        return
    # Replacing certain data with a more readable version
    for row in data:
        if "timestamp" in row:
            row["timestamp"] = timeToReadableString(row["timestamp"])
    # Getting headers
    headers = list(data[0].keys())
    # Getting max data lengths
    lengths = [len(headers[i]) for i in range(len(headers))]
    for row in data:
        values = list(row.values())
        for i in range(len(row)):
            if len(str(values[i])) > lengths[i]:
                lengths[i] = len(str(values[i]))
    # Showing headers
    output = ""
    i = 0
    for header in headers:
        output += header.upper().ljust(lengths[i] + 3)
        i+=1
    prints(output)
    # Printing divider
    prints((sum(lengths) + (len(lengths) -1) * 3) * "-")
    # Showing data
    for row in data:
        output = ""
        i = 0
        for value in list(row.values()):
            output += str(value).ljust(lengths[i] + 3)
            i+=1
        prints(output)


#########################################################################################


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


def show():
    """Prints out list of timestamps
    """
    printTable(Timer().loadTimestamps())
    

#########################################################################################


# List of all commands (with description and a pointer to a function)
commandList = {
    ("help", "cmd", "command", "commands"): "Prints list of usable commands",
    #("status", "state", "info", "information"): "Prints out information about the timestamps",
    ("show", "list", "timestamps"): "Shows list of timestamps",
    ("start", "begin"): "Adds new START timestamp",
    ("stop", "end"): "Adds new STOP timestamp",
    #("terms", "term"): "Calculates time spent between timestamps",
    #("days", "day", "daily"): "Calculates time spent day by day",
    #("weeks", "week", "weekly"): "Calculates time spent for each week",
    #("months", "month", "monthly"): "Calculates time spent for each month",
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
    

#########################################################################################


if __name__ == '__main__':
    main(sys.argv)