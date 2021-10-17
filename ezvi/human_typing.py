# -*- coding: utf-8 -*-
"""Functions to help with fake typing"""
import pexpect
import time
import random
from typing import List, Dict, Union

LEFT_HAND: List[str] = [
    "as",
    "sa",
    "er",
    "re",
    "sd",
    "ds",
    "ec",
    "ce",
    "ew",
    "we",
    "wa",
    "aw",
    "cr",
    "sc",
    "cs",
]
RIGHT_HAND: List[str] = [
    "lk",
    "lo",
    "ol",
    "op",
    "po",
    "io",
    "oi",
    "no",
    "on",
    "in",
    "ni",
]
HAND_ALTERNATION: List[str] = [
    "al",
    "la",
    "ak",
    "ka",
    "am",
    "ma",
    "an",
    "na",
    "ai",
    "ia",
    "so",
    "os",
    "sp",
    "ps",
    "en",
    "ne",
    "em",
    "me",
    "el",
    "le",
    "ep",
    "pe",
]

PLAUSIBLE_TYPOS: Dict[str, List[str]] = {  # In keyboard order.
    "q": ["w", "a"],
    "w": ["q", "e", "s"],
    "e": ["w", "r", "d"],
    "r": ["e", "t", "f"],
    "t": ["r", "y", "g"],
    "y": ["t", "u", "h"],
    "u": ["y", "i", "j"],
    "i": ["u", "o", "k"],
    "o": ["i", "p", "l"],
    "p": ["o", "[", ";"],
    "a": ["s", "q"],
    "s": ["a", "w", "d"],
    "d": ["s", "f", "e"],
    "f": ["d", "d", "r"],
    "g": ["f", "h", "t"],
    "h": ["g", "j", "y"],
    "j": ["h", "k", "i"],
    "k": ["j", "l", "o"],
    "l": ["k", "o", "p", ";"],
    "z": ["a", "x", "s"],
    "x": ["z", "c", "s"],
    "c": ["x", "v", "d"],
    "v": ["c", "b", "f"],
    "b": ["v", "n", "g"],
    "n": ["b", "m", "h"],
    "m": ["n", "j", "k", ","],
}


def is_typo() -> bool:
    """
    Determines wether or not a combination of key presses should
    generate a typo. For now, we assume that every key press has
    an equal chance of being a typo.

    According to some papers[0], there is between 0.62% and 3.2%
    chances that a keypress will be a typo. For our purposes, we
    will assume that this percentage is between 1 and 3 percent.

    [0]: Refer the documentation.

    Returns:
        bool: Whether or not there will be a typo.

    """
    error_percent = random.randint(1, 4)  # 3.2 rounded up
    # Randint includes the upper bound.
    return random.randint(1, 100) <= error_percent


def is_pause() -> bool:
    """Checks if the computer should pause typing for a while.

    Similar to `is_typo()`, but is not based on any research.
    The chances of taking a small pause has been determined
    by testing different combinations of `is_pause()` and
    `pause_time()`.

    Returns:
        bool: Whether or not the program should stop typing.
    """
    pause_percent: int = random.randint(20, 30)
    return random.randint(1, 100) <= pause_percent


def pause_time() -> float:
    """Returns for how long the program should pause when typing.

    The short pause time is based on what felt more natural when
    testing.

    Returns:
        float: How long the pause shoud last **in seconds**.
    """
    # Between .5 to 1 seconds
    pause_ms: int = random.randint(500, 1000)
    return pause_ms / 1000  # returned pause is in seconds.


def pick_typo(next_letter: str) -> Union[str, None]:
    """Picks a typo according to the next letter to type.

    This function uses `is_typo()` to determine wether or
    not there will be a typo.

    Plausible typos are defined in the `PLAUSIBLE_TYPOS`
    global variable. If `next_letter` is not a key in the
    `PLAUSIBLE_TYPOS` dict, the typo is set to none.

    Args:
        next_letter (str): The next letter that should be typed.

    Returns:
        str/None: The typo or `None` if there is no typo.
    """

    typo: Union[str, None] = None

    if is_typo():

        try:
            plausible_for_letter = PLAUSIBLE_TYPOS[next_letter.lower()]
            # Pick a random typo in the list associated with the
            # key.
            typo = random.choice(plausible_for_letter)

        except KeyError:  # No typo defined for `next_letter`
            typo = None

    else:

        typo = None

    return typo


