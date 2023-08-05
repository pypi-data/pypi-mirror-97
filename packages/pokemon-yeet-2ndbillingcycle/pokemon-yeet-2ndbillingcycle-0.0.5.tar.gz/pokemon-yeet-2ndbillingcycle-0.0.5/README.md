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

With the game [installed](#install), run the command `pokemon` to play:

```
$ pokemon
Creating pokemon directory...
Importing Pokemon....
...

Game is Setup and Ready to begin
get ready, now recruiting your team of pokemon!


team selected! meet your new team
victreebel: HP: 80 TYPE: grass
mr-mime: HP: 40 TYPE: psychic
clefable: HP: 95 TYPE: fairy


now recruiting the enemy team!


team selected! meet your enemies!
doduo: HP: 35 TYPE: normal
nidorina: HP: 70 TYPE: poison
krabby: HP: 30 TYPE: water
PREPARE TO FIGHT!!!!!
victreebel attacked with scratch and it did 35 damage
doduo: HP: 0 TYPE: normal
doduo has FAINTED
doduo: HP: 0 TYPE: normal
THE SCORE IS: ME:1 ENEMY:0
mr-mime attacked with scratch and it did 35 damage
nidorina: HP: 35 TYPE: poison
nidorina attacked with scratch and it did 35 damage
mr-mime: HP: 5 TYPE: psychic
mr-mime attacked with leer and it did 20 damage
nidorina: HP: 15 TYPE: poison
nidorina attacked with cut and it did 25 damage
mr-mime: HP: -20 TYPE: psychic
mr-mime has FAINTED
mr-mime: HP: -20 TYPE: psychic
THE SCORE IS: ME:1 ENEMY:1
clefable attacked with cut and it did 25 damage
krabby: HP: 5 TYPE: water
krabby attacked with scratch and it did 35 damage
clefable: HP: 60 TYPE: fairy
clefable attacked with cut and it did 25 damage
krabby: HP: -20 TYPE: water
krabby has FAINTED
krabby: HP: -20 TYPE: water
THE SCORE IS: ME:2 ENEMY:1
WE WON HAHAHAHAHAHAHAHAHAHAHAHA
```

_note: running `pokemon` will create a directory called `pokemon/` to store information about Pokémon_

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
