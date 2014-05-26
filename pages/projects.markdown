title: Projects
date: 2012-10-16 19:02
comments: true
sharing: false

I like to tinker.  Here are some things I'm tinkering with.  Few of them are finished, but some of them are useful, and all of them would appreciate a pull request...

As a general rule, all of my code [lives on GitHub](https://github.com/eevee), because git is awesome and I am an open source hippie.

This list is not exhaustive, but rather representative of the most interesting things as of the last time I touched it.


## Live

Running in production.  Might still garner improvements, but is "done enough".

* **veekun** — [Live site](http://veekun.com/) · [GitHub](https://github.com/veekun)

    A Pokémon database website, and by far the oldest thing I've built that still exists.  Development waxes and wanes, but the site continues to be useful to people, so it's all good.

    Written in [Python][], powered by [Pylons][], stored in [PostgreSQL][], served by [nginx][] and [gunicorn][] on a [Linode][] running [Ubuntu Linux][].

    The database and various related Python utilities are a separate library, which is [also on GitHub](https://github.com/veekun/pokedex).


* **rc** — [GitHub](https://github.com/eevee/rc)

    My dot files.  Got some stuff for vim, git, tmux, zsh, X, et al. in here.  I like to keep it fairly simple, but it's all pretty well-documented; maybe you'll find something useful in here.


* **kouyou** — [Live site](http://apps.veekun.com/kouyou/) · [GitHub](https://github.com/eevee/kouyou)

    Just a little color picker, because I could never find one that I liked.  (Most of them are HSV, which is unintelligible to me; this one also has HSL.)

    I had a lot of ideas for color-related features, but never needed any of them quite enough to get around to building them.  Still, I use this fairly often for Web design.

    Written in JavaScript.


* **pmde-unflash** — [Live site](http://apps.veekun.com/pmde-unflash/)

    Animations done as Flash-less alternatives for some of the prologues and epilogues of [PMD Explorers](http://pmd-explorers.deviantart.com/).  They will probably not make sense without the tons and tons of existing context.

    Written in JavaScript, with some fun use of prototypes and Deferreds.

## In progress

Not done yet, but I'm hopeful, and I try to devote some time regularly.

* **veekun8** — [Beta site](http://beta.veekun.com/) · [GitHub](https://github.com/veekun/veekun-pokedex)

    I admittedly lost interest in working with the current veekun codebase, and concluded the only way I'd really feel like making significant contributions again would be if I rewrote it all.  So, once again, I'm doing that a bit at a time.  Most of the old Python is perfectly serviceable, and it's been easy enough to move it over a chunk at a time and tidy it up as I go.  The frontend will get a heck of a revamp, though.

    Written in [Python][], powered by [Pyramid][], stored in [PostgreSQL][].  Not in production yet.

    * **archetype** — [GitHub](https://github.com/eevee/archetype)

        Attempt at compiling all the CSS I end up writing for a new project.  Kind of a giant mess right now.  veekun8 is definitely the biggest consumer, and the two are kind of developed in lockstep.

        Written with SCSS.


* **sanpera** — [GitHub](https://github.com/eevee/sanpera) · [Documentation](http://sanpera.readthedocs.org/en/latest/) · [Website?](http://eevee.github.com/sanpera/) · [PyPI](http://pypi.python.org/pypi/sanpera)

    I've always been kind of underwhelmed by [PIL](http://www.pythonware.com/products/pil/index.htm), and the Python ecosystem doesn't offer much else for image manipulation.

    sanpera is an attempt to breathe some life into this space by providing a high-level, idiomatic Python imaging library that _happens to be_ powered by [ImageMagick][].

    (The name is the Hindi term for a snake charmer.  You know, pythons, magic...  ahem.)

    Written mostly in [Cython][].  There's a release, but it's pretty young yet, and I have a lot of ImageMagick battling to do before it's solid and useful.


* **dywypi** — [GitHub](https://github.com/eevee/dywypi)

    A Python IRC bot that tries to do everything "right": an async approach built on [Twisted][], an event system, a developer console to avoid the need for `reload`.


* **clio** — [GitHub](https://github.com/eevee/clio)

    I want to write a roguelike.  I love the feel of NetHack, but it's very dated, and other games don't really play anywhere near the same.

    Not very far along; current blocking on figuring out how to build the kind of component-based trait system I want, and on building a TUI library to actually draw the screen.

    Written in [Rust][].

    * **amulet** — [GitHub](https://github.com/eevee/amulet)

        Rust terminal display library.  Somewhere between the horrors of curses and the undocumented wonders of urwid.  Intended to be able to work as both a light widget library and a simple "print some text in green, if supported" library (a la [blessings](https://pypi.python.org/pypi/blessings)).

        So named because it's a Rusty device intended to save you from curses.


* **mamayo** — [GitHub](https://github.com/eevee/mamayo)

    An attempt at making Python Web deployment (almost) as easy as PHP deployment: upload files and the right thing happens.

    Done for Yelp Hackathon 10, though the idea is much older.  Written in [Python][] and largely powered by [Twisted][].


* **tcup** — [GitHub](https://github.com/eevee/tcup)

    I love [git](http://www.git-scm.com/), but its user experience clearly leaves some things to be desired.  tcup is an attempt to write a complete and compatible replacement for the `git` utility, using `libgit2`.

    A tiny bit is done, but I really want to sit down and figure out a [solid plan](https://github.com/eevee/tcup/wiki/Planning) before I build very far.

    Written in [Rust][].


## Work projects

Still open source, but I have cleverly invented an excuse/reason why I should find an hour or two a week to hack on these at work.

* **pyscss** — [GitHub](https://github.com/eevee/pyscss)

    A SCSS compiler, written in Python.

    pyScss isn't my project, but I'm heavily refactoring it in a fork, attempting to fix some very deep-rooted bugs and add tests and otherwise clean it up.  (It was originally ported from a PHP project that implemented a _different_ CSS preprocessor flavor, so...  I'm sure you can imagine the current state of it.)


* **lurid** — [GitHub](https://github.com/eevee/lurid)

    URI parser, scanner, manipulator class.

    Perl relies _critically_ on its URI.pm module.  Python doesn't have a URI class anywhere!  We just have `urlparse`, which everyone uses independently and slightly differently.  This is ridiculous.

    Currently usable, though the API is about to become radically different, as I had a change of heart regarding mutability.

    Written in (and for ♥) [Python][].


* **splinter** — [GitHub](https://github.com/eevee/splinter)

    This is hard to explain, because for some reason, no one seems to have ever done it.

    The basic idea is to write a highly-opinionated base for content-centric Web apps, then implement several apps atop it as (large) plugins.  The plugins would all be completely independent, but could coexist happily within the same WSGI app, and could define particular ways to interact with each other.

    Think of Trac, except _none_ of the components are required, and they all deserve to stand alone.  Want a bug tracker?  Use only the bug tracker plugin.  Want a pastebin?  Use only the bug tracker plugin.  Want a fansite?  Load up a forum, wiki, image gallery, and oekaki; they'll all share the same set of users and the same login mechanism, and they'll know how to link to each other.

    It's my answer to the Wordpress monopoly.  It's also a ridiculously gigantic undertaking, but would be pretty cool if it worked out.

    Might need to rename to "spline" (the name of my first crack at this concept), because it's come to my attention that a very young testing library named "splinter" already exists for Python.

    Written in [Python][] atop [Pyramid][].  Currently working on this a bit at a time internally, because we have some very dinky and bad internal apps, and they're a good proof-of-concept for the core API and general idea.  Don't think I've pushed any of it for a while.


## Minor distractions

Not quite "real" projects, but things I poke at every so often.

* **heteroglot** — [GitHub](https://github.com/eevee/project-euler/tree/master/heteroglot) · [Blog posts](/blog/tags/project-euler/)

    Solutions to [Project Euler](http://projecteuler.net/) problems...  all in different programming languages.

    The [first blog post](http://me.veekun.com/blog/2012/09/07/heteroglot-number-15-in-cobol/) has an introduction.

    Written in, well, a bit of everything.


## On hold

I yearn to hack these, but they're intractibly blocked on something.

* **flora** — [GitHub](https://github.com/eevee/flora) · [Blog posts](/blog/tags/flora/)

    An adventure game I'm writing along with Mel ([PurpleKecleon](http://purplekecleon.tumblr.com/)) about her homegrown universe of [cats with flowers on their heads](http://purplekecleon.deviantart.com/gallery/308455).

    Currently blocking on our finding a huge chunk of time to devote to it, as well as a potential redesign of how the game fundamentally works.

    Written in [Python][], because why not.


## Future

Gosh, these would be cool to do.  Maybe I should start on them.  In my copious free time.

* **rasp**

    A PEG-based parser-generator for [Rust][], possibly doing all its work at compile time using Rust macros.  Inspired by [Parsley](https://pypi.python.org/pypi/Parsley).


## Dormant

Used to work on these actively, but haven't touched them in a while and have no short-term plans to do so.

* **floof** — [GitHub](https://github.com/eevee/floof) · [Landing page](https://squig.gl/) · ["Beta" site](https://beta.squig.gl/)

    There aren't many art sites, and they tend to kinda suck.  I wanted to build a better one, for a very long time.  I sat down and gave it a decent try, but even with a few other developers chipping in, I realized I didn't have the resources or desire to run the community side of such a thing.

    Written in [Python][], using [Pyramid][].


* **porigon-z** — [GitHub](https://github.com/eevee/porigon-z)

    Not quite a library, but a small collection of tools that were useful for extracting information from Pokémon games.  Can parse NARC (a file format commonly used by DS games) and some common formats.  Didn't really catch on outside veekun and is semi-obsoleted by the existence of the 3DS, but still comes in handy on occasion.

    Written in [Python][].  Command-line tool.




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
