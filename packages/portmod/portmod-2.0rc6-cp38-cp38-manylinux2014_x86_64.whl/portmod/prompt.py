# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import re
import sys
from typing import List, Optional, Tuple

from portmod.colour import bright, lgreen, lred

from .l10n import l10n


def strtobool(value: str) -> bool:
    """
    Returns true if the value is a string with contents representing true
    and false if the value is a string with contents representing false

    True options include: yes, y, true, t, 1
    False options include: no, n, false, f, 1

    This function is localized.
    """
    _true = {
        l10n("yes-short"),
        l10n("yes").lower(),
        l10n("true").lower(),
        l10n("true-short"),
        "1",
    }
    _false = {
        l10n("no-short"),
        l10n("no").lower(),
        l10n("false").lower(),
        l10n("false-short"),
        "0",
    }

    if value.lower() in _true:
        return True
    if value.lower() in _false:
        return False
    raise ValueError(f"Invalid boolean value {value}")


def prompt_bool(question):
    sys.stdout.write(
        "{} [{}/{}]: ".format(
            question, bright(lgreen(l10n("yes"))), bright(lred(l10n("no")))
        )
    )
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            sys.stdout.write(
                l10n(
                    "prompt-invalid-response",
                    yes=bright(lgreen(l10n("yes"))),
                    no=bright(lred(l10n("no"))),
                )
            )


def prompt_options(question: str, options: List[Tuple[str, str]]) -> str:
    print(question)
    for option, desc in options:
        print(option + ":", desc)
    sys.stdout.write("[{}]: ".format("/".join([option for option, _ in options])))
    option_set = {option for option, _ in options}
    while True:
        result = input().strip()
        if result in option_set:
            return result
        else:
            sys.stdout.write(
                l10n(
                    "prompt-invalid-response-multiple",
                    options="/".join([option for option, _ in options]),
                )
            )


def parse_num_list(string):
    if string == "":
        return list()

    m = re.match(r"(\d+)(?:-(\d+))?$", string)
    if not m:
        raise TypeError(l10n("prompt-invalid-range"))
    start = m.group(1)
    end = m.group(2) or start
    return list(range(int(start, 10), int(end, 10) + 1))


def prompt_num_multi(question, max_val):
    print("{}: ".format(question))
    while True:
        try:
            result = [y for x in input().split(",") for y in parse_num_list(x)]
            if next(filter(lambda x: x > max_val or x < 0, result), None):
                print(l10n("prompt-range-too-large-number", max=max_val))
            else:
                return result
        except ValueError:
            print(l10n("prompt-invalid-range-multi", max=max_val))


def prompt_num(question, max_val, cancel=False):
    print("{}: ".format(question))
    while True:
        try:
            result = int(input())
            if result > max_val or result < 0:
                if result == -1 and cancel:
                    return result

                print(l10n("prompt-range-too-large-number", max=max_val))
            else:
                return result
        except ValueError:
            print(l10n("prompt-invalid-range", max=max_val))


def prompt_str(question: str, default: Optional[str] = None) -> Optional[str]:
    """
    Prompts for string input

    If the user enters an EOF, returns None
    """
    if default:
        print(f'{question} (default "{default}"): ', end="")
    else:
        print(f"{question}: ", end="")
    while True:
        try:
            result = input()
        except EOFError:
            return None

        if result:
            return result

        return default
