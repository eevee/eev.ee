title: Attribution on the web
date: 2016-08-15 01:00
category: articles
tags: tech, web, culture

The web is a great thing that's come a long way, yadda yadda.  It used to be an obscure nerd thing where you could read black Times New Roman text on a gray background.  Now, it's a hyper popular nerd thing where you can read black Helvetica Neue text on a white background.  I hear it can do other stuff, too.

That said, I occasionally see little nagging reminders that the web is still quite primitive in some ways.  One such nag: it has almost no way to preserve attribution, and sometimes actively strips it.

As a programmer, I'm here to propose some technical solutions to this social problem.  It's so easy!  Why hasn't anyone thought of this before?

<!-- more -->

----

I'm mostly thinking about images, but most of these ideas apply to other forms of media as well.

If you are familiar with The Twitter or other form of social media (read: website with people on it), you've seen some images float past.  The vast majority were probably some form of artwork, interpreted loosely: maybe a photo, maybe a screenshot of part of an article.

Perhaps you have also asked the age-old question, _where did this come from?_

It can be surprisingly difficult to answer, and the web-savvy have a mental toolbox for figuring it out.  You can try asking the person who tweeted it, but they might not know either, if it came from their hard drive or another social site.  If it's a screenshot of text, you can manually retype the text in a search engine and hope for the best.  Otherwise, you can use reverse image search and...  again, hope for the best.  Ironically, a great deal of images on Twitter and Tumblr and Facebook don't seem to be indexed by Google's reverse image search, so if one of those is the original source (and a lot of people use Tumblr as a primary art gallery!), you're out of luck.

The web is supposed to be a glorious land where anyone can contribute their own voice and work, so it's a wee bit conspicuous to me that we're pretty bad at preserving _who made_ that stuff.

A lot of art sites do make some small effort at this.  I looked at DeviantArt's front page and the top item was [Last Wish by radittz](http://radittz.deviantart.com/art/Last-Wish-628186535), for which the direct link is `last_wish_by_radittz-dae07tz.jpg`.  If someone links the image directly (and this happens fairly frequently, for whatever reason), I have a pretty good idea of how to find the page dedicated to it.

If you _save_ it, a little more effort is involved.  If you don't recognize DeviantArt's particular filename pattern, you won't even know what site it came from.  (The `da` near the end seems to be constant, so maybe it's meant to stand for "DeviantArt", but to me it just looks like part of that nonsense slug.)  You can try googling the filename, which sometimes works, but I don't think Google itself indexes those.  You can of course google the title and the artist name, and that'll probably work — but if you have to use Google at all, the filename is clearly not working very well as a _global_ identifier.

Non-art-gallery social sites, meanwhile, use unintelligible slurry as filenames.  Twitter uses a short string of alphanumeric garbage.  Facebook uses three long sequences of digits, separated by underscores.  Tumblr is kind enough to start their filenames with `tumblr_`, which narrows it down a _bit_, but the rest is alphanumeric junk again.  None of these platforms give you a way to get from an image filename back to an original post (and author!), and Google generally can't make heads or tails of them.  Even Google's reverse image search generally comes up blank for an image that only exists on Tumblr.

The big three images formats — PNG, JPEG, and GIF — all support arbitrary metadata.  It wouldn't be terribly difficult to agree on some simple format for storing attribution.  Show it in the UI, add it if it's not there, and otherwise preserve it.  Image metadata isn't surfaced too well in a lot of image editors, but perhaps that'd start to change if it were used for something _interesting_ and not just "this was made in Photoshop!"

The rest of this post is dedicated to explaining why that won't possibly work.  Sigh.


## Problem: identity

First question: what precisely do you attribute work _to_?

Hmm.

The obvious thing is that if you upload a new image to Twitter and it doesn't already have some form of attribution, it gets attributed to your Twitter account.  But that's clearly not right.  Maybe you have a website and think of that as identifying you.  Or maybe you use Tumblr or DeviantArt or Twitch or whatever, and you think of one of those as your "primary" representation.  You could always manually add the attribution metadata, but who would bother?  I don't know if _I_ would bother.

Even quite a few years into the web game, we don't have any real concept of global identifiers (say, URLs) for _people_.  That's kind of weird.  We do have email addresses, but those are black holes you _write to_, not something you can read.  (Various proposals have attempted to bridge this gap; none have caught on.)

Of course, individual platforms have little interest in trying to fill this gap, since they all want you to use _them_ as your primary identity.  Ever seen a small forum with built-in support for linking to your profile on a bunch of other sites?  Enter your YouTube account name, and now your posts will have a tiny YouTube logo pointing straight there.  Somehow these end up working as _better_ hubs than huge platforms.  Good luck linking to much of anything on Twitter: you can put one URL in the URL field, and you can sacrifice your bio and pinned tweet to squeeze a couple more in.  Hell, I keep seeing Brand™ accounts that use Snapchat's QR-code-esque thing for their avatars, which makes them all nigh indistinguishable.

Okay, what about attributing to whatever's in the account's URL field?  I don't know if that would work, either — this website doesn't actually have my artwork on it.  In fact, the more I think about this, the more I'd want the attribution to point to the original page hosting the work, not just the person.  (Or...  perhaps both?)  That creates a chicken-and-egg problem that only the site you upload to can actually resolve.

