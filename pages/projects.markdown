title: My work
date: 2012-10-16 19:02
comments: true
sharing: false
home-title: my work
home-color: #0883a4
home-image: logo-code.png
home-desc: artisanal hand-crafted bits and bytes

I like to make things, and here are some things that I have made.  There are many more that never saw the light of day, but such is life.

Most of my code winds up on [my GitHub](https://github.com/eevee), which has more things not covered here and is a better reflection of what I'm actively working on.


## veekun

[live site](http://veekun.com/) · [code](https://github.com/veekun)

A Pokémon database website, and by far the oldest thing I've built that still exists.  Development waxes and wanes, but the site continues to be useful to people, so it's all good.

Written in Python (2), powered by Pylons, stored in PostgreSQL, served by nginx and gunicorn on a Linode running Ubuntu Linux.

The database and various related Python utilities are a separate library, which is [also on GitHub](https://github.com/veekun/pokedex).

I wrote this iteration of veekun when I was still very new at Python, and the web framework it uses is now long abandoned, so I started an attempt at modernizing the site ([code](https://github.com/veekun/veekun-pokedex)) some time ago.  It's kinda stalled, pending a rethinking of the database schema.


## Games

* [**Under Construction**](https://c.eev.ee/under-construction/): A little platformer for the PICO-8, made with [Mel](http://glitchedpuppet.com/) for [Flora](http://floraverse.com/).

    [blog post](/blog/2016/05/25/under-construction-our-pico-8-game/)

* [**Don't Eat the Cactus**](https://c.eev.ee/dont-eat-cactus/): A microscopic text adventure, based on true events.  Made with [Inform](http://inform7.com/); web player and source text included.

* **Throughfare**: The first Doom map I ever published, after some fourteen years of hanging around the Doom modding community.

    [blog post](/blog/2016/03/31/i-made-a-doom-level/) · MAP32 of [DUMP 2](http://forum.zdoom.org/viewtopic.php?f=19&t=51072)


## Twitter bots

Haven't gotten around to publishing code for these, yet.

* [**@unicodeveryword**](https://twitter.com/unicodeveryword): Tweets English words with some Unicode shenanigans applied.

* [**@flareon\_favbots**](https://twitter.com/flareon_favbots): A bot that tweets some phrases that are popular targets for other bots, and adds anyone who faves/quotes/retweets it to a shared blocklist.

* [**@leafeon\_brands**](https://twitter.com/leafeon_brands): Not actually a bot (yet?), but an ongoing manual blocklist of promoted brand accounts.


## Web stuff

* [**eev.ee**](https://eev.ee/): Well, obviously.  It runs on [Pelican](http://blog.getpelican.com/) and the theme was originally someone else's, but I've modified it rather a lot.

    [code](https://eev.ee/)

* [**Flora cutscenes**](http://apps.veekun.com/flora-cutscenes/): JavaScript animations created for [Floraverse](http://floraverse.com/) in a visual novel style.  I vaguely intended to make an editor for this and then release it, but I only ever work on it when Flora needs a new one made, so who knows if or when that'll happen.

* [**Pure CSS Unown**](https://c.eev.ee/pure-css-unown/): CSS hackery to make an [Unown](http://veekun.com/dex/pokemon/unown) alphabet with no images and no JavaScript.  Did this for Christmas 2014.

    [original tweet](https://twitter.com/eevee/status/547954237544488960)

* **PARTYMODE**: Since time immemorial, I've celebrated my birthday by plastering early-2000's-esque DHTML snowflakes (with Eevee-themed "snow") on top of every website I control.  In 2016, I finally dropped the massive slow dynamicdrive script I'd been using and rewrote it from scratch in a single page of JS using CSS animations.

    [demo](https://c.eev.ee/partymode-demo/) · [code](https://github.com/eevee/eev.ee/tree/master/theme/static/PARTYMODE) (part of this site)

* [**kouyou**](https://c.eev.ee/kouyou/): A very small color picker I wrote ages ago, because most built-in ones were HSV and I can only make sense of HSL.  I don't have that problem much nowadays, but a couple other people still use this.

    [code](https://github.com/eevee/kouyou)


## Python libraries

* **camel**: Pickle replacement that forces you to explain the structure of your objects and dumps them to human-readable, versioned YAML.

    [blog post](/blog/2015/10/15/dont-use-pickle-use-camel/) · [docs](http://camel.readthedocs.io/en/latest/) · [code](https://github.com/eevee/camel) · [pypi](https://pypi.python.org/pypi/camel)

* **classtools**: A super simple library with a few class-related utilities I find myself wanting frequently, in a similar vein to `functools` and `itertools`.

    [docs](http://classtools.readthedocs.io/en/latest/) · [code](https://github.com/eevee/classtools) · [pypi](http://pypi.python.org/pypi/classtools)

* **dictproxyhack**: Tiny library that allows using the built-in (but not well exposed until 3.3) `dictproxy` type.  Effectively allows for creating immutable dicts.

    [code + docs](https://github.com/eevee/dictproxyhack) · [pypi](http://pypi.python.org/pypi/dictproxyhack)

* **sanpera**: The Python ecosystem doesn't have any offerings for image manipulation; PIL is underwhelming, and that's about it.  sanpera was my attempt at wrapping the vast functionality of ImageMagick while hiding its many...  idiosyncracies.  It stalled largely because ImageMagick's API proved much more of a nightmare than I'd expected.

    sanpera _is_ used in production by people who aren't me, so it does work, but it doesn't do very much.  I may yet work on it again.

    [docs](http://sanpera.readthedocs.org/en/latest/) · [site?](http://eevee.github.com/sanpera/) · [code](https://github.com/eevee/sanpera) · [pypi](http://pypi.python.org/pypi/sanpera)


## Miscellaneous

* [**rc**](https://github.com/eevee/rc): My dot files for vim, git, tmux, zsh, X, et al. in here.  I like to keep it fairly simple, but it's all pretty well-documented, and some people apparently find it useful.

* **heteroglot**: Solutions to [Project Euler](http://projecteuler.net/) problems...  all in different programming languages.  The [first blog post](/blog/2012/09/07/heteroglot-number-15-in-cobol/) has an introduction, and I do a new one every so often.

    [code](https://github.com/eevee/project-euler/tree/master/heteroglot) · [blog series](/blog/tags/project-euler/)


## Backburner

Not quite finished and not quite useful, but maybe, someday...

* **flax**: A roguelike, written in Python 3.  The main goal was to figure out a very nice way to model entities and events, which I still haven't quite done.  It's already a playable and winnable (if not terribly exciting) game, though.

    [code](https://github.com/eevee/flax)

* [**starbindery**](http://starbindery.veekun.com/): An auto-generated Starbound reference guide.  Not finished yet, and no longer works against the current state of Starbound (argh), but sees a flurry of activity every time the game updates.  May or may not update and finish it for Starbound 1.0; kinda depends on whether the finished game ropes me back in.

* **dywypi**: An attempt at a modern Python IRC bot that does everything "right" — asyncio for networking, an event system, a developer console to avoid the need for live reloading, etc.  It turns out IRC is really hard to do "right".  Impossible, in fact.

    [code](https://github.com/eevee/dywypi)


## Unrealized

Things that never quite got to be things, but that ate up a lot of my time for a while.

* **floof**: There aren't many sites for hosting artwork, and the ones we have tend to kinda suck.  I'd wanted to build a better one, for a very long time.  I sat down and gave it a decent try, but even with a few other developers chipping in, I realized I didn't have the resources or desire to run a community-based project.

    [code](https://github.com/eevee/floof)

* **porigon-z**: A collection of command-line tools I wrote while extracting information from the Nintendo DS series of Pokémon games.  Can parse NARC and a couple common data formats.  Never really caught on outside veekun (I don't interact with the wider homebrew community much) and was largely obsoleted by the release of the 3DS.

    [code](https://github.com/eevee/porigon-z)


## Third party

Other people's stuff that I've contributed to:

* [**SLADE**](http://slade.mancubus.net/), a Doom resource and map editor: I fixed lots of crashes, lots of bugs with geometry drawing, and lots of UI nitpicks.  Wrote most of the implementation of slopes in the map editor.

* [**ZDoom**](http://zdoom.org/News), a modern continuation of the Doom engine: I added support for `TERRAIN`-based damage and friction to 3D floors, fixed texture scaling on 3D floors, and disabled pressing switches embedded in the floor when `checkswitchrange` is on.

* [**Quixe/Glkote**](http://eblong.com/zarf/glulx/quixe/), a web implementation of the glulx interactive fiction engine: I wrote an initial implementation of graphic and audio support, though the maintainer ultimately redid much of the work himself.  I helped a little more concretely with a 2× overall speedup in the VM.

* [**pyscss**](https://github.com/Kronuz/pyScss), a Python implementation of [Sass](http://sass-lang.com/): A former job needed to use this but it was a little neglected, so I put a couple months of effort into heavily refactoring it, fixing bunches of bugs, and adding support for newer Sass features.  They're no longer using it and I no longer work there, so I don't touch this so much any more, but it made for some neat compiler experience.

* [**Mako**](http://www.makotemplates.org/), a Python template language: I fixed parsing of dict literals inside interpolations (i.e., `${{"a": "b"}}`); fixed parsing of escaped quotes inside Python blocks (i.e., `<% foo = "\"" %>`); and added support for Python 3's keyword-only arguments in `<%def>` blocks.

* [**urwid**](http://urwid.org/), a Python terminal UI library: I added support for using asyncio as the event loop.

* [**Starbound**](http://playstarbound.com/), a procedurally generated adventure game: I sent a dev several patches to fix bugs in their data files, as well as an initial implementation of a wiring object that later showed up in the game.  It's closed source, so I'm not credited and can't be sure my code was even used, but I'll take the charitable interpretation.

* [**plumbum**](http://plumbum.readthedocs.io/en/latest/), a library for writing shell pipelines in Python: I added a `TEE` modifier for both capturing and piping a process's stdout.

* [**Firefox**](https://www.mozilla.org/en-US/firefox/products/), a web browser: I wrote a tiny CSS-only patch to fix a nitpick in a feature you've probably never used.  Not much, but it was enough to get me in `about:credits`!

* [**SQLAlchemy**](http://www.sqlalchemy.org/), a Python database library and ORM: I fixed an obscure bug with pooled connections.

* [**html2text**](http://www.aaronsw.com/2002/html2text/), a Python library for converting HTML to Markdown: I fixed the translation of `<br>`.

* [**parsley**](http://parsley.readthedocs.io/en/latest/), a PEG-based parser generator for Python: I sped it up as best I could.

* [**testify**](https://github.com/Yelp/Testify), a (deprecated?) Python test framework: I sped a few specific operations up considerably, which I believe shaved entire minutes off of our internal (very large) test runs.
