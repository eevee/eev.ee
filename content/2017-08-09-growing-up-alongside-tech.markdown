title: Growing up alongside tech
date: 2017-08-09 08:18
category: articles
tags: patreon

[IndustrialRobot](https://www.patreon.com/user/creators?u=199476) asks...  or, uh, asked last month:

> industrialrobot: How has your views on tech changed as you've got older?

This is so open-ended that it's actually stumped me for a solid month.  I've had a surprisingly hard time figuring out where to even start.

<!-- more -->

----

It's not that my views of tech have changed too _much_ — it's that they've changed very _gradually_.  Teasing out and explaining any one particular change is tricky when it happened invisibly over the course of 10+ years.

I think a better framework for this is to consider how my _relationship_ to tech has changed.  It's gone through three pretty distinct phases, each of which has strongly colored how I feel and talk about technology.


## Act I

In which I start from nothing.

_Nothing_ is an interesting starting point.  You only really get to start there once.

Learning something on my own as a kid was something of a magical experience, in a way that I don't think I could replicate as an adult.  I liked computers; I liked toying with computers; so I did that.

I don't know how universal this is, but when I was a kid, I couldn't even _conceive_ of how incredible things were made.  Buildings?  Cars?  Paintings?  Operating systems?  Where does any of that come from?  Obviously _someone_ made them, but it's not the sort of philosophical point I lingered on when I was 10, so in the back of my head they basically just appeared fully-formed from the æther.

That meant that when I started trying out programming, I had _no aspirations_.  I couldn't imagine how far I would go, because all the _examples_ of how far I would go were completely disconnected from any idea of human achievement.  I started out with [BASIC on a toy computer]({filename}/2016-04-05-my-first-computer.markdown); how could I possibly envision a connection between that and something like a mainstream video game?  Every new thing felt like a new form of magic, so I couldn't conceive that I was even in the same ballpark as whatever process produced _real_ software.  (Even seeing the source code for `GORILLAS.BAS`, it didn't quite click.  I didn't think to try _reading_ any of it until years after I'd first encountered the game.)

This isn't to say I didn't have _goals_.  I invented goals constantly, as I've always done; as soon as I learned about a new thing, I'd imagine some ways to use it, then try to build them.  I produced a lot of little weird goofy toys, some of which entertained my tiny friend group for a couple days, some of which never saw the light of day.  But none of it felt like steps along the way to some mountain peak of mastery, because I didn't realize the mountain peak was even a place that could be gone to.  It was pure, unadulterated (!) playing.

I contrast this to my art career, which started only a couple years ago.  I was already in my late 20s, so I'd already spend decades _seeing_ a very broad spectrum of art: everything from quick sketches up to painted masterpieces.  And I'd seen the _people_ who create that art, sometimes seen them create it in real-time.  I'm even in a relationship with one of them!  And of course I'd already had the experience of advancing through tech stuff and discovering first-hand that even the most amazing software is still _just code someone wrote_.

So from the very beginning, from the moment I touched pencil to paper, I _knew_ the possibilities.  I _knew_ that the goddamn Sistine Chapel was something I could learn to do, if I were willing to put enough time in — and I knew that I'm not, so I'd have to settle somewhere a ways before that.  I _knew_ that I'd have to put an awful lot of work in before I'd be producing anything very impressive.

I did it anyway (though perhaps waited longer than necessary to start), but those aren't things I can _un-know_, and so I can never truly explore art from a place of pure ignorance.  On the other hand, I've probably [learned to draw]({filename}/2016-05-06-learning-to-draw-learning-to-learn.markdown) much more quickly and efficiently than if I'd done it as a kid, precisely _because_ I know those things.  Now I can decide I want to do something far beyond my current abilities, then go figure out how to do it.  When I was just _playing_, that kind of ambition was impossible.

----

So, I played.

How did this affect my views on tech?  Well, I didn't...  _have_ any.  Learning by playing tends to teach you things in an outward sprawl without many abrupt jumps to new areas, so you don't tend to run up against conflicting information.  The whole point of opinions is that they're your own resolution to a conflict; without conflict, I can't meaningfully say I had any opinions.  I just accepted whatever I encountered at face value, because I didn't even know enough to suspect there could be alternatives yet.


## Act II

That started to seriously change around, I suppose, the end of high school and beginning of college.  I was becoming aware of this whole "open source" concept.  I took classes that used languages I wouldn't otherwise have given a second thought.  (One of them was Python!)  I started to contribute to other people's projects.  Eventually I even got a job, where I _had_ to work with _other people_.  It probably also helped that I'd had to maintain my own old code a few times.

Now I was faced with conflicting subjective ideas, and I had to form opinions about them!  And so I did.  With _gusto_.  Over time, I developed an idea of what was _Right_ based on experience I'd accrued.  And then I set out to always do things _Right_.

That's served me decently well with some individual problems, but it also led me to inflict a lot of unnecessary pain on myself.  Several endeavors languished for no other reason than my dissatisfaction with the _architecture_, long before the basic functionality was done.  I started a number of "pure" projects around this time, generic tools like imaging libraries that I had no direct need for.  I built them for the sake of them, I guess because I felt like I was improving some niche...  but of course I never finished any.  It was always in areas I didn't know that well in the first place, which is a fine way to learn if you have a specific concrete goal in mind — but it turns out that building a generic library for editing images means you have to know _everything_ about images.  Perhaps that ambition went a little haywire.

I've said [before]({filename}/2016-06-12-one-year-later.markdown) that this sort of (self-inflicted!) work was unfulfilling, in part because the best outcome would be that a few distant programmers' lives are slightly easier.  I do still think that, but I think there's a deeper point here too.

In forgetting how to play, I'd stopped putting any of _myself_ in most of the work I was doing.  Yes, building an imaging library is kind of a slog that _someone_ has to do, but...  I assume the people who work on software like PIL and ImageMagick are _actually interested in it_.  The few domains I tried to enter and revolutionize weren't _passions_ of mine; I just happened to walk through the neighborhood one day and decided I could obviously do it better.

Not coincidentally, this was the same era of my life that led me to write stuff like that PHP post, which you may notice I am conspicuously not even linking to.  I don't think I would write anything like it nowadays.  I could see myself approaching the same _subject_, but purely from the point of view of language design, with more contrasts and tradeoffs and less going for volume.  I certainly wouldn't lead off with inflammatory puffery like "PHP is a community of amateurs".


### Act III

I _think_ I've mellowed out a good bit in the last few years.

It turns out that being _Right_ is much less important than being _Not Wrong_ — i.e., rather than trying to make something perfect that can be adapted to any future case, just avoid as many pitfalls as possible.  Code that does something useful has much more practical value than unfinished code with some pristine architecture.

Nowhere is this more apparent than in game development, where all code is doomed to be crap and the best you can hope for is to stem the tide.  But there's also a fixed _goal_ that's completely unrelated to how the code looks: does the game work, and is it fun to play?  Yes?  Ship the damn thing and forget about it.

Games are also nice because it's very easy to pour my own feelings into them and evoke feelings in the people who play them.  They're _mine_, something with my fingerprints on them — even the [games](https://eevee.itch.io/) I've built with glip have plenty of my own hallmarks, little touches I added on a whim or attention to specific details that I care about.

Maybe a better example is the Doom map parser I started writing.  It sounds like a "pure" problem again, except that I actually know an awful lot about the subject already!  I also cleverly (accidentally) released some useful _results_ of the work I've done thusfar — like statistics about Doom II maps and a few screenshots of flipped stock maps — even though I don't think the parser itself is far enough along to release yet.  The tool has served a purpose, one with my fingerprints on it, even without being released publicly.  That keeps it fresh in my mind as something interesting I'd like to keep working on, eventually.  (When I run into an architecture question, I step back for a while, or I do other work in the hopes that the solution will reveal itself.)

I also made two simple Pokémon ROM hacks this year, despite knowing nothing about Game Boy internals or assembly when I started.  I just decided I wanted to do an open-ended thing beyond my reach, and I went to do it, not worrying about cleanliness and willing to accept a bumpy ride to get there.  I _played_, but in a more experienced way, invoking the stuff I know (and the people I've met!) to help me get a running start in completely unfamiliar territory.

----

This feels like a really fine distinction that I'm not sure I'm doing justice.  I don't know if I could've appreciated it three or four years ago.  But I missed making toys, and I'm glad I'm doing it again.

In short, I forgot how to have fun with programming for a little while, and I've finally started to figure it out again.  And that's far more important than whether you use PHP or not.
