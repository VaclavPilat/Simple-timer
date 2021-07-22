#!/usr/bin/env python3
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


# Importing modules
import sys, os, json, datetime


# Global variables
filename = 'timestamps.json' # Json file that contains timestamps
dateformat = '%d.%m.%Y %H:%M:%S' # Datetime format
space = '    ' # Message indentation


def print_space(message):
	""" Prints a message with spacing """
	print(space + message)


def show_commands():
	""" Printing out usable commands """
	for command in commands:
		print_space(command + ' - ' + commands[command]['description'])


def load_json():
	""" Loading data from json file into list """
	try:
		f = open(filename, "r") # File
		timestamps = json.loads(f.read()) # List
		f.close()
	except:
		print_space('Cannot load timestamps from file. An empty list is used instead.')
		timestamps = []
	else:
		print_space('File "' + filename + '" contains ' + str(len(timestamps)) + ' timestamps.')
	return timestamps


def save_json(timestamps):
	""" Saving data from list into json file """
	try:
		f = open(filename, "w") # File
		f.truncate()
		f.write(json.dumps(timestamps, indent=4, sort_keys=True))
		f.close()
		print_space('File content has been replaced with new data.')
	except:
		print_space('An error occured while saving timestamps into file: ' + str(sys.exc_info()))


def get_status():
	""" Gets basic information about the file """
	try:
		if os.path.isfile(filename): # File exists
			timestamps = load_json()
			if len(timestamps) > 0: # Printing out first timestamp
				print_space('First timestamp: ' + str(timestamps[0]))
				if len(timestamps) > 1: # Printing out last timestamp
					print_space('Last timestamp: ' + str(timestamps[-1]))
				if timestamps[-1]['type'] == 'start':
					print_space('File doesn\'t end with a stop timestamp. Calculations will use current time instead.')
		else: # File doesn't exist
			print_space('File "' + filename + '" doesn\'t exist. Making a new "start" timestamp will create it.')
	except:
		print_space('An error occured while getting file status: ' + str(sys.exc_info()))


def new_timestamp(type, timestamps):
	""" Creates new timestamp of a selected type """
	try:
		timestamp = {
			'id': len(timestamps) +1,
			'type': type,
			'time': datetime.datetime.now().strftime(dateformat)
		}
		timestamps.append(timestamp)
		print_space('New timestamp: ' + str(timestamp))
		save_json(timestamps)
		load_json()
	except:
		print_space('An error occured while creating new timestamp: ' + str(sys.exc_info()))


def start_timestamp():
	""" Attempts to create a new start timestamp """
	try:
		timestamps = load_json()
		if len(timestamps) > 0:
			if timestamps[-1]['type'] == 'start':
				print_space('File cannot contain two same consecutive timestamps.')
			else:
				new_timestamp('start', timestamps)
		else:
			new_timestamp('start', timestamps)
	except:
		print_space('An error occured while attempting to create a start timestamp: ' + str(sys.exc_info()))


def stop_timestamp():
	""" Attempts to create a new stop timestamp """
	try:
		timestamps = load_json()
		if len(timestamps) > 0:
			if timestamps[-1]['type'] == 'stop':
				print_space('File cannot contain two same consecutive timestamps.')
			else:
				new_timestamp('stop', timestamps)
		else:
			print_space('File has to start with a "start" timestamp.')
	except:
		print_space('An error occured while attempting to create a stop timestamp: ' + str(sys.exc_info()))


def time_days():
	""" Gets total time spent + time day by day """
	pass


def time_terms():
	""" Gets total time spent + time spent between start and stop timestamps """
	pass


def erase_last():
	""" Erases last timestamp from file """
	try:
		if os.path.isfile(filename): # File exists
			timestamps = load_json()
			if len(timestamps) > 0:
				del timestamps[-1]
				save_json(timestamps)
				load_json()
			else:
				print_space('This file doesn\'t have any timestamps.')
		else:
			print_space('File "' + filename + '" doesn\'t exist. Making a new "start" timestamp will create it.')
	except:
		print_space('An error occured while attempting to create a start timestamp: ' + str(sys.exc_info()))


def delete_file():
	""" Removing file """
	try:
		if os.path.isfile(filename): # File exists
			os.remove(filename)
			print_space('File "' + filename + '" removed.')
		else:
			print_space('File "' + filename + '" doesn\'t exist. Making a new "start" timestamp will create it.')
	except:
		print_space('An error occured while deleting file: ' + str(sys.exc_info()))


# List of all commands (with description and a pointer to a function)
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


def execute_command(command):
	""" Attempt to execute a command """
	if command in commands:
		commands[command]['function']() # Calling a function stored in selected command
	else:
		print_space('Command "' + command + '" doesn\'t exist. Use "help" to get list of all commands.')
	print()


def main(args):
	""" Main function, asks for commands and executes them """
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
	except SystemExit:
		pass
	except:
		print_space('An error occured: ' + str(sys.exc_info()))


if __name__ == '__main__':
	main(sys.argv)
