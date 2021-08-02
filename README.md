# Simple timer
Simple console timer to keep track of total time spent.

## How it works
The program, while running, asks for commands. The most important commands are `start` and `stop`, which are used to create new timestamps. These timestamps are stored in a (newly created) JSON file `timestamps.json` and are used to calculate total time spent. If the file doesn't end with a "stop" timestamp, time calculations will use current time instead.

The current version has these ways to calculate time:
* `terms`, by simply adding up time between "start" and "stop" timestamps:
  ```
  #1 (15.07.2021 16:31:22 - 18.07.2021 16:31:23) :: 72:00:01 = 72.00028 hours
  #2 (22.07.2021 16:31:25 - 22.07.2021 16:31:26) :: 0:00:01 = 0.00028 hours
  #3 (22.07.2021 16:35:12 - 22.07.2021 16:54:31) :: 0:19:19 = 0.32194 hours
  #4 (22.07.2021 16:54:33 - 22.07.2021 18:52:03) :: 1:57:30 = 1.95833 hours
  #5 (22.07.2021 19:46:02 - 23.07.2021 12:01:22) :: 16:15:20 = 16.25556 hours
  #6 (23.07.2021 12:15:31 - 23.07.2021 16:22:45) :: 4:07:14 = 4.12056 hours
  #7 (23.07.2021 18:05:11 - 23.07.2021 22:58:14) :: 4:53:03 = 4.88417 hours
  TOTAL TIME SPENT: 99:32:28 = 99.54111 hours
  ```
* and more complicated `days`, which prints out time spent for each day:
  ```
  #1 15.07.2021 :: 7:28:38 = 7.47722 hours
  #2 16.07.2021 :: 24:00:00 = 24.0 hours
  #3 17.07.2021 :: 24:00:00 = 24.0 hours
  #4 18.07.2021 :: 16:31:23 = 16.52306 hours
  #5 22.07.2021 :: 6:30:48 = 6.51333 hours
  #6 23.07.2021 :: 21:01:39 = 21.0275 hours
  TOTAL TIME SPENT: 99:32:28 = 99.54111 hours
  ```

Use command `help` to show all available commands and their description.

## How to run
To run this program, make sure you have installed Python 3. You don't have to install any other packages or modules.

This program is meant to be run from a command line interface. Navigate to the folder that contains file `Timer.py` and use the following command to run the program. Then the program will start asking for commands, which requires user interaction. 
```
./Timer.py
```
Another way to run the code is to put the commands as arguments when running the program. This will run them all at once.
```
./Timer.py status terms days
```