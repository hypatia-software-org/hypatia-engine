# Hypatia 0.2.13 (alpha)

![Hypatia 0.2](media/logos/logotype-blacktext-transparentbg.png)

[![Travis](https://img.shields.io/travis/lillian-lemmer/hypatia.svg?style=flat-square)](https://travis-ci.org/lillian-lemmer/hypatia) [![GitHub license](https://img.shields.io/github/license/lillian-lemmer/hypatia.svg?style=flat-square)](https://raw.githubusercontent.com/lillian-lemmer/hypatia/master/license.txt) [![Coveralls](https://img.shields.io/coveralls/lillian-lemmer/hypatia.svg?style=flat-square)](https://coveralls.io/r/lillian-lemmer/hypatia) [![Code Climate](https://img.shields.io/codeclimate/github/kabisaict/flow.svg?style=flat-square)](https://codeclimate.com/github/lillian-lemmer/hypatia) [![PyPI](https://img.shields.io/pypi/v/nine.svg?style=flat-square)](https://pypi.python.org/pypi/hypatia_engine/) [![PyPI](https://img.shields.io/pypi/dm/hypatia.svg?style=flat-square)](https://pypi.python.org/pypi/hypatia_engine/) [![Gratipay](https://img.shields.io/gratipay/lillian-lemmer.svg?style=flat-square)](https://gratipay.com/~lillian-lemmer/) [![Bountysource](https://img.shields.io/bountysource/team/hypatia/activity.svg?style=flat-square)](https://www.bountysource.com/teams/hypatia) 

Make 2D action adventure games. For programmers and nonprogrammers alike.

With Hypatia you can create a games like [_Legend of Zelda: Oracle of Ages_ and _Oracle of Seasons_](http://en.wikipedia.org/wiki/The_Legend_of_Zelda:_Oracle_of_Seasons_and_Oracle_of_Ages).

There is an included demo game (`demo/game.py`). Here it is in action:

![The demo game in action.](http://lillian-lemmer.github.io/hypatia/media/recordings/2015-06-28-develop-640x480.gif)

[Hypatia is a cross-platform project (Windows, Mac, Linux, BSD), and it puts FreeBSD development first.](https://github.com/lillian-lemmer/hypatia/wiki/Platform-Support)

Hypatia is a labor of love, [permissively (MIT) licensed](license.txt), and crafted by [Lillian Lemmer](http://github.com/lillian-lemmer/hypatia/wiki/About-the-Creator).

# Resources

For info on installation, checkout the [installation instructions page](https://github.com/lillian-lemmer/hypatia/wiki/Installation-Instructions).

  * [Hypatia Wiki](https://github.com/lillian-lemmer/hypatia/wiki/) (great resource for nonprogrammers, too!)
  * [Hypatia API Docs](https://lillian-lemmer.github.io/hypatia/api)
  * For people, checkout the [socialization and contact methods for the Hypatia project](https://github.com/lillian-lemmer/hypatia/wiki/Profiles).
  * [The official Hypatia website](http://lillian-lemmer.github.io/hypatia/)
  * Official support chat: [#hypatia on Freenode (webui!)](http://webchat.freenode.net/?channels=hypatia)
  * You can contact the author via email: lillian.lynn.lemmer@gmail.com, [@LilyLemmer](https:/twitter.com/LilyLemmer) on Twitter.

# Dive in without any programming

The included demo allows you to mess with all of its resources (see the `resources` directory!). With it you can:

  * [Create tilesheets to make tilemaps](https://github.com/lillian-lemmer/hypatia/wiki/Tilesheets)
    * Configure tiles from the tilesheet
    * Chain tiles together to create animations
    * Apply the "cycle" effect, which takes a non-animated tile, and creates an animated tile by rotating the colors used in the tile
    * Set tile flags, like the `impass_all` flag which makes a flag impassable to the player
  * [Create tilemaps with an arbitrary number of layers, using plaintext files](https://github.com/lillian-lemmer/hypatia/wiki/tilemap.txt)
  * [Create scenes, with configurable NPCs, configurable scene data (player start position)](https://github.com/lillian-lemmer/hypatia/wiki/Nonprogrammer-Guide#editing-scene-data)
  * [Create character sprites using animated or non-animated GIFs](https://github.com/lillian-lemmer/hypatia/wiki/Walkabout-Sprites)

For more information, please read the [official wiki guide for non-programmers](https://github.com/lillian-lemmer/hypatia/wiki/Nonprogrammer-Guide).

# Quick Demo

## Windows

Simply run `game.exe` after extracting [hypatia-demo-windows-current.zip](https://lillian-lemmer.github.io/hypatia/releases/hypatia-demo-windows-current.zip).

## Other

To get setup quickly and start tinkering around with the demo, simply issue the following commands:

  1. `pip install hypatia_engine`
  2. `cd demo`
  3. `python game.py`

# License

Hypatia is MIT licensed, which means you can use it for whatever purpose you'd like.

    The MIT License (MIT)

    Copyright (c) 2015 Lillian Lemmer

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
