title: Did some spline work
date: 2015-10-30 03:22
category: dev
tags: tech, python, web, spline, making things, patreon

Sketch bought a day of my time this month (and, er, last month) to work on adding "pull requests" to a git-backed wiki.  I picked `spline`, because, uh, I wrote it.

<!-- more -->


## About spline

Back in ye olden days, when I still worked for a big company, we had some little app known as the "love machine".  You could send another employee some "love" for something they did, and every week there was some brief recognition of who had sent or received the most love.  Aww.

Unfortunately the app itself was kind of cumbersome to use (who wants to navigate through an app to say a sentence to a person?), plus surprisingly slow for what little it did.  We had various ad-hoc band-aids for this, like a CLI wrapper around the API (I say "API" but I'm not sure there was one), but, you know.

During some hackathon or other I was thinking about this, and how surely it couldn't take too much effort to write something this simple.  Then my mind wandered, as it's wont to do.

I remember, remembered, back in the day when people actually ran their own websites.  I knew at least a handful of people who managed to get little community sites running with zero technical knowledge, thanks to a handful of stock PHP apps.  If you were lucky, some rando on a forum somewhere had posted instructions that would let all of them use the same user table and cookie as well.  So maybe you'd have phpBB for a forum, and some clunky plugin that turned forum threads into a news page, and an image gallery, and a wiki and an oekaki and whatever else, and they'd all be wired together into this single lumbering monstrosity.  Everything would look completely different, but it would be _yours_, your little website that you put together and could run however you wanted.

It seems a shame that we haven't really improved on this process in the last 10+ years.  If anything, as web apps and authentication have gotten more complicated, Frankensteining them together has gotten harder.

Reimplementing the "love machine" seemed easy enough.  We also lacked some other simple niceties, like a quote db for IRC — we had a fortune file in git somewhere, which isn't the friendliest interface.

So I had the thought to try building both of these simple things as parts of the same Pyramid app, but against a plugin interface.  Then either part could be disabled, or even uninstalled, without affecting the other.  Effectively you'd have two apps that could be installed together and happily coexist, because all the boring common stuff like authentication would live in a shared core.

This isn't a particularly novel idea.  Some apps like Trac use the same sort of approach internally, but are really designed for their own purposes rather than for writing arbitrary new components.  Some frameworks like Rails and Django are sort of plugin-oriented, but at a lower level that's more concerned with assets and endpoints and not so much with helping plugins coexist.  I was imagining a product somewhere down the line where turning on the "love" plugin wouldn't just add some new pages, but also show loves on a user profile page and a love count in a user infobox and whatnot.

Plus, if all the mind-numbingly boring parts of webdev were done in the core, I could avoid thinking about them again the next time I went to cobble together something simple.

Unfortunately this didn't get terribly far.  I got some of the bare minimum working, but some later hackathon project (with considerably more people working on it) spat out a replacement "love machine" that also had email and native apps and nice artwork and various other bells and whistles.  It was still an interesting idea, but I didn't really have a good excuse to work on it.

(Incidentally, I tried this once before with Pylons, and also didn't get very far.  The remnants of the attempt still run veekun.com.)

Nowadays, `spline` just runs the [Floraverse](http://floraverse.com/) site, and its feature set is more along the lines of "whatever Mel needs most urgently".  I'm a little burnt out on web dev, so my wild aspirations are somewhat tamer than before.  I might try to make it actually usable for other people/developers, someday.  Or not.

Anyway, the point of all this is that one of the things `spline` has is a dead simple git-backed wiki.  There's no storage besides a git repository.  Page titles are Markdown metadata; the changelog is just git history, with emails (poorly) matched to users.  It was kind of experimental, but ended up being thrust into [production](http://floraverse.com/wiki/) out of necessity.  Just like `spline` itself!


## The request

Sketch asked for something akin to GitHub's pull requests, but for a wiki.  It's something that's occurred to me before, and I'm surprised it's not a feature in any wiki software I've seen.

So I did that.

I spent an inordinate amount of time wrestling pygit2's docs.  I'd been using pygit2 since the beginning, rather than shelling out to git — partly to avoid caring about the git CLI's ambiguous grammar and ad-hoc output formats, but partly just because it was interesting.  I like to hamstring myself, you see.

For some reason or other, pygit2's documentation has been AWOL for over a month now, and [its website](http://www.pygit2.org/) is nothing more than a default Apache "it works!" page.  I dug it up on archive.org, but the docs themselves are subtly awkward, and I always come away from reading them not feeling like I've quite learned anything.  The API documentation for the main class `Repository` is scattered across half a dozen topic pages.  Very little of it is interlinked.  Sometimes the documentation for a property is extremely vague (there's a property `hunks` that is documented as "hunks").  Sometimes an important method is mentioned _and used in code_ as though it were a free function.  Sometimes an important method isn't documented as part of the API, only mentioned in passing in prose.  It's great that the documentation _exists_, and from a casual glance it _looks_ very helpful, yet it seems to be mildly incompatible with my brain.

That aside, this wasn't particularly tricky:

1. Add a separate button to "propose" an edit rather than save it
2. Perform a "propose" by writing the new commit to a new branch, rather than master
3. Cobble together a terrible page listing all proposal branches
4. When someone approves a proposal, do a merge and delete the branch

It's not _nice_, exactly, but it does work.  Couple issues that come to mind:

* I didn't slap permissions on anywhere, so anyone can merge a proposal branch.  Oops.

* You can't actually disable editing in any way yet, so this isn't really useful.  But that's okay because there's no user registration either.

* The change is shown as a line diff, which isn't very helpful if a few words of prose changed in a very long single-line paragraph.

* Because the only storage is the git repository, there's nowhere to put a title or description or comments, like GitHub issues and pull requests have.  I think using commit messages for this could work pretty well, or maybe notes if necessary.

* Again, the only storage is the git repo, so a new branch name is picked by looking for branches named `proposal/N` and going with `proposal/N+1`.  Deleting the branch on merge thus means that the same branch name might be reused (and also that the comments and whatnot become Web-inaccessible).  _Not_ deleting the branch on merge means the repo potentially collects a zillion dead branches, which experience tells me can slow down pulls dramatically.

* If there's a merge conflict, the app just vomits.  Which is a bit of a problem, since there's no way to resolve the conflict via the web.  I'm not even sure what that would look like yet.

Because of these (especially those first two), I didn't merge this yet.  It's sitting in [a branch](https://github.com/eevee/spline/tree/wiki-proposals), which seems appropriate.  I'd definitely like to clean it up, of course, so I'll get to that the next time I do a batch of `spline` work for Floraverse.

More generally, I _would_ like to get `spline` a little closer to being ready for primetime, at least so other people can give it a spin and tell me if the idea is good.  It needs some more basics implemented, some documentation, and some cleaning up in places where I tried multiple approaches and didn't delete the ones I gave up on.  Nothing too exotic — just that, like I said, I'm a little tired of web dev, and whatever web dev motivation I can drum up tends to go towards Floraverse's more practical demands.  Like being able to edit stuff, so I can stop jiggering the database manually when there's a typo.

Yep.  One day (or even two days) of working on something that wasn't actively in my head isn't terribly exciting.  Oh well.
