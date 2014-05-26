title: informative title
date: 2011-08-24 21:20:00
tags: linux, interfaces, veekun, squiggle, raidne, sanpera
category: status

Hello here is what's going on.

<!-- more -->

## job

I work for [Yelp][] now.  PERHAPS YOU'VE HEARD OF THEM.

In all seriousness, it's pretty nice to work for a place that maybe people have heard of.  For four years i've had to mumble something about taxes and Florida and quietly realize i barely understood what i was doing, either.  No longer!

Enjoying myself so far; it definitely has the feel of a company of engineers who build stuff just because they like building stuff.  The difference is _night and day_.

## grammar

I'm no longer capitalizing "i" as though it were a proper noun.  Right, okay.

## psych

I'm kind of liking this whole full-disclosure thing with my dumb glitches.  In the past week i have noticed:

* I still try way, way, way too hard to find elegant solutions to problems.  I said this before in some form, but i had engineering in mind.  This week, i needed to get an Android device for Mel so she could use [Square][] to peddle her wares at a con this weekend.  I put considerable effort into figuring out how to re-juggle wireless service, or excuse buying a tablet because it'd be cheaper than a family plan, or whatever the goddamn fuck.

    In the end i just strolled into Best Buy, bought a new phone i wanted, and gave her my old phone.  Which was my original plan.

    Embracing failure don't cut it.  **Fail _fast_.**

* I seriously need to stop making ad hoc todo lists and dump stuff into bug trackers.

    I spent the first two weeks of the month out in a tiny hotel room in San Fransisco.  And it was _great_.  I worked on things i've been avoiding for ages, i started a project that's only been a daydream for years.

    Then i returned home, and immediately noticed that everything seemed like a drag again.  It took me a week, but i realized why.

    I have dozens of things i want to do.  Some of them involve writing code.  Many of them do not: replacing the router, hanging my whiteboard again, doing laundry, getting this crap off my desk, whatever endless list of errands.

    When i was out of town, none of these things were relevant; i couldn't really do anything about them, so they weren't on my mind at all.  The moment i got home, i suddenly had a mental laundry list of Things To Do Right Now again.  Because that's where those things lurk: in RAM, in volatile memory, where i have to keep thinking about them for fear i'll forget.  I jot them down in todo files (todo, todo1, todo-new...), but then i have to keep glancing at the list to avoid forgetting about it, and i just see an impenetrable wall of stuff i don't want to do.

    I don't know what to do about that, specifically, but it helps tremendously to not let development contribute.  I keep accumulating such lists of dozens of bugfixes or small features i intend to get to Real Soon Now, because they each individually seem like they should only take a few minutes, and it's "a shame" to fill up the bug tracker with...  bugs.  (???)  Naturally i don't get around to them for whatever reason, so they become persistent baggage; things i have to juggle in my head all the time or keep jotted down on loose paper spread across my desk.  It's paralyzing, and it's exhausting.  Also, it's dumb and i keep re-learning this lesson.

I'm toying with the idea of flipping my sleep schedule so i work at the _end_ of the day; it might help some with the burnout and distractions, since nothing really happens at 3am.  I don't tend to deal well with weird sleep patterns, though.  I may try it next week and see how it goes.

## hackin

Speaking of, here are some things.

**veekun** has, er, not moved too much.  A lot of stuff i want to do is held up while i fuck around with a JSON API.  I'm happy to say that i've managed to un-overengineer what i wanted to do here, and i have a little test suite, and it's gradually creeping closer to passing.

**floof** is, at last, ported to Pyramid.  This doesn't mean anything to anyone, which makes the work not worth it at all.  Maybe now i'll do something user-visible.  After having pored over every last goddamn line of code in this thing, i really hope i've learned something about not overengineering in the beginning and focusing on getting a usable product first.  (Doubtful.)

I agonized over AI for **raidne** for ages and finally implemented something, which involves passing Action objects around.  You can now be attacked by a newt until you die.  Death is indicated with a (deliberate) Python stack trace.

I started **sanpera**, an attempt at building a not-PIL imaging library for Python, atop Cython and GraphicsMagick.  Fun times so far; i haven't touched C in ages and it's fun to do so in a somewhat padded environment.  The "library" is just a bad port of the example GraphicsMagick program right now and i haven't much touched it since i got home, but i'd like to actually make something of this.

Also, i threw some stuff up on [github][my github].  I don't think i like GitHub Issues enough to jump ship right now, but it's a nice git interface, so i might as well mirror to it manually or something.

I'd like to make enough progress on something to deserve a dedicated blog post, but durrrr.  Getting better.

---

Christ i have a flight at 7:30 in the morning goodnight.

[my github]: https://github.com/eevee
[Square]: http://squareup.com/
[Yelp]: http://www.yelp.com/
