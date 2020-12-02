import time
import os
import pty
import tty
import sys
from select import select

STDIN_FILENO = 0
STDOUT_FILENO = 1
CHILD = 0

#######################################################################
#                       Character Encoding                            #
#######################################################################

def ez_encode(tw):
    """
    Encodes a `dict` for which every value is a string. The strings
    are encoded per character and the returned `dict` contains lists
    of encoded chars.
    
    tw (dict): `dict` of strings that will be encoded. The strings
    also already be encoded. In such cases, they will be returned
    as-is.
    
    returns (dict): `dict` that contains the encoded strings as lists
    of encoded chars.
    """
    to_return = tw.copy()
    for key, value in to_return.items():
        if type(value) != bytes:
            try:
                chars = list(value)
                to_return[key] = [item.encode('utf-8') for item in chars]
            except AttributeError:
                raise("Instructions must be of type string.")
        else:
            to_return[key] = [value]
    return to_return

def ez_encode_str(to_encode):
    """
    Similar to `ez_encode`, except it encodes a `str` instead of a `dict`.
    It encodes per character and puts them into a list.

    to_encode (str): The string that has to be encoded.

    returns (list): A `list` of encoded chars. Encodes in UTF-*8.
    """
    to_return = []
    for char in list(to_encode):
        if type(char) != bytes:
            try:
                to_return.append(char.encode("utf-8"))
            except AttributeError:
                raise("`to_encode` must be of type `str`")
        else:
            # This is a problem as they could be encoded differently.
            to_return.append(char)


#######################################################################
#                         Read function                               #
#######################################################################

def ez_read(fd):
    """
    Standard read function.
    
    fd(int): File descriptor.
    
    returns(byte string): Up to 1024 bytes that have been read from `fd`.
    """
    return os.read(fd, 1024)

#######################################################################
#                Spawning an writing to process                       #
#######################################################################
    
def ez_spawn(argv, instructions, master_read = ez_read, stdin_read = ez_read):
    """
    To spawn the process. Heavily inspired from Python's `pty`
    module. `ez_spawn()` should only be used once per file that
    needs to be edited. This function can write a whole text file
    following the instructions dictionary and executing those
    instructions using `ez_copy()`.
    
    argv (tuple): First element should be the program to run.
    The other elements are the arguments passed to the program.
    instructions (dict): Contains the insctuctions that will be
    passed to VI and the text that should be written. The options
    available will soon be documented.
    master_read (function): The function that will be used to read
    info from the master's file descriptor.
    stdin_read (function): The function that will be used to read
    from STDIN (if the user wants to write to the program).
    
    
    returns (tuple): A tuple that contains the process id and exit
    status.
    """
    all_written = [] # Useful for debugging.
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
        tty.setraw(STDIN_FILENO) # disable line buffering
        # interrupt signals are no longer interpreted
        restore = 1
    except tty.error:
        # Did not work, no need to restore.
        restore = 0
    # This is where the fun begins.
    # Encoding the instructions.
    encoded = ez_encode(instructions)
    try:
        for key, value in encoded.items():
        # For now my program isn't being too wise about what to
        # do depending on the type of instructions.
            all_written.append(ez_write(master_fd, 
                                        value, 
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

def ez_write(master_fd, to_write, master_read = ez_read, stdin_read = ez_read):
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
                data = to_write.pop(0) # The item should already be encoded.
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
    """
    To type `to_write` to the file.
    """
    to_write = ez_encode_str(to_write)

    return(to_write)

def write_after(to_write, type):
    """
    Writes `to_write` after `type`. `type` could be line, word or char.
    """

    pass

def write_before(to_write, type):
    """
    Writes `to_write` before `type`. `type` could be line, word or char.
    """

    pass

# Movement

def goto_line(line_num):
    """
    Moves the cursor to `line_num`.
    """

    pass

def goto_column(column_num):
    """
    Moves the cursor to `column_num` on the current line.
    """

    pass

# Replace functions

def replace(start, end, new):
    """
    Replaces from `start` to `end` on the current line.
    """

    pass

def find_replace(old, new):
    """
    Finds `old` on the current line and replaces it with `new`.
    """

    pass

def replace_line(new):
    """
    Replaces the whole line with `new`.
    """

    pass
