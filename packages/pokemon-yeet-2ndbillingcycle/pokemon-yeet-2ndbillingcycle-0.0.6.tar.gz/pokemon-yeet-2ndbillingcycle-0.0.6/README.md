# Pokemon YEET

An auto battling Pokémon cli game.

This game was created as part of the [2021 MASTERMND deCoded Journey sofware bootcamp][decoded 2021]:

1. [creating a Pokemon class (starts at 1:24:48)][part 1]
1. [making it into a game][part 2]
1. [using an API][part 3]

## Install

This game is built with [Python][], which has [installation instructions here][python-installation].

Download the game with `pip`:

```sh
pip install --user -U pokemon-yeet-2ndbillingcycle
```

### Installation error

If `pip` returns an error like the following:

```
...
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pip-req-build-h6qzslht/setup.py'

----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-req-build-h6qzslht/
```

`pip` is out of date, and needs to be updated:

```sh
pip install --user --upgrade pip
```

## Play

With the game [installed](#install), run the command `pokemon-yeet` to play:

```
$ pokemon-yeet
...
Downloading pokemon #151
Pokemon data downloaded
get ready, now recruiting your team of pokemon!


team selected! meet your new team
omastar: HP: 70 TYPE: rock
nidoking: HP: 81 TYPE: poison
tentacool: HP: 40 TYPE: water


now recruiting the enemy team!


team selected! meet your enemies!
kakuna: HP: 45 TYPE: bug
nidorino: HP: 61 TYPE: poison
venomoth: HP: 70 TYPE: bug
PREPARE TO FIGHT!!!!!
omastar attacked with scratch and it did 35 damage
kakuna: HP: 10 TYPE: bug
kakuna attacked with leer and it did 20 damage
omastar: HP: 50 TYPE: rock
omastar attacked with tackle and it did 10 damage
kakuna: HP: 0 TYPE: bug
kakuna has FAINTED
kakuna: HP: 0 TYPE: bug
THE SCORE IS: ME:1 ENEMY:0
nidoking attacked with cut and it did 25 damage
nidorino: HP: 36 TYPE: poison
nidorino attacked with cut and it did 25 damage
nidoking: HP: 56 TYPE: poison
nidoking attacked with tackle and it did 10 damage
nidorino: HP: 26 TYPE: poison
nidorino attacked with leer and it did 20 damage
nidoking: HP: 36 TYPE: poison
nidoking attacked with cut and it did 25 damage
nidorino: HP: 1 TYPE: poison
nidorino attacked with tackle and it did 10 damage
nidoking: HP: 26 TYPE: poison
nidoking attacked with leer and it did 20 damage
nidorino: HP: -19 TYPE: poison
nidorino has FAINTED
nidorino: HP: -19 TYPE: poison
THE SCORE IS: ME:2 ENEMY:0
tentacool attacked with tackle and it did 10 damage
venomoth: HP: 60 TYPE: bug
venomoth attacked with cut and it did 25 damage
tentacool: HP: 15 TYPE: water
tentacool attacked with leer and it did 20 damage
venomoth: HP: 40 TYPE: bug
venomoth attacked with tackle and it did 10 damage
tentacool: HP: 5 TYPE: water
tentacool attacked with leer and it did 20 damage
venomoth: HP: 20 TYPE: bug
venomoth attacked with leer and it did 20 damage
tentacool: HP: -15 TYPE: water
tentacool has FAINTED
tentacool: HP: -15 TYPE: water
THE SCORE IS: ME:2 ENEMY:1
WE WON HAHAHAHAHAHAHAHAHAHAHAHA
```

_note: running `pokemon-yeet` will create a directory to store information about Pokémon_

## Development

This repository can be downloaded with [`git`][] ([a mastermndio video about `git`](https://youtu.be/4AmqVslOw58)). Once that's done, [create a virtual environment in the same directory][python-venv]:

```sh
python -m venv venv
```

_note: depending on how [Python][] was installed, `python` may be `python3`, and `venv` may need to be downloaded separately (e.g. as `python3-venv`)_

This creates a directory called `venv` in the current directory.

Then, activate the virtual environment. On Linux, this looks like:

```sh
. venv/bin/activate
```

Make sure `pip` inside the virtual environment is up to date:

```sh
pip install --upgrade pip
```

Then, install the game in the virtual environment:

```sh
pip install ./
```

And you're ready to go! Change some files, re-install, and run again!

### Packaging

[Flit][] is used to package and upload the game.

To upload your own version, change the information in [`pyproject.toml`][flit pyproject.toml]:

- `dist-name`: replace `2ndbillingcycle` with your username
- `author`: your name
- `author-email`: your email
- `home-page`: either put the link to your GitHub fork, or remove this line

Then, install [Flit][] and build the distribution files. With the virtual environment activated:

```sh
pip install --upgrade flit
python -m flit build
```

Then, follow [the official Python packaging guide][python packaging tutorial] for uploading the package to the [Test Python Package Index][testpypi].

Alternatively, you can [create an API token on PyPI with a scope for "Entire account"][api token], and run `flit publish`, pasting the created API token for the password.

### API dependencies

This game uses <https://pokeapi.co/> to get information about Pokémon.

[python]: <https://www.python.org/>
[python-installation]: <https://realpython.com/installing-python/> "RealPython's guide to installing Python on Windows, MacOS, and Linux"
[`git`]: <https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository> "brief guide on using git"
[python-venv]: <https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments> "tutorial on creating virtual environments in Python"
[flit]: <https://flit.readthedocs.io/> "Documentation for Flit"
[decoded 2021]: <https://courses.mastermnd.io/72579a892507473ab4681876f8299977> "2021 deCoded Journey"
[part 1]: <https://www.twitch.tv/videos/917000567> "Part 1 on Twitch"
[part 2]: <https://www.twitch.tv/videos/919551146> "Part 2 on Twitch"
[part 3]: <https://www.twitch.tv/videos/934768927> "Part 3 on Twitch"
[python packaging tutorial]: <https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives>
[testpypi]: <https://test.pypi.org/> "The Test Python Package Index"
[test api token]: <https://pypi.org/help/#apitoken>