What of creators that aren't even people?  Say, GIFs or screencaps from a TV show or movie.  Does every TV show and movie have its own website?  Does it make sense to attribute like that if you can't even find the given material on those sites?  Does anyone know or care where those websites are?


## Problem: resharing

Art sites are probably willing to stick the uploader's name in the filename because for the most part, _the uploader is the creator_.  That's the whole point of an _art_ site, after all.

In a general-purpose forum, the uploader is almost certainly _not_ the creator.  That's not a condemnation, just common sense: any given work can only be created _once_, but can be shared any number of times.

So if you're Twitter, and you really buy into this whole idea, what do you do when someone uploads an image with no attribution?  Do you leave it blank (somewhat defeating the purpose), attribute it to them (almost certainly wrong), or force them to enter something (a good way to kill your platform)?

If you're uploading a screenshot of some text...  where is the attribution ever going to come from?  Built into your screenshot tool, by some demon magic?

Twitter also reminds me of kind of the inverse problem: it re-encodes your images as relatively low-quality JPEGs, even if they were already JPEGs!  Twitter itself could just preserve the metadata when it does this, but how many other platforms resize or re-encode your uploads and lose the metadata in the process?


## Problem: remixing

Remixing is great, but it raises some questions here.

If you have two source images and you edit them together somehow, who gets the attribution?  You?  One of the original creators?  All three?

Okay, let's say attribution is a list, and image editors are clever and know how to combine attributions.  Now what if you only opened the image in your editor to scale it down, crop it, or (how ironic) erase the artist's signature?  Do you still get attribution?


## Problem: assholes

There are already people who erase artists' signatures from their work (for seemingly _no reason_; this is so baffling), and there would of course be people who erase the original attribution and claim it as their own.  That's thinking small, though.

If a wizard cast a spell to make this system widespread overnight, two things would immediately happen in quick succession.

1. Someone would build a thing to index attributions from all across the web, so you can search for a creator and find all of their work.

2. Some asshole would start adding false attributions to horrible images, so the search would make people they don't like look bad.

I already hear someone yelling from the back about PGP signatures — for data I'm not sure how to reliably get onto files in the first place.  Yeah.  Good luck with that.


## Problem: no one cares, really

Twitter has a number of self-described "parody" accounts that exist solely to steal other people's jokes, rack up followers, and then get paid big bucks by advertisers to drop in the occasional link to some skeezy thing that can't survive on its own merits.

Twitter has, by and large, not done a goddamn thing about any of these.  I can't imagine them buying into a whole system of attribution.

Less obviously, consider: both Twitter and Tumblr prominently feature ways to share other people's work while preserving the attribution (as long as they're on the same platform, of course).  Twitter has retweets; Tumblr has reblogs.  However, _neither_ of them have any way to browse through a user's post history _excluding reshares_.  Twitter has "images-only" view, but that only works if your work is visual, doesn't include embeds, and includes other junk like photos of your cats; Tumblr has a standard archive view, which is at least nicer than scrolling back a page at a time, but makes it even harder to distinguish originals from reblogs.

Both platforms also treat work as semi-disposable: the primary interface is a chronological-ish deluge of _stuff_, and anything you miss is basically lost forever.  They both archive everything back to the beginning of time, but navigating backwards on either is kind of painful.  Especially Twitter, where you're stuck with either infinite scrolling or manually filtering by date via Twitter search.

I guess the _true_ problem here isn't really metadata, but the sharp contrast between platforms for people who _make stuff_ and platforms for people who _look at stuff_.  (Most of us are some blend of both, of course — all the more reason that the separation sucks.)  Twitter is made for looking and sharing, so it's used by everyone but sucks for creators; something like Flickr is made for making, so it has a lot of relevant tools but isn't very heavily frequented.  The result is that work gets clumsily cross-posted all over the place, and it's left to individual creators to come up with their own ad-hoc rituals for disseminating new work.

Even the maker platforms are struggling a bit lately.  DeviantArt looks to be in decline since everyone flocked to Tumblr, but Tumblr is a poor substitute for an art gallery.  YouTube is 70% pirated TV shows by volume.  Twitch and other streaming sites treat work as even more disposable than Twitter, not saving it _at all_ by default.  (There are obvious economic reasons for this, but still.)

Embedding would be a helpful alternative solution to this: put your work on a maker platform, then just link it everywhere else.  Twitter sort of does this already; I think Facebook does it a bit but is more limited in what it embeds; Tumblr basically doesn't do it at all.

If Twitter is really the reigning champ in this area, then it's in a pretty sorry state.  Embeds are very clearly second-class citizens.  If you post a few images on Tumblr as a photo set and then link them on Twitter, Twitter will only preview a crop of the first one, and you'll have to click through to the actual Tumblr website (even on mobile, where it is buggy garbage) to get a full view or see the rest.  Twitter's preview doesn't even hint that there _are_ more.


## Sigh

Attribution seems like such a trivial thing for computers to track for us...  yet it would take a complete overhaul of how we think about and handle media, plus buy-in from numerous large companies that aren't known for cooperating with each other.

Maybe this isn't a real problem.  We seem to be managing okay so far.  It nags at me from time to time, though, as a sign that the web just doesn't interoperate with itself terribly well.

Now if you'll excuse me, I'm off to link to this post on Twitter and Patreon.
