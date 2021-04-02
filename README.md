# Teleprompter for Terminals
Ever thought an Electron based teleprompting software consumes way too many resources for your needs? SSH into Teleprompter for Terminals by Imaginary Sense, a teleprompting solution with no dependencies on X.

# How to use
1. Load the program from your terminal.
2. Type the text you wish to prompt.
3. Press Ctrl-G to prompt.
4. Use W to decrease the speed and S to increase the speed.

# How to run from Telnet
Install an xinetd daemon and telnetd, put this in `/etc/xinetd.d/telnet` and restart xinetd.
```
# default: on
# description: The telnet server serves telnet sessions; it uses
# unencrypted username/password pairs for authentication.
service telnet
{
disable = no
flags = REUSE
socket_type = stream
wait = no
user = userwithnoprivileges
server = /usr/sbin/in.telnetd
server_args = -h -L /path/to/teleprompter-for-terminals.py
log_on_failure += USERID
cps = 10 30
instances = 200
}
```
# Dependencies
Teleprompter for Terminals by Imaginary Sense is written in Python 3 and depends on the curses library.
