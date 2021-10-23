"""
``tools.py`` contains functions used in the funcmodule to interact with
the ``vi`` editor. Most functions can be mapped to existing ``vi``
commands.

This module is also where the API is documented. Each funcion's docstring
contains documentation on how to use the function with the API and with
the command line interface.
"""
from typing import List, Dict, Callable, Any

ESCAPE: str = chr(27)

#######################################################################
#                       Character Encoding                            #
#######################################################################


def ez_encode_str(to_encode: str) -> list:
    """Encodes a `str` per character and puts them into a list.

    :type to_encode: str
    :param to_encode: The string that has to be encoded.

    :rtype: list
    :return: A list of encoded chars. Encodes in UTF-8
    """
    to_return: List[bytes] = []
    for char in list(to_encode):
        if not isinstance(char, bytes):
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
def write_chars(to_write: str) -> list:
    """To type ``to_write`` to the file.

    ``write_chars`` will type the passed string after the cursor position.
    From Vi’s command mode, it types ``a`` to insert after and then types the
    string.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_chars: "snek"

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_chars("snek")

    :type to_write: str
    :param to_write: The characters to write.

    :rtype: str
    :return: A string that corresponds to the keys that would be
    pressed to insert text after the current cursor position.
    """

    to_write = "a" + to_write + ESCAPE

    return to_write


def write_line(to_write: str) -> str:
    """To type `to_write` and create a new line.

    Starts typing after the current cursor position by pressing
    ``a`` from the command mode. ``to_write`` is then typed and
    a new line is created.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_line: "Python is fun."

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_line("Python is fun.")

    :type to_write: str
    :param to_write: The characters to write.

    :rtype: str
    :return: A string that contains the keystrokes that would be used
    to write a whole line in ``Vi``.
    """

    to_write = "a" + to_write + "\n" + ESCAPE

    return to_write


def new_line(amount=1):
    """Creates an ``amount`` of new lines.

    ``new_line`` inserts a certain number of new lines to the file.
    From Vi’s command mode, ``ezvi`` first presses ``o``. This ensures
    that the current line won’t be split even if the cursor is not
    at the end of the line.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - new_line: 3


    `Using the API:`

    .. code-block:: python

      ezvi.tools.new_line(3)

    :type amount: int
    :param amount: The number of new lines to create.

    :rtype: str
    :return: A string that contains the characters that would be used
    to create a certain amount of new lines in ``Vi``.
    """
    # TODO: use ``isinstance``
    if type(amount) != int:
        try:
            amount = int(amount)
        except TypeError:
            amount = 1

    to_write = "o" + "\n" * (amount - 1) + ESCAPE

    return to_write


def new_line_over():
    """Creates a new line over the cursor.

    The cursor is also moved to the beginning of the new line. It is
    not possible to create more than one new line over the cursor
    at a time for now.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - new_line_over:


    `Using the API:`

    .. code-block:: python

      ezvi.tools.new_line_over()

    :rtype: str
    :return: Characters that would be used in ``Vi`` to add a new line
    over the cursor.
    """

    to_write = "O" + ESCAPE

    return to_write


def write_after_word(to_write):
    """To write ``to_write`` after the current word.

    This function uses ``e`` from the command mode to go to the end
    of the word. ``to_write`` is then written after the end of the
    word using the ``a`` command. **This function does not add a
    space to the beginning of ``to_write``.**

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_after_word: " General Kenobi."

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_after_word(" General Kenobi.")

    :type to_write: str
    :param to_write: What to write after the word.

    :rtype: str
    :return: Characters that would be used to type contents after the
    current word.
    """

    prepend = "e" + "a"
    append = ESCAPE
    to_write = prepend + to_write + append

    return to_write


def write_after_line(to_write):
    """To write ``to_write`` after the current line.

    This function uses ``$`` from the command mode to go to the
    end of the line. ``to_write`` is then written after the cursor
    position using the ``a`` command. **This function does not add a
    space to the beginning of ``to_write``.**

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_after_line: " General Kenobi."

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_after_line(" General Kenobi.")

    :type to_write: str
    :param to_write: What to write after the line.

    :rtype: str
    :return: Characters that would be used to append content to a line.
    """

    prepend = "$" + "a"
    append = ESCAPE
    to_write = prepend + to_write + append

    return to_write


def write_after_char(to_write):
    """To write ``to_write`` after the cursor's position (current char).

    ``to_write`` is written after the cursor
    position using the ``a`` command.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_after_char: "Greetings!"

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_after_char("Greetings!")

    :type to_write: str
    :param to_write: What to write after the cursor.

    :rtype: str
    :return: Characters that would be used to add contents after the 
    current cursor position.
    """

    prepend = "a"
    append = ESCAPE
    to_write = prepend + to_write + append

    return to_write


def write_before_word(to_write):
    """To write ``to_write`` before the current word.

    ``write_before_word`` uses ``b`` from the command mode to move
    the cursor to the beginning of the current word. ``to_write`` is
    then written before the cursor's position using the ``i``
    command.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_before_word: "Hello there."

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_before_word("Hello there.")

    :type to_write: str
    :param to_write: What to write before the current word.

    :rtype: str
    :return: Keystrokes that can be used to prepend a word with new contents.
    """

    prepend = "b" + "i"  # TODO: Replace "b" by something that works.
    append = ESCAPE
    to_write = prepend + to_write + append

    return to_write


