#######################################################################
#                       Character Encoding                            #
#######################################################################

def ez_encode_str(to_encode: str) -> list:
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
#                            Vi tools                                 #
#######################################################################


# Writing

def write_chars(to_write):
    """To type `to_write` to the file.

    :rtype: list
    """

    to_write = "a" + to_write + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


def write_line(to_write):
    """To type `to_write` create a new line

    :rtype: list
    """

    to_write = "a" + to_write + "\n" + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


def new_line(amount):
    """Types a new line.
    This also moves the cursor to the beginning of the new line.

    :rtype: list
    """
    if type(amount) != int:
        amount = int(amount)

    to_write = "o" + "\n" * (amount-1) + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


def new_line_over():
    """To create a new line over the cursor
    This also moves the cursor to the beginning of the new line.

    :rtype: list
    """

    to_write = "O" + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


def write_after_word(to_write):
    """To type `to_write` after `thing`. `thing` could be line, word or char.

    :rtype: list
    """
    prepend = "e" + "a"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_after_line(to_write):
    """To type `to_write` at the end of the line.

    :rtype: list
    """

    prepend = "$" + "a"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_after_char(to_write):
    """To type `to_write` after the cursor's position.

    :rtype: list
    """

    prepend = "a"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_before_word(to_write):
    """To type `to_write` before `thing`. `thing` could be line, word or char.

    :rtype: list
    """

    prepend = "b" + "a"  # TODO: Replace "b" by something that works.
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_before_line(to_write):
    """To type `to_write` at the end of the line.

    :rtype: list
    """

    prepend = "0" + "i"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


def write_before_char(to_write):
    """To type `to_write` before the cursor's position.

    :rtype: list
    """

    prepend = "i"
    append = chr(27)
    to_write = prepend + to_write + append
    to_write = ez_encode_str(to_write)

    return to_write


# Movement

def goto_line(line_num):
    """To move the cursor to `line_num`.

    :rtype: list
    """

    to_write = str(line_num) + "G"
    to_write = ez_encode_str(to_write)

    return to_write


def goto_column(column_num):
    """To move the cursor to `column_num` on the current line.

    :rtype: list
    """

    # This would be much cleaner if I could get the cursor's position.
    to_write = "0" + str(column_num - 1) + "l"
    to_write = ez_encode_str(to_write)

    return to_write


# Replace functions

def replace(start, end, new):
    """To replace from `start` to `end` on the current line.

    :rtype: list
    """

    movement = goto_column(start)
    replace = "c" + str(end - start)
    to_write = movement + replace + new + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


def find_replace(old, new):
    """To find `old` on the current line and replaces it with `new`."""

    pass


def replace_line(new):
    """To replace the whole line with `new`.

    :rtype: list
    """

    movement = "0"
    replace = "c" + "$"
    to_write = movement + replace + new + chr(27)
    to_write = ez_encode_str(to_write)

    return to_write


# Vi commands

def write_file(filename):
    """To write the contents to `filename`.

    :rtype: list
    """

    to_write = ":w " + filename + "\n"
    to_write = ez_encode_str(to_write)

    return to_write


def quit_editor():
    """To quit the editor.

    :rtype: list
    """

    to_write = ":q" + "\n"
    to_write = ez_encode_str(to_write)

    return to_write


def force_quit_editor():
    """To force quit the editor.

    :rtype: list
    """

    to_write = ":q!" + "\n"
    to_write = ez_encode_str(to_write)

    return to_write


all_tools = {
    write_chars.__name__: write_chars,
    write_line.__name__: write_line,
    new_line.__name__: new_line,
    new_line_over.__name__: new_line_over,
    write_after_word.__name__: write_after_word,
    write_after_line.__name__: write_after_line,
    write_after_char.__name__: write_after_char,
    write_before_word.__name__: write_before_word,
    write_before_line.__name__: write_before_line,
    write_before_char.__name__: write_before_char,
    goto_line.__name__: goto_line,
    goto_column.__name__: goto_column,
    replace.__name__: replace,
    replace_line.__name__: replace_line,
    write_file.__name__: write_file,
    quit_editor.__name__: quit_editor,
    force_quit_editor.__name__: force_quit_editor,
}
