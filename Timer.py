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
import sys, os, json, datetime, traceback


# Global variables
file_name = 'timestamps.json' # Json file that contains timestamps
datetime_format = '%d.%m.%Y %H:%M:%S' # Datetime format
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
		f = open(file_name, "r") # File
		timestamps = json.loads(f.read()) # List
		f.close()
	except:
		print_space('Cannot load timestamps from file. An empty list is used instead.')
		timestamps = []
	else:
		print_space('File "' + file_name + '" contains ' + str(len(timestamps)) + ' timestamps.')
	return timestamps


def save_json(timestamps):
	""" Saving data from list into json file """
	try:
		f = open(file_name, "w") # File
		f.truncate()
		f.write(json.dumps(timestamps, indent=4, sort_keys=True))
		f.close()
		print_space('File content has been replaced with new data.')
	except:
		traceback.print_exc()


def get_status():
	""" Gets basic information about the file """
	try:
		if os.path.isfile(file_name): # File exists
			timestamps = load_json()
			if len(timestamps) > 0: # Printing out first timestamp
				print_space('First timestamp: ' + str(timestamps[0]))
				if len(timestamps) > 1: # Printing out last timestamp
					print_space('Last timestamp: ' + str(timestamps[-1]))
				if timestamps[-1]['type'] == 'start':
					print_space('File doesn\'t end with a stop timestamp. Calculations will use current time instead.')
		else: # File doesn't exist
			print_space('File "' + file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')
	except:
		traceback.print_exc()


def new_timestamp(type, timestamps):
	""" Creates new timestamp of a selected type """
	try:
		timestamp = {
			'id': len(timestamps) +1,
			'type': type,
			'datetime': datetime.datetime.now().strftime(datetime_format)
		}
		timestamps.append(timestamp)
		print_space('New timestamp: ' + str(timestamp))
		save_json(timestamps)
		load_json()
	except:
		traceback.print_exc()


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
		traceback.print_exc()


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
		traceback.print_exc()


def delta_to_time_string(delta):
	""" Gets a formatted string from a deltatime object """
	hours, remaining_seconds = divmod(delta.seconds, 3600)
	minutes, seconds = divmod(remaining_seconds, 60)
	hours += delta.days * 24
	return str(hours) + ':' + str(minutes) + ':' + str(seconds) + ' = ' + str(round(delta.seconds / 3600, 5))


def time_days():
	""" Gets total time spent + time day by day """
	pass


def time_terms():
	""" Gets total time spent + time spent between start and stop timestamps """
	try:
		if os.path.isfile(file_name): # File exists
			timestamps = load_json()
			if len(timestamps) > 0:
				total = datetime.timedelta() # Total time spent
				for i in range(0, len(timestamps), 2): # Loops through timestamp by 2 steps
					start = datetime.datetime.strptime(timestamps[i]['datetime'], datetime_format)
					if (i + 1) < len(timestamps): # Checking if a stop timestamp is available
						stop = datetime.datetime.strptime(timestamps[i + 1]['datetime'], datetime_format)
					else: # Using current time instead of missing stop timestamp
						stop = datetime.datetime.now()
					delta = stop - start # Timedelta of start and stop timestamps
					total += delta # Adding current delta to total time
					delta_string = delta_to_time_string(delta)
					print_space('#' + str(int(i/2 + 1)) + ' (' + str(start.strftime(datetime_format)) + " - " + str(stop.strftime(datetime_format)) + '): ' + delta_string)
				if len(timestamps) % 2 == 1:
					print_space('File doesn\'t end with a stop timestamp. Current time was used instead.')
				print_space('TOTAL TIME SPENT: ' + delta_to_time_string(total))
			else:
				print_space('This file doesn\'t have any timestamps. Cannot perform any calculations.')
		else:
			print_space('File "' + file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')
	except:
		traceback.print_exc()


def erase_last():
	""" Erases last timestamp from file """
	try:
		if os.path.isfile(file_name): # File exists
			timestamps = load_json()
			if len(timestamps) > 0:
				del timestamps[-1]
				save_json(timestamps)
				load_json()
			else:
				print_space('This file doesn\'t have any timestamps.')
		else:
			print_space('File "' + file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')
	except:
		traceback.print_exc()


def delete_file():
	""" Removing file """
	try:
		if os.path.isfile(file_name): # File exists
			os.remove(file_name)
			print_space('File "' + file_name + '" removed.')
		else:
			print_space('File "' + file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')
	except:
		traceback.print_exc()


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
		traceback.print_exc()


if __name__ == '__main__':
	main(sys.argv)
