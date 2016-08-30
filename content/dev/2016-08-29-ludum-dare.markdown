title: Weekly roundup: Ludum Dare
date: 2016-08-29 13:49
category: dev
tags: status, veekun, runed awakening, gamedev

August is loosely about **video games**, but really it's about [three big things in particular]({filename}2016-08-07-weekly-roundup-three-big-things.markdown).

- **book**: Wrangled LaTeX some more.  Came up with a new style for admonitions (little set-out boxes) that I really like.  Drew some icons for a few of them.  Started on another chapter, for reasons; see below.

- **veekun**: Regexing machine code for addresses was getting really clumsy, so I went one step further and wrote a disassembling pattern matcher thing.  You write some assembly with some variables in it, and it finds occurrences of that code and tells you what the variables are.  I can pretty much paste in entire functions, massage them slightly, and find matches.  It's pretty slick.

    The upshot of this is that loading original Japanese Red and Green now works!  But Yellow doesn't.  So I fixed that, and now Japanese Blue is broken.  Or maybe I fixed it and that broke Yellow again?  I'm not sure.  There were some tiny changes to core code between some of these games, and the pattern-matcher has no way to express alternatives.  I don't know if I'm better off _inventing_ one or just fudging it.
    
    Anyway, pretty close to having all of gen 1 dumping Pokémon reliably.  Still need to actually dump other stuff — moves, items, encounters, and the like — but that's much more straightforward.

- **hax**: I was still in a mood to dink around with Game Boy stuff, so I added Python 3 support to some relevant tooling and wrote a proof of concept for storing Pokémon maps in Tiled format.

- **blog**: I wrote a thing about [writing tests]({filename}/2016-08-22-testing-for-people-who-hate-testing.markdown).

- **twitter**: I taught [@perlin\_noise](https://twitter.com/perlin_noise) a few new tricks.

- **art**: I [drew a friend's lizard pal based on a reference photo](https://lexyeevee.tumblr.com/post/149481403117/drawn-based-on-this-photo-of-poketto-monstas-bab), which isn't something I'd seriously tried before.  Value-only, only one layer, only one brush.  It came out surprisingly well.

- **gamedev**: I participated in Ludum Dare 36, a 48-hour game jam.  I'd never done LD before, and naturally I picked the only one that has no ratings round (for administrative shuffling reasons).  Oh, well.

    The result was Isaac's Descent, a short puzzle-platformer for the PICO-8.  You can [play it via the web](https://c.eev.ee/isaacs-descent/) (source code included), and I also wrote [a post about it]({filename}/2016-08-29-i-entered-ludum-dare-36.markdown).

----

So!  There are a few days left, but it's pretty much the end of August.  Let's see how I did.

- _Draft three chapters of this book, August: one chapter_

    Well, I didn't get a chapter done.  I did make _huge_ progress on the chapter I started, though — plus I began a second chapter, and generated enough notes for the entirety of a third.  I spent a decent amount of time wrangling Sphinx and LaTeX, too, which I would've had to do sooner or later regardless.

    So I didn't do quite what I wanted, but I _did_ do far more than I've put into any previous harebrained book idea, and it was a pretty decent chunk of work.  I'm okay with that.

    Just what _is_ this damn book, you ask?  Ah, perhaps you should read that Ludum Dare post.

- _Get veekun beta-worthy, August: basics of the new schema committed; basics of gen 1 and gen 6 games dumped; skeleton cli and site_

    Haha, no.  I got gen 1 almost working for Pokémon only.  It turns out that while gen 1 has the simplest data, it probably has the most convoluted storage.

    On the other hand, the detours taught me a lot about Game Boy architecture, which was interesting _and_ helpful for making the dumper fairly robust thusfar.  I also made some breakthroughs on architecture that had been haunting me for a while.  I'll have to move my ass in the next week or two to catch up — hopefully finish gen 1 and get a few other generations dumped _real soon_ — but I think this is still doable.

- _Finish Runed Awakening, August: working ending; at least one solution to each puzzle; private beta_

    Whoops!  I did basically squat on Runed Awakening.  I figured out _most_ of the ending, which had been my major roadblock, but I didn't touch the code or run the game a single time.  Dang.  It's not like I was goofing off all month, either; I just didn't have a big block of time to devote to the weird mishmash of writing and planning and programming that IF requires.

    I _really_ want to finish this game, but end of October is not looking too great.  I don't know why it's proving so difficult; it's not _that_ complicated, and I started on it almost two years ago now.  I've made multiple other games just so far _this year_!  Argh.

    If it's any consolation (to me): I picked November as a target because Mel wanted to embed Runed Awakening on Floraverse as an update around that time.  But Isaac's Descent takes place in the same universe, so it works just as well.  Goal accomplished!

Onwards to September.  The only thing on the list with a real _solid_ deadline is veekun, since the new games will be coming out.  It's a bit behind, but I'm pretty sure I can catch up.  Gen 2 shouldn't be too different from gen 1, and I've done gen 4 and onwards before.
