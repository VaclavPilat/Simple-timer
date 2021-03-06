#!/usr/bin/env python3
import sys, os, json, datetime, calendar, traceback, math


def trycatch(function, *args):
	def inner(*args):
		try:
			function(*args)
		except:
			traceback.print_exc()
	return function


class Timer:

	file_name = 'timestamps.json' # Json file that contains timestamps
	date_format = '%d.%m.%Y' # Date format
	time_format = '%H:%M:%S' # Time format
	display_empty = False # Displaying days/months on which there was no activity


	current_directory = os.path.dirname(__file__) # The directory where this script is located
	absolute_filepath = os.path.join(current_directory, file_name) # Absolute path to a timesheet file
	datetime_format = date_format + ' ' + time_format # Datetime format


	@trycatch
	def printspace(self, text):
		"""Prints a text with spacing

		Args:
			text (str): Message to print out
		"""
		print(' '*3 + str(text))


	def __string_to_datetime(self, string):
		""" Converts a string with a date and time to a datetime object """
		return datetime.datetime.strptime(string, self.datetime_format)


	def __string_to_date(self, string):
		""" Converts a string with a date and time to a date object """
		return self.__string_to_datetime(string).date()


	def __date_to_datetime(self, date):
		""" Converts a date object to a datetime object """
		return datetime.datetime.combine(date, datetime.time.min)


	def __delta_to_time_string(self, delta):
		""" Gets a formatted string from a deltatime object """
		# Hours
		hours, remaining_seconds = divmod(delta.seconds, 3600)
		minutes, seconds = divmod(remaining_seconds, 60)
		hours += delta.days * 24
		output = str(hours) + ':'
		if len(str(minutes)) == 1:
			output += "0"
		output += str(minutes) + ':'
		if len(str(seconds)) == 1:
			output += "0"
		# Hours (decimal)
		hours_decimal = ((delta.days * 24 * 60 * 60) + delta.seconds) / 3600
		output += str(seconds) + ' = ' + str(round(hours_decimal, 5)) + ' hours'
		# Approximated hours (decimal)
		output += ' ≈ '
		hours_decimal_rest = (hours_decimal - math.floor(hours_decimal))
		if hours_decimal_rest < 0.25:
			output += str(math.floor(hours_decimal))
		elif hours_decimal_rest < 0.75:
			output += str(math.floor(hours_decimal) + 0.5)
		else:
			output += str(math.floor(hours_decimal) + 1)
		output += " hours"
		return output
	

	@trycatch
	def exists(self):
		"""Checks if file containing timestamps exists

		Returns:
			bool: Does file exist?
		"""
		return os.path.isfile(self.absolute_filepath)


	@trycatch
	def load(self):
		"""Loading data from json file into list

		Returns:
			list: List of timestamps
		"""
		try:
			with open(self.absolute_filepath, "r") as f:
				timestamps = json.loads(f.read())
		except:
			self.printspace('Cannot load timestamps from file. An empty list is used instead.')
			timestamps = []
		else:
			self.printspace('File "' + self.file_name + '" contains ' + str(len(timestamps)) + ' timestamps.')
		return timestamps


	@trycatch
	def save(self, timestamps):
		"""Saving data from list into json file

		Args:
			timestamps (list): List of timestamps
		"""
		with open(self.absolute_filepath, "w") as f:
			f.truncate()
			f.write(json.dumps(timestamps, indent=4, sort_keys=False))
		self.printspace('File content has been replaced with new data.')


	@trycatch
	def print_commands(self):
		"""Printing out usable commands
		"""
		for command in self.commands:
			self.printspace(command + ' - ' + self.commands[command]['description'])


	@trycatch
	def print_status(self):
		"""Gets basic information about the file and prints it out
		"""
		if self.exists(): # File exists
			timestamps = self.load()
			if len(timestamps) > 0: # Printing out first timestamp
				self.printspace('First timestamp: ' + str(timestamps[0]) + ' from ' + str(datetime.datetime.now() - self.__string_to_datetime(timestamps[0]['datetime'])).split(".")[0] + ' ago')
				if len(timestamps) > 1: # Printing out last timestamp
					self.printspace('Last timestamp: ' + str(timestamps[-1]) + ' from ' + str(datetime.datetime.now() - self.__string_to_datetime(timestamps[-1]['datetime'])).split(".")[0] + ' ago')
				if timestamps[-1]['type'] == 'start':
					self.printspace('File doesn\'t end with a stop timestamp. Calculations will use current time instead.')
		else: # File doesn't exist
			self.printspace('File "' + self.file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')


	def __new_timestamp(self, type, timestamps):
		""" Creates new timestamp of a selected type """
		try:
			timestamp = {
				'id': len(timestamps) +1,
				'type': type,
				'datetime': datetime.datetime.now().strftime(self.datetime_format)
			}
			timestamps.append(timestamp)
			self.printspace('New timestamp: ' + str(timestamp))
			self.save(timestamps)
			self.load()
		except:
			traceback.print_exc()


	def start_timestamp(self):
		""" Attempts to create a new start timestamp """
		try:
			timestamps = self.load()
			if len(timestamps) > 0:
				if timestamps[-1]['type'] == 'start':
					self.printspace('File cannot contain two same consecutive timestamps.')
				else:
					self.__new_timestamp('start', timestamps)
			else:
				self.__new_timestamp('start', timestamps)
		except:
			traceback.print_exc()


	def stop_timestamp(self):
		""" Attempts to create a new stop timestamp """
		try:
			timestamps = self.load()
			if len(timestamps) > 0:
				if timestamps[-1]['type'] == 'stop':
					self.printspace('File cannot contain two same consecutive timestamps.')
				else:
					self.__new_timestamp('stop', timestamps)
			else:
				self.printspace('File has to start with a "start" timestamp.')
		except:
			traceback.print_exc()


	def __get_timestamps_within_date_span(self, timestamps, date_from, date_to = None):
		""" Returns all timestamps that have a date within a selected time span """
		if date_to == None:
			date_to = date_from
		timestamps_with_date = []
		for timestamp in timestamps:
			if self.__string_to_date(timestamp['datetime']) >= date_from and self.__string_to_date(timestamp['datetime']) <= date_to:
				timestamps_with_date.append(timestamp)
			else:
				if len(timestamps_with_date) > 0: # Breaking the loop if there aren't any more timestamps with matching date
					break
		return timestamps_with_date


	def __calculate_terms(self, timestamps, printing = False):
		""" Returns total time calculated by adding up time between start and stop timestamps """
		total = datetime.timedelta()
		for i in range(0, len(timestamps), 2): # Loops through timestamp by 2 steps
			start = self.__string_to_datetime(timestamps[i]['datetime']) # Start datetime
			if (i + 1) < len(timestamps): # Checking if a stop timestamp is available
				stop = self.__string_to_datetime(timestamps[i + 1]['datetime']) # Stop datetime
			else: # Using current time instead of missing stop timestamp
				stop = datetime.datetime.now()
			delta = stop - start # Timedelta of start and stop timestamps
			total += delta # Adding current delta to total time
			delta_string = self.__delta_to_time_string(delta)
			if printing:
				self.printspace('[' + str(int(i/2 + 1)) + '] ' + str(start.strftime(self.datetime_format)) + " - " + str(stop.strftime(self.datetime_format)) + ' :: ' + delta_string)
		return total


	def __calculate_days(self, timestamps, first_date, last_date, last_timestamp = None, printing = False):
		""" Returns total time calculated by adding up time spent on each day within a set time span """
		timespan_total = datetime.timedelta() # Total time spent in this timespan
		current_date = first_date
		message_id = 1 # ID of a printed out message
		for i in range((last_date - first_date).days + 1): # Looping for number of days from first to last date, inluding both
			day_total = datetime.timedelta()
			timestamps_with_date = self.__get_timestamps_within_date_span(timestamps, current_date)
			# Checking if there is an unclosed term left from the past
			if not last_timestamp == None and last_timestamp['type'] == 'start': 
				if len(timestamps_with_date) > 0:
					day_total += (self.__string_to_datetime(timestamps_with_date[0]['datetime']) - self.__date_to_datetime(current_date)) # Adding time from midniht to next stop timestamp
				else:
					if current_date == datetime.date.today():
						day_total += (datetime.datetime.now() - self.__date_to_datetime(current_date))
					else:
						day_total += datetime.timedelta(days=1)
			# Looping through timestamps from current date
			if len(timestamps_with_date) > 0:
				last_timestamp = timestamps_with_date[-1]
				# Removing redundant timestamps
				if timestamps_with_date[0]['type'] == 'stop':
					del timestamps_with_date[0]
				if len(timestamps_with_date) > 0 and timestamps_with_date[-1]['type'] == 'start':
					del timestamps_with_date[-1]
			day_total += self.__calculate_terms(timestamps_with_date)
			# Checking if there is an unclosed term left from today
			next_day = (self.__date_to_datetime(current_date) + datetime.timedelta(days=1)).date() # Next day (midnight)
			if not last_timestamp == None and last_timestamp['type'] == 'start' and self.__string_to_date(last_timestamp['datetime']) == current_date:
				if current_date == last_date and last_date == datetime.datetime.now().date():
					day_total += datetime.datetime.now() - self.__string_to_datetime(last_timestamp['datetime'])
				else:
					day_total += self.__date_to_datetime(next_day) - self.__string_to_datetime(last_timestamp['datetime'])
			if not day_total == datetime.timedelta() or self.display_empty: # Printing out day total
				timespan_total += day_total
				if printing == True:
					self.printspace('[' + str(message_id) + '] ' + str(current_date.strftime(self.date_format)) + ' :: ' + self.__delta_to_time_string(day_total))
				if current_date == datetime.date.today(): # Breaking the loop if there aren't any timestamps left (necessary for months calculations)
					break
				message_id += 1
			current_date = next_day # Changing current date to a next day
		return [timespan_total, last_timestamp]


	def time_terms(self):
		""" Gets total time spent + time spent between start and stop timestamps """
		try:
			if self.exists(): # File exists
				timestamps = self.load()
				if len(timestamps) > 0:
					total = self.__calculate_terms(timestamps, True) # Calculates total time in terms
					if len(timestamps) % 2 == 1:
						self.printspace('File doesn\'t end with a stop timestamp. Current time was used instead.')
					self.printspace('TOTAL TIME SPENT: ' + self.__delta_to_time_string(total))
				else:
					self.printspace('This file doesn\'t have any timestamps. Cannot perform any calculations.')
			else:
				self.printspace('File "' + self.file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')
		except:
			traceback.print_exc()


	def time_days(self):
		""" Gets total time spent + time day by day """
		try:
			if self.exists(): # File exists
				timestamps = self.load()
				if len(timestamps) > 0:
					first_date = self.__string_to_date(timestamps[0]['datetime']) # Date of a first timestamp
					if len(timestamps) % 2 == 0:
						last_date = self.__string_to_date(timestamps[-1]['datetime']) # Date of a last timestamp
					else:
						last_date = datetime.date.today()
					total = self.__calculate_days(timestamps, first_date, last_date, None, True)[0] # Total time spent
					if len(timestamps) % 2 == 1:
						self.printspace('File doesn\'t end with a stop timestamp. Current time was used instead.')
					self.printspace('TOTAL TIME SPENT: ' + self.__delta_to_time_string(total))
				else:
					self.printspace('This file doesn\'t have any timestamps. Cannot perform any calculations.')
			else:
				self.printspace('File "' + self.file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')
		except:
			traceback.print_exc()


	def time_months(self):
		""" Gets total time spent + time spent each month """
		try:
			if self.exists(): # File exists
				timestamps = self.load()
				if len(timestamps) > 0:
					first_date = self.__string_to_date(timestamps[0]['datetime']) # Date of a first timestamp
					if len(timestamps) % 2 == 0:
						last_date = self.__string_to_date(timestamps[-1]['datetime']) # Date of a last timestamp
					else:
						last_date = datetime.date.today()
					total = datetime.timedelta() # Total time spent
					last_timestamp = None
					current_first_day = datetime.date(first_date.year, first_date.month, 1) # First day of the current month
					message_id = 1
					while (current_first_day.year < last_date.year) or (current_first_day.year == last_date.year and current_first_day.month <= last_date.month):
						current_days = calendar.monthrange(current_first_day.year, current_first_day.month)[1] # Looping through each month
						current_last_day = datetime.date(current_first_day.year, current_first_day.month, current_days) # Last day of the current month
						current_timestamps = self.__get_timestamps_within_date_span(timestamps, current_first_day, current_last_day) # Timestamps from the current month
						if current_last_day.year == datetime.date.today().year and current_last_day.month == datetime.date.today().month:
							calculated_days = self.__calculate_days(current_timestamps, current_first_day, datetime.date.today(), last_timestamp) # Calculating this month's total time spent
						else:
							calculated_days = self.__calculate_days(current_timestamps, current_first_day, current_last_day, last_timestamp) # Calculating this month's total time spent
						current_total = calculated_days[0]
						last_timestamp = calculated_days[1]
						if not current_total == datetime.timedelta() or self.display_empty: # Printing out month total
							total += current_total
							self.printspace('[' + str(message_id) + '] ' + calendar.month_name[current_first_day.month] + " " + str(current_first_day.year) + " :: " + self.__delta_to_time_string(current_total))
							message_id += 1
						current_first_day = current_last_day + datetime.timedelta(days=1)
					if len(timestamps) % 2 == 1:
						self.printspace('File doesn\'t end with a stop timestamp. Current time was used instead.')
					self.printspace('TOTAL TIME SPENT: ' + self.__delta_to_time_string(total))
				else:
					self.printspace('This file doesn\'t have any timestamps. Cannot perform any calculations.')
			else:
				self.printspace('File "' + self.file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')
		except:
			traceback.print_exc()


	@trycatch
	def erase(self):
		"""Erases last timestamp from file
		"""
		if self.exists(): # File exists
			timestamps = self.load()
			if len(timestamps) > 0:
				del timestamps[-1]
				self.save(timestamps)
				self.load()
			else:
				self.printspace('This file doesn\'t have any timestamps.')
		else:
			self.printspace('File "' + self.file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')


	@trycatch
	def delete(self):
		"""Removing file
		"""
		if self.exists(): # File exists
			os.remove(self.absolute_filepath)
			self.printspace('File "' + self.file_name + '" removed.')
		else:
			self.printspace('File "' + self.file_name + '" doesn\'t exist. Making a new "start" timestamp will create it.')


	# List of all commands (with description and a pointer to a function)
	commands = {
		'help':    {'description': 'shows all usable commands',                   'function': print_commands    },
		'status':  {'description': 'shows basic information about the file',      'function': print_status       },
		'start':   {'description': 'creates new "start" timestamp',               'function': start_timestamp  },
		'stop':    {'description': 'creates new "stop" timestamp',                'function': stop_timestamp   },
		'terms':   {'description': 'calculates time spent (between timestamps)',  'function': time_terms       },
		'days':    {'description': 'calculates time spent (day by day)',          'function': time_days        },
		'months':  {'description': 'calculates time spent (each month)',          'function': time_months      },
		'erase':   {'description': 'removes last timestamp',                      'function': erase       },
		'delete':  {'description': 'deletes the whole file',                      'function': delete      },
		'exit':    {'description': 'exits the app',                               'function': sys.exit         }
	}


	@trycatch
	def execute(self, command):
		"""Attempt to execute a command from list of commands

		Args:
			command (str): Command name
		"""
		if command in self.commands:
			self.commands[command]['function'](self) # Calling a function stored in selected command
		else:
			self.printspace('Command "' + command + '" doesn\'t exist. Use "help" to get list of all commands.')
		print()


	def main(self, args):
		"""Main function, asks for commands and executes them

		Args:
			args (list): List of commands
		"""
		try:
			if len(args) > 1: # Executes arguments (if exist)
				for argument in sys.argv[1:]:
					self.execute(argument)
				self.execute('exit')
			else: # Asking for commands
				print('Usable commands:')
				self.execute('help')
				while True:
					command = input('Enter command: ')
					self.execute(command)
		except (SystemExit, KeyboardInterrupt):
			pass
		except:
			traceback.print_exc()


if __name__ == '__main__':
	timer = Timer()
	timer.main(sys.argv)