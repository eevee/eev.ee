title: Status recap
date: 2011-02-12 00:15:00
modified: 2011-02-12 14:43:00
category: dev
tags: veekun, squiggle, raidne, dywypi, status

It's been a while since I've really sat down and thought about where my pet projects are and where they're going, either publicly or privately.  Part of this is just because I haven't really done a lot in the past month and a half or so; between Christmas interruptions, having Mel move in, a brief and disasterous switch of medications, and restless nights due to cats wandering around on my bed, I've been varyingly exhausted or distracted or some other excuse.

Lately magical has ever-so-subtly hinted that [roadmaps are a good thing][roadmapping], so in the interest of project management, here's a rough outline of what I'm up to.  With any luck, this will make it into a [bug tracker][redmine] _and_ actually get done!

I'd still like to do these weekly, and I think being able to dump a splat-delimited list into a text file will help considerably.  Here's hoping.

<!-- more -->

## veekun: Pokédex

Other clever people have been hard at work building cool things into my baby, like the start of [i18n][veekun i18n] support.  I've been slacking considerably.

**I did**:

* Black and White item effects, though they're still trapped in a local branch of mine somewhere.  I've been trying to get a bigger [item effect rewrite][veekun item rewrite] done for some time, but it's a big undertaking and I keep getting sidetracked trying to find out specifics about items when I thought I could just rewrite existing text.
* I fixed a bunch of obscure problems with [HeartGold and SoulSilver encounters][veekun hgss encounters], mostly to do with swarms.  So, the intricately-detailed encounter pages will now be slightly less confusing to read for two games.  I'm sure at least four people are overjoyed.

**I'd like to do**:

* Load the move metadata from Black and White, and replace my ad-hoc "categories" idea.  Completely rewrite move search and move pages to match.  Blurgh.  I'm on this now; it's just tedious.
* Finish Black and White!  We still need encounters; magical is on that.  I think everything else is about taken care of, though having locations for TMs is a common request that we ought to try fulfilling.
* A UI overhaul; both the design (see below) and a whole lot of smaller things about the site that keep nagging at me and which I really need to write down.  This is obviously not going to happen in the next couple months, but I'm keeping it in mind and want to get to it soon before I start hating my site again.
* Internationalization.  There's not much work for _me_ to do on that, as another dev has taken up the mantle, but I'm interested in attempting to contribute Japanese translations of the interface.
* Prose, something we've been sorely lacking.  I just need to sit down and _write stuff_, keeping in mind that I am in fact allowed to edit it later.
* Spruce up the searches, which are still big and imposing and awkward to use.
* Locations, locations, locations.  Location pages are impossible to read, and they seriously need some prose.  There's no reason you shouldn't be able to use the location pages themselves as a simple walkthrough of the games.
* A JSON API.  I think this would be rad, even if my IRC Pokédex bot would be the only thing to actually use it.


## veekun: other

I use my servers for a variety of things and slap most of it under the veekun "banner", though in practice that doesn't mean much of anything.

**I did**:

* I did create this blog, which consumed far too much of my time over the past month or two.  It's not really Blogofile's fault, either; the vast majority of that time was spent designing and fiddling with CSS.  The stylesheets are actually written in SCSS, which supports nested style rules and variable interpolation and functions and macros, all of which are fabulously useful.  My intent is to get this design to a point where I actually _like_ it, then sit down and convert veekun to use it (and SCSS) as well.
* Switched WSGI servers from [Paster][paster] to [Green Unicorn][gunicorn].  It's a bit more configurable, actually seems targeted at production use, and doesn't seem to kill requests when it restarts.  I'm tired of email complaining about SystemExit "errors".
* Hacked around a frequent crash with izchak, my (kind of unloved) [NetHack recorded game archive][izchak].  Apparently NetHack will record crazy junk to the log file if you had [IBMgraphics][ibmgraphics] on and examined architecture just before your game ended; the architecture glyph comes out totally bogus, and Python can't decode it.  (I couldn't decode it either, so errant characters just get replaced by the missing-character glyph now.  Lame.)

**I'd like to do**:

* Make the blog automatically rebuild itself without my intervention.  I don't think this is reasonably possible since the repository and the built files are on different machines, so I'll probably just end up writing a little shell script.  Then I can bind it to F17 and press one key to update my blog.  Rad.
* Whip up a landing page for ["meta"][meta], which is currently kind of a catchall subdomain for stuff related to my machines.  I have a lot of crap running, and I think it'd be nice to have a little overview of what it all is.
* Find a way to get gitweb to show recent commits across _all_ projects.  I have a lot of them and browsing for recent activity is currently a giant pain.  Might be easier to just use Redmine's global activity whatsit for this.


## floof

