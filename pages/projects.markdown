title: Projects
date: 2012-10-16 19:02
comments: true
sharing: false
home-title: code, etc.
home-color: #0883a4
home-image: logo-code.png
home-desc: things i have made with the aid of computers, beep boop

I like to make things, so here are some things I have made.  There are many more that are unfinished, but such is life.

Most of my code winds up on [my GitHub](https://github.com/eevee), which has more things not covered here and is a better reflection of what I'm actively working on.


## Stable

### veekun

[live site](http://veekun.com/) · [code](https://github.com/veekun)

A Pokémon database website, and by far the oldest thing I've built that still exists.  Development waxes and wanes, but the site continues to be useful to people, so it's all good.

Written in [Python][] (2), powered by [Pylons][], stored in [PostgreSQL][], served by [nginx][] and [gunicorn][] on a [Linode][] running [Ubuntu Linux][].

The database and various related Python utilities are a separate library, which is [also on GitHub](https://github.com/veekun/pokedex).

I wrote this iteration of veekun when I was still very new at Python, and the web framework it uses is now long abandoned, so I started an attempt at modernizing the site ([code](https://github.com/veekun/veekun-pokedex)) but it's kinda stalled pending a rethinking of the database schema.



### Floraverse cutscenes

[live site](http://apps.veekun.com/flora-cutscenes/)

JavaScript animations created for [Floraverse](http://floraverse.com/) in a visual novel style.

The code isn't published because it keeps undergoing heavy churn as the requirements continue to change, but it would be nice to have this be a real engine with an editor and whatnot someday.


### rc

[code](https://github.com/eevee/rc)

Dot files.  Got some stuff for vim, git, tmux, zsh, X, et al. in here.  I like to keep it fairly simple, but it's all pretty well-documented, and some people apparently find it useful.


### classtools

[docs](http://classtools.readthedocs.org/en/latest/) · [code](https://github.com/eevee/classtools) · [pypi](http://pypi.python.org/pypi/classtools)

A super simple [Python][] library with a few class-related utilities I find myself wanting frequently, in a similar vein to `functools` and `itertools`.


### dictproxyhack

[code + docs](https://github.com/eevee/dictproxyhack) · [pypi](http://pypi.python.org/pypi/dictproxyhack)

Tiny [Python][] library that allows using the built-in (but not well exposed until 3.3) `dictproxy` type.  Effectively allows for creating immutable dicts.


### kouyou

[live site](http://apps.veekun.com/kouyou/) · [code](https://github.com/eevee/kouyou)

Just a little color picker, because I could never find one that I liked.  (Most of them are HSV, which is unintelligible to me; this one also has HSL.)

I had a lot of ideas for color-related features, but never needed any of them quite enough to get around to building them, and now CSS has `hsl()` so I don't need a color picker quite so much.  But maybe you do.


## In progress

### flax

[code](https://github.com/eevee/flax)

A roguelike, written in [Python][] 3.  Kind of in flux as I keep exploring how best to represent objects and events, and I tend to work on it in bursts, but it's already a playable and winnable (if not terribly exciting) game.


### starbindery

[site](http://starbindery.veekun.com/)

An auto-generated Starbound reference guide.  Not finished yet, but sees a flurry of activity every time the game updates.  Code isn't published because...  well, no particular reason, it just doesn't feel stable or useful yet.


## Dormant

### floof

[code](https://github.com/eevee/floof)

There aren't many sites for hosting artwork, and the ones we have tend to kinda suck.  I'd wanted to build a better one, for a very long time.  I sat down and gave it a decent try, but even with a few other developers chipping in, I realized I didn't have the resources or desire to run the community side of such a thing.

Written in [Python][], using [Pyramid][].


### porigon-z

[code](https://github.com/eevee/porigon-z)

Not quite a library, but a small collection of tools that were useful for extracting information from Pokémon games.  Can parse NARC (a file format commonly used by DS games) and some common formats.  Didn't really catch on outside veekun and is semi-obsoleted by the existence of the 3DS, but still comes in handy on occasion.

Written in [Python][] 2.  Command-line tool.



## Stalled

### sanpera

[docs](http://sanpera.readthedocs.org/en/latest/) · [site?](http://eevee.github.com/sanpera/) · [code](https://github.com/eevee/sanpera) · [pypi](http://pypi.python.org/pypi/sanpera)

I've always been kind of underwhelmed by [PIL](http://www.pythonware.com/products/pil/index.htm), and the Python ecosystem doesn't offer much else for image manipulation.  sanpera is an attempt to breathe some life into this space by providing a high-level, idiomatic Python imaging library that _happens to be_ powered by [ImageMagick][], without exposing you to its travesty of an API.

Working on this turned out to involve far more wrangling of ImageMagick's undocumented corners than useful work, so it didn't get too far.  It does run in production, though, and I may yet pick it back up.


### dywypi

[code](https://github.com/eevee/dywypi)

An attempt at a modern Python IRC bot that does everything "right" — asyncio for networking, an event system, a developer console to avoid the need for live reloading, etc.

It turns out IRC is really hard.


## Miscellaneous

### heteroglot

[code](https://github.com/eevee/project-euler/tree/master/heteroglot) · [blog series](/blog/tags/project-euler/)

Solutions to [Project Euler](http://projecteuler.net/) problems...  all in different programming languages.

The [first blog post](http://me.veekun.com/blog/2012/09/07/heteroglot-number-15-in-cobol/) has an introduction.


## Third party

Not mine, but I've got my fingers in it somewhere.

### pyscss

Reimplementation of [Sass](http://sass-lang.com/), in Python.  ([code](https://github.com/eevee/pyscss))

A former job needed to use this but it was a little neglected, so I put a couple months of effort into heavily refactoring it, fixing bunches of bugs and adding support for newer Sass features.  They're no longer using it and I no longer work there, so I don't touch this so much any more, but it was a great foray into compiler development.


### Mako

A Python templating language.  ([site](http://www.makotemplates.org/) · [code](https://bitbucket.org/zzzeek/mako))

I fixed parsing of dict literals inside interpolations (i.e., `${{"a": "b"}}`), fixed parsing of escaped quotes inside Python blocks (i.e., `<% foo = "\"" %>`), and added support for Python 3's keyword-only arguments in `<%def>` blocks.


### urwid

Python terminal UI library.  ([site](http://urwid.org/) · [code](https://github.com/wardi/urwid))

Added support for using asyncio as the event loop.


### Firefox

I wrote a nitpicky CSS-only patch for a feature you've probably never used.  Hey, it was enough to get me in `about:credits`.


### SLADE

Doom resource and map editor.  ([site](http://slade.mancubus.net/) · [code](https://github.com/sirjuddington/SLADE))

I fixed some crashes, fixed a lot of bugs in geometry drawing, fixed a lot of UI nitpicks, and did most of the implementation of slope support.


### ZDoom

Modern continuation of the Doom engine.  ([site](http://zdoom.org/News) · [code](https://github.com/rheit/zdoom/))

I added support for `TERRAIN`-based damage and friction to 3D floors, fixed texture scaling on 3D floors, and disabled pressing switches embedded in the floor when `checkswitchrange` is on.


### Quixe/Glkote

Web implementation of the glulx interactive fiction engine.  ([quixe site](http://eblong.com/zarf/glulx/quixe/) · [quixe code](https://github.com/erkyrath/quixe) · [glkote site](http://eblong.com/zarf/glulx/quixe/) · [glkote code](https://github.com/erkyrath/quixe))

Wrote an initial implementation of graphic and audio support, though it was sort of absorbed and rewritten by the maintainer.  Helped more concretely with a 2× overall speedup in the VM.


## Wishlist

Haha, well.  I want to give Python a better URI library.  I want to invent a better parser generator language, that's as accessible as regexes.  I want to do things with [Rust][].  I want to create an open source replacement for IRC that preserves the same spirit.  I want to design a programming language.  I want to do a lot of things.  Fingers crossed.



[Cython]: http://cython.org/
[ImageMagick]: http://www.imagemagick.org/script/index.php
[Linode]: http://www.linode.com/
[PostgreSQL]: http://www.postgresql.org/
[Pylons]: http://www.pylonsproject.org/projects/pylons-framework/about
[Pyramid]: http://www.pylonsproject.org/projects/pyramid/about
[Python]: http://www.python.org/
[Rust]: http://www.rust-lang.org/
[Twisted]: http://twistedmatrix.com/trac/
[Ubuntu Linux]: http://www.ubuntu.com/
[gunicorn]: http://gunicorn.org/
[nginx]: http://www.nginx.org/
