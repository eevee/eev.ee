title: Weekly roundup: slow but steady
date: 2016-08-14 20:03
category: dev
tags: status, runed awakening, veekun

August is loosely about **video games**, but really it's about [three big things in particular]({filename}2016-08-07-weekly-roundup-three-big-things.markdown).

- **book**: Lots of progress!  I'm definitely getting a feel for the writing style I want to use, I've wrangled Sphinx into a basically usable state, I've written a lot of tentative preface stuff and much of the intro part of the chapter, and I've written a _ton_ of scratchy prose (like notes, but full sentences that just need some editing and cleanup later).  Also worked around some frequent crashes with, ah, a thing I'm writing about.

- **veekun**: I did a serious cleanup of the gen 1 extraction code; added some zany heuristics for detecting data that should work even in fan hacks (if there even are any for gen 1); and hacked multi-language extraction into working well enough for starters.

    Finally, and I do mean _finally_, I built some groundwork for versioning support in the Python API.  This has been hanging over my head for probably a year and was one of the biggest reasons I kept putting off working on this whole concept.  I just didn't quite know how I wanted to do it, and I was terrified of doing it "wrong".  At long last, yesterday I pushed through, and now I can see the light at the end of the tunnel.

    I also committed what I had so far, which is a complete mess but also a _working_ mess, and that makes me feel better about the state of things.  You can [have a look if you want](https://github.com/veekun/pokedex/tree/yaml).

- **runed awakening**: I didn't get any _tangible_ work done, but after some months of agonizing, I _finally_ figured out how to make the ending sensible.  Mostly.  Like 80%.  I'm much closer than I used to be.  Once I nail down a couple minor details, I should be able to go _actually build it_.

----

- **blog**: I finally fixed veekun's front page — the _entire contents_ of blog posts will no longer appear there.  (The actual problem was that Pelican, the blog generator I use, puts the entirety of blog posts in Atom's `<summary>` field and wow is that wrong.  I've [submitted a PR](https://github.com/getpelican/pelican/pull/1989) and patched my local install.)

    I wrote about half a post on testing, which I'd really like to finish today.

- **zdoom**: My Lua branch can now list out an actor's entire inventory — the first capability that's actually _impossible_ using the existing modding tools.  (You can check how many of a particular item an actor is carrying, but there's no way to iterate over a list of strings from a mod.)

- **doom**: Almost finished my anachrony demo map, but stopped because I wasn't sure how to show off the last couple things.  Fixed a couple items that had apparently been broken the entire time, whoops.

- **slade**: I added the most half-assed stub of a list of all the things in the current map and how many there are on each difficulty.  I vaguely intend to make a whole map info panel, and I still need to finish 3D floors; I just haven't felt too inclined to pour much time into SLADE lately.  Both C++ and GUI apps are a bit of a slog to work with.

- **art**: I scribbled [Latias with a backpack](https://lexyeevee.tumblr.com/post/148659933187) and [some other things](https://lexyeevee.tumblr.com/post/148960080152/oh-yeah-so-here-are-some-other-doodly-things-i).

    I did _two_ [daily Pokémon](https://lexyeevee.tumblr.com/tagged/daily-pok%C3%A9mon), which is, at least, better than one.  I think they're getting better, but I also think I'm just trying to draw more than I know how to do in an hour.

    I hit a skill wall this week, where my own expectations greatly outpaced my ability.  It happens every so often and it's always maddening.  I spent a lot of time sketching and looking up refs (for once) and eventually managed to pierce through it — somehow I came out with a markedly improved understanding of general anatomy, hands, color, perspective, and lighting?  I don't know how this works.  The best thing I drew is not something I'll link here, but you can enjoy [this](https://lexyeevee.tumblr.com/post/148958794787/squishfox-hanging-out-with-nine-doodles) which is pretty good too.  Oh, I guess I did a semi-public art stream for the first time  this week, too.

    Now my arm is tired and the callus where I grip the pen too hard is a bit sore.

- **irl**: Oh boy I got my oil changed?  Also I closed a whole bunch of tabs and went through some old email again, in a vain attempt to make my thinkin' space a bit less chaotic.

Wow!  A lot of things again.  That's awesome.  I really don't know where I even found the time to do quite so much drawing, but I'm not complaining.

I'm a _little_ panicked, since we're halfway through the month and I don't think any of the things I'm working on are half done yet.  I did try to give myself a lot of wiggle room in the October scheduling, and it's still early, so we'll see how it goes.  I can't remember the last time I was quite this productive for this long continuously, so I'm happy to call this a success so far either way.
