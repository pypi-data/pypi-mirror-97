from aleat3 import Aleatoryous, coinToBool, coinToBinary
from aleat3.output.colored import UNABLE

__all__ = ["main",
           "coin",
           "dice",
           "roulette"]


# Main demostration of Aleatoryous:
def demo():
    # Based from Tests/aleatoryous.py
    # some fixes added at version 0.2.3
    a = Aleatoryous("aleatory.coin")
    print("coin " + str(a.single() in ["Head", "Tails"]))
    print("cointobinary  %s"%coinToBinary(a.single()) in [0, 1])
    print("cointobool %s"%coinToBool(a.single()) in [True, False])
    a.changemode("aleatory.dice")
    print("dice %s"%a.single() in [0, 1, 2, 3, 4, 5, 6])
    b = ["a", "b", "c"]
    a.changemode("aleatory.roulette", b)
    print("roulette %s"%a.single() in b)
    print("colorama output %s"%UNABLE)
    print("Done")


# coin():
def coin():
    c = Aleatoryous("aleatory.coin")
    cc = c.single()
    print("""coin single() result: %s
coinToBool conversion: %s
coinToBinary conversion: %s"""%(cc, coinToBool(cc), coinToBinary(cc)))


# dice():
def dice():
    d = Aleatoryous("aleatory.dice")
    print("dice single() result: %s"%d.single())


# roulette():
def roulette():
    l = ["Option 1", "Option 2", "Option 3"]
    print("Available options:")
    for ll in range(len(l)):
        print(" - %s"%l[ll])
    r = Aleatoryous("aleatory.roulette", l)
    print("roulette single(): %s"%r.single())
