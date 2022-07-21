#!/usr/bin/env python3
from core.Timer import *
import sys, datetime, math


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


def timeToReadableString(time: int) -> str:
    """Converts timestamp to readable datetime string

    Args:
        time (int): Timestamp

    Returns:
        str: Timestamp converted to readable datetime
    """
    return datetime.datetime.fromtimestamp(time).strftime(datetimeFormat())


def dateToReadableString(date: datetime.date) -> str:
    """Converts date to readable date string

    Args:
        date (int): Date

    Returns:
        str: Date converted to readable date
    """
    return datetime.datetime.combine(date, datetime.time.min).strftime(dateFormat)


def deltaToReadableTime(delta: int) -> str:
    """Converts delta time to readable format

    Args:
        delta (int): Time delta

    Returns:
        str: Time delta converted to readable version
    """
    hours = delta // 3600
    minutes = (delta % 3600) // 60
    seconds = math.floor(delta % 60)
    return str(int(hours)) + ":" + str(int(minutes)) + ":" + str(int(seconds))


#########################################################################################


def prints(text: str):
    """Prints text with an indent

    Args:
        text (str): Text to print
    """
    print(indent + text)


def processTableData(data: list) -> list:
    """Processes data into a more readable version

    Args:
        data (list): List of objects to be processed

    Returns:
        list: Processed data
    """
    if len(data) == 0:
        return
    # Altering row data
    for row in data:
        if "timestamp" in row and row["timestamp"] != "":
            row["timestamp"] = timeToReadableString(row["timestamp"])
        if "start" in row and row["start"] != "":
            row["start"] = timeToReadableString(row["start"])
        if "stop" in row and row["stop"] != "":
            row["stop"] = timeToReadableString(row["stop"])
        if "time" in row and row["time"] != "":
            row["hours"] = round(row["time"] / 3600, 3)
            if row["hours"] % 1 >= 0.75:
                row["rounded"] = row["hours"] - row["hours"] % 1 + 1
            elif row["hours"] % 1 >= 0.25:
                row["rounded"] = row["hours"] - row["hours"] % 1 + 0.5
            else:
                row["rounded"] = row["hours"] - row["hours"] % 1
            row["time"] = deltaToReadableTime(row["time"])
        if "date" in row and row["date"] != "":
            row["date"] = dateToReadableString(row["date"])
    # Altering result data
    if data[-1]["id"] == "TOTAL" and "rounded" in data[-1]:
        data[-1]["rounded"] = sum(row["rounded"] for row in data[:-1])
    return data


def printTable(data: list, result: dict = None):
    """Prettyprints data in a table

    Args:
        data (list): List of objects
        result (dict): Object with result data
    """
    if len(data) == 0:
        prints("No data found.")
        return
    if result is not None:
        data += [result, ]
    # Replacing certain data with a more readable version
    processTableData(data)
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
        if "id" in row and type(row["id"]) is not int:
            prints((sum(lengths) + (len(lengths) -1) * 3) * "-")
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


def terms():
    """Calculates time between timestamps and shows the result
    """
    data, result = Timer().calculateTerms(Timer().loadTimestamps())
    #print(result)
    printTable(data, result)


def days():
    """Calculates time for each day
    """
    data, result = Timer().calculateDays(Timer().loadTimestamps())
    #print(result)
    printTable(data, result)
    

#########################################################################################


# List of all commands (with description and a pointer to a function)
commandList = {
    ("help", "cmd", "command", "commands"): "Prints list of usable commands",
    #("status", "state", "info", "information"): "Prints out information about the timestamps",
    ("show", "list", "timestamps"): "Shows list of timestamps",
    ("start", "begin"): "Adds new START timestamp",
    ("stop", "end"): "Adds new STOP timestamp",
    ("terms", "term"): "Calculates time spent between timestamps",
    ("days", "day", "daily"): "Calculates time spent day by day",
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