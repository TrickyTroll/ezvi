#!/usr/bin/env python3

import time
import os
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

def ez_copy(master_fd, master_read = _read, stdin_read = _read):
    fds = [master_fd, STDIN_FILENO]
    return None
