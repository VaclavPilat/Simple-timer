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
    return str(int(hours)) + ":" + str(int(minutes)).rjust(2, "0") + ":" + str(int(seconds)).rjust(2, "0")


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
            row["hours"] = format(row["hours"], ".3f")
        if "date" in row and row["date"] != "":
            row["date"] = dateToReadableString(row["date"])
        if "month" in row and row["month"] != "":
            row["month"] = row["month"].strftime("%B %Y")
    # Altering result data
    if "id" in data[-1] and data[-1]["id"] == "TOTAL" and "rounded" in data[-1]:
        data[-1]["rounded"] = sum(row["rounded"] for row in data[:-1])
    return data


def selectCorrectFieldJustification(type: str, value, length: int) -> str:
    """Creates a new string with the correct justification based on field type

    Args:
        type (str): Field type (name)
        value (mixed): Value
        length (int): Desired length of string

    Returns:
        str: New, justifed string
    """
    if type in ("time", "hours", "rounded"):
        value = value.rjust(length)
    return value.ljust(length + 3)


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
        for key in list(row.keys()):
            output += selectCorrectFieldJustification(key, str(row[key]), lengths[i])
            i+=1
        prints(output)


#########################################################################################


def help():
    """Prints out all usable commands
    """
    printTable(commandList)


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
    printTable(data, result)


def days():
    """Calculates time for each day
    """
    data, result = Timer().calculateDays(Timer().loadTimestamps())
    printTable(data, result)


def today():
    """Calculates time for each day
    """
    data, result = Timer().calculateToday(Timer().loadTimestamps())
    printTable(data)


def months():
    """Calculates time for each month
    """
    data, result = Timer().calculateMonths(Timer().loadTimestamps())
    printTable(data, result)


def erase():
    """Erasing last timestamp
    """
    timestamps = Timer().loadTimestamps()
    if len(timestamps) == 0:
        prints("No timestamps found.")
        return
    timestamps.pop()
    if Timer().saveTimestamps(timestamps):
        prints("Successfully removed last timestamp.")
    else:
        prints("An error occured while saving file.")


def delete():
    """Deleting the whole file
    """
    if Timer().deleteFile():
        prints("Successfully removed file with timestamps.")
    else:
        prints("An error occured while deleting file with timestamps.")
    

#########################################################################################


# List of all commands (with description and a pointer to a function)
commandList = [
    {
        "command": "help",
        "description": "Prints list of usable commands",
    },
#    {
#        "command": "status",
#        "description": "Prints out information about the timestamps",
#    },
    {
        "command": "show",
        "description": "Shows list of timestamps",
    },
    {
        "command": "start",
        "description": "Adds new START timestamp",
    },
    {
        "command": "stop",
        "description": "Adds new STOP timestamp",
    },
    {
        "command": "erase",
        "description": "Removes last timestamp"
    },
    {
        "command": "delete",
        "description": "Deletes the whole file"
    },
    {
        "command": "terms",
        "description": "Calculates time spent between timestamps",
    },
    {
        "command": "days",
        "description": "Calculates time spent day by day",
    },
#    {
#        "command": "weeks",
#        "description": "Calculates time spent for each week",
#    },
    {
        "command": "months",
        "description": "Calculates time spent for each month",
    },
    {
        "command": "today",
        "description": "Calculates time spent on the current day",
    },
    {
        "command": "exit",
        "description": "Exits the application"
    }
]


def execute(command: str):
    """Attempts to execute the specified command

    Args:
        command (str): Command to run
    """
    # Searcing list of commands
    for commands in commandList:
        if command in commands["command"]:
            getattr(sys.modules[__name__], commands["command"])()
            print()
            return
    # Message in case the command is not found
    prints("Command not found, use '" + commandList[0]["command"] + "' to list all usable commands.")
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
            execute('help')
            while True:
                execute(input('Enter command: '))
    except (SystemExit, KeyboardInterrupt):
        prints("Exitting...")
    

#########################################################################################


if __name__ == '__main__':
    main(sys.argv)