#!/usr/bin/env python3
import sys, os, json, datetime

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
	print_space('Loading contents of "' + filename + '"...')
	try:
		f = open(filename, "r") # File
		timestamps = json.loads(f.read()) # List
		f.close()
	except:
		print_space('An error occured while loading timestamps from file: ' + str(sys.exc_info()[0]) + '". An empty list is used instead. ' + str(sys.exc_info()[0]), 2)
		timestamps = []
	else:
		print_space('File "' + filename + '" contains ' + str(len(timestamps)) + ' timestamps.', 2)
	return timestamps


"""
Saving data from list into json file
"""
def save_json(timestamps):
	print_space('Saving data into "' + filename + '"...')
	try:
		if os.path.isfile(filename): # File already exists
			print_space('File "' + filename + '" exists. Replacing its content with new data...', 2)
			f = open(filename, "w")
			f.truncate()
		else: # Creating new file
			print_space('File "' + filename + '" doesn\'t exist. Creating new file...', 2)
			f = open(filename, "w")
		f.write(json.dumps(timestamps, indent=4, sort_keys=True))
		f.close()
	except:
		print_space('An error occured while saving timestamps into file: ' + str(sys.exc_info()[0]), 2)


"""
Gets basic information about the file
"""
def get_status():
	try:
		if os.path.isfile(filename): # File exists
			timestamps = load_json()
			if len(timestamps) > 0: # Printing out last timestamp
				print_space('First timestamp: #' + str(timestamps[0]['id']) + ' "' + timestamps[0]['type'] + '" from ' + timestamps[0]['time']) # Info about first timestamp
				print_space('Last timestamp: #' + str(timestamps[len(timestamps) - 1]['id']) + ' "' + timestamps[len(timestamps) - 1]['type'] + '" from ' + timestamps[len(timestamps) - 1]['time']) # Info about last timestamp
		else: # File doesn't exist
			print_space('File "' + filename + '" doesn\'t exist. Creating a new timestamp will create it.')
	except:
		print_space('An error occured while getting file status: ' + str(sys.exc_info()[0]))


"""
Creates new timestamp of a selected type
"""
def new_timestamp(type, timestamps):
	try:
		timestamp = {
			'id': len(timestamps) +1,
			'type': 'start',
			'time': datetime.datetime.now().strftime(dateformat)
		}
		timestamps.append(timestamp)
		print_space('Created new timestamp: "' + str(timestamp) + '"')
		save_json(timestamps)
		load_json()
	except:
		print_space('An error occured while creating new timestamp: ' + str(sys.exc_info()[0]))


"""
Attempts to create a new start timestamp
"""
def start_timestamp():
	try:
		timestamps = load_json()
		if len(timestamps) > 0:
			if timestamps[len(timestamps) - 1]['type'] == 'start':
				print_space('File cannot contain two same consecutive timestamps.')
			else:
				new_timestamp('start', timestamps)
		else:
			new_timestamp('start', timestamps)
	except:
		print_space('An error occured while attempting to create a start timestamp: ' + str(sys.exc_info()[0]))


"""
Attempts to create a new stop timestamp
"""
def stop_timestamp():
	try:
		timestamps = load_json()
		if len(timestamps) > 0:
			if timestamps[len(timestamps) - 1]['type'] == 'stop':
				print_space('File cannot contain two same consecutive timestamps.')
			else:
				new_timestamp('stop', timestamps)
		else:
			print_space('File has to start with a "start" timestamp.')
	except:
		print_space('An error occured while attempting to create a stop timestamp: ' + str(sys.exc_info()[0]))


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
def delete_file():
	try:
		if os.path.isfile(filename): # File exists
			print_space('Removing file "' + filename + '"...')
			os.remove(filename)
		else:
			print_space('File "' + filename + '" doesn\'t exist.')
	except:
		print_space('An error occured while deleting file: ' + str(sys.exc_info()[0]))


"""
List of all commands (with description and a pointer to a function)
"""
commands = {
	'help':    {'description': 'shows all usable commands',               'function': show_commands    },
	'status':  {'description': 'shows basic information about the file',  'function': get_status       },
	'start':   {'description': 'creates new "start" timestamp',           'function': start_timestamp  },
	'stop':    {'description': 'creates new "stop" timestamp',            'function': stop_timestamp   },
	'days':    {'description': 'calculates time spent (day by day)',      'function': time_days        },
	'terms':   {'description': 'calculates time spent (start to stop)',   'function': time_terms       },
	'erase':   {'description': 'removes last timestamp',                  'function': erase_last       },
	'delete':  {'description': 'deletes the whole file',                  'function': delete_file      },
	'exit':    {'description': 'exits the app',                           'function': sys.exit         }
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
	try:
		if len(args) > 1: # Executes arguments (if exist)
			for argument in sys.argv[1:]:
				execute_command(argument)
		else:
			print('Usable commands:')
			execute_command('help')
		while 1: # Asking for commands
			command = input('Enter command: ')
			execute_command(command)
	except:
		print_space('An error occured: ' + str(sys.exc_info()[0]))


if __name__ == '__main__':
	main(sys.argv)
