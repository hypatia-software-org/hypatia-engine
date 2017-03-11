"""Hypatia 2D game engine.

Usage:
    hypatia run <path> [options]
    hypatia new-game <path> [options]

Options:
    --version    Display Hypatia version and exit.
    --help       Display this help notice and exit.

"""

import os
import docopt

from hypatia import __version__
from hypatia.game import Game


def main():
    args = docopt.docopt(__doc__, version=f"Hypatia Engine {__version__}")

    if args['run']:
        game = Game(args['<path>'])
        game.run()

    elif args['new-game']:
        raise NotImplementedError("No functionality to create new games exists yet.")

    else:
        print("What do you want me to do?")

if __name__ == "__main__":
    main()