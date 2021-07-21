#!/usr/bin/env python3
import sys

#                 __                                                                            __
#                /_/                                                                           /_/
#   _     __   ___      _____      __        ___    _     __         ____     __   __        ___    _________
#  | |   / /  /   |    / ___/     / /       /   |  | |   / /        / __ \   / /  / /       /   |  /___  ___/
#  | |  / /  / /| |   / /        / /       / /| |  | |  / /        / /_/ /  / /  / /       / /| |     / /
#  | | / /  / /_| |  | |        / /       / /_| |  | | / /        / ____/  / /  / /       / /_| |    / /
#  | |/ /  / ____ |  | |___    / /___    / ____ |  | |/ /        / /      / /  / /____   / ____ |   / /
#  |___/  /_/   |_|   \____/  /______/  /_/   |_|  |___/        /_/      /_/  /______/  /_/   |_|  /_/

# Prints a message witth spacing
def print_space(message):
	print('    ' + message)

# Printing out usable commands
def show_commands():
	for command in commands:
		print_space(command + ' - ' + commands[command]['description'])

# List of all commands
commands = {
	'help':		{'description': 'shows all usable commands',				'callback': show_commands},
	'status':	{'description': 'shows basic information about the file',	'callback': show_commands},
	'start':	{'description': 'creates new \'start\' timestamp',			'callback': show_commands},
	'stop':		{'description': 'creates new \'stop\' timestamp',			'callback': show_commands},
	'days':		{'description': 'calculates time spent (day by day)',		'callback': show_commands},
	'terms': 	{'description': 'calculates time spent (start to stop)',	'callback': show_commands},
	'erase':	{'description': 'removes last timestamp',					'callback': show_commands},
	'delete': 	{'description': 'deletes the file',							'callback': show_commands},
	'exit': 	{'description': 'exits the app',							'callback': sys.exit}
}

# Main function, asks for commands and executes them
def execute_commands():
	print('Usable commands:')
	show_commands()
	while 1:
		print()
		command = input('Enter command: ')
		if command in commands:
			commands[command]['callback']()
		else:
			print_space('Command "' + command + '" doesn\'t exist. Use "help" to get list of all commands.')

execute_commands()
