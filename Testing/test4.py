#!/usr/bin/env python3
import pty
import time
import os
import tty
import sys
from select import select

STDIN_FILENO = 0
STDOUT_FILENO = 1

CHILD = 0

def my_copy(master_fd, master_read=pty._read, stdin_read=pty._read):
    """Parent copy loop.
    Copies
            pty master -> standard output   (master_read)
            standard input -> pty master    (stdin_read)"""
    fds = [master_fd, STDIN_FILENO]
    while True:
        rfds, wfds, xfds = select(fds, [], [])
        if master_fd in rfds:
            data = master_read(master_fd)
            if not data:  # Reached EOF.
                fds.remove(master_fd)
            else:
                os.write(STDOUT_FILENO, data)

        if STDIN_FILENO in rfds:
            data = "i".encode()
            time.sleep(1)
            os.write(master_fd, data)
            time.sleep(1)
            data_2 = list("This is a test!")
            for char in data_2:
                os.write(master_fd, char.encode())
            time.sleep(1)
#        if STDIN_FILENO in rfds:
#            data = stdin_read(STDIN_FILENO)
#            if not data:
#                fds.remove(STDIN_FILENO)
#            else:
#                pty._writen(master_fd, data)

def my_copy_2(master_fd, master_read=pty._read, stdin_read=pty._read):
    """Parent copy loop.
    Copies
            pty master -> standard output   (master_read)
            standard input -> pty master    (stdin_read)"""
    fds = [master_fd, STDIN_FILENO]
    my_data = ["i"]
    for char in list("This is a test!"):
        my_data.append(char)

    while True:
        for char in my_data:
            rfds, wfds, xfds = select(fds, [], [])
            if master_fd in rfds:
                data = master_read(master_fd)
                if not data:  # Reached EOF.
                    fds.remove(master_fd)
                else:
                    os.write(STDOUT_FILENO, data)

            if STDIN_FILENO in rfds:
                data = char.encode()
                time.sleep(1)
                os.write(master_fd, data)
                time.sleep(1)

        rfds, wfds, xfds = select(fds, [], [])
        if master_fd in rfds:
            data = master_read(master_fd)
            if not data:  # Reached EOF.
                fds.remove(master_fd)
            else:
                os.write(STDOUT_FILENO, data)

        if STDIN_FILENO in rfds:
            data = stdin_read(STDIN_FILENO)
            if not data:
                fds.remove(STDIN_FILENO)
            else:
                pty._writen(master_fd, data)


def my_spawn(argv, master_read=pty._read, stdin_read=pty._read):
    """Create a spawned process."""
    if type(argv) == type(''):
        argv = (argv,)
   # sys.audit('pty.spawn', argv)
    pid, master_fd = pty.fork()
    if pid == CHILD:
        os.execlp(argv[0], *argv)
    try:
        mode = tty.tcgetattr(STDIN_FILENO)
        tty.setraw(STDIN_FILENO)
        restore = 1
    except tty.error:    # This is the same as termios.error
        restore = 0
    try:
        my_copy_2(master_fd, master_read, stdin_read)
    except OSError:
        if restore:
            tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)

    os.close(master_fd)
    return os.waitpid(pid, 0)[1]

my_spawn("vi")
print("Done")
