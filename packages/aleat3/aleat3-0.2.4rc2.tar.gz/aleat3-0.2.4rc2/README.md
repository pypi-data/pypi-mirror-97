# Aleatoryous 3

This is the 3rth Generation of aleatory objects, built by Diego
Ramirez.

## Introduction

The Aleatoryous package allows you to build:

- Aleatory Syntax objects
  - Dice: aleatory.dice
  - Coin: aleatory.coin
  - Roulette: aleatory.roulette

By using the [Python](http://python.org) library [random](http://docs.python.org/3.8/library/random), Aleatoryous object can build many solutions
for problems where aleatory numbers or specific output are needed.

This package is built to be used with Python versions 3.5 to 3.9.

To enjoy the Aleatoryous materials, you must download the package from the [PyPi](http://pypi.org/project/aleat3#files)
and install it with pip by one of this ways:

```
pip install aleat3_[version]_[platform].whl

pip install aleat3_[version]_[platform].tar.gz

pip install aleat3==[version]

pip install --upgrade aleat3

pip install aleat3
```

#### The story of Aleatoryous

Well, you might ask: "If this package is a 3rth generation of Aleatoryous project,
what about generations 1 and 2?".

The answer is that versions [1](http://pypi.org/project/aleat1) and [2](http://pypi.org/project/aleat2) could be called
"deprecated versions" of final package. Even when this versions where released after version [3](http://pypi.org/project/aleat3),
they are incomplete or not functional.

So, don't worry: you are handling the best version of Aleatoryous.

#### Want to join the project?

This project needs __you!__ You can be a maintainer of Aleatoryous 3. Contribute
with ideas, code, or fixes you could find. Try to download the [source file](http://pypi.org/project/aleat3#files) and
[contact us](mailto:dr01191115@gmail.com) if you find a way to improve the project.

## Release notes

#### What's new in aleat3 0.2.4 (as a release candidate)

- The aleat3 scripts has changes. __Check documentation to learn about this fixes.__
- The aleat3 script `aleat3` is fixed.

#### What's new in aleat3 0.2.3

- Minor bug fixes
  - Variable minor fixes

#### What's new in aleat3 0.2.2

- The aleat3 scripts has changes. __Check documentation to learn about this fixes.__

#### What's new in aleat3 0.2.1

- Minor bug fixes
  - Some variable fixes

#### What's new in aleat3 0.2

- New `setup()` feature: [console_scripts](https://packaging.python.org/guides/distributing-packages-using-setuptools/#console-scripts).
  - View documentation, at section "aleat3 scripts".
- Some variable fixes

#### What's new in aleat3 versions 0.1.6 up to 0.1.9

- 'Applications' library fixes
  - `CoinWinners.py` fixed
- Code bug fixes
  - Get the `__version__` and the `__author__` data easier.

#### What's new in aleat3 0.1.5

- Minor bug fixes
  - Less repetitions at code.
  - 'Applications' library corrected
- New colored output
  - More [Colorama](http://pypi.org/project/colorama) functions are used
- New 'Applications' file: `diceMove.py`
  - Play with the computer to gain 50 points with `aleatory.dice`

#### What's new in aleat3 0.1.4

- Minor bug fixes
  - Less repetitions at code.
  - Variable `aleat3.constructor.__version__` corrected.

#### What's new in aleat3 0.1.3

- Bug fixes attempted
  - Fixed `aleat3.Aleatoryous.first_given()` method.
- New feature: __'Applications' library__.

Let's talk about this new feature. At `aleat3.applications` library you can run many
examples of Aleatoryous programming. The unable examples at this version are:

- diceInterface.py
  - Use [tkinter](http://docs.python.org/3.8/library/tkinter) library for a dice interface.
- rouletteWinners.py
  - Operate a long string of names and get 5 winners.
- coinWinners.py
  - Play with Heads or Tails and receive if you won or not.

To call this functions, import the example and just `run()` it:

```python
from aleat3.applications import rouletteWinners  # As an example
rouletteWinners.run()
```

#### What's new in aleat3 0.1.2 / aleat3 0.1.2.post1

- Minor bug fixes
  - Sometimes, the `module_test()` function failed at `__main__` level.

#### What's new in aleat3 0.1.1

- New developer features: Module tests
  - We are talking about `module_test()` function. View the new section _Module tests_.

#### What's new in aleat3 0.0.9

- New features:
  - Some output is colored with [Colorama](http://pypi.org/project/colorama).
    - _To view this function, you must install the Colorama library at PyPi._
  - __New function: coinToBool__. View the _aleatory.coin_ section to learn more.

#### Hold on... what about 0.0.8?

This version where released before, but it returned several errors. Then, version
0.0.9 is now released.

#### What's new in aleat3 0.0.7

- Minor bugs resolved:
  - Sometimes, version 0.0.6 could not make the "no-repetition" operation.

#### What's new in aleat3 0.0.6

- Minor bugs resolved:
  - Sometimes, version 0.0.5 did not return `__version__` output correctly.
  - Some exception handling were wrong at versions 0.0.4 and 0.0.5.
  - The operations are much cleaner and without repetitions.
- __New option at__ `Aleatoryous.first_given()`__: no-repetition.__
  - _View the "Iterating with aleatory.roulette" section_ to learn more about his feature.

#### What's new in aleat3 0.0.5

- Some variables deleted or recycled:
  - Private variables recycled

#### What's new in aleat3 0.0.4

- Minor bugs resolved:
  - Cleaner output
  - Faster operations
- Some variables deleted or recycled:
  - Variable `Aleatoryous.cache` deleted
  - Variable `Aleatoryous.it` deleted
  - Private variables recycled

#### What's new in aleat3 0.0.3

At version 0.0.2, you could change the Aleatoryous mode by typing:

```python
obj = Aleatoryous("aleatory.coin")

obj.mode = "Dice"
```

But now, **that operation is forbidden**, and the system might return a message
like this:

```
Traceback (most recent call last):
File .../-.py in <module>
    obj.mode = "Dice"
        ^
AttributeError: object "Aleatoryous" has no attribute "mode"
```

Instead of that, **use the new method _Aleatoryous.changemode()_**:

```python
obj.changemode("aleatory.dice")
```

Also, in version 0.0.3, you can get the mode name of your object:

```python
print(obj.getmode())
```

## Building Aleatory Objects

To import the aleat3 library, type:

```python
from aleat3 import *  # Call the whole aleat3 library
```

After aleat3 library is imported, type:

```python
obj = Aleatoryous()   # Build an aleatory coin by default
```

All 3 objects are built at the same way in Python. No matter the mode, you can
get aleatory output with methods:

```python
# Return: strings or integers
obj.single()         # Only one iteration
# Return: lists
obj.first_5()        # First 5 results
obj.first_10()       # First 10
obj.first_50()       # First 50
obj.first_100()      # First 100
obj.first_given(3)   # Iterate all the given times
```

Now, we give you a description of the items:

### *aleatory.coin*

The most simple mode of Aleatoryous. It can be called by 2 ways:

- Just typing `obj = Aleatoryous()`. The default "mode" is *aleatory.coin*.
- Being more specific, typing `obj = Aleatoryous("aleatory.coin")`.

The *aleatory.coin* can return 2 different results:

- String "Head"
- String "Tails"

###### Using *CoinToBinary* function

If you want, you can convert the *string* output from *aleatory.coin* to *int*
output with the function `aleat3.coinToBinary` included in the " * " import.

Follow the example:

```python
from aleat3 import *
obj = Aleatoryous("aleatory.coin")

result = obj.single()  # return only 1 value
print(coinToBinary(result))
```

###### Using *CoinToBool* function

Just like _coinToBinary_, the function _coinToBool_ can make conversions from
_aleatory.dice_ output, but returns a boolean constant (True/False).

Following the example from _coinToBinary_:

```python
print(coinToBool(result))
```


### *aleatory.dice*

The second mode of Aleatoryous returns a range **between 1 and 6**, just like
traditional dices. If you want an *aleatory.dice*, type:

```python
obj = Aleatoryous("aleatory.dice")
```

And, like traditional dices, **you could use more than one to get a larger result:**

```python
dice1 = Aleatoryous("aleatory.dice")
dice2 = Aleatoryous("aleatory.dice")

res = dice1.single() + dice2.single() # returns a range between 2 and 12
print(res)
```

### *aleatory.roulette*

The third and the most complex mode of Aleatoryous.
__This is the only mode that takes both parameters__ of Aleatoryous object:

```
Aleatoryous(mode, extras)
```

The **mode** parameter is taken by all the 3 modes. But the **extras** is only made
for *aleatory.roulette*. There you put a list of possible results. The list can have
any Python data structure, it will be iterated.

Follow the example:

```python
# Put your options here
lst = ["Option 1",
       {"Sub Option 1": 2, "Sub Option 2": None},
       10.9,
       [3, 4, 1],
       None]

# Build the object
obj = Aleatoryous("aleatory.roulette", lst) # The 2nd parameter is taken
print(obj.single())
```

#### Debugging *aleatory.roulette* errors

Remember, **you can only include lists in the "mode" parameter.** For example,
if you type:

```python
obj = Aleatoryous("aleatory.roulette", {"Option 1": 1, "Option 2": 2}) # A dictionary
```

You'll receive a message like this:

```
Traceback (most recent call last):
File .../-.py in <module>
    obj = Aleatoryous("aleatory.roulette", {"Option 1": 1, "Option 2": 2})
                                            ^
File .../aleat3/constructor.py in __init__
    raise ...
aleat3.constructor.InitError: __init__() Invalid Syntax (Unexpected parameter given: extras)
```

## Making solutions with Aleatoryous - Some examples

There are several ways to applicate the aleat3 features, from math education to
game development, you can use the Aleatoryous object and other functions included
by many, many ways. We are giving some examples:

#### Iterating with _aleatory.roulette_

The most used mode is *aleatory.roulette*, because you can control data to be
iterated in aleatory selection.

For example, if you read a file and want to get a random line:

```python
# The file register.txt will contain many-many-many names. We want 5 aleatory
# winners:

# John
# Richard
# Tamara
# Axel
# Gael
# Sarah
# Chuck

f = open("C://Users/Admin/Documents/register.txt", "r")
l = []

for i in f:
  l.append(i.rstrip())

# Operate the file data
from aleat3 import *

r = Aleatoryous("aleatory.roulette", l)
res = r.first_given(5, repeat=False)      # New since version 0.0.6: no-repetition
print(res)
```

And we'll get an output like:

```
["Richard", "Gael", "John", "Tamara", "Sarah"]
```

#### Binary aleatory numbers with _aleatory.coin + coinToBinary_

As we said before, the *coinToBinary* function converts an *aleatory.coin* output
to pseudo-binary numbers (1 or 0). We can use this function when you need an aleatory
output between 1 and 0. View the _Using coinToBinary function_ process shown above.

#### Building games with _aleatory.dice_

You could use the *aleatory.dice* natural properties for building complex games
where a dice is required.

For example, you can use the [tkinter](http://docs.python.org/3.8/library/tkinter) module for building
graphical interfaces, and then use the *aleatory.dice* to create a game where
the user can use a dice.

## Module tests

Since version 0.1.1, some aleat3 folder files have a new function: `module_test()`.

Only this files are available for testing:

- aleat3/constructor.py
- aleat3/output/colored.py
- aleat3/output/init_errors.py

(Other files are private or `__init__` scripts).

To use the `module_test()`, type:

```python
from aleat3.constructor import module_test # Using constructor.py as an example
module_test()
```

Then, you'll receive an output like:

```
----Module test: constructor.py----

Testing module...

Testing objects...
-Testing object 'aleat3.Aleatoryous'...
 The object 'aleat3.Aleatoryous' is OK.

(...)

The module is OK.

----Test finished----

Done
```

Also, when using the file as `__main__` level:

```
NOTE: When using the file as __main__ level, you are executing the module test.
This operation may take some minutes.

----Module test: constructor.py----

Testing module...

Testing objects...
-Testing object 'aleat3.Aleatoryous'...
 The object 'aleat3.Aleatoryous' is OK.

(...)

The module is OK.

----Test finished----

Done
```

__NOTE:__ These tests are based in common use of each function or object in file.
If you run the test, tells you the module is OK, and your package still failing,
please send an e-mail [here](mailto:dr01191115@gmail.com).


## aleat3 scripts

Since 0.2.0, aleat3 setup added some *console_scripts*, who work like short "demos"
about the power of aleat3:

```
$ aleat3 add aleatory.coin
6

$ aleat3_demo
coin True
 ...

$ aleat3_coin
coin.single() result: Tails
 ...

$ aleat3_dice
dice.single() result: 3

$ aleat3_roulette
Options:
 ...
roulette.single() result: Option 2

$
```

_Changed in version 0.2.2:_ The console script `aleat3` is now deleted. Now, use
command `aleat3_demo`.

_Changed in version 0.2.4:_ The console script `aleat3` is restored, but taking a
new role, different than the actual command `aleat3_demo`. __This new command takes__
__one of this arguments:__

- `add / a`
  - Add an Aleatoryous type and retrieve a result: `aleat3 add aleatory.dice`.
  - __Arguments__: A formal name of any aleat3 syntax (which start with prefix "aleatory")
- `--coinconvert / --c / --coin`
  - Make a `coinToBool()` or a `coinToBinary()` conversion: `add aleatory.coin --c bool`.
  - __Arguments__: "bool" or "binary"
- `version / v`
  - Get the version of aleat3: `aleat3 version`.
  - __Arguments__: None.

## More information online

Visit [pypi.org](http://pypi.org) or the [latest Python docs](http://docs.python.org) to learn more
about referenced libraries or package installation.
