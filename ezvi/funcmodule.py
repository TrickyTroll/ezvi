import os
import pty
import time
from typing import Dict, Any, Callable
from pathlib import Path
from ezvi import tools
import yaml
import tty
from select import select

STDIN_FILENO = 0
STDOUT_FILENO = 1
CHILD = 0


#######################################################################
#                         Read function                               #
#######################################################################

def ez_read(fd) -> bytes:
    """ Standard read function.

    :type fd: int
    :param fd: File descriptor.

    :rtype: bytes
    :return: Up to 1024 bytes that have been read from `fd`.
    """
    return os.read(fd, 1024)


#######################################################################
#                Spawning an writing to process                       #
#######################################################################

def ez_spawn(argv, instructions, master_read=ez_read, stdin_read=ez_read):
    """ Spawns a process
    To spawn the process. Heavily inspired from Python's `pty`
    module. `ez_spawn()` should only be used once per file that
    needs to be edited. This function can write a whole text file
    following the instructions dictionary and executing those
    instructions using `ez_copy()`.

    :type argv: tuple
    :param argv: First element is the program to run. Other elements
    are the arguments passed to the program.
    :type instructions: list
    :param instructions: Contains all the instructions that will be
    passed to Vi. Its contents should have been created using the
    "Vi tools".
    :type master_read: function
    :param master_read: The function that will be used to read
    info from the master's file descriptor.
    :type stdin_read: function
    :param stdin_read: The function that will be used to read
    info from the master's file descriptor.

    :rtype: int
    :return: Exit status
    """
    all_written = []  # Useful for debugging.
    if type(argv) == str:
        argv = (argv,)
    pid, master_fd = pty.fork()
    if pid == CHILD:
        # Fork worked, run the program
        os.execlp(argv[0], *argv)
    try:
        mode = tty.tcgetattr(STDIN_FILENO)
        # The next line is required to make sure that you can't type over vi
        # either.
        tty.setraw(STDIN_FILENO)  # disable line buffering
        # interrupt signals are no longer interpreted
        restore = 1
    except tty.error:
        # Did not work, no need to restore.
        restore = 0
    # This is where the fun begins.
    # Encoding the instructions.
    try:
        for item in instructions:
            all_written.append(ez_write(master_fd,
                                        item,
                                        master_read,
                                        stdin_read))
    except OSError:
        if restore:
            # Discard queued data and change mode to original.
            tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)
    if restore:
        tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)
    os.close(master_fd)
    # wait for completion and return exit status
    return os.waitpid(pid, 0)[1]


def ez_write(master_fd, to_write, master_read=ez_read, stdin_read=ez_read):
    """Writes every char in `to_write` to `master_fd`.

    :type master_fd: int
    :param master_fd: Master's file descriptor.
    :type to_write: list
    :param to_write: List of encoded chars that will be
    written to `master_fd`.
    :type master_read: function
    :param master_read: The function that will be used to read
    info from the master's file descriptor.
    :type stdin_read: function
    :param stdin_read: The function that will be used to read
    from STDIN (if the user wants to write to the program).

    :rtype: list
    :return: A list of all chars that have been written.
    """
    written = []
    fds = [master_fd, STDIN_FILENO]
    while True:
        rfds, wfds, xfds = select([fds[0]], [fds[1]], [])
        if master_fd in rfds:
            # This is required to see the program running.
            data = master_read(master_fd)
            if not data:
                fds.remove(master_fd)
            else:
                # Printing the program
                os.write(STDOUT_FILENO, data)
        # This should always be true.
        if STDIN_FILENO in wfds:
            try:
                data = to_write.pop(0)  # The item should already be encoded.
            except IndexError:
                data = None
            if not data:
                break
            else:
                # This should be randomized to simulate typing.
                os.write(master_fd, data)
                written.append(data)
                time.sleep(.1)
    return written


#######################################################################
#                            YAML parsing                             #
#######################################################################

def yaml_parser(stream) -> list:
    """Loads a YAML file. 

    :type stream: textIO
    :param stream: A stream of text to be parsed.

    :rtype: list
    :return: The parsed yaml file.
    """

    available = [key for key, value in tools.all_tools.items()]

    parsed = yaml.safe_load(stream)
    for instruction in parsed:
        for key, value in instruction.items():
            # If the function is available, run it with "value"
            # as an argument. This translates the text (values)
            # according to the instructions (values).
            if key in available:
                # Removing None types from dict.
                if instruction[key] is not None:
                    instruction[key] = (tools.all_tools[key](value))
                else:
                    instruction[key] = (tools.all_tools[key]())
            else:
                raise NotImplementedError(key + " does not exist.")

    return parsed


#######################################################################
#                       File comparison                               #
#######################################################################

# To convert an existing text file to some ez-vi commands.

def file_parser(stream, name=""):
    """To parse a pre-typed text file.

    :param stream: The stream of text to parse.
    :type stream: textIO

    :param save: Where the file should be saved.
    :type save: str

    :return: The parsed text.
    :rtype: list
    """

    to_return = []

    file = stream.readlines()
    for line in file:
        to_return.append(tools.write_chars(line))

    if name == "":
        to_return.append(tools.force_quit_editor())
    else:
        if Path(name).is_file():
            raise Exception("{} already exists.".format(name))
        to_return.append(tools.write_file(name))
        to_return.append(tools.quit_editor())

    return to_return

#######################################################################
#                      Searching/editing tools                        #
#######################################################################
