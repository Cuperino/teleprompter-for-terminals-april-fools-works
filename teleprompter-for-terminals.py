#! /usr/bin/python3

#	Teleprompter for Terminals by Imaginary Sense Inc.
#	Copyright (C) 2021 Imaginary Sense Inc and contributors
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

#	Hello there!
#	This software was made as an April Fools joke and is not meant to be
#	used in production.

# Load dependencies
import curses
import time
import math
from curses import wrapper
from curses.textpad import Textbox, rectangle

# Globals
debug = True
delay = 1
# Default values for velocity control
x = 4
speedMultip = 1.2
sensitivity = 1.45

# Main
def main(stdscr):
	# Setup terminal screen
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)

	# Clear screen
	stdscr.clear()

	# BEGIN APP
	prompt(stdscr)

	# Restore terminal
	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()

# Other methods
def main(stdscr):
	global x

	# Compute terminal size and, thus, usable area
	height = curses.LINES - 3
	width = curses.COLS - 4
	begin_y = 2
	begin_x = 1
	progress = 0

	# Display header information
	stdscr.addstr(0, width//2-26, " Teleprompter for Terminals by Imaginary Sense Inc. ", curses.A_STANDOUT)
	stdscr.addstr(1, 0, "Enter text to prompt: (press Ctrl-G to start prompting)")

	# Create editable area window
	editwin = curses.newwin(height, width, begin_y, 1+begin_x)
	rectangle(stdscr, begin_y, begin_x, 2+height, 2+width)
	stdscr.refresh()

	editwin.insstr(1,1,"Welcome to Teleprompter for Terminals")
	editwin.insstr(2,4,"Are you ready to tell a story?")
	editwin.move(2,34)

	# Turn edit window into a Textbox 
	box = Textbox(editwin)
	# Keep whitespace when gathering data
	box.stripspaces = False

	# Let the user edit until Ctrl-G is struck.
	box.edit()

	# Get resulting contents
	message = box.gather()
	
	# Add reading area markers
	stdscr.addstr(height//2+1, 0, ">>")
	stdscr.addstr(height//2+1, width+1, "<<")
	# Display instructions
	stdscr.addstr(height+2, 5, " [ W decrease speed ]  [ S increase speed ] ")
	stdscr.refresh()

	# Create prompter pad (a pad can extend beyond viewable area)
	# Having a fixed pad size (height*3) is one of those things that makes this implementation impractical for production.
	# Pagination functions would have to be implemented, but hey, this is an April Fools joke.
	prompter = curses.newpad(height*3, width)
	# Overlay prompter over editwin
	prompter.overlay(editwin, 0, 0, begin_y, begin_x, height-2, width-2)
	# Don't prompt the user for input, grab the last keypress on getch()
	prompter.nodelay(True)
	
	# Set velocity for the first time
	updateVelocity()
	# pause = False

	# Add text to prompter
	prompter.addstr(height-1, 0, message)
	# Begin scroll loop
	# Using Python's for loop is a bad implementation because it makes it difficult to change scrolling directions.
	# Re implementing this with a while loop is adviced for production.
	i = 1
	while i < height*3:
		# Refresh promptable area while scrolling the pad.
		if x > 0:
			prompter.refresh(i, 0, 2, 2, height+1, width)	
			i = i + 1
		if x < 0:
			prompter.refresh(i, 0, 2, 2, height+1, width)	
			i = i - 1
		else:
			i = i
		# Post scrolling delay
		while x==0 or delay-progress > 0.002:
			time.sleep(0.002)
			progress = progress + 0.002
			# Debug: Default delay used during testing
			# time.sleep(0.2)
			# Grab the last key pressed
			key = prompter.getch()
			if key != -1:
				# if key == 32:
					# pause = not pause
				if key in (87, 119):
					x = x-1
				if key in (83, 115):
					x = x+1
				updateVelocity()
				# Debug: Display key on prompable area
				if debug:
					message = str(key)
					prompter.addstr(height-1, 0, message)
		progress = 0
	# Add a 0.5s delay for retro feelings
	time.sleep(0.5)

	# Notify prompting complete
	stdscr.addstr(height//2+1, width//2+1-8, "Prompting complete")
	stdscr.refresh()
	time.sleep(2)
	stdscr.addstr(height//2+2, width//2+1-5, "April fools!")
	stdscr.refresh()
	time.sleep(4)

# Update velocity with something similar to Imaginary Teleprompter's exponential curve
def updateVelocity():
	global delay
	global x
	if x != 0:
		velocity = speedMultip*math.pow(math.fabs(x),sensitivity)
		delay = 5/velocity
	else:
		delay = 0

# Run main with nCurses
# Wrapping with nCurses instead of running directly prevents the terminal from getting screwed up on a crash
wrapper(main)

# Unload nCurses
curses.endwin()