def write_before_line(to_write):
    """To write ``to_write`` at the beginning of the line.

    ``write_before_line`` uses ``0`` from the command mode to move
    the cursor to the beginning of the current line. ``to_write`` is
    then written before the cursor's position using the ``i``
    command.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_before_line: "Hello there."

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_before_line("Hello there.")

    :type to_write: str
    :param to_write: What to write before the current line.

    :rtype: str
    :return: Characters that can be used to prepend content to a line.
    """

    prepend = "0" + "i"
    append = ESCAPE
    to_write = prepend + to_write + append

    return to_write


def write_before_char(to_write):
    """To write ``to_write`` at the beginning of the line.

    ``write_before_line`` uses ``0`` from the command mode to move
    the cursor to the beginning of the current line. ``to_write`` is
    then written before the cursor's position using the ``i``
    command.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_before_line: "Hello there."

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_before_line("Hello there.")

    :type to_write: str
    :param to_write: What to write before the current line.

    :rtype: str
    :return: Keystrokes that can be used to add content before the
    current cursor position.
    """

    prepend = "i"
    append = ESCAPE
    to_write = prepend + to_write + append

    return to_write


# Movement


def goto_line(line_num):
    """To go to a certain line.

    This function uses the ``G`` command to move the cursor to
    the beginning of a certain line.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - goto_line: 5

    `Using the API:`

    .. code-block:: python

      ezvi.tools.goto_line(5)

    :type line_num: int
    :param line_num: The number of the line to move the cursor to.

    :rtype: str
    :return: A line number appended with ``G``.
    """

    to_write = str(line_num) + "G"

    return to_write


def goto_column(column_num):
    """To go to a certain column.

    This function uses the ``l`` command to move the cursor to
    a certain column on the **current line**.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - goto_column: 5

    `Using the API:`

    .. code-block:: python

      ezvi.tools.goto_column(5)

    :type column_num: int
    :param column_num: The number of the column to move the cursor to.

    :rtype: str
    :return: ``0`` plus a column position appended with ``l``.
    """

    # This would be much cleaner if I could get the cursor's position.
    to_write = "0" + str(column_num - 1) + "l"

    return to_write


# Replace functions


def replace(start, end, new):
    """Replaces text on the current line.

    This function replaces from the column number ``start`` to the
    column number ``end`` with the ``new`` text. ``replace`` moves
    the cursor to the starting position and then uses the change
    command (``c``) to replace the text.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - replace: 0, 4, "Snek"

    `Using the API:`

    .. code-block:: python

      ezvi.tools.replace(0, 4, "Snek")

    :type start: int
    :param start: The number of the column to start replacing (inclusively).

    :type end: int
    :param end: The number of the column to stop replacing (exlusively).

    :type new: str
    :param new: The new text to type.

    :rtype: str
    :return: Keystrokes that can be used to replace text from start to end.
    """

    movement = goto_column(start)
    replace = "c" + str(end - start)
    to_write = movement + replace + new + ESCAPE

    return to_write


def find_replace(old, new):
    """To find `old` on the current line and replaces it with `new`."""
    raise NotImplementedError
    pass


def replace_line(new):
    """Replaces text on the current line.

    ``replace`` moves the cursor to the beginning of the line
    using ``0`` from the command mode and then uses command
    (``c$``) to replace the whole line.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - replace_line: "Hello there."

    `Using the API:`

    .. code-block:: python

      ezvi.tools.replace_line("General Kenobi.")

    :type new: str
    :param new: The new text to replace the current line.

    :rtype: str
    :return: Characters that can be typeed to change the current line
    with new content.
    """

    movement = "0"
    replace = "c" + "$"
    to_write = movement + replace + new + ESCAPE

    return to_write


# Vi commands


def write_file(filename):
    """Write the current buffer.

    From the command mode, ``write_file`` uses Vi's ``:w`` command to
    write the current buffer.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - write_file: "message.txt"

    `Using the API:`

    .. code-block:: python

      ezvi.tools.write_file("message.txt")

    :type filename: str
    :param filename: The path towards where to save the current buffer.

    :rtype: str
    :return: ``:w`` plus a file name and a newline.
    """

    to_write = ":w " + filename + "\n"

    return to_write


def quit_editor():
    """To quit the editor.

    From the command mode, ``quit_editor`` uses Vi's ``:q`` command to
    quit the editor. Since Vi makes sure that the current buffer
    is saved before quitting, ``force_quit_editor`` should be used instead
    if the buffer must not be saved.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - quit_editor:

    `Using the API:`

    .. code-block:: python

      ezvi.tools.quit_editor()

    :rtype: str
    :return: ``:q`` and a newline.
    """

    to_write = ":q" + "\n"

    return to_write


def force_quit_editor():
    """To force quit the editor.

    From the command mode, ``force_quit_editor`` uses Vi's ``:q!`` command to
    force quit the editor. All unsaved progress will be lost.

    Usage:

    `In a config file:`

    .. code-block:: yaml

      - force_quit_editor:

    `Using the API:`

    .. code-block:: python

      ezvi.tools.force_quit_editor()

    :rtype: str
    :return: ``:q!`` and a newline character.
    """

    to_write = ":q!" + "\n"

    return to_write


# TODO: Replace ``Any`` with something more accurate.
all_tools: Dict[Any, Callable] = {
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
