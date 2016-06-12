title: One year later
date: 2016-06-12
category: blog
tags: tech, personal

A year ago today was my [last day working a tech job](/blog/2015/06/09/i-quit-the-tech-industry/).

<!-- more -->

## What I didn't do

I think I spent the first few months in a bit of a daze.  I have a bad habit of expecting worst case scenarios, so I was in a constant state of mild panic over whether I could really earn enough to support myself.  Not particularly conducive to _doing things_.

There was also a very striking change in...  people scenery?  Working for a tech company, even remotely, meant that I spent much of my time talking to a large group of tech-minded people who knew the context behind things I was working on.  Even if they weren't the things I wanted to be working on, I could at least complain about an obscure problem and expect to find someone who understood it.

Suddenly, that was gone.  I know some tech people, of course, and have some tech followers on Twitter, but those groups are much more heterogenous than a few dozen people all working on the same website.  It was a little jarring.

And yet, looking back, I suspect that feeling had been fading for some time.  I'd been working on increasingly obscure projects for Yelp, which limited how much I could really talk to anyone about them.  Towards the end I was put on a particularly thorny problem just because I was the only person who knew anything about it at all.  I spent a few weeks hammering away at this thing that zero other people understood, that I barely understood myself, that I didn't much enjoy doing, and that would ultimately just speed deployments up by a few minutes.

Hm.

When I left, I had a lot of ideas for the kinds of things I wanted to do with all this newfound free time.  Most of them were "pure" programming ideas: design and implement a programming language, build a new kind of parser, build a replacement for IRC, or at least build a little IRC bot framework.

I ended up doing...  none of those!  With more time to do things, rather than daydream restlessly about doing things, I discovered that building libraries and infrastructure is incredibly tedious and unrewarding.  (For me, I mean.  If that's your jam, well, I'm glad it's someone's.)

I drifted for a little while as I came to terms with this, trying to force myself to work on these grandiose dreams.  Ultimately, I realized that I most enjoy programming when it's a means to an end, when there's a goal beyond "write some code to do this".  Hence my recent tilt towards game development, where the code is just one part of a larger whole.

And, crucially, that larger whole is something that _everyone_ can potentially enjoy.  The difference has been night and day.  I can tweet a screenshot of a _text adventure_ and catch several people's interest.  On the other hand, a Python library for resizing images?  Who cares?  It's not a complete _thing_; it's a building block, a tool.  At worst, no one ever uses it, and I have nothing to show for the time.  Even at best, well...  let's just say the way programmers react to technical work is very different from the way everyone else reacts to creative work.

