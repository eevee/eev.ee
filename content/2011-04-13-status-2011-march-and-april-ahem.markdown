title: Status, 2011 March...  and April...  ahem
date: 2011-04-13 18:56:00
tags: veekun, squiggle, dywypi
category: status

Just as I sit down to actually blog something, I see the first gigantic spider of the summer on my wall, and have to run away screaming like a little girl.  The universe doesn't want me to write!  (Let's pretend every other week for the past six was stalled by _way more_ spiders.)

<!-- more -->

* I fixed excerpts on **ye olde blog**, so more than a sentence appears on the front page.  Hurrah.

* **veekun** has consumed most of my time, and probably put me in a horrible slump for a while.  I've crawled back out of my hole at last, again, and am delighted to be excited about building things.

    * The Pokédex database schema was rewritten to support spitting out pages in any supported language, and I got all nitpicky about the way it was done and decided to fix it up "real quick".  Cue two weeks of mucking about with SQLAlchemy wizardry.  At the same time I was stubbornly refusing to learn that I cannot, in fact, get much work of note done while chilling with my tiny laptop on Mel's bed watching her draw.  This has been a hard-won dual victory.

    * A lot of crap broke because of this change.  I fixed most of it, maybe.

    * Black and White items grew some effects, and I rewrote some of the old effects (with syntax that no longer works).

    * And honestly that was most of it.  Some little things were fixed or improved, and there was some whole mess with move metadata, but not much user-facing of note.

    I intend to break the media (200+ MB of ripped sprites, official art, etc.) out of the repository tonight, and consolidate the proliferation of littler repositories for various parts of the site.  This will break everything _again_, but it's been a long time coming and will be an improvement overall.  Then I'll finally have all the major bottlenecks out of the way, and I can start working on the lengthy list of interesting ideas I've accumulated over the past month.

* Less activity on **floof**, which is unfortunate, but I'm trying to give it some TLC lately.  I did finish the whole art browsing thing, and now I'm trying to make [MogileFS][] play nicely with Python.  I read a few articles targeted at startups over the past couple weeks, and despite my meticulous launch plan, I'm convinced that I should just get the thing working and "launch" it.  Maybe not advertise much for a while, but I figure a half-working site with some users is better than no site at all.

* I read a lot of stuff about [Twisted][], and I have a decent grasp of how it works.  **dywypi 2.0** is thus coming along decently, and shouldn't take too much more work before it can replace the `dywypi` currently sitting in my channel.

Both at work and while working on dywypi, I've learned that I am really _really_ bad at architecture design.  I resist actually writing anything until I have a decent idea of how it works, but I don't really have a good grasp of how something works until it's being used, so I end up twiddling my thumbs and jotting down endless notes for far too long.  And then what I actually implement ends up being inappropriate anyway.

The only cure seems to be acknowledging that this is a problem, being willing to refactor, and writing something that works before all else.  Premature generalization wastes as much time as premature optimization.

[MogileFS]: http://code.google.com/p/mogilefs/wiki/Start
[Twisted]: http://twistedmatrix.com/trac/
