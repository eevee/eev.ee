title: Teaching tech
date: 2017-06-10 15:16
category: blog
tags: tech, patreon

A [sponsored post](https://www.patreon.com/eevee) from [Manishearth](https://www.patreon.com/user/creators?u=4520892):

> I would kinda like to hear about any thoughts you have on technical teaching or technical writing. Pedagogy is something I care about. But I don't know how much you do, so feel free to ignore this suggestion :)

Good news: I care enough that I'm trying to write a sorta-kinda-teaching book!

Ironically, one of the biggest problems I've had with writing the introduction to that book is that I keep accidentally rambling on for pages about problems and difficulties with teaching technical subjects.  So maybe this is a good chance to get it out of my system.

<!-- more -->

## Phaser

I recently tried out a new thing.  It was [Phaser](https://phaser.io/), but this isn't a dig on them in particular, just a convenient example fresh in my mind.  If anything, they're better than most.

As you can see from Phaser's website, it appears to have _tons_ of documentation.    Two of the six headings are "LEARN" and "EXAMPLES", which seems very promising.  And indeed, Phaser offers:

- Several getting-started walkthroughs
- Possibly hundreds of examples
- A news feed that regularly links to third-party tutorials
- Thorough API docs

Perfect.  Beautiful.  Surely, a dream.

Well, almost.

The examples are all microscopic, usually focused around a single tiny feature — many of them could be explained just as well with one line of code.  There are a few example games, but they're short aimless demos.  None of them are complete _games_, and there's no showcase either.  Games sometimes pop up in the news feed, but most of them don't include source code, so they're not useful for learning from.

Likewise, the API docs are _just_ API docs, leading to the sorts of problems you might imagine.  For example, in a few places there's a mention of a `preUpdate` stage that (naturally) happens before `update`.  You might rightfully wonder what kinds of things happen in `preUpdate` — and more importantly, what should _you_ put there, and why?

Let's check the API docs for [`Phaser.Group.preUpdate`](https://photonstorm.github.io/phaser-ce/Phaser.Group.html#preUpdate):

> The core preUpdate - as called by World.

Okay, that didn't help too much, but let's check what [`Phaser.World`](https://photonstorm.github.io/phaser-ce/Phaser.World.html#preUpdate) has to say:

> The core preUpdate - as called by World.

Ah.  Hm.  It turns out `World` is a subclass of `Group` and inherits this method — and thus its unaltered docstring — from `Group`.

I did eventually find some brief docs attached to [`Phaser.Stage`](https://photonstorm.github.io/phaser-ce/Phaser.Stage.html#preUpdate) (but only by grepping the source code).  It mentions what the framework uses `preUpdate` for, but not _why_, and not when I might want to use it too.

----

The trouble here is that there's no narrative documentation — nothing explaining how the library is put together and how I'm supposed to use it.  I get handed some brief primers and a massive reference, but nothing in between.  It's like buying an O'Reilly book and finding out it only has one chapter followed by a 500-page glossary.

API docs are great _if you know specifically what you're looking for_, but they don't explain the best way to approach higher-level problems, and they don't offer much guidance on how to mesh nicely with the design of a framework or big library.  Phaser does a decent chunk of stuff for you, off in the background somewhere, so it gives the strong impression that it expects you to build around it in a particular way...  but it never tells you what that way is.


## Tutorials

Ah, but this is what tutorials are for, right?

I confess I recoil whenever I hear the word "tutorial".  It conjures an image of a uniquely useless sort of post, which goes something like this:

1. Look at this cool thing I made!  I'll teach you how to do it too.

2. Press all of these buttons in this order.  Here's a screenshot, which looks nothing like what you have, because I've customized the hell out of everything.

3. You did it!

The author is often less than forthcoming about _why_ they made any of the decisions they did, where you might want to try something else, or what might go wrong (and how to fix it).

And this is to be expected!  Writing out any of that stuff requires far more extensive knowledge than you need just to do the thing in the first place, _and_ you need to do a good bit of introspection to sort out something coherent to say.

In other words, **teaching is hard.**  It's a skill, and it takes practice, and most people blogging are not experts at it.  Including me!

----

With Phaser, I noticed that several of the third-party tutorials I tried to look at were 404s — sometimes less than a year after they were linked on the site.  Pretty major downside to relying on the community for teaching resources.

But I also notice that...  um...

Okay, look.  I **really** am not trying to rag on this author.  I'm not.  They tried to share their knowledge with the world, and _that's a good thing_, something worthy of praise.  I'm glad they did it!  I hope it helps someone.

But for the sake of example, [here is the most recent entry](https://phaser.io/news/2017/06/mike-dangers-tutorial-part-2) in Phaser's [list of community tutorials](https://phaser.io/learn/community-tutorials).  I _have_ to link it, because it's such a perfect example.  Consider:

- The post itself is a bulleted list of explanation followed by a single contiguous 250 lines of source code.  (Not that there's anything wrong with bulleted lists, mind you.)  That code contains zero comments and zero blank lines.

- This is only part two in what I think is a series aimed at beginners, yet the title and much of the prose focus on _object pooling_, a performance hack that's easy to add later and that's almost certainly unnecessary for a game this simple.  There is no explanation of _why_ this is done; the prose only says you'll understand why it's critical once you add a lot more game objects.

- It turns out I only have two things to say here so I don't know why I made this a bulleted list.

In short, it's not really a guided explanation; it's "look what I did".

And that's fine, and it can still be interesting.  I'm not sure English is even this person's first language, so I'm hardly going to criticize them for not writing a novel about platforming.

The trouble is that I doubt a beginner would walk away from this feeling very enlightened.  They _might_ be closer to having the game they wanted, so there's still value in it, but it feels closer to having someone else do it for them.  And an awful lot of tutorials I've seen — particularly of the "post on some blog" form (which I'm aware is the genre of thing I'm writing right now) — look similar.

This isn't some huge social problem; it's just people writing on their blog and contributing to the corpus of written knowledge.  It _does_ become a bit stickier when a large project relies on these community tutorials as its main set of teaching aids.

----

Again, I'm not ragging on Phaser here.  I had a slightly frustrating experience with it, coming in knowing what I wanted but unable to find a description of the semantics anywhere, but I do sympathize.  Teaching is hard, writing documentation is hard, and programmers would usually rather _program_ than do either of those things.  For free projects that run on volunteer work, and in an industry where anything other than programming is a little undervalued, getting good docs written can be tricky.

(Then again, Phaser sells books and plugins, so maybe they could hire a documentation writer.  Or maybe the whole point is for you to buy the books?)


## Some pretty good docs

Python has pretty good [documentation](https://docs.python.org/3/).  It introduces the language with a [tutorial](https://docs.python.org/3/tutorial/index.html), then documents everything else in both a library and language reference.

This sounds an awful lot like Phaser's setup, but there's some considerable depth in the Python docs.  The tutorial is highly narrative and walks through quite a few corners of the language, stopping to mention common pitfalls and possible use cases.  I clicked [an arbitrary heading](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions) and found a pleasant, informative read that somehow avoids being bewilderingly dense.

The API docs also take on a narrative tone — even something as humble as the [`collections` module](https://docs.python.org/3/library/collections.html) offers numerous examples, use cases, patterns, recipes, and hints of interesting ways you might extend the existing types.

I'm being a little vague and hand-wavey here, but it's hard to give specific examples without just quoting two pages of Python documentation.  Hopefully you can see right away what I mean if you just take a look at them.  They're good docs, Bront.

I've likewise always enjoyed the [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/), which follows much the same structure as the main Python documentation.  SQLAlchemy is a database abstraction layer plus ORM, so it can do a _lot_ of subtly intertwined stuff, and the complexity of the docs reflects this.  Figuring out how to do very advanced things correctly, in particular, can be challenging.  But for the most part it does a very thorough job of introducing you to a large library with a particular philosophy and how to best work alongside it.

I softly contrast this with, say, the Perl documentation.

It's gotten better since I first learned Perl, but Perl's docs are still a bit of a strange beast.  They exist as a flat collection of manpage-like documents with terse names like [perlootut](http://perldoc.perl.org/perlootut.html).  The documentation is certainly thorough, but much of it has a strange...  allocation of detail.

For example, [perllol](http://perldoc.perl.org/perllol.html#Growing-Your-Own) — the explanation of how to make a list of lists, which somehow merits its own separate documentation — offers no fewer than _nine_ similar variations of the same code for reading a file into a nested lists of words on each line.  Where Python offers examples for a variety of different problems, Perl shows you a lot of subtly different ways to do the same basic thing.

A similar problem is that Perl's docs sometimes offer far too much context; consider the [references tutorial](http://perldoc.perl.org/perlreftut.html), which starts by explaining that references are a powerful "new" feature in Perl 5 (first released in 1994).  It then explains why you might want to nest data structures...  from a Perl 4 perspective, thus explaining why Perl 5 is so much better.


## Some stuff I've tried

I don't claim to be a great teacher.  I like to talk about stuff I find interesting, and I try to do it in ways that are accessible to people who aren't lugging around the mountain of context I already have.  This being just some blog, it's hard to tell how well that works, but I do my best.

I also know that I learn best when I can _understand_ what's going on, rather than just seeing surface-level cause and effect.  Of course, with complex subjects, it's hard to develop an understanding before you've seen the cause and effect a few times, so there's a balancing act between showing examples and trying to provide an explanation.  Too many concrete examples feel like rote memorization; too much abstract theory feels disconnected from anything tangible.

The attempt I'm most pleased with is probably my [post on Perlin noise]({filename}/2016-05-29-perlin-noise.markdown).  It covers a fairly specific subject, which made it much easier.  It builds up one step at a time from scratch, with visualizations at every point.  It offers some interpretations of what's going on.  It clearly explains some possible extensions to the idea, but distinguishes those from the core concept.

It _is_ a little math-heavy, I grant you, but that was hard to avoid with a fundamentally mathematical topic.  I had to be economical with the background information, so I let the math be a little dense in places.

But the best part about it by far is that _I_ learned a lot about Perlin noise in the process of writing it.  In several places I realized I couldn't explain what was going on in a satisfying way, so I had to dig deeper into it before I could write about it.  Perhaps there's a good guideline hidden in there: don't try to teach as much as you know?

I'm also fairly happy with my series on [making Doom maps]({filename}/2015-12-19-you-should-make-a-doom-level-part-1.markdown), though they meander into tangents a little more often.  It's hard to talk about something like Doom _without_ meandering, since it's a convoluted ecosystem that's grown organically over the course of 24 years and has at least three ways of doing anything.

----

And finally there's the book I'm trying to write, which is sort of about game development.

One of my biggest grievances with game development teaching in particular is how often it leaves out important touches.  Very few guides will tell you how to make a title screen or menu, how to handle death, how to get a Mario-style variable jump height.  They'll show you how to build a clearly unfinished demo game, then leave you to your own devices.

I realized that the only reliable way to show how to build a game is to _build a real game_, then write about it.  So the book is laid out as a narrative of how I wrote my first few games, complete with stumbling blocks and dead ends and tiny bits of polish.

I have no idea how well this will work, or whether recapping my own mistakes will be interesting or distracting for a beginner, but it ought to be an interesting experiment.
