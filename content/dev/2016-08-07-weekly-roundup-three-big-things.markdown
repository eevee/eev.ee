title: Weekly roundup: three big things
date: 2016-08-07 17:35
category: dev
tags: status

August is about **video games**.  Actually, the next three months are about video games.  Primary goals and their rough stages:

1. Draft three chapters of this book
    - August: one chapter (at which point I might start talking about what the book _is_)
    - September: another chapter
    - October: yet another chapter
2. Get veekun beta-worthy
    - August: basics of the new schema committed; basics of gen 1 and gen 6 games dumped; skeleton cli and site
    - September: most games dumped; lookup; core pages working; new site in publicly-available beta
    - October: all games dumped; new site design work; extras like search and calculators
3. Finish Runed Awakening
    - August: working ending; at least one solution to each puzzle; private beta
    - September: alternate solutions; huge wave of prose editing; patreon beta
    - October: fix the mountains of issues people find; finish any remaining illustrations

Yeah, we'll see how all that goes.  I also have some vague secondary goals like "do art" and "release tiny games" and "do Doom stuff" but those are extremely subject to change.  Hopefully I can stick to the above three big things for three months.

Anyway, this week:

- **blog**: Finished and published posts on [why to use Python 3]({filename}/2016-07-31-python-faq-why-should-i-use-python-3.markdown) and [how to port to it]({filename}/2016-07-31-python-faq-how-do-i-port-to-python-3.markdown), plus made numerous suggested edits.  Wrote a brief thing about [my frustrations with Pokémon Go]({filename}/2016-07-31-i-wish-i-enjoyed-pokémon-go.markdown).  _And_ wrote about [veekun's schema woes]({filename}/2016-08-05-storing-pokémon-without-sql.markdown), which helped me reason through a few lingering thorny problems.

    That might be a record for most things I've published within a calendar week.

- **art**: I tried an hour of timed (real-life) figure drawings, which was kinda weird.  I've really lapsed on the [daily Pokémon](https://lexyeevee.tumblr.com/tagged/daily-pok%C3%A9mon), possibly because I changed up the rules to be an hour for a single painting, and that feels like a huge amount of time (...for something I don't think will come out very well).  I'll either make a better effort to do them every day, or change the rules again so I stop putting them off.

    I drew [Griffin's Nuzlocke team](https://lexyeevee.tumblr.com/post/148613924637/ive-never-drawn-a-team-pose-i-started-drawing-as) kind of on a whim?  A day-long whim?

- **book**: I wrote some preface, which you're probably supposed to do last, but it helped me figure out the tone of the writing.  I've mentioned this before regarding previous failed attempts, but writing a book is surprisingly harder than writing a blog post — I can't quite put my finger on why, but the medium feels completely different and alien, and I'm much more self-conscious about how I write.

    I did get a bit of a chapter written, though.  I probably spent much more time wrangling authoring tools into producing something acceptable.

- **doom**: I somehow drifted into doing stuff to anachrony again.  Apparently I left it in near-shambles, with at least a dozen half-finished things all over the place and few comments about what on Earth I was thinking.  I've cleaned a _lot_ of them up, figured out how to fix some long-standing irritations, and excised some bad ideas.  It's almost presentable now, and I started building a little contrived demo map that tries to show how some of the things work.  Someday I might even use all this for a real map, wow.

- **zdoom**: Oops, I also picked up my Lua-in-ZDoom experiment again.  After doing some things to C++ that made me feel like a witch, someone recommended [Sol](https://github.com/ThePhD/sol2), a single-file (10k line...) C++ library for interacting with Lua.  It is _fucking incredible_ and makes everything _so much easier_ and the author is on Twitter and fixes things faster than I can bring them up.

    I don't know how much time I want to devote to this — it _is_ just an experiment — but Sol will make it go preposterously faster.  It's single-handedly made a proof of concept look feasible.

- **ops**: I spent half a day fixing microscopic IPv6 problems that have been getting on my nerves for ages.

- **veekun**: After publishing the schema post, I went to have a look at where I'd left the new dumper code.  I spent a few hours writing rock-solid(-ish) version and language detection, which doesn't have much to do with the schema but is really important to have.

I just about filled a page in my notebook with all this, which I haven't done in a while.  Feels pretty good!  I'm also a quarter through the month already, so I'd better get moving on those three big things.
