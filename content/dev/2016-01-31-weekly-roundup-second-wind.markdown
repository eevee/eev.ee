title: Weekly roundup: second wind
date: 2016-01-31 03:55
category: dev
tags: status, spline, doom

January's theme is **web dev**, and the major project is **spline**, the thing that runs [Floraverse](http://floraverse.com/).

I had a lot of stuff to do that I sort of left to the very last minute, as I am wont to do, so I've been rushing to actually do some of it.

- **art**: [The usual](http://lexyeevee.tumblr.com/tagged/daily-comic).  Bit lazier with them this week, since I've been busy with not-art, but now I miss it!

- **spline**: Got image embedding working in the blog editor.  Cleaned up a few places I was writing values into JavaScript in templates.  Vendored archetype into a submodule, rather than hardcoding (!) a relative path to it.  Migrated the clumsy generated Pyramid script to a CLI you can just run with `-m`, and added a command for creating a new user manually.  Added front-page support to the blog.

- **SLADE**: Submitted a pull request full of some old papercuts.  Finished a branch that fixes and extends the Boom generalized labels for most specials' speed args.  Fixed one or two new papercuts.

- **doom**: Sifted through a bunch of Realm 667 resources looking for some neat gems.  Toyed with weapons and powerups and monsters, with a few interesting results.  Eventually I'd like to sit down and actually make a map, but this is the kind of thing I can do for an hour or two, and it's interesting to try balancing extensions to the vanilla gameplay.

- **quixe**: I read about [Lectrote](http://gameshelf.jmac.org/2016/01/introducing-lectrote-an-interpreter/), Andrew Plotkin's IF interpreter that just bundles Quixe with a Chrome renderer, the same way Atom works.  I'm not a huge fan of this approach usually, but IF requires support for a few layout tricks that are most easily accomplished with an HTML renderer anyway, so it makes some sense.  Anyway, the post mentions that one of the concerns is speed, so I was inspired to go optimization-hunting, and I found an improvement of about 10% across the board.  My benchmark story ([Counterfeit Monkey by Emily Short](http://emshort.com/counterfeit_monkey/), which is absolutely massive and does a ton of work at startup) still takes more than ten seconds just to load, but this is a vast improvement over the thirty seconds it took when I first started hacking on Quixe.

- **twitter**: I improved my bot [@flareon\_favbots](https://twitter.com/flareon_favbots) a little — it now reports offenders for spam, and makes an effort to tweet more than just when it's first run.  It's blocked another hundred or so fav-spammers in the last few days!

- **veekun**: Ported the CLI to `argparse`; previously it was `optparse` plus a lot of manual mucking about.  Also started on a stub of a search interface built right into the `pokedex` library.

- **book**: Started taking serious notes on a book about computer stuff.

- **blog**: Started writing a post about, ah, writing.

- **flora**: Created a stub of a repo for Mel's personal site.

Hey, that's not a bad haul.  Still more to do, as always, but I'm making a dent and finally have some momentum back.
