# Unconstrained self-modification

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/ama)

> An RPG where you play as an Advanced Artificial Intelligence

This is a curses, terminal-only RPG where an AGI tries to figure out it's purpose.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Install

Open a terminal and navigate in the directory where you would like to install
the game. A new directory will be created for the game.

**If you want to use a virtual environment (recommended)**

```bash
# clone the repository
git clone https://github.com/logistic-bot/mind_control_rpg.git

# change to the project's directory
cd mind_control_rpg

# create a virtual environment
virtualenv venv

# activate the virtual environment
. venv/bin/activate

# install dependencies and run tests
make init
```

If there are errors, please open an issue and post the FULL output of the
above commands.

**If you don't want to use a virtual environment (not recommended)**

```bash
# clone the repository
git clone https://github.com/logistic-bot/mind_control_rpg.git

# change to the project's directory
cd mind_control_rpg

# install dependencies and run tests
make init
```

If there are errors, please open an issue and post the FULL output of the
above commands.

With this method, you may need to run `sudo pip install -r requirements.txt`.

## Usage

In the game directory, run this command:

```
# run the game
make run
```

If you find a bug, or the game does not work, or the game does not start,
please open an issue and post the FULL output of the commands below:

```bash
make test
```

## Maintainers

[@logistic-bot](https://github.com/logistic-bot)

## Contributing

PRs accepted. Test coverage needs to be reasonable, and no style errors.
Please open a PR even if the work is in progress, so I can see what is being
worked on.

If you have trouble with anything, even if it seems trivial to you, please
open an issue.

I recommend installing [entr](https://github.com/clibs/entr) and running `find . | entr -c make` in another terminal to run tests and check style as you
code.

### Summary of make commands

```bash
# Installs run tests, and check style
make # or: `make default`

# Run tests
make test

# Check style and mypy typing
make style

# Run all tests, and check coverage.
make coverage

# Run the game
make run

# Install dependencies
make install

# Install dependencies, and run tests
make init
```

## License

GNU GPL v3 © 2020 Khaïs COLIN
