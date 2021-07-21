#!/usr/bin/env python3
import sys

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
Prints a message with spacing
"""
def print_space(message):
	print('    ' + message)


"""
Printing out usable commands
"""
def show_commands():
	for command in commands:
		print_space(command + ' - ' + commands[command]['description'])


"""
Gets basic information about the file
"""
def get_status():
	pass


"""
Creates new timestamp
"""
def new_timestamp():
	pass


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
List of all commands (with description and function function)
"""
commands = {
	'help':		{'description': 'shows all usable commands',				'function': show_commands	},
	'status':	{'description': 'shows basic information about the file',	'function': get_status		},
	'start':	{'description': 'creates new \'start\' timestamp',			'function': new_timestamp	},
	'stop':		{'description': 'creates new \'stop\' timestamp',			'function': new_timestamp	},
	'days':		{'description': 'calculates time spent (day by day)',		'function': time_days		},
	'terms': 	{'description': 'calculates time spent (start to stop)',	'function': time_terms		},
	'erase':	{'description': 'removes last timestamp',					'function': erase_last		},
	'delete': 	{'description': 'deletes the file',							'function': remove_file		},
	'exit': 	{'description': 'exits the app',							'function': sys.exit		}
}


"""
Main function, asks for commands and executes them
"""
def main(args):
	try:
		print('Usable commands:')
		show_commands()
		while 1:
			print()
			command = input('Enter command: ')
			if command in commands:
				commands[command]['function']() # Calling a function stored in selected command
			else:
				print_space('Command "' + command + '" doesn\'t exist. Use "help" to get list of all commands.')
	except:
		print_space('An error occured: ')


if __name__ == '__main__':
	main(sys.argv)