def get_delay(previous_letter: str, next_letter: str) -> float:
    """Function to get the delay before the next letter is typed.

    This function uses the fact that letters typed by two different
    hands will usually be typed 30 to 60ms faster than two letters
    pressed by the same hand.

    There is also an average delay of betweem 120 and 170ms between
    two keystrokes.

    Args:
        previous_letter (str): The previously typed letter.
        next_letter (str): The next letter to type.

    Returns:
        float: The time **in seconds** before the next keystroke.
            This value is calculated using the previous and next
            letter.
    """
    avg_delay = random.randint(120, 170) / 1000  # in seconds
    if (previous_letter + next_letter).lower() in HAND_ALTERNATION:
        # Two letters typed by different hands are 30-60ms faster.
        faster_by = random.randint(30, 60) / 1000
        avg_delay -= faster_by
    return avg_delay


def type_typo(child: pexpect.pty_spawn.spawn, next_letter: str, typo: str) -> None:
    """Sends a typo to the child process and corrects it afterwards.

    Delays are computed between each keystroke, including when the computer
    presses backspace. For now, only one typo can be introduced at a time.
    More than one would be distracting for the user.

    Args:
        child (pexpect.pty_spawn.spawn): The child process where the typo
            will be sent.
        next_letter (str): The next letter that would be typed if there
            was no typo. This is the letter that will be typed in the
            end.
        typo (str): The letter that will be typed instead of `next_letter`
            the first time.
    """
    child.send(typo)
    time.sleep(get_delay(typo, "backspace"))
    child.send("\b")
    time.sleep(get_delay(typo, next_letter))
    child.send(next_letter)


def type_letters(child: pexpect.pty_spawn.spawn, previous: str, next: str) -> None:
    """Sends the next letter to the process.

    This function also calculates the delay using the previous letter
    and the chances of typing a typo.

    If there is a typo, `type_typo()` is called and sends the wrong letter
    to the process before correcting it.

    If the next character to type is a space, there are chances that the
    program will take a pause. Indeed, people are more likely to hesitate
    between words than while typing a word.

    Args:
        child (pexpect.pty_spawn.spawn): The child process to which the next
            letter will be sent.
        previous (str): The last letter that has been sent to the process.
        next (str): The next letter to send to the process.
    """
    typo: Union[str, None] = pick_typo(next)

    if next == " ":
        # If the next char to type is a space, compute chances of taking
        # a pause.
        if is_pause():
            time.sleep(pause_time())
    else:
        delay: float = get_delay(previous, next)
        time.sleep(delay)
    if typo:
        type_typo(child, next, typo)
    else:
        child.send(next)


def type_sentence(child: pexpect.pty_spawn.spawn, sentence: str) -> None:
    """Types a full sentence to the child program.

    It uses delays and typos to make typing human like.

    This function ends by sending a newline to the child process.

    Args:
        child (pexpect.pty_spawn.spawn): The child process to which
            the sentence will be sent.
        sentence (str): What will be typed and sent to the process.

    Raises:
        TypeError: Raises a `TypeError` if the `sentence` argument
        is not of type `str`. This makes sure that once loaded, the
        yaml configuration file did not contain other types.
    """
    if not isinstance(sentence, str):
        raise TypeError(f"Cannot type a {type(sentence)}.")

    letters: List[str] = list(sentence)

    if not letters[-1] == "\n":
        letters.append("\n")

    for index, letter in enumerate(letters):
        if index > 0:
            type_letters(child, letters[index - 1], letter)
        else:
            # Setting `letter` as previous letter when there
            # is none.
            type_letters(child, letter, letter)
