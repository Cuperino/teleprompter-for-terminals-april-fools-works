# Teleprompter for Terminals
Ever thought an Electron based teleprompting software consumes way too many resources for your needs? SSH into Teleprompter for Terminals by Imaignary Sense, a teleprompting solution with no dependencies on X.

# How to use
1. Load the program from your terminal.
2. Type the text you wish to prompt.
3. Press Ctrl-G to prompt.
4. Use W to decrease the speed and S to increase the speed.

# How to run from Telnet
Install an inetd daemon and telnetd, put this in `/etc/inetd.conf` and restart inetd.
    telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd -L /path/to/teleprompter-for-terminals.py

# Dependencies
Teleprompter for Terminals by Imaginary Sense is written in Python 3 and depends on the curses library.
