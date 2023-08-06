"Base for aleat3 console script."

import argparse
import os
import sys
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
to build aleatory objects that make different solutions at life for
Python programmers.
"""

def console_parser():
    parser = argparse.ArgumentParser(epilog=get_aleat_version())
    parser.add_argument("--version", "--v", action="version", version=get_aleat_version())
    parser.add_argument("--add", "--a", dest="aleat", metavar="DIRS",
    help="Append an aleatory-based object to the aleat3 clipboard and get a result")
    parser.add_argument("--coinconvert", "--c", "--coin", action="append", dest="aleat", metavar="DIRS",
    help="Create an aleatory.coin and get a coinToBool() or a coinToBinary")
    parser.usage = parser.format_usage()[len("usage: ") :] + get_project_description()
    return parser

def console_main():
    nonparsed = console_parser()
    parsed = nonparsed.parse_args()
    if isCoin(parsed.coin) and parsed.aleat is None:
        a = Aleatoryous()
        if parsed.coin == "bool":
            print(coinToBool(a.single()))
        elif parsed.coin in ["binary", "bin"]:
            print(coinToBinary(a.single()))
        else:
            nonparsed.error("you must enter 'bool' or 'binary' for the coin conversion argument")
    elif len(parsed.aleat.strip()) > 0 and parsed.aleat != "aleatory.roulette":
        a = Aleatoryous(parsed.aleat)
        print(a.single())
    elif len(parsed.aleat.strip()) > 0 and parsed.aleat == "aleatory.roulette":
        l = ["1", "2", "3"]
        print("Options: %s"%l)
        a = Aleatoryous(parsed.aleat, l)
        print(a.single())
    else:
        nonparsed.error("you must enter one of the formal modes of aleat3")
