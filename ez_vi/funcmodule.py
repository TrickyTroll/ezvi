import os
import pty
import time
import tty
from select import select

STDIN_FILENO = 0
STDOUT_FILENO = 1
CHILD = 0


#######################################################################
#                       Character Encoding                            #
#######################################################################

def ez_encode_str(to_encode) -> list:
    """ Encodes a `str` per character and puts them into a list.

    :type to_encode: str
    :param to_encode: The string that has to be encoded.

    :rtype: list
    :return: A list of encoded chars. Encodes in UTF-8
    """
    to_return = []
    for char in list(to_encode):
        if type(char) != bytes:
            try:
                to_return.append(char.encode("utf-8"))
            except AttributeError:
                raise Exception("`to_encode` must be of type `str`")
        else:
            # This is a problem as they could be encoded differently.
            to_return.append(char)
    return to_return


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
    """
    Writes every char in `to_write` to `master_fd`.

    master_fd (int): Master's file descriptor.
    to_write (list of bytes): List of encoded chars that will be
    written to `master_fd`.
    master_read (function): The function that will be used to read
    info from the master's file descriptor.
    stdin_read (function): The function that will be used to read
    from STDIN (if the user wants to write to the program).

    returns written(list of bytes): A list of all chars that
    have been written.
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
#                            Vi tools                                 #
#######################################################################

# Writing

def write_chars(to_write):
    """To type `to_write` to the file."""

    to_write = "i" + to_write + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


def newline():
    """Types a new line."""

    to_write = "\n"
    to_write = ez_encode_str(to_write)

    return to_write


def write_after_word(to_write):
    """To type `to_write` after `thing`. `thing` could be line, word or char.
    """
    prepend = "e" + "a"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_after_line(to_write):
    """To type `to_write` at the end of the line."""

    prepend = "$" + "a"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_after_char(to_write):
    """To type `to_write` after the cursor's position."""

    prepend = "a"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_before_word(to_write):
    """To type `to_write` before `thing`. `thing` could be line, word or char."""

    prepend = "b" + "a"  # TODO: Replace "b" by something that works.
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_before_line(to_write):
    """To type `to_write` at the end of the line."""

    prepend = "0" + "i"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_before_char(to_write):
    """To type `to_write` before the cursor's position."""

    prepend = "i"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


# Movement

def goto_line(line_num):
    """To move the cursor to `line_num`."""

    to_write = str(line_num) + "G"
    to_write = ez_encode_str(to_write)

    return to_write


def goto_column(column_num):
    """To move the cursor to `column_num` on the current line."""

    # This would be much cleaner if I could get the cursor's position.
    to_write = "0" + str(column_num - 1) + "l"
    to_write = ez_encode_str(to_write)

    return to_write


# Replace functions

def replace(start, end, new):
    """To replace from `start` to `end` on the current line."""

    movement = goto_column(start)
    replace = "c" + str(end - start)
    to_write = movement + replace + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


def find_replace(old, new):
    """To find `old` on the current line and replaces it with `new`."""

    pass


def replace_line(new):
    """To replace the whole line with `new`."""

    movement = "0"
    replace = "c" + "$"
    to_write = movement + replace + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


# Vi commands

def write_file(filename):
    """To write the contents to `filename`."""

    to_write = ":w " + filename
    to_write = ez_encode_str(to_write)

    return to_write


def quit_editor():
    """To quit the editor."""

    to_write = ":q"
    to_write = ez_encode_str(to_write)

    return to_write

#######################################################################
#                      Searching/editing tools                        #
#######################################################################
