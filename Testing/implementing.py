#!/usr/bin/env python3

import time
import os
import pty
import tty
import sys
from select import select

STDIN_FILENO = 0
STDOUT_FILENO = 1

CHILD = 0

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
    while True:
        for char in to_write:
            rfds, wfds, xfds = select(fds, [], [])
            if master_fd in rfds:
                # This is required to see the program running
                data = master_read(master_fd)
                if not data:
                    fds.remove(master_fd)
                else:
                    # Printing the program
                    os.write(STDOUT_FILENO, data)

            if STDIN_FILENO in rfds:
                data = char.encode()
                time.sleep(.1)
                os.write(master_fd, data)
#        break
    return None

ez_spawn("vi")
print("Done")
