#!/usr/bin/env python3
import sys, os.path, json, datetime

"""
                __                                                                            __
               /_/                                                                           /_/
  _     __   ___      _____      __        ___    _     __         ____     __   __        ___    _________
 | |   / /  /   |    / ___/     / /       /   |  | |   / /        / __ \   / /  / /       /   |  /___  ___/
 | |  / /  / /| |   / /        / /       / /| |  | |  / /        / /_/ /  / /  / /       / /| |     / /
 | | / /  / /_| |  | |        / /       / /_| |  | | / /        / ____/  / /  / /       / /_| |    / /
 | |/ /  / ____ |  | |___    / /___    / ____ |  | |/ /        / /      / /  / /____   / ____ |   / /
 |___/  /_/   |_|   \____/  /______/  /_/   |_|  |___/        /_/      /_/  /______/  /_/   |_|  /_/
"""


"""
Global variables
"""
space = '    ' # Message indentation
filename = 'time.json' # Json file that contains timestamps
dateformat = '%d.%m.%Y %H:%M:%S' # Datetime format


"""
Prints a message with spacing
"""
def print_space(message, count = 1):
	spaces = ''
	for i in range(count):
		spaces += space
	print(spaces + message)


"""
Printing out usable commands
"""
def show_commands():
	for command in commands:
		print_space(command + ' - ' + commands[command]['description'])


"""
Loading data from json file into list
"""
def load_json():
	print_space('Loading data from "' + filename + '"...')
	try:
		f = open(filename, "r") # File
		j = f.read() # JSON
		l = json.loads(j) # List
	except:
		print_space('Cannot load timestamps from "' + filename + '". An empty list is used instead. ' + str(sys.exc_info()[0]), 2)
		l = []
	else:
		print_space('File "' + filename + '" contains ' + str(len(l)) + ' timestamps.', 2)
	finally:
		f.close()
	return l


"""
Saving data from list into json file
"""
def save_json(timestamps):
	print_space('Saving data into "' + filename + '"...')
	try:
		f = open(filename, "w")
		if os.path.isfile(filename): # File already exists
			print_space('File "' + filename + '" exists. Replacing its content with new data...', 2)
			f.truncate()
		else: # Creating new file
			print_space('File "' + filename + '" doesn\'t exist. Creating new file...', 2)
		f.write(json.dumps(timestamps))
	except:
		print_space('Cannot save data into "' + filename + '". ' + str(sys.exc_info()[0]))
	finally:
		f.close()


"""
Gets basic information about the file
"""
def get_status():
	try:
		if os.path.isfile(filename): # File exists
			timestamps = load_json()
			if len(timestamps) > 0: # Printing out last timestamp
				print_space('Last timestamp: ' + timestamps[len(timestamps) - 1]['type'] + ' from ' + timestamps[len(timestamps) - 1]['time'], 2)
		else: # File doesn't exist
			print_space('File "' + filename + '" doesn\'t exist. Creating a new timestamp will create it.', 2)
	except:
		print_space('An error occured. ' + str(sys.exc_info()[0]), 2)

"""
Creates new timestamp
"""
def new_timestamp():
	try:
		timestamps = load_json()
		timestamp = {
			'id': len(timestamps),
			'type': 'start',
			'time': datetime.datetime.now().strftime(dateformat)
		}
		timestamps.append(timestamp)
		print_space('Created new timestamp: "' + str(timestamp) + '"')
		save_json(timestamps)
		load_json()
	except:
		print_space('An error occured. ' + str(sys.exc_info()[0]))


"""
Gets total time spent + time day by day
"""
def time_days():
	pass


"""
Gets total time spent + time spent between start and stop timestamps
"""
def time_terms():
	pass


"""
Erases last timestamp from file
"""
def erase_last():
	pass


"""
Removing file
"""
def remove_file():
	pass


"""
List of all commands (with description and a pointer to a function)
"""
commands = {
	'help':     {'description': 'shows all usable commands',                'function': show_commands   },
	'status':   {'description': 'shows basic information about the file',   'function': get_status      },
	'start':    {'description': 'creates new "start" timestamp',            'function': new_timestamp   },
	'stop':     {'description': 'creates new "stop" timestamp',             'function': new_timestamp   },
	'days':     {'description': 'calculates time spent (day by day)',       'function': time_days       },
	'terms':    {'description': 'calculates time spent (start to stop)',    'function': time_terms      },
	'erase':    {'description': 'removes last timestamp',                   'function': erase_last      },
	'delete':   {'description': 'deletes the whole file',                   'function': remove_file     },
	'exit':     {'description': 'exits the app',                            'function': sys.exit        }
}


"""
Try to execute a command
"""
def execute_command(command):
	if command in commands:
		commands[command]['function']() # Calling a function stored in selected command
	else:
		print_space('Command "' + command + '" doesn\'t exist. Use "help" to get list of all commands.')
	print()


"""
Main function, asks for commands and executes them
"""
def main(args):
	if len(args) > 1: # Executes arguments (if exist)
		for argument in sys.argv[1:]:
			execute_command(argument)
	else:
		print('Usable commands:')
		execute_command('help')
	while 1: # Asking for commands
		command = input('Enter command: ')
		execute_command(command)


if __name__ == '__main__':
	main(sys.argv)
