title: We have always been at war with UI
date: 2016-02-10 16:41
category: articles
tags: tech, culture, ui


A familiar story: company makes product, product becomes wildly popular, company royally fucks product up.

The most recent example of this is [TimelineGate](https://blog.twitter.com/2016/never-miss-important-tweets-from-people-you-follow), but it's something I've had on my mind for a while.  Thus I present to you a list of complaints about personally-inconvenient UI changes, carefully disguised as a thoughtful essay.


<!-- more -->

## Why change anything?

### For the sake of change

Something is old, and programmers don't like old things, so someone wants to change it.  Or maybe there's a new PM or tech lead or whoever, and they want to make a statement by putting their fingerprints all over something.  It happens.  Plenty of Google+ press gave the impression that it was driven in part by such office politics.

Bear in mind, this isn't _necessarily_ bad, and sometimes it can be important.  We're affected quite a bit by our perceptions of what's "new" versus "old", so even if a website were completely perfect, it would very gradually rot if it never changed.  And that's in a world where nothing else is changing, either, which is not the case.  If a feature or design trope becomes standard in the rest of the world but your thing lacks it, your thing has just become relatively worse, even though _it_ didn't change.  Take a look around your grocery store sometime and you'll surely find a box or two boasting its "new look, same great taste!" — just to look more "modern" than everything else on the shelf.

Of course, that same reasoning is trivial to apply to just about any change.  Consider, if you will, virtually any bank website redesign in the history of the Web.  The tax prep thing I use changes every year to look a little more Web Two Point Oh (in that special don't-quite-get-it way unique to financial institutions), and this year they've unveiled quite a novel monstrosity: their own scrollbar!  Yes, they've hidden the native scrollbar and replaced it with one that drifts lazily up and down, taking several whole seconds to come to a stop after a single click of the mouse wheel.  Why?  I have no idea.  Maybe someone just thought it was cool.  Maybe they have a lot of Windows 2000 users and can't bear to see a square scrollbar.  There's no clear technical or functional reason to do this; it's just a whizbang thing someone felt like creating.


## Up and to the right

Web Twitter is currently running an experiment that displays single tweets as popups above a skeletal user profile.  Yesterday I saw a tweet snarking about this float by, and in the replies was a Digital Marketing Expert® who was dispensing some sage wisdom like:

> I listen to the data that shows high conversions from popups. A more democratic measure than twitter opinions.

If you're not familiar with marketing-speak, "conversion" is the thing the Borg do to you.  Wait, sorry, that's something else.  "Conversion" refers to "converting" someone from not-a-customer to a customer, or more generally just getting someone to push a button somewhere.  It's really handy if you like to think of fellow human beings as lumbering piles of resources just waiting to be extracted.

And yet this _is_ how UI changes are decided upon.

1. You make a huge change.
2. You rig your site to randomly show the new thing to half your users, while the other half stay with the old thing.
3. You don't say a word about this.  Everyone is completely fucking confused, and it takes a day or two to figure out what the hell happened.
4. Meanwhile, you have picked a completely arbitrary number to measure.
5. If the number is higher for the people with the new thing, it's a winner!  You release it to everyone and delete the old thing.

Consider Twitter's recent injection of "who to follow" suggestions into your timeline on mobile.  They almost certainly just measured new follows.  If people with the suggestions do more following than people without them, the experiment is a success, and the feature stays.  (Given that it's still around, it probably succeeded.)

The problem is that [we suck at measuring](/blog/2015/11/06/the-tech-diversity-blind-spot/).  Of _course_ people will end up doing more following if you stick more follow buttons in front of them.  But how many of those follows are _deliberate_?  And how much are you annoying people who don't use the widget at all?  Plotting two lines on a graph won't tell you that.

I'm not saying that this specific feature is a bad idea — I don't mind it, and I think I've followed a couple people because of it.  I _am_ saying that determining a feature's goodness by measuring how many people mash their fingers against it doesn't necessarily tell you squat.

See, until very recently, Android Twitter had a follow icon at the bottom right corner of every tweet from someone you're not already following.  They formed a column on the right side, in exactly the place where a right-handed person might use their thumb to scroll.  Guess how many accidental follows that led to?  And every single one made it look like that icon was a success.

Or consider Moments, the new feature that stuck its icon exactly where the notifications tab used to be on Android.  For days after it first came out, my timeline was awash in complaints about accidentally hitting it.  And every one of those taps would look, to a naïve graph, like someone was genuinely interested in Moments.

This is the age of Big Data, where programmers can measure anything and everything, but don't necessarily know what they're measuring or what to do with it.  The extreme cases are "[dark patterns](http://darkpatterns.org/)" — UI tricks that pretty much _fool_ users into doing something unintentional, but happen to be profitable.  The site lists some few recognizable names, which may be surprising for a catalog of nefarious decisions.  But how can you really tell whether your own ideas are nefarious?  Graphs of button presses and checkouts and "conversions" don't tell you whether they were wanted, deliberate, or appreciated.  You could measure how many people change their minds later, but it may be weeks or months before they realize what's happened, and plenty of people just won't bother.

### Genuine improvements

Not all change is bad, of course!  All software is lugging around some regrettable decisions and accumulated legacy cruft.  There's a constant tension between fixing/removing it (which may make the software simpler, faster, easier to understand, etc.) or leaving it be (which will preserve compatibility).

On one end of the spectrum we have projects that fiercely cling to compatibility, like Windows, which can still run a lot of Windows 95 software.  The cost is, presumably, an ever-sprawling API (how many native first-party GUI toolkits does Windows have now?), an absolutely massive codebase, and the constant risk that a new feature or bugfix will need some workaround to keep old software limping along.

The other end of the spectrum...  doesn't really exist, because projects that aggressively and regularly cleanse themselves tend not to become very popular.  A decent example might be Rust in its pre-stable days, when every new release seemed to remove a third of the existing syntax.  That's pretty harsh for a programming language.  It paid off, though: Rust 1.0 was fairly minimal and consistent despite having been in development for years.  Going forward, there are clear rules about what's a new and experimental feature and what can be relied upon for the long term.

In the middle, where most projects lie, you end up with surprise bumps in the road.  Some bumps are bigger than others.  Python 3 made some relatively modest changes: removing _long_-deprecated features, fixing some weird special-cased syntax, and making the default string type Unicode-aware.  The language is 99% identical to Python 2, but the cruft it shed was just enough of a change to make virtually all Python 2 code not quite work with Python 3.  Seven years later, there's finally enough third-party support that Python 3 is gaining some momentum.

These examples are all pretty technical.  It's hard to name a UI change that's _unambiguously_ positive; there's no accounting for taste.  Even Python 3 has been, ah, controversial.

And that brings me to the elephant in the room.


## Why do people get so angry?

The short answer is: people have made your thing a part of their lives in some way, and you're pulling the rug out from under them.  The longer answers are...

### Misunderstanding the ecosystem

KDE is now working on version 5, which means they threw everything out and started again, again.  Lost in the shuffle was support for system tray icons.  I found out about this _after_ upgrading to KDE 5, because I have an app that _will not start_ if there's no system tray.

As far as I can tell, this was only really mentioned in [some developer's blog](http://blog.martin-graesslin.com/blog/2014/03/system-tray-in-plasma-next/).  Apparently the old crufty approach is clumsy because of some technical details in X, and it only supports pretty small icons which look bad on modern screens, and apps implement it inconsistently, and so forth.  Those aren't _bad_ concerns, but here's the kicker:

> Nevertheless, we decided to not implement support for it as we want to focus on the core and it was not justified to invest lots of time on an implementation only needed for a short period of time. Applications still using Qt 4 will hopefully soon get ported to Qt 5 and then the issue fixes itself.

In other words: they threw out the old thing, but new Qt has support for the new thing, so as soon as everyone upgrades, all will be fixed.  If you are not familiar, Qt is a widget toolkit — a library responsible for actually drawing windows and scrollbars and checkboxes and whatnot.  Crucially, **it is not the only one**.  Software _not_ using Qt includes: Firefox, Thunderbird, Chrome, GIMP, gvim, Pidgin, Deluge, Transmission.  Those last three have system tray icons, which quietly vanished under KDE 5.  Also, upgrading to the new Qt is not a trivial task — Krita has been at it for months now.

Somehow, it never occurred to anyone involved with this project that maybe breaking an extremely popular IM client is a bad idea.  Actually, scratch that, it's much worse — they decided to ship this change without reaching out to the high-profile applications that would be affected and working on a fix with them.  That still wouldn't have helped my app, but it would've been _something_.  Instead, they got to pat themselves on the back for how much technically nicer their software is, while I couldn't use my computer.  (For what it's worth, they eventually relented after a year and a  half — as of a few weeks ago, KDE 5 has support for "legacy" system tray gizmos again.)

This is particularly ironic for me, since I've [written before](/blog/2011/05/10/unity-vs-gnome-shell/#what-id-like-to-see) about how I'd like to see the desktop communicate more with applications.  KDE's replacement for system tray icons is designed to do that, but the desktop _developers_ neglected to communicate with application _developers_.  I don't have high hopes that these cool integration features will actually get used, if you can't tell either your users or complementary developers about them.

Speaking of GNOME 3, a further irony is that _exactly the same thing happened_ when GNOME 3 came out.  A GNOME developer [filed a ticket on Transmission](https://trac.transmissionbt.com/ticket/3685) asking them to remove their system tray icon and replace it with GNOME 3's own new thing.  Which doesn't exist on other desktops.  A Transmission dev objected, and the GNOME dev replied with this gem:

> I guess you have to decide if you are a GNOME app, an Ubuntu app, or an XFCE app unfortunately. I'm sorry that this is the case but it wasn't GNOME's fault that Ubuntu has started this fork. And I have no idea what XFCE is or does sorry.

"_I have no idea what XFCE is or does._"  XFCE is the most popular of the "minority" desktops, and is based on GNOME's technology!  There's even an entire Ubuntu variant, Xubuntu, based on it.  That you can work on GNOME and _not know this_ is outrageous.

That's a pretty good way to rile people up.  Make a fundamental and highly-visible change, then make it abundantly clear that you don't know a _goddamn thing_ about the ecosystem you're impacting.

### Incomplete replacements

Code, and specifically code that interacts with the outside world, tends to accrete lint over time.  I don't mean "lint" in the sense of code linting; I mean in the sense of little eyesores clinging on here and there that don't directly relate to what the code is trying to do.  Programmers then come along, scowl a lot, and want to rewrite it.  Sometimes, rightly so.

Sometimes, not so much.  I don't generally link Joel Spolsky, but I really like [this point](http://www.joelonsoftware.com/articles/fog0000000069.html):

> ... Yes, I know, it's just a simple function to display a window, but it has grown little hairs and stuff on it and nobody knows why. Well, I'll tell you why: those are bug fixes. One of them fixes that bug that Nancy had when she tried to install the thing on a computer that didn't have Internet Explorer. Another one fixes that bug that occurs in low memory conditions. Another one fixes that bug that occurred when the file is on a floppy disk and the user yanks out the disk in the middle. That LoadLibrary call is ugly but it makes the code work on old versions of Windows 95.

> Each of these bugs took weeks of real-world usage before they were found. The programmer might have spent a couple of days reproducing the bug in the lab and fixing it. If it's like a lot of bugs, the fix might be one line of code, or it might even be a couple of characters, but a lot of work and time went into those two characters.

Rewriting the function will give you something "clean", but you're likely to miss out on some of those edge cases.  Now something that worked just fine yesterday is broken again today.  This kind of lint is also the worst to break, because it's very hard to test — you'd have to set up a test computer without Internet Explorer, or find an old verison of Windows 95, or simulate just the right amount of lag, or control the temperature of your GPU, or...

Alas, exactly the same thing happens with UI.  This is one of my biggest irritations with JavaScript-happy Web developers: reinventing native browser features and _fucking them up_.  Your ajax link can't be middle-clicked.  Your custom faux link can't be tabbed to.  Your custom dropdown doesn't support typing to jump to an option.  Your custom scrollbar moves the wrong distance.  And so on.

For a more concrete example, allow me to pick on KDE some more.  In their grand upgrade, they also rewrote their screenshot tool from scratch.  Now, KDE's screenshot gizmo is pretty slick — it lets me capture a single window, or even draw a rectangle on the screen and just copy that.  It's super convenient because if you draw a rectangle and then try to take a _second_ screenshot, the rectangle starts out in the same place, so I can capture how a part of a window changes over time.  Or, I _could_, until the rewrite, which no longer has this feature.

Okay that's a little obscure.  Here's something with slightly wider impact: last year, Tumblr changed how reblogging works.  You see, a Tumblr reblog is not at all like a Twitter retweet — the original post is wrapped in `<blockquote>` and copied into a new post, which you can then amend how you like.  It's all one single post in the same text editor, so you can edit the old text too.  That meant you could reblog someone's text and edit it, so it would look to your followers as though they'd said something they hadn't.

I don't know exactly what prompted the change, but Tumblr decided to fix this.  Now the reblog interface shows the existing post as a single rendered block, outside the editor; you have the option to delete all the quoted text or preserve it in its entirety, but that's it.  On its surface, this seems reasonable — but it broke some things people might reasonably want to do, like respond to a post inline, or delete older parts of a reblog chain while preserving the more recent responses.

This is the risk of replacing an entirely freeform feature with something more structured.  If you don't understand how people are using it, you can't possibly take those use cases into account.  I already thought this change was mildly annoying, but a lot of people were _really angry_ about it.  I went looking for why, and found that this had severely affected the (previously unknown to me) roleplaying community, who frequently reblog each other back and forth as a way of roleplaying conversations!  With the change, they could no longer trim the older segments of their conversations, meaning that their threads rapidly grew out of control.

The punchline is that you can still do everything you could do before; it's just a bigger pain in the ass.  Nothing about the reblog markup was special in any way, so you can just copy-paste the existing text into the editor, delete Tumblr's frozen quote of it, and edit however you like.

Tumblr completely overlooked this prolific segment of its userbase and broke a feature they relied crucially on.  Not many people cared about the the "social exploits" the old system allowed, either, so this came across as a pointless change that destroyed workflows for no reason.  Speaking of which:

### Breaking things for no good reason

The Tumblr change _could have_ supported 90% of the workflows it broke with a little more effort.  Sometimes, a change is functionally equivalent (or better), but still ruffles feathers.

Changes have tradeoffs.  Sometimes you make a bad trade.  Remember Microsoft Office circa 2000 or so?  The menus were getting way out of hand, so someone had the brilliant idea to hide items you don't use very often.  I'm sure on paper that sounds great, but in practice, it meant that menus seemed to abruptly rearrange themselves for no discernible reason, which completely broke muscle memory for familiar tools.  Unfamiliar tools took twice as long to find — you had to look through all the abridged menus, not find it, then go back and look through the unabridged menus.  Everything was still there, everything was still possible, but it was a much bigger pain in the ass.

Twitter recently started converting uploaded PNGs to JPEGs of really poor quality.  I'm sure it saves them a lot of storage space (i.e. money), but it makes all of my screenshots look like complete garbage.

Or look at OpenGL, which deprecated immediate mode seven years ago.  "Immediate mode" refers to the part of the API that lets you draw a triangle by naming three points and saying "hey, draw a triangle here".

Yes, let that sink in for a moment.  How do you draw a triangle _now_, you may wonder?  Don't worry, you only need [thrice as much code](http://stackoverflow.com/a/6734071/17875) involving buffers and vertex arrays and whatever.

This has all been _infuriating_ to me.  I don't really "do" OpenGL; I've had to dip into it a few times, and every time it's been code that uses immediate mode.  But any time I go looking or asking for help, I find a bunch of game dev snobs explaining how immediate mode is just _comically suboptimal_, and it's so much better for me to use the even more newfangled thing that involves writing code in a separate language that my goddamn video driver is going to compile on the fly.  No one really uses immediate mode these days, sneers someone who assumes that the only reason to write graphics code is to participate in a polygon jerkfest that you'll ship once and then throw away.

That's all great, except (a) I'm writing a 2D tile game in Python and really don't care if my video card is only at 99% efficiency, (b) I don't control the original code and am not really positioned to learn the entirety of OpenGL so I can port someone else's entire library to a thing that half their target audience doesn't support, (c) fuck you.

The ludicrous part is that immediate mode is _still there_ on desktops, and probably will be forever.  It's only missing from "OpenGL ES", a trimmed-down spec used on smaller devices (and which is [perfectly capable of emulating immediate mode anyway](https://www.jwz.org/blog/2012/06/i-have-ported-xscreensaver-to-the-iphone/)).  So the change has really only happened in the culture and ecosystem.  Surreal.

Anyway, uh.

Sometimes you do make a good trade, but you do a bad job of selling the advantages.  Remember Microsoft Office circa 2007 or so?  The menus were getting way out of hand, so someone had the brilliant idea to put as many items as possible into a fat tabbed toolbar.  As far as I can remember, everyone _hated it_.

But it was a good idea!  Office's menus were absolutely ludicrous, to the point that it was hard to even know what was _possible_.  The ribbon exposed a large chunk of Office's surface area in a visual way, similar to toolbars but with much more flexibility in grouping and labeling.  I don't think it was implemented as well as it could've been — the choice and arrangement of buttons was pretty questionable in places from what I saw, and the use of the ribbon for simpler apps like Paint seems kind of ridiculous — but it wasn't a bad attempt at dealing with overwhelming clutter.

Alas, it _also_ broke muscle memory, and that's a pretty serious thing to do.  Microsoft just sort of dropped it as though it spoke for itself, with little explanation as to the problem they thought they were solving.  So I can imagine that to a lot of people, this too seemed like shuffling things around for its own sake.

Python 3 has also done a pretty bad job of defending itself.  I'll, ah, leave that at that.

I see this a lot with Firefox changes, too, maybe because their internal bug tracker is open to the public.  Look at a thread for virtually any feature removal, and you'll probably find someone sternly asserting that Mozilla is clueless and Firefox is supposed to be about customizability and this is why they're switching to Chrome (which already removed the feature in question).

The problem here is that it's their bug tracker, intended for tracking the work, not justifying it.  Sometimes the scorn comes long before the change actually makes it into a final release, so there are no release notes yet; sometimes the change is innocuous enough not to make a big deal over.  One such case that always sticks out to me is the removal of the checkbox for disabling JavaScript, which outraged a few people who perceived it as a sign of reduced customizability.  But it turns out a non-trivial number of non-technical Firefox users had _inadvertently_ disabled JavaScript and then had no idea why half the Web was broken.  There's little reason to have a switch like that when NoScript offers a more surgical approach, either.  So away the checkbox went.

### Users do just hate change sometimes

Ah, but _why_?  I think too many developers trot this line out as an excuse to ignore all criticism of a change, which is very unhealthy.  Complaints will always taper off over time, but that doesn't mean people are _happy_, just that they've gone hoarse.  Or, worse, they've quietly left, and your graphs won't tell you why.  People aren't like computers and may not react instantly to change; they may stew for a while and drift away, or they may join a mass exodus when a suitable replacement comes along.

Twitter recently changed "favorites" to "likes" and swapped out the star for a heart.  I'm pretty used to this from Tumblr, so I was surprised by the amount of pushback.  Until I saw someone make a brilliant point (which I neglected to save a link to): these tiny changes bother us because they remind us that even our very personal spaces are owned by someone else.

Twitter is a very intimate platform; people use it to talk about themselves, talk to the people they care about.  Nobody _asked_ if changing a star to a heart was a good idea.  We don't even know who decided to do it or who was responsible for the work.  It was just dropped on us.  Not even to make the service better for us, but to make it more accessible to _new_ people — in service of the great god, Exponential Growth.

I can see how that would make people uncomfortable.

Tools aren't so personal, but changes to something you use every day are still jarring.  The whole point of a tool is to _disappear_.  You develop some muscle memory for it, you learn how to smoothly get stuff done, and you largely forget about it.  Then you upgrade something, and suddenly the tool breaks!  It leaps out of the background to say hey, here I am, remember me?  I know I'm very important, so let me tell you about all the new things you suddenly have to learn.

It can come across as hugely disrespectful of one's time.  I don't care about the developers' internal goals; if there's not some big and immediately-telegraphed advantage, you've basically barged into my house and rearranged all my furniture just because you can.

I'm reminded of whoosh, a Python text indexing library that veekun uses.  veekun has been largely in maintenance mode for the last few years, but every so often there's a flurry of changed data or bugfixes, and I have to update the site.  Several times now, whoosh has gotten an upgrade and abruptly broken in a very unclear way, and I've had to drop whatever I was doing and go figure out what changed and how to compensate.  I don't expect the library to _never_ change, but it's still frustrating to have a surprise timesink dropped in my lap if I want to keep my own software working how it worked yesterday.

The alternative would be to stick with an old version forever, but that seems impractical.  Software moves fast, and nobody keeps maintaining branches of their library that are more than a couple revisions old.  I'd fall behind on bugfixes or possibly even _security_ fixes, and catching up later would be all the more painful.


## What do we do about it?

Here, "we" refers to the developers, who hold all the power.  Which is, y'know, why change is annoying.

### Communicate

I remember the olden days when software came in boxes, and every box would brag about all the new amazing things it did.  It had to, to convince you to buy the new thing.

Now, half (or more) of the software you use every day just changes out from under you, and odds are good that there will be no explanation.  Or even acknowledgement.  Here are some things Twitter has publicly announced:

* We changed the star to a heart
* We made photo crops bigger
* We added polls
* We're making it easier to [shill Brands® to your friends](https://blog.twitter.com/2016/introducing-conversational-ads)
* We added a "top tweets" thing to the timeline (but only after a misunderstood rumor hit Buzzfeed)
* We're going to do something about abuse (half a dozen times so far, and with little explanation of what they think "abuse" means or what they plan to do about it)

Here are some things Twitter has _not_ publicly announced, and that have to either be figured out by the userbase or [dug out of earnings statements by the press](http://venturebeat.com/2016/02/10/twitter-is-fixing-that-thing-where-you-type-for-everyone-to-see-your-tweet/):

* We put a ton of people in an experiment that pops opens tweets in an overlay rather than expanding them inline
* We put some people in an experiment that rearranges the buttons on Android (particularly weird since one of my accounts is in it and the others are not)
* We are jpegging everything you upload into complete garbage
* We _expanded_ polls to include up to four options and an arbitrary time limit
* We're going to "fix" `.@` replies, whatever that means
* We're putting "who to follow" in your timeline

I don't know, some of those sound like things that are good to know?  That earnings statement mentions fixing the kind of obscure hacks like `.@` that make Twitter seem impenetrable to new users, but half the changes Twitter makes have to be spread through the grapevine, because they don't say what they're doing.  (For example, you can currently make a single pixel of an image translucent to get a PNG upload instead of a terrible JPEG.)

Some of these can't really be "announced", because they're still just experiments.  Sorry, hang on, if you have visibly and radically altered your product for a significant number of people, _you have changed it_.  If you decide to nix the change, that just means you changed it _back_.  There seems to be this idea that experiments aren't "really" part of the app yet, even though the code is there and running for a lot of people.

There's no avenue for feedback, either.  If there's a bug in Twitter, who do I report it to?  If an experiment sucks, how do I complain or get put in another cohort?  Tumblr is _full_ of bugs, and the mobile app in particular is atrocious, but who do I tell?  Even GitHub, who are pretty good about announcing the changes they make, have no real avenue for reporting bugs or critically-needed features in their core product.  Recently, a bunch of devs had to make a whole [song and dance](https://github.com/dear-github/dear-github) just to get some acknowledgement about minor issue-tracking features.  In my experience, the only way to get an obscure problem fixed on a popular platform is to know an employee on Twitter!

Check out this excerpt from Twitter's [timeline announcement](https://blog.twitter.com/2016/never-miss-important-tweets-from-people-you-follow):

> We've already seen that people who use this new feature tend to Retweet and Tweet more, creating more live commentary and conversations, which is great for everyone. To check it out now, just go into the timeline section of your settings and choose 'Show me the best Tweets first'. We'll be listening to your feedback and making it even better over time.

Did you catch that?  They know the feature is "great for everyone" because "people ... tend to retweet and tweet more", i.e., because the graphs go up and to the right.  So how will they "be listening to your feedback"?  Where do I put my feedback, exactly?

I'm not saying you should implement literally every feature request you get.  It's not a big secret that users don't always know what they want.  But they _do_ know what _problems they have_, and they know a hell of a lot better than you, especially if you [don't even use your own product](http://www.theguardian.com/technology/2015/apr/23/seven-of-twitters-11-top-executives-tweet-less-than-once-a-day).  Remember, many of Twitter's most fundamental features are just formalizations of idioms users invented to solve problems on their own.  Retweets and hashtags are user inventions!  Can you imagine Twitter without them now?

### Have a plan

In case you've lost track, here are Twitter's recent attempts at showing you important tweets:

* Discover, some combination of personalized stuff and "trending" junk — now gone
* Highlights, a blend of good stuff from my timeline and stuff slightly outside my circles, which works pretty well and has a neat dedicated UI — Android-only and buried in a menu
* Moments, a curated list of incredibly bland cable news stories — behind a very prominent button on all platforms
* While You Were Gone, a fairly useful though slightly buggy list of a few good tweets from your timeline — appears in your timeline whenever it feels like it, on all platforms
* Top Tweets, another list of tweets from your timeline?? — appears at the top of your timeline when you opt in

Meanwhile, you still can't scroll back more than a couple hours in your timeline without Twitter losing your place.  Maybe that's why we need so many of these recap features!  There are a few ways to avoid having your place lost, which work some of the time; more of that delightful apocryphal knowledge.  Or maybe this is fixed now?  Hell if I know; there's no changelog.

So how are Top Tweets different from While You Were Gone?  Why is the fairly solid Highlights still relegated to only one platform and hidden somewhere I'll generally forget about it?  I have no idea.  But all of these things (save Discover) now coexist simultaneously.

The impression I get is that they have _no goddamn clue what they're doing_, so they're throwing a bunch of stuff at the wall and hoping something will stick.  They're experimenting on me and hoping something will "work", where "work" is defined by a graph somewhere, and possibly the scowls of investors.  This does not fill me with confidence.

So.  Have a plan, and continuing with the "communication" theme, maybe share what that plan is.  I know, it sucks to say you'll do something and then change your mind later, but it _is_ possible to give out some speculative plans without diluting them down to marketing noise.

Hey, let's pick on Tumblr again.  Responding to people on Tumblr is pretty weird (and bad, but that's another post).  Generally you reblog them to add commentary, but that means the entire exchange is now on _your_ blog for all to see, which you may not want.  There are Disqus comments (?!), but most people don't bother enabling them, and of course the accounts are totally separate.

As a decent middle ground, you could enable "replies", which let followers (and only followers — there's not even UI for this outside the dashboard) add a brief plaintext response.  It would only appear in the activity for that post.  It got pretty popular among art circles — and what is Tumblr good for if not sharing art — where fans could say "hey this is cool!" without making tons of full reblogs.

And then Tumblr removed it.  [Three and a half months ago](http://support.tumblr.com/post/131951272032/pardon-our-dust-hey-you-know-the-reply-feature).  They're "making room for something bigger and better coming down the pike", and apparently that required outright deleting a feature and leaving it with no equivalent in the meantime.  [Only a few thousand blogs a month were even receiving them](http://www.davidslog.com/132564574700/wizardries-can-tumblr-make-it-so-we-can-reply), and, well, fuck those few thousand blogs.  Weird how these two announcement posts have 153,000 and 80,000 notes for such an obscure feature, though.

### This applies to policy too

**Policy is part of your UI.**  It governs what people can and cannot do and expect, albeit in social rather than technical terms.

So it's slightly maddening when no one has any idea what the policies _are_.  Virtually no platform publicizes who they punish, for what, or why.  Contrast with most legal systems, where virtually everything is public record.  It _has_ to be, or we can't tell how the law is interpreted or who's being punished unfairly.  Whoops, that's exactly what happens with platforms.

Twitter has some kind of copyrighted tweet system in place now, yet tons of hyper-popular "parody" accounts that just repost others' jokes are still around.  An account parodying Twitter's confounding treatment of harassment reports was [suspended](http://motherboard.vice.com/read/trusty-support-why-twitter-suspended-an-account-that-makes-fun-of-twitter)...  for trademark violation, over the word "support".  I recently heard that a couple accounts were permanently suspended after receiving too many DMCA reports...  over anime screencaps...  from a company that has no relation to the anime.  Plus there's the handling of harassment reports, but that's a whole separate can of worms.

If this is what you see happen in practice, and you have zero insight into the decision-making process, how are you supposed to know what the rules really are?  There's no case law.  Or, rather, there _is_ case law, but only the judges get to know what it is.

I can guess at why this happens.  Liability, something something, of course.  Less obviously, if you explain your reasons to someone in great detail, there is a _much_ better chance that they will endlessly nitpick your decision.

Meanwhile, at Tumblr, I've heard multiple anecdotes about artists who've had their blogs permanently nuked after receiving too many bogus reports from people holding a grudge.  How did they violate the rules?  No one seems to know, and the only way you find out you've been reported is by having your post deleted, at which point you can't see what the post contained.  What's allowed, then?  Who knows?  On the other hand, I've reported things on Tumblr that virtually mirror an example of disallowed behavior they have in their own rules, and nothing has happened.  One might reasonably start to think that the reporting system is largely automatic and geared towards covering Yahoo's ass, not so much enforcing their own rules.

Besides the complete black hole from which judgment emerges, I think a major problem here is that none of these platforms really have any level of punishment between "quietly do nothing" and "delete you forever".  Twitter can lock your account until you comply with their demands, which is interesting, but still pretty heavy-handed.  If a situation calls for a "hey could you knock this off" — which I'm sure is very common — then there's nothing to be done.

And, of course, I have never in my life seen any kind of repercussion for abusing a reporting system.

This all exemplifies the worst about UI change in the platform era.  No one knows what's going on, no one knows when something will suddenly drop out from under them, and only a small handful of experts can actually navigate effectively.

----

Please be careful with your UI changes.  Most of us understand the need to change things sometimes, but at the very least, you could acknowledge the trouble you're causing and explain what you're up to.  You know, treat your userbase as humans rather than Sims™.  Thanks.  ♥
