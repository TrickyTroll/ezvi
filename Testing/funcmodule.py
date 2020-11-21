import time
import os
import pty
import tty
import sys
from select import select

STDIN_FILENO = 0
STDOUT_FILENO = 1
CHILD = 0

# Need to remove this later
writing = ["i", "foooo", "\n", "bar", chr(27)]

def encode(to_write):
	"""
	Encodes a list of strings.
	
	to_write(list): List of strings that will be encoded. The strings
	also already be encoded. In such cases, they will be returned
	as-is.
	
	returns(list): List of encoded strings.
	"""
	to_return = []
	for item in to_write:
		if type(item) != bytes:
			to_return.extend(item.encode())
		else:
			to_return.extend(item)
	return to_return
	
def _read(fd):
    return os.read(fd, 1024)

def ez_spawn(argv, master_read = _read, stdin_read = _read):
    """
    To spawn the process.
    """
    if type(argv) == str:
        argv = (argv,)
    pid, master_fd = pty.fork()
    if pid == CHILD:
        # Fork worked, run the program
        os.execlp(argv[0], *argv)
    try:
        mode = tty.tcgetattr(STDIN_FILENO)
        tty.setraw(STDIN_FILENO) # disable line buffering
        # interrupt signals are no longer interpreted
        restore = 1
    except tty.error:
        # Did not work, no need to restore.
        restore = 0
    try:
        ez_copy(master_fd, "toto", master_read, stdin_read)
    except OSError:
        if restore:
            # Discard queued data and change mode to original
            tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)
    os.close(master_fd)
    # wait for completion and return exit status
    return os.waitpid(pid, 0)[1]

def ez_copy(master_fd, to_write, master_read = _read, stdin_read = _read):
    fds = [master_fd, STDIN_FILENO]
    to_write = list(to_write)
    to_write.insert(0, "i")
    index = 0
    max = len(to_write)
    while True:
        if index > max:
            break
        for char in to_write:
            rfds, wfds, xfds = select([fds[0]], [fds[1]], [])
            if master_fd in rfds:
                # This is required to see the program running
                data = master_read(master_fd)
                if not data:
                    fds.remove(master_fd)
                else:
                    # Printing the program
                    os.write(STDOUT_FILENO, data)

            if STDIN_FILENO in wfds:
                data = char.encode()
                time.sleep(.1)
                os.write(master_fd, data)
        index += 1
    return None

ez_spawn("vi")
print("Done")