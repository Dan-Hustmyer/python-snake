# python-snake

A Snake clone written in python in only 100 lines of code. Check out the
`additional features` branch for more features like Pause and New Game.

![Screenshot][screenshot]

## Usage

```bash
git clone https://github.com/jeremija/python-snake
cd python-snake
python3 -m snake.main
```

Tested on Arch Linux, Mac OS Sierra and Windows 10.

## Requirements

[Python3][python] and [tk-tcl][tk-tcl].

### Windows

[Download][python] and install Python 3.

### Mac OS

Read the [requirements][mac-py-tk]. If you are using homebrew,
you can just run:

```bash
brew install tcl-tk
brew install python3 --with-tcl-tk
```

Without homebrew, download and install:

- [ActiveTcl][tk-tcl]
- [Python 3][python]

### Arch Linux

```bash
sudo pacman -S tk python3
```

### Ubuntu / Debian

```bash
sudo apt-get install python3 python3-tk
```

# License

MIT

[screenshot]: https://raw.githubusercontent.com/jeremija/python-snake/master/snake.png
[python]: https://www.python.org/downloads/
[mac-py-tk]: https://www.python.org/download/mac/tcltk/
[tk-tcl]: https://www.activestate.com/activetcl/downloads
