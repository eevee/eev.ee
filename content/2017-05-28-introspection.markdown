title: Introspection
date: 2017-05-28 13:59
category: personal
tags: patreon

This month, IndustrialRobot has [generously donated](https://www.patreon.com/eevee) in order to ask:

> How do you go about learning about yourself? Has your view of yourself changed recently? How did you handle it?

Whoof.  That's incredibly abstract and open-ended — there's a lot I could say, but most of it is hard to turn into words.

<!-- more -->

----

The first example to come to mind — and the most conspicuous, at least from where I'm sitting — has been the transition from _technical_ to _creative_ since quitting my tech job.  I think I touched on this a year ago, but it's become all the more pronounced since then.

I quit in part because I wanted more time to work on my own projects.  Two years ago, those projects included such things as: giving the Python ecosystem a better imaging library, designing an alternative to regular expressions, building a Very Correct IRC bot framework, and a few more things along similar lines.  The goals were all to _solve problems_ — not hugely important ones, but mildly inconvenient ones that I thought I could bring something novel to.  Problem-solving for its own sake.

Now that I had all the time in the world to work on these things, I...  didn't.  It turned out they were almost as much of a slog as my job had been!

The problem, I think, was that there was no _point_.

This was really weird to realize and come to terms with.  I do _like_ solving problems for its own sake; it's interesting and educational.  And most of the programming folks I know and surround myself with have that same drive and use it to create interesting tools like Twisted.  So besides taking for granted that this was the kind of stuff I _wanted_ to do, it seemed like the kind of stuff I _should_ want to do.

But even if I create a really interesting tool, what do I have?  I don't have a _thing_; I have a tool that can be used to _build_ things.  If I want a _thing_, I have to either now build it myself — starting from nearly zero despite all the work on the tool, because it can only do so much in isolation — or convince a bunch of other people to use my tool to build things.  Then they'd be _depending_ on my tool, which means I have to maintain and support it, which is even more time and effort poured into this non-thing.

Despite frequently being drawn to _think_ about solving abstract tooling problems, it seems I truly want to make _things_.  This is probably why I have a lot of abandoned projects boldly described as "let's solve X problem forever!" — I go to scratch the itch, I do just enough work that it doesn't itch any more, and then I lose interest.

I spent a few months quietly flailing over this minor existential crisis.  I'd spent years daydreaming about making tools; what did I have if not that drive?  I was having to force myself to work on what I thought were my passion projects.

Meanwhile, I'd vaguely intended to do some game development, but for some reason dragged my feet forever and then took my sweet time dipping my toes in the water.  I did work on a text adventure, Runed Awakening, on and off...  but it was a fractal of creative decisions and I had a hard time making all of them.  It might've been too ambitious, despite _feeling_ small, and that might've discouraged me from pursuing other kinds of games earlier.

A big part of it might have been the same reason I took so long to even give art a serious try.  I thought of myself as a _technical person_, and art is a thing for _creative people_, so I'm simply disqualified, right?  Maybe the same thing applies to games.

Lord knows I had enough trouble when I tried.  I'd orbited the Doom community for _years_ but never released a single finished level.  I did finally give it a shot again, now that I had the time.  Six months into my funemployment, I wrote a three-part guide on [making Doom levels]({filename}/2015-12-19-you-should-make-a-doom-level-part-1.markdown).  Three months after that, I finally [released one of my own]({filename}/release/2016-03-31-i-made-a-doom-level.markdown).

I suppose that opened the floodgates; a couple weeks later, glip and I decided to try making something for the [PICO-8](http://www.lexaloffle.com/pico-8.php), and then we [did that]({filename}/release/2016-05-25-under-construction-our-pico-8-game.markdown) (almost exactly a year ago!).  Then [kept doing it](https://eevee.itch.io/).

It's been incredibly rewarding — far moreso than any "pure" tooling problem I've ever approached.  Moreso than even something like [veekun](https://veekun.com/), which is a useful _thing_.  People have _thoughts_ and _opinions_ on games.  Games give people _feelings_, which they then tell you about.  Most of the commentary on a reference website is that something is missing or incorrect.

_I like doing creative work._  There was never a singular moment when this dawned on me; it was a slow process over the course of a year or more.  I probably should've had an inkling when I started drawing, half a year before I quit; even my early (and very rough) daily comics made people laugh, and I liked that a lot.  Even the most well-crafted software doesn't tend to bring _joy_ to people, but amateur art can.

I still like doing technical work, but I prefer when it's a means to a creative end.  And, just as important, I prefer when it has a clear and constrained scope.  "Make a library/tool for X" is a nebulous problem that could go in a great many directions; "make a bot that tweets Perlin noise" has a pretty definitive finish line.  It was interesting to write a little physics engine, but I would've hated doing it if it weren't for a game I were making and didn't have the clear scope of "do what I need for this game".

----

It feels like creative work is something I've been wanting to do for a long time.  If this were a made-for-TV movie, I would've discovered this impulse one day and immediately revealed myself as a natural-born artistic genius of immense unrealized talent.

That didn't happen.  Instead I've found that even something as mundane as _having ideas_ is a skill, and while it's one I enjoy, I've barely ever exercised it at all.  I have plenty of ideas with technical work, but I run into brick walls _all the time_ with creative stuff.

How do I theme this area?  Well, I don't know.  How do I think of something?  I don't know that either.  It's a strange paradox to have an urge to create things but not quite know what those things are.

It's such a new and completely different kind of problem.  There's no right answer, or even an answer I can check for "correctness".  I can do _anything_.  With no landmarks to start from, it's easy to feel completely lost and just draw blanks.

I've essentially recalibrated the _texture_ of stuff I work on, and I have to find some completely new ways to approach problems.  I haven't found them yet.  I don't think they're anything that can be told or taught.  But I'm starting to get there, and part of it is just _accepting_ that I can't treat these like problems with clear best solutions and clear algorithms to find those solutions.

A particularly glaring irony is that I've had a really tough problem designing abstract spaces, even though that's exactly the kind of architecture I praise in Doom.  It's much trickier than it looks — a good abstract design is _reminiscent_ of something without quite _being_ that something.  

I suppose it's similar to a struggle I've had with art.  I'm drawn to a cartoony style, and cartooning is also a mild form of abstraction, of whittling away details to leave only what's most important.  I'm reminded in particular of the forest background in fox flux — I was completely lost on how to make something _reminiscent_ of a tree line.  I knew enough to know that drawing trees would've made the background far too busy, but trees are _naturally busy_, so how do you represent that?

The answer glip gave me was to make [big chunky leaf shapes](https://github.com/eevee/fox-flux/blob/059bf95e6a038bcf0f387965e5acdeab6e1ff47e/assets/images/landscape.png) around the edges and where light levels change.  Merely overlapping those shapes implies depth well enough to convey the overall shape of the tree.  The result works very well and looks very simple — yet it took a lot of effort just to get to the _idea_.

It reminds me of mathematical research, in a way?  You know the general outcome you want, and you know the tools at your disposal, and it's up to you to make some creative leaps.  I don't think there's a way to directly learn how to approach that kind of problem; all you can do is look at what others have done and let it fuel your imagination.

----

I think I'm getting a little distracted here, but this is stuff that's been rattling around lately.

If there's a more personal meaning to the tree story, it's that this is a thing _I can do_.  I can learn it, and it makes sense to me, despite being a huge nerd.

Two and a half years ago, I never would've thought I'd ever make an entire game from scratch _and do all the art for it_.  It was completely unfathomable.  Maybe we can do a lot of things we don't expect we're capable of, if only we give them a serious shot.

And ask for help, of course.  I have a hell of a time doing that.  I did a [painting](https://twitter.com/eevee/status/867960854611763200) recently that factored in _mountains_ of glip's advice, and on some level I feel like I didn't quite do it myself, even though every stroke was made by my hand.  Hell, I don't even look at references nearly as much as I should.  It feels like cheating, somehow?  I know that's ridiculous, but my natural impulse is to put my head down and figure it out myself.  Maybe I've been doing that for too long with programming.  Trust me, it doesn't work quite so well in a brand new field.

----

I'm getting distracted again!

To answer your _actual_ questions: how do I go about learning about myself?  I don't!  It happens completely by accident.  I'll consciously examine my surface-level thoughts or behaviors or whatever, sure, but the _serious fundamental revelations_ have all caught me completely by surprise — sometimes slowly, sometimes suddenly.

Most of them also came from listening to the people who observe me from the outside: I only started drawing in the first place because of some ridiculous deal I made with glip.  At the time I thought they just wanted everyone to draw because art is _their thing_, but now I'm starting to suspect they'd caught on after eight years of watching me lament that I couldn't draw.

I don't know how I _handle_ such discoveries, either.  What _is_ handling?  I imagine someone discovering something and trying to come to grips with it, but I don't know that I have quite that experience — my grappling usually comes earlier, when I'm still trying to figure the thing out despite not knowing that there's a thing to find out.  Once I know it, it's on the table; I can't un-know it or reject it meaningfully.  All I can do is figure out what to do with it, and I approach that the same way I approach every other problem: by flailing at it and hoping for the best.

This isn't quite 2000 words.  Sorry.  I've run out of things to say about me.  This paragraph is very conspicuous filler.  Banana.  Atmosphere.  Vocation.
