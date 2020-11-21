import time
import os
import pty
import tty
import sys
from select import select

STDIN_FILENO = 0
STDOUT_FILENO = 1
CHILD = 0

# Need to remove this later. This is what the instructions should look like.
writing = {"insert":"i", "text":"foooo", "newline":"\n", "text":"bar", "escape":chr(27)}

def ez_encode(to_write):
	"""
	Encodes a `dict` for which every value is a string. The strings
	are encoded per character and the returned `dict` contains lists
	of encoded chars.
	
	to_write (dict): `dict` of strings that will be encoded. The strings
	also already be encoded. In such cases, they will be returned
	as-is.
	
	returns (dict): `dict` that contains the encoded strings as lists
	of encoded chars.
	"""
	to_return = to_write
	for key, values in to_write:
		if type(value) != bytes:
			try:
				chars = list(value)
				to_return[key] = [item.encode() for item in chars]
			except AttributeError:
				raise("Instructions must be of type string.")
		else:
			to_return[key] = [value]
	return to_return
	
def ez_read(fd):
	"""
	Standard read function.
	
	fd(int): File descriptor.
	
	returns(byte string): Up to 1024 bytes that have been read from `fd`.
	"""
    return os.read(fd, 1024)

def ez_spawn(argv, master_read = ez_read, stdin_read = ez_read, instructions):
    """
    To spawn the process. Heavily inspired from Python's `pty`
    module. `ez_spawn()` should only be used once per file that
    needs to be edited. This function can write a whole text file
    following the instructions dictionary and executing those
    instructions using `ez_copy()`.
    
    argv (tuple): First element should be the program to run.
    The other elements are the arguments passed to the program.
    master_read (function): The function that will be used to read
    info from the master's file descriptor.
    stdin_read (function): The function that will be used to read
    from STDIN (if the user wants to write to the program).
    instructions (dict): Contains the insctuctions that will be
    passed to VI and the text that should be written. The options
    available will soon be documented.
    
    returns (tuple): A tuple that contains the process id and exit
    status.
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
    # This is where the fun begins.
    try:
		for key, values in instructions:
		# For now my program isn't being too wise about what to
		# do depending on the type of instructions.
        	ez_copy(master_fd, values, master_read, stdin_read)
    except OSError:
        if restore:
            # Discard queued data and change mode to original.
            tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)
    os.close(master_fd)
    # wait for completion and return exit status
    return os.waitpid(pid, 0)[1]

def ez_copy(master_fd, to_write, master_read = _read, stdin_read = _read):
    fds = [master_fd, STDIN_FILENO]
    to_write = list(to_write)
    for i in range(len(to_write)):
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