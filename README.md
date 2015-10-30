MagicExplorer
=============

This is our contribution to SonenGameJam autumn 2015 we're we make a game from
scratch over the course of one weekend.

Our game is a zelda-style top-down 2d-adventuregame where the goal is to
discover your past. You do this by gathering pages from a journal that you
wrote, but can't remember having wrote.

## Intro

How does it feel to be an outcast, to be completely abandoned by those around
you?

You wake up on the shore of an island without remembering why you're there. The
only thing you find beside you is the page of a journal. Telling the story of a
great civilization falling into ruin.

In this game you will explore the island and try to communicate with the
inhabitants. However that doesn't seem to be as easy as one would thought. They
avoid you and if they speak they speak rudely to you.

Did you do something to them in the past? The only solution is to find the rest
of the journal and find out what went down on this island.

## Instructions

You move with A-W-S-D and communicate with the inhabitants with E.

In order to travel on water you need a boat.

## Running it

Download from the [releases](https://github.com/benedicteb/outcast/releases)
page.

Currently we only have a precompiled OS X-version. However you are welcome to
clone the source, install the dependencies and run the game.

### Compiling

In order to run the game from source. Clone the repo, and then do the following.

```
$ easy_install virtualenv
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements
$ python outcast.py
```
