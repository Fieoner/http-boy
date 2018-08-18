# HTTP-boy

Server that exposes an interface to a Game Boy emulator

# Installation (tested only on Ubuntu 18.04)

1. Clone this repo
2. `cd` into the repo directory
3. Clone [PyBoy](https://github.com/Baekalfen/PyBoy)
4. Create the virtual environment (read below)

# Virtual environment setup

> Taken from the [PyBoy README.md](https://github.com/Baekalfen/PyBoy#ubuntulinux) (modified for this project and with some fixes)

Ubuntu has some problems installing PyPy in parallel with the system version of CPython. Therefore, we will install the PyPy version of NumPy and PySDL2 in a virtualenv.

```
sudo apt update
sudo apt install git pypy pypy-dev virtualenv libsdl2-dev
```

Move to the root directory and create the virtual environment:

```
virtualenv . -p `which pypy`
source ./bin/activate

pip install git+https://bitbucket.org/pypy/numpy.git
pip install git+https://github.com/marcusva/py-sdl2.git
```

To install the `imageio` dependency you'll need to install a lib first:

```
sudo apt install libjpeg-dev
pip install imageio
```

# Usage

> Important: you'll need to put a ROM (which you of course dumped yourself with a tool such as [PyBoyCartridge](https://github.com/Baekalfen/PyBoyCartridge)) in the `ROM/` directory

Run `pypy main.py`, choose a ROM and enjoy!

You can also specify the ROM directly as a command line argument.

# Interface

The server is exposed in localhost by default, in port `8123`. You can send the following HTTP requests to the server:

## start()

Starts a game and returns the initial screenshot and the turn data. If the game has already started, the response will have the same data (screenshot and turn data) but it will include an `error` property with the error code `EGAMESTARTED`.

## execute(action)

Executes an action in the game and returns the resulting screenshot and the turn data.

# About turn data

Turn data is a data structure we created for this project which supports different ways to express the result of the last move and the available options for the next one.

It can be the simplest form (just a screenshot and normal controller input) or it can be something more ellaborate (like game stats in the result or game menu options as available options). The disponibility of this advanced formats will be different in each ROM, but the format should be standard and therefore the interface should be game-agnostic.

The payload of each request response is simple JSON. The result and the available options for the next turn are different pieces of data, and any combination should be possible. Example of the structure:

```
{
  "result": {
    "type": <result type>,
    ...other data
  },
  "options": {
    "type": <options type>,
    ...other data
  }
}
```

Here are the available turn data types:

## Result

### Simple

The simplest form of result. Just a screenshot.

```
{
  "type": "simple",
  "screenshot": "<base64-encoded image>"
}
```

## Options

### Controller

The simplest form of options. Just a controller input (A, B, up, down, etc).

```
{
  "type": "controller"
}
```
