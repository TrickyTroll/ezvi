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


def ez_copy(master_fd, master_read = _read, stdin_read = _read):
    fds = [master_fd, STDIN_FILENO]
    return None
