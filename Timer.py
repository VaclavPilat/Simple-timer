#!/usr/bin/env python3
#                 __                                                                            __
#                /_/                                                                           /_/
#   _     __   ___      _____      __        ___    _     __         ____     __   __        ___    _________
#  | |   / /  /   |    / ___/     / /       /   |  | |   / /        / __ \   / /  / /       /   |  /___  ___/
#  | |  / /  / /| |   / /        / /       / /| |  | |  / /        / /_/ /  / /  / /       / /| |     / /
#  | | / /  / /_| |  | |        / /       / /_| |  | | / /        / ____/  / /  / /       / /_| |    / /
#  | |/ /  / ____ |  | |___    / /___    / ____ |  | |/ /        / /      / /  / /____   / ____ |   / /
#  |___/  /_/   |_|   \____/  /______/  /_/   |_|  |___/        /_/      /_/  /______/  /_/   |_|  /_/

# List of all commands
commands = [
	{ 'command': 'help', 	'description': 'shows all usable commands'					},
	{ 'command': 'status', 	'description': 'shows basic information about the file'		},
	{ 'command': 'start', 	'description': 'creates new \'start\' timestamp'			},
	{ 'command': 'stop', 	'description': 'creates new \'stop\' timestamp'				},
	{ 'command': 'days', 	'description': 'calculates time spent (day by day)'			},
	{ 'command': 'terms', 	'description': 'calculates time spent (start to stop)'		},
	{ 'command': 'erase', 	'description': 'removes last timestamp'						},
	{ 'command': 'delete', 	'description': 'deletes the file'							},
	{ 'command': 'exit', 	'description': 'exits the app'								}
]

# Printing out usable commands
def show_commands():
	for command in commands:
		print('    ' + command['command'] + ' - ' + command['description'])

# Main function, asks for commands and executes them
def execute_commands():
	print('Usable commands:')
	show_commands()
execute_commands()
