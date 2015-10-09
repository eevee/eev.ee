title: Redmine vs GitHub
date: 2011-07-14 16:49:00
category: blog
tags: git, systems, veekun, squiggle, tech

I'm currently hosting a small pile of projects on a combination of self-hosted [gitweb][] and self-hosted [Redmine][].  I keep glancing meaningfully in the direction of [GitHub][]; it's code-oriented, it has wiki support, it has an issue tracker, and it can do simple site hosting via [some contrived abuse of git][github pages].  So why am I bothering to host my own stuff?  There are actually a few reasons, thus I need the Internet to decide for me.

<!-- more -->

I'd rather go all-or-nothing, instead of having one foot in each approach.  Thus moving to GitHub would involve moving veekun, floof, the old copies of both, the new dywypi, etc.

### Pro Redmine

* Independence, not being a cog in the corporate machine, etc etc.

* We're already on it.  Zero effort needed.

* More "pro inertia", but the biggest stumbling block is migrating issues to GitHub.  Redmine numbers issues sequentially across _all_ projects, whereas GitHub numbers issues _per-project_—and you can't force gaps.  So I'd end up renumbering all the existing issues from 1, which would conflict with all the existing issue references in git history and be generally awful and confusing.

    I emailed GitHub support asking about this, and they proposed the following:

    > We can tweak your starting number, but we can't do multiple gap I'm afraid. It might be best to have us set the starting issue number after the last number you've used on redmine, recreate any open tickets in our tracker (with a new number), and then close all the open issues on redmine with a link to the new issue. Then you can put redmine into a read-only state until you feel you don't need those archived issues any longer.

    So I'd start each GitHub project from issue 600 (or whatever), create a new copy of all open Redmine tickets, link the Redmine tickets to the new GitHub ones, and close Redmine.  This is actually kind of a clever solution.  Of course I'd still have to do the actual migration, and it would lose the history of closed tickets, so it's still a plus for Redmine.

* Redmine supports subprojects; GitHub does not.  veekun is split across `spline`, `spline-pokedex`, `pokedex`, `pokedex-media`, and `veekun` repositories.  The practical impact of this is that I can view a list of all tickets across all of "veekun" at once, whereas GitHub Issues cannot.  I think.

* Redmine allows moving issues between projects.  This is sometimes helpful for issues that span several of veekun's components, or for tickets filed by third parties that don't know how the parts are split up.

* I doubt GitHub would appreciate my hosting the `pokedex-media` repository on their servers, seeing as its contents are exclusively images and audio extracted from copyrighted games.  (Also it's comically large; already bigger than the free account soft-limit.)  So if we moved, I'd still need to host that myself anyway.

### Abstentions

* GitHub is a big fancy social thing.  I don't care so much about that, but it would potentially make my work more visible.  My gitweb is kind of out of the way.

* Redmine has issue relationships and workflow and all fancy stuff.  GitHub Issues has "open" vs "closed", plus tags.  I'm not sure if this is better or worse.

* I don't know a lot about GitHub Issues, having only used it from a user's point of view.  Can guests file issues?  It'd be a shame to require that passersby get a GitHub account to report problems with veekun.  On the other hand, I get more (and more useful) bug reports in the forums and via email anyway.

* I'm not sure how to feel about GitHub Pages.  I already have a whole site that I could just describe these projects on, and I'm not terribly happy that my blog is a separate component already; splitting code into a third place kind of sucks.  But I don't _have_ pages devoted to most of these projects yet, whereas maybe I'd have more incentive with Pages.  And it's not like I'm forced to use it anyway.  Eh.

### Pro GitHub

* I wouldn't have to maintain Redmine or gitweb!  _Or_ gitosis!

* GitHub is far nicer an interface than either gitweb or Redmine's repository browser; quicker, more reliable highlighting, nicer URLs, etc.

* GitHub has in-line code review.

* GitHub has pull requests, which I don't really care about personally, but I've had contributors gripe that they can't so easily offer changes to me.  Keeping contributors happy is a Good Thing.

* I think, but am not sure, that GitHub has a more usable permissions model than Redmine.  Redmine is some intricately detailed ACL nonsense that I basically set once and have never touched again.

* Redmine development is...  not exactly speedy.  I can't actually tell you any significant new feature introduced in the years I've been using it, unless you count "upgraded Rails and thus fucking broke everything".  Twice!  And a third time in the new release which I don't want to install!

* I just don't really like Redmine.  It has a lot of functionality, but the whole thing feels stale and...  _enterprisey_.  Like it's been abstracted so much that there's no soul left.  I might as well be using an Excel spreadsheet with a bunch of macros.


I don't know.  Someone sell me one way or the other.

[gitweb]: http://git.veekun.com/
[Redmine]: http://bugs.veekun.com/
[GitHub]: https://github.com/eevee
[github pages]: http://pages.github.com/