Unlike [veekun][veekun roadmap], [floof's roadmap][floof roadmap] actually kind of means something.  Okay, yes, we're past the closed-alpha date, but the dates were arbitrary anyway.  Point is, stuff is in a clear order, and we're trying to stick to it.

I've somehow only barely found time to review other people's code (and they keep writing more!  gah!), but we _did_ get a fairly well fleshed-out implementation of [client certificates][client certs].  I want to require them for administrative actions, and offer them to anyone else who wants to use them, so it's nice to see others with enough interest in the idea to _implement_ it.

**I need to do**:

* Write some non-code: add a license (whoops), add a contributor list, update the readme, throw some docs on the wiki.  Maybe actually start on a philosophy document if inspiration strikes.
* Get generic art searching done, as that's required for pretty much any page that shows art.
* Implement mogile support.  We've got a CDN interested in us, but it acts as a caching proxy rather than a dedicated filestore like [Amazon S3][s3], so I'll still need to handle storing and serving files locally and mogile looks great for that.  I also need to fix plain file storage to respond with the correct mimetypes.

Those are by far the most important for me; after that I might go for something more user-visible, like putting interesting content on the landing page.


## raidne

I don't know who actually remembers this, but raidne is one of my guilty pleasure projects: it'll likely never be finished, it doesn't have an obvious target audience, and I work on it fairly rarely.  It's intended to be a modernish roguelike, but biased more towards exploration and item collection than Smogon-like stat improvement.

So far it, uh, has [a dude][u263b] who can work around.  I've spent far more time on architecture than any actual game stuff so far, but I don't think that's a bad thing.

I need to do _everything_ next.  Right now I'm trying to make the main UI work: scrollable map, scrollable backlog of messages, and a little status window.  I'm using [urwid][urwid], which is fabulous except for its [abysmal documentation][urwid docs].  :(  If I get a significant chunk of time to work on this soon, I'm going to take notes on what I learn from sourcediving and try to contribute some doc patches to urwid.

It could also stand to get promoted to a first-class project; public repository, bug tracker project, some tickets filed, etc.


## dywypi (2.0)

My _other_ guilty pleasure project, though significantly more likely to produce results in the near future.  He's an IRC bot in Python (because there aren't enough of _those_!), because nobody has done this right yet.  There's [supybot][supybot], but it's this clunky 2.2-era thing and its documentation might as well not exist.

I'm trying to wire together [twisted words][twisted words] (Python's excellent networking platform and its IRC protocol support) and [exocet][exocet] (a glorious hack of Python's import system that should allow for true plugin reloading).  The results so far are ghastly but promising.

**I need to do**:

* As above, needs some actual project love.
* Finish the basic plugin registration API.  The idea is for plugins to decorate methods that should be commands, then allow running them with `plugin.command`.  Commands can also have global names registered, but I want them to explicitly ask for this for each command; supybot comes with a proliferation of plugins that all have tons of commands with similar names, and it tries to guess which command in which plugin you mean, and it's left a bad taste in my mouth.
* Support a special `core` plugin, which would have commands for high-level stuff like loading plugins.
* Add configuration and make the thing run under twistd.
* Allow plugins to respond to events other than active commands.  A common example is watching for URLs and doing something with them, or noticing when people enter/leave.
* Allow plugins to run asynchronously, whatever that means.  There are several distinct use cases here, and I might just scrawl an API for each to encourage API authors not to do heavy synchronous work.
    1. Communicating with another server in response to an event.  Twisted is built for this, so.
    2. Long-running polling, such as listening to a pipe.  (I want this for a git commit bot!)  Twisted can take care of this, too, but the tricky bit is having it run continuously in the background.
    3. Processing that just outright takes a long time.  I'm a little doubtful that this should happen with an IRC bot, but who knows.  I _think_ Twisted has some facility for dealing with this, if you write your code politely, but I haven't used it enough to be sure.
* Authn/authz.  Suddenly, far more complicated!  I really really want to make this integrate with IRC services rather than building a parallel user list, but I don't know how feasible that is.  Nobody has tried it before; is that because it's really hard, or because nobody thought of it?

I don't think any of this is particularly difficult, up until the last bit.  I threw together the plugin core in an hour or so, and it does some nifty tricks.  Just need to do enough on important projects to earn some time on this one.


[client certs]: http://www.gnegg.ch/2008/05/why-is-nobody-using-ssl-client-certificates/
[exocet]: http://washort.twistedmatrix.com/2011/01/introducing-exocet.html
[floof roadmap]: http://bugs.veekun.com/projects/floof/roadmap
[gunicorn]: http://gunicorn.org/
[ibmgraphics]: http://nethackwiki.com/wiki/IBMgraphics
[izchak]: http://nethack.veekun.com/
[meta]: http://meta.veekun.com/
[paster]: http://pythonpaste.org/
[redmine]: http://bugs.veekun.com/
[roadmapping]: http://blogs.gnome.org/bolsh/2011/02/07/drawing-up-a-roadmap/
[s3]: http://aws.amazon.com/s3/
[supybot]: http://sourceforge.net/projects/supybot/
[twisted words]: http://twistedmatrix.com/trac/wiki/TwistedWords
[u263b]: http://www.fileformat.info/info/unicode/char/263b/index.htm
[urwid]: http://excess.org/urwid/
[urwid docs]: http://excess.org/urwid/reference.html
[veekun i18n]: http://bugs.veekun.com/issues/401
[veekun item rewrite]: http://bugs.veekun.com/issues/247
[veekun hgss encounters]: http://bugs.veekun.com/issues/297
[veekun roadmap]: http://bugs.veekun.com/projects/veekun/roadmap
