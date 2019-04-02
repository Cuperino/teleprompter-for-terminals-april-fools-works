#! /usr/bin/python3

#	Teleprompter for Terminals by Imaginary Sense Inc.
#	Copyright (C) 2020 Imaginary Sense Inc and contributors
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See theRemote 
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

#	Hello there!
#	This software was made as an April Fools joke and is not meant to be
#	used production used in production.

# Load dependencies
import curses
import time
import math
from curses import wrapper
from curses.textpad import Textbox, rectangle

# Globals
x = 4
speedMultip = 3
sensitivity = 1.65
delay = 1

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

	height = curses.LINES - 3
	width = curses.COLS - 4
	begin_y = 2
	begin_x = 1

	stdscr.addstr(0, width//2-26, " Teleprompter for Terminals by Imaginary Sense Inc. ", curses.A_STANDOUT)
	stdscr.addstr(1, 0, "Enter text to prompt: (press Ctrl-G to start prompting)")

	editwin = curses.newwin(height, width, begin_y, 1+begin_x)
	rectangle(stdscr, begin_y, begin_x, 2+height, 2+width)
	# stdscr.addstr(height+2, 5, "Licensed under the General Public License v3")
	stdscr.refresh()

	box = Textbox(editwin)
	box.stripspaces = False

	# Let the user edit until Ctrl-G is struck.
	box.edit()

	# Get resulting contents
	message = box.gather()
	
	stdscr.addstr(height//2+1, 0, ">>")
	stdscr.addstr(height//2+1, width+1, "<<")
	stdscr.addstr(height+2, 5, " [ W decrease speed ]  [ S increase speed ] ")
	stdscr.refresh()

	# Prompt
	prompter = curses.newpad(height*3, width) #, begin_y, 1+begin_x
	prompter.overlay(editwin, 0, 0, begin_y, begin_x, height-2, width-2) #
	prompter.nodelay(True)
	
	updateVelocity()
	pause = False

	# Add text to prompter
	prompter.addstr(height-1, 0, message) # ("message: ,  height: "+str(height)+" ")*200
	for i in range(0, height*3):
		prompter.refresh(0+i, 0, 2, 2, height+1, width)
		time.sleep(delay)
		# time.sleep(0.2)
		key = prompter.getch()
		if key != -1:
			if key == 32:
				pause = not pause
			if key in (87, 119):
				x = x-1
			if key in (83, 115):
				x = x+1
			updateVelocity()
			message = str(key)
			prompter.addstr(height-1, 0, message) # ("message: ,  height: "+str(height)+" ")*200
	time.sleep(0.5)

	# Prompting complete 
	stdscr.addstr(height//2+1, width//2+1-8, "Prompting complete")
	stdscr.refresh()
	time.sleep(2)
	stdscr.addstr(height//2+2, width//2+1-5, "April fools!")
	stdscr.refresh()
	time.sleep(4)

def updateVelocity():
	global delay
	global x
	if x == 0:
		x = 1
	velocity = speedMultip*math.pow(math.fabs(x),sensitivity)
	delay = 5/velocity

# Run main
wrapper(main)

# Unload nCurses
curses.endwin()
