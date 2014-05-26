title: Status, 2011 February wk 3
date: 2011-02-21 09:12:00
tags: veekun, squiggle, puzzles, web
category: status

Mel lives here now, and I want to spend time with her whenever I can, naturally.  This is something I've never had in my life before, and it presents something of a complication.

Weeknights consist of an eight-hour solid block of free time.  I'd usually spend half of that doing absolutely nothing, another hour or two trying to pick up my last-known-state for whatever I wanted to work on, and then finally get a couple hours of actual "work" done.  It was hardly efficient, but it kinda worked.  And this was all a single workflow, to me; the hours of time-passing made for some irrational mental preparation for sitting down and _doing_ something.

Now, though, I don't have solid eight-hour blocks; I'm instead affected by a regular human being's schedule, which includes going out or talking or eating or what-have-you in the middle of the evening.  That free time is now carved into multiple smaller chunks of a few hours each.  For most people, that wouldn't make any difference, but for me those chunks are almost entirely consumed by the time-wasting that _would_ lead up to a context switch.

So, I'm having to learn very quickly to knock this crap off, or I just won't get any work done on anything.  Frustrating in the short term, but certainly beats the...  system I had going before.

<!-- more -->

Let's see, then.

* I applied some OCD design powers to **this blog** again—slightly paler colors, more subtle gradients, fixes for the posts' appearance—and I dislike it substantially less now.  I also rewrote all the Mozilla-specific CSS3 rules to work across every engine that supports them, learning several things in the process:
    1. Webkit now supports the W3C's gradient syntax!  This is fabulous news, as the old syntax they had was _god-awful_.  They have a [blog post about it](http://webkit.org/blog/1424/css3-gradients/).
    2. Gradients with hard edges render horribly in Chromium.  Bit of a downer, since the entire header texture for this design relies on hard-edged gradients.  I filed [a bug](https://bugs.webkit.org/show_bug.cgi?id=54347) which has not yet gotten any response.
* I sorted through and schema-normal-ized most of the Black and White move metadata for **veekun**.  Not really ready to go yet; I have a few move categories that are missing from the canon data, the appearance on move pages is ugly, and I need to redo the move search entirely.  Really hoping to get this out the door by the end of the month, in time for the international release of Black and White.
* I'm trying to give **floof** a central helper class for dealing with "show me this chunk of art", which will take care of paging, default filters, custom user-entered filters, rendering, etc. all in one place.  It's going...  okay, ish.  I think I've descended into some kind of API yak-shaving at this point, and I'm hoping a night's sleep will untangle my brain a little.
* Yet Another IRC Bot **dywypi** is starting to grow a plugin system, though every time it gets half-finished I change my mind and rewrite it all.  It should stabilize pretty soon, and then I can work on replacing my current supybot-powered bot.
  Right now, the current bot relies on having `pokedex.git` checked out and installed, and uses it directly.  This kinda sucks, and keeping it in sync is a pain, so instead I'd like to write a little JSON API for veekun and have the bot use that.  It'd give others something to target, too, without having to figure out my terrible db schema or catch up with massive unpredictable changes to it.
  Essentially I want to do a whole bunch of work that will have no visible effect.  The best kind!
* I got my hands on a bunch of twisty puzzles, which have stolen too much of my attention.  I'm now a proud owner of an order-7 Rubik's cube, which is surprisingly fun to solve, as well as a regular order-3 speed cube (it turns like _lightning_) and a void cube (which is a regular cube with holes straight through where the centers would be).  I may blog about cubing more again sometime, now that it's caught my interest again.  The post will probably be entitled "Fuck Parity Errors".

I cobbled together this whole cool static blog thing, and now I don't know what I want to write in it.  Help me, Internet.

Okay, well, yes, it would help if anyone actually knew this were here.