I do still like building libraries on occasion, but my sights are much smaller now.  I may pick up sanpera or dywypi again, for instance, but I think that's largely because other people are already using them to do things.  I don't have much interest in devoting months to designing and building a programming language that only a handful of PLT nerds will even look at, when I could instead spend a day and a half making [a Twitter bot that posts random noise](https://twitter.com/perlin_noise) and immediately have multiple people tell me it's relaxing or interesting.

In short, I've learned a lot about what's important to me!

Ah, yes, I also thought I would've written a book by now.  I, uh, haven't.  Writing a book apparently takes a lot more long-term focus than I tend to have available.  It also requires enough confidence in a single idea to write tens of thousands of words about it, and that doesn't come easily either.  I've taken a lot of notes, written a couple short drafts, and picked up a bit of TeX, so it's still on the table, but I don't expect any particular timeframe.


## What I did do

Argh, this is going to overlap with my birthday posts.  But:

I **wrote** a whopping 43 blog posts, totalling just over 160,000 words.  That's two or three novels!  Along the way, my [Patreon](https://www.patreon.com/eevee) has more than tripled to a level that's, well, more reassuring.  **Thank you so much**, everyone who's contributed — I can't imagine a better compliment than discovering that people are willing to directly pay me to keep writing and making whatever little strange things I want.

I **drew** a hell of a lot.  My progress has been documented [elsewhere](/blog/2016/05/06/learning-to-draw-learning-to-learn/), but suffice to say, I've come a long way.  I also expanded into a few new media over this past year: watercolors, pixel art, and even a teeny bit of animation.

I made some **games**.  The release of Mario Maker was a really nice start — I could play around with level design ideas inside a world with established gameplay and [let other people play them](/everything/tags/mario-maker/) fairly easily.  Less seriously, I made [Don't Eat the Cactus](https://c.eev.ee/dont-eat-cactus/), which was microscopic but ended up entertaining a surprising number of people — that's made me rethink my notions of what a game even needs to _be_.  [I made a Doom level](/blog/2016/03/31/i-made-a-doom-level/), and released it, for the first time.  Most recently, of course, Mel and I made [Under Construction](/blog/2016/05/25/under-construction-our-pico-8-game/), a fully-fledged little pixel game.  I've really enjoyed this so far, and I have several more small things going at the moment.

The elephant in the room is perhaps **Runed Awakening**, the text adventure I started almost two years ago.  It was supposed to be a small first game, but it's spiraled a little bit out of hand.  Perhaps I underestimated text adventures.  A year ago, I wasn't really sure where the game was going, and the ending was vague and unsatisfying; now there's a clear ending, a rough flow through the game, and most importantly enough ideas to see it through from here.  I've rearchitected the entire world, added a few major NPCs, added core mechanics, added scoring, added a little reward for replaying, added several major areas, implemented some significant puzzles, and even made an effort to illustrate it.  There's still quite a lot of work left, but I enjoy working on it and I'm excited about the prospect of releasing it.

I did more work on **SLADE** while messing around with Doom modding, most notably adding support for ZDoom's myriad kinds of slopes.  I tracked down and fixed _a lot_ of bugs with editing geometry, which is a really interesting exercise and a challenging problem, and I've fixed dozens of little papercuts.  I've got a few major things in progress still: support for 3D floors is maybe 70% done, support for lock types is about 70% done.  Oh, yes, and I started on a static analyzer for scripts, which is a fantastic intersection of "pure programming" and "something practical that people could make use of".  That's maybe 10% done and will take a hell of a lot of work, but boy would it be great to see.

I improved **spline** (the software powering [Floraverse](http://floraverse.com/)) more than I'd realized: arbitrarily-nested folders, multiple media per "page", and the revamped archives were all done this past year.  I used the same library to make Mel a [simple site](http://glitchedpuppet.com/), too.  It's still not something I would advise other people run, but I did put a modicum of effort into documenting it and cleaning up some general weirdness, and I made my own life easier by migrating everything to runit.

**veekun** has languished for a while, but fear not, I'm still working on it.  I wrote brand new code to dump (most of) RBY from scratch, using a YAML schema instead of a relational database, which has grown increasingly awkward to fit all of Pokémon's special cases into.  I still hope to revamp the site based on this idea in time for Sun and Moon.  I also spent a little time modernizing the `pokedex` library itself, most notably making it work with Python 3.

I wrote some **other code**, too.  [Camel](/blog/2015/10/15/dont-use-pickle-use-camel/) was an idea I'd had for a while, and I just sat down and wrote it over the course of a couple days, and I'm glad I did.  I rewrote [PARTYMODE](https://c.eev.ee/partymode-demo/).  I did another round of [heteroglot](/blog/2016/01/12/heteroglot-number-16-in-pascal-number-17-in-inform7/).  I fixed some bugs in ZDoom.  I sped [Quixe](https://github.com/erkyrath/quixe) (a JavaScript interpreter for some text adventures) up by 10% across the board.  I wrote some [weird Twitter bots](/projects/#twitter-bots).  I wrote a lot of one-off stuff for various practical purposes, some of it abandoned, some of it used once and thrown away.

Is that a lot?  It doesn't even feel like a lot.  I want to do just as much again by the end of the year.  I guess we'll see how that goes.


## Some things people said

Not long after my original post made the rounds, I was contacted by a Vox editor who asked if I'd like to expand my post into an article.  A _paid_ article!  I thought that sounded fantastic, and could even open the door to more paid writing.  I spent most of a week on it.

It went up with the title "I'm 28, I just quit my tech job, and I never want another job again" and a hero image of fists slamming a keyboard.  I hadn't been asked or told about either, and only found out by seeing the live page.  I'd even given my own title; no idea what happened to that, or to the byline I wrote.

I can't imagine a more effective way to make me sound like a complete asshole.  I barely remember how the article itself was phrased; I could swear I tried to adapt to a broader and less personal audience, but I guess I didn't do a very good job, and I'm too embarrassed to go look at it now.

I found out very quickly, via some heated Twitter responses, that it looks _even worse_ without the context of "I wrote this in my blog and Vox approached me to publish it".  It hadn't even occurred to me that people would assume writing an article for a news website had been _my_ idea, but of course they would.  Whoops.  In the ensuing year, I've encountered one or two friends of friends who proactively blocked me just over that article.  Hell, I'd block me too.

I don't think I want to do any more writing where I don't have final editorial control.

I bring this up because there have been some wildly differing reactions to what I wrote, and Vox had the most drastic divide.  A lot of people were snarky or angry.  But just as many people contacted me, often privately, to say they feel the same way and are hoping to quit their jobs in the future and wish me luck.

It's the money, right?  You're not supposed to talk about money, but I'm an idiot and keep doing it anyway.

I don't want anyone to feel bad.  I tried, actively, not to say anything wildly insensitive, in both the original post and the Vox article.  I know a lot of people hate their jobs, and I know most people can't afford to quit.  I wish everyone could.  I'd love to see a world where everyone could do or learn or explore or make all the things they wanted.  Unfortunately, my wishes have no bearing on how the system works.

I suspect...  people have expectations.  The American Dream™ is to get a bunch of money, at which point you _win_ and can be happy forever.

I had a cushy well-paying job, and I wasn't happy.  That's not how it's supposed to work.  Yet if anything, the money made me _more_ unhappy, by keeping me around longer.

People like to quip that money can't buy happiness.  I think that's missing the point.  Money can _remove sadness_, but only if that sadness is related to not having enough money.  My problem was not having enough _time_.

I was tremendously lucky to have stock options and to be able to pay off the house, but those things cancelled each other out.  The money was finite, and I spent it all at once.  Now it's gone, and I still have bills, albeit fewer of them.  I still need to earn income, or I'll run out of money for buying food and internets.

I make considerably less now.  I'm also much, much happier.

----

I don't know why I feel the need to delve so deeply into this.  The original post happened to hit lobste.rs a few days ago, and there were a couple "what a rich asshole" comments, which reminded me of all this.  They were subtly weird to read, as though they were about an article from a slightly different parallel universe.  I was reminded that many of the similar comments from a year ago had a similar feel to them.

If you think I'm an asshole because I've acted like an asshole, well, that's okay.  I try not to, and I'll try to be better next time, but sometimes I fuck up.

If you think I'm an asshole because I pitched a whiny article to Vox about how one of the diamond lightbulbs in my Scrooge McDuck vault went out, damn.  It bugs me a little to be judged as a caricature with little relation to what I've actually done.


## To the people who ask me for advice

Here's a more good comment:

> > The first week was relaxing, productive, glorious. Then I passed the midpoint and saw the end of my freedom looming on the horizon. Gloom descended once more.
> 
> I thought I was the only one, who felt like this. I see myself in everything \[they\] describe. I just don’t have the guts to try and sell my very own software as a full time thing.
> 
> > I like to liberally license everything I do, and I fucking hate advertising and will never put it on anything I control
> 
> It’s almost as if that \[person\] is me, with a different name, and cuter website graphics.

First of all, thank you!  I have further increased the cuteness of my website graphics since this comment.  I hope you enjoy.

I've heard a lot of this over the past year.  _A lot._  There are a shocking number of people in tech who hate being in tech, even though we all get paid in chests full of gold doubloons.

A decent number of them also asked for my input.  What should they do?  Should they also quit?  Should they switch careers?

I would like to answer everyone, once and for all, by stressing that _I have no idea what I'm doing._  I don't know anything.  I'm not a renowned expert in job-quitting or anything.

I left because, ultimately, I had to.  I was utterly, utterly exhausted.  I'd been agonizing over it for almost a _year_ prior, but had stayed because I didn't think I could pull it off.  I was terrified of failure.  Even after deciding to quit, I'd wanted to stay another six months and finish out the year.  I left when I did because I was _deteriorating_.

I hoped I could make it work, Mel told me I could make it work, and I had some four layers of backup plans.  I still might've failed, and every backup plan might've failed.  I didn't.  But I could've.

I can't tell you whether it's a good decision to quit your job to backpack through Europe or write that screenplay you've always wanted to write.  I could barely tell _myself_ whether this was a good idea.  I'm not sure I'd admit to it even now.  I can't decide your future for you.

On the other hand...

On the other hand, if you're just looking for someone to tell you what you want to hear, what you've already decided...

Well, let's just say you'd know better than I would.
