title: Did some Spline work, again
date: 2015-11-30 21:46
category: dev
tags: patreon, spline, tech, making things, python

Sketch is still buying days of my time, which is super cool of him.  [Continuing from last month]({filename}/2015-10-30-did-some-spline-work.markdown), he asked that I make it possible to disable normal editing and only accept proposals on the wiki.

After some internal debate about how to add a real configuration system, I realized this could just be expressed with permissions, so I wrote some little permissions UI.  And actually added them to the proposal code.  Which is good.

I wanted to have a nice way to iterate all _possible_ permissions from whatever plugins are currently active, but the way permissions work right now is kind of fucked up anyway, so in the end I just hardcoded a list of existing permissions.  Oh, well.  I'll get around to it.

Also I added CSRF protection everywhere.  _Whoops._  Like I said, spline is still lacking in a lot of niceties, such as "being ready for production use".  But it's getting there, one architecture astronauting session at a time.

While I was in there I finally added UI so Glip can attach videos and cutscenes to [Floraverse](http://floraverse.com/) pages without my intervention.  It was pretty easy and I don't know why I subjected myself to messing with the db manually for so long.

This isn't very long or exciting; it was my project and I knew what I was doing, and there was a lot of pondering involved, and I don't have anything to complain about.

----

Which is why I'm using it to start off a _dev log_, containing shorter posts about things I have done that don't merit some deep dive into obscure technology.  I also started keeping a notebook (a real, physical notebook) for jotting down stuff I do every day, and maybe I'll summarize it once a week or so.  I'll also post about little "releases" like Mario Maker levels.  In fact I might go make backdated posts for all the levels I've made so far.

Remember, if you're following via the Atom feed and only want to see the blog, [there's a feed with only blog posts](http://eev.ee/feeds/blog.atom.xml).

I'm not sure what this means for the [projects page](/projects/), which has always been kind of a mess.  It's also annoying that you can't easily filter by project, because they're just tags, and it's not obvious which tags are projects.  I'll figure this out as I go, I suppose.
