"Base for aleat3 console script."

import argparse
import os
import sys
import warnings
from aleat3 import Aleatoryous, coinToBool, coinToBinary, __version__

__all__ = ["console_main"]

def get_aleat_version():
    return """
%(prog)s {}
Copyright (c) 2017-2021 Diego Ramirez. All rights reserved.
""".format(__version__)

def get_project_description():
    return """
Aleatoryous 3 (or aleat3) is an open project
to build aleatory objects for Python programmers.
"""

def console_parser():
    parser = argparse.ArgumentParser(epilog=get_aleat_version())
    parser.add_argument("version", "v", action="version", version=get_aleat_version())
    parser.add_argument("add", "a", dest="aleat", metavar="DIRS",
    help="Append an aleatory-based object to the aleat3 clipboard and get a result")
    parser.add_argument("--coinconvert", "--c", "--coin", dest="coins", metavar="DIRS",
    help="Get a coinToBool() or a coinToBinary from the added Aleatoryous object")
    parser.usage = parser.format_usage()[len("usage: "):] + get_project_description()
    return parser

def console_main():
    nonparsed = console_parser()
    parsed = nonparsed.parse_args()
    if parsed.aleat is None:
        nonparsed.error("the 'add' argument cannot be None")
    elif len(parsed.aleat.strip()) > 0 and parsed.aleat != "aleatory.roulette":
        a = Aleatoryous(parsed.aleat)
        if parsed.aleat == "aleatory.coin" and parsed.coins is not None:
            if parsed.coins == "bool":
                print(coinToBool(a.single()))
            elif parsed.coins in ["bin", "binary"]:
                print(coinToBinary(a.single()))
            else:
                nonparsed.error("the '--coin' argument must be 'bool' or 'binary', not %s"%parsed.coins)
        else:
            print(a.single())
    elif len(parsed.aleat.strip()) > 0 and parsed.aleat == "aleatory.roulette":
        if parsed.roulette_list is None:
            warnings.warn("You must add a 'roulette_items' to use an aleatory.roulette. "
                          "We are giving a default list to replace the expected list")
            l = ["1", "2", "3"]
        else:
            l = parsed.roulette_list
        print("Options: %s"%l)
        a = Aleatoryous(parsed.aleat, l)
        print(a.single())
    else:
        nonparsed.error("you must enter one of the formal modes of aleat3 for the 'add' argument")
