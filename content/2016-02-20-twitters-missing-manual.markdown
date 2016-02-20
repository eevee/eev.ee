title: Twitter's missing manual
date: 2016-02-20 04:57
category: blog
tags: tech, ui


I mentioned recently, buried in [a post about UI changes](/blog/2016/02/10/we-have-always-been-at-war-with-ui/), that Twitter's latest earnings report [included this bombshell](http://venturebeat.com/2016/02/10/twitter-is-fixing-that-thing-where-you-type-for-everyone-to-see-your-tweet/):

> We are going to fix the broken windows and confusing parts, like the .@name syntax and @reply rules, that we know inhibit usage and drive people away

There's an interesting problem here.  UI is hard.  You can't just slap a button on the screen for every feature that could conceivably be used at any given time.  Some features are only of interest to so-called "power users", so they're left subtle, spread by word-of-mouth.  Some features you try to make invisible and heuristic.  Some features are added just to solve one influential user's problem.  Some features are, ah, accidental.

A sufficiently mature, popular, and interesting product thus tends to accumulate a small pile of hidden features, sometimes not documented or even officially acknowledged.  I'd say this is actually a _good thing_!  Using something for a while should absolutely reward you with a new trick every so often — that below-the-surface knowledge makes you feel involved with the thing you're using and makes it feel deeper overall.

The hard part is striking a balance.  On one end of the spectrum you have tools like Notepad, where the only easter egg is that pressing F5 inserts the current time.  On the other end you have tools like vim, which consist exclusively of easter eggs.

One of Twitter's problems is that it's tilted a little too far towards the vim end of the scale.  It looks like a dead-simple service, but those humble 140 characters have been crammed full of features over the years, and the ways they interact aren't always obvious.  There are rules, and the rules generally make sense once you know them, but it's also really easy to overlook them.

Here, then, is a list of all the non-obvious things about Twitter that I know.  Consider it both a reference for people who aren't up to their eyeballs in Twitter, and an example of how these hidden features can pile up.  I'm also throwing in a couple notes on etiquette, because I think that's strongly informed by the shape of the platform.

<!-- more -->


## Text

* Tweets are limited to 140 _Unicode_ characters, meaning that even astral plane characters (such as emoji) only count as one.

* Leading and trailing whitespace is stripped from tweets.

* Tweets may contain newlines, and there doesn't seem to be any limit to how many.

* In the middle of a tweet, strings of whitespace (e.g. multiple spaces) are preserved.

* Anything remotely resembling a link will be mangled into some `http://t.co/asdf` link-shortened garbage.  In some cases, such as when talking about a domain name, this can make the tweet _longer_.  You can defeat this by sticking an invisible character, such as U+200D ZERO WIDTH JOINER, around the final dot so it no longer looks like a domain name.

* For the sake of its SMS-based roots, Twitter supports performing several commands by typing them _in a tweet_.  In particular, if you start a tweet with the word `d` or `dm`, the second word will be treated as a username, and the rest of the tweet will be DM'd to that user.

* Accounts managed by multiple people, such as support accounts or politicians' accounts, sometimes sign tweets with a `^` followed by the author's initials.  This has no special significance to Twitter.


## Replies and mentions

A tweet can "mention" other users, which just means including their `@handle` somewhere in the tweet.  This will notify every mentioned user of the tweet.

* A tweet that _begins_ with a mention — that is, the very first character is `@` and it's immediately followed by an extant username — won't appear on your profile on Web Twitter.  It'll still appear on the "with replies" page.  It'll also appear on your profile on Android Twitter, which doesn't separate replies from not.

* A tweet that begins with a mention won't appear on the timelines of anyone who follows you, _unless_ they also follow the first person you mention.  That is, if you tweet `@foo @bar heya`, it'll only appear on the timelines of people who follow both you and `@foo`.

* If you put some other character before the first `@`, the previous rule no longer applies, and your tweet will appear to all your followers.  So `.@foo @bar heya` will be visible to everyone (and show on your Web profile).  This is called "dot-replying".  The dot isn't actually special; it's just an easy-to-type and unobtrusive character.  I like to use `→` or `\\`.  Some people prefer to put the mentions at the end instead, producing `heya @foo @bar`.

You can reply to tweets, which threads them together.  A tweet can only have one parent (or no parent), but any number of replies.  Everything on Twitter is thus arranged into a number of trees, where the root of the tree is a new tweet not responding to anything, and replies branch out from there.

* A reply _must_, somewhere, mention the author of the tweet it's replying to.  If you reply to a tweet and delete the author's `@handle`, it'll become a new top-level tweet rather than a reply.

* There is one exception to the previous rule: if you're replying to _yourself_, you don't have to include your own `@handle`, even though clients include it by default.  So if you want to say something that spans multiple tweets, you can just keep replying to yourself and deleting the `@handle`.

    It's a really good idea to do this whenever you're making multiple tweets about something.  Otherwise, someone who stumbles upon one of the tweets later will have no idea what the context was, and won't be able to find it without scrolling back however long on your profile.

    If you reply to yourself but leave your `@handle` at the beginning, the first tweet will appear on your profile, but the others won't, because they start with a mention.

* The previous rule also applies when making longer replies to someone else.  Reply to them once, then reply to _yourself_ with the next tweet (and remove your own `@handle`).  You'll end up with three tweets all threaded together.

    This is even more important, because Twitter shows the replies to a tweet in a somewhat arbitrary order, bubbling "important" ones to the top.  If you write a very long response and break it across three tweets, all replying to the same original tweet, they'll probably show as an incoherent jumble to anyone reading the thread.  If you make each tweet a reply to the previous one, they're guaranteed to stay in order.

* Replying to a tweet will also prefill the `@handle` of anyone mentioned in the tweet.  Replying to a retweet will additionally prefill the `@handle` of the person who retweeted it.  In some cases, it may be polite to remove some of these; you only need the original author's `@handle` to make a reply.  (It's not uncommon to accumulate multiple mentions, then end up in an extended conversation with only one other person, while constantly notifying several third parties.)

* In official clients (Web and Android, at least), long threads of tweets are collapsed on your timeline.  Only the first tweet and the last _two_ tweets are visible.  If you have a lot to say about something, it's a good idea to put the important bits in one of those three tweets where your followers will actually see them.  This is another reason it's polite to thread your tweets together — it saves people from having their timelines flooded by your tweetstorm.

    Sometimes, it's possible to see multiple "branches" of the same conversation on your timeline.  For example, if A makes a few tweets, and B and C both reply, and you follow all three of them, then you'll see B's replies and C's replies separately.  Clients don't handle this particularly well and it can become a bit of a clusterfuck, with the same root tweet appearing multiple times.

* Because official clients treat a thread as a single unit, you can effectively "bump" your own tweet by replying to it.  Your reply is new, so it'll appear on your followers' timelines; but the client will also include the first tweet in the thread as context, regardless of its age.

* When viewing a single tweet, official clients may not show the replies in chronological order.  Usually the "best" replies are bumped to the top.  "Best" is entirely determined by Twitter, but it seems to work fairly well.  If you reply to yourself, your own replies will almost certainly appear first.

* If reply to a tweet with `@foo heya`, and `@foo` later renames their account to `@quux`, the tweet will retain its threading even though it no longer mentions the author of the parent tweet.  However, your reply will now appear on your profile, because it doesn't begin with the handle of an existing user.  Note that this means it's fairly easy for a non-follower to figure out what you renamed your account to, by searching for replies to your old name.

* Threads are preserved even if some of the tweets are hidden (either because you've blocked some participants, or because they have their accounts set to private).  Those tweets won't appear for you, but any visible replies to them will.

* If a tweet in the _middle_ of a thread is deleted (or the author's account is deleted), the thread will break at that point.  Replies to the deleted tweet won't be visible when looking at the parent, and the parent won't be visible when looking at the replies.

* You can _quote_ tweets by including a link to them in your tweet, which will cause the quoted tweet to appear in a small box below yours.  This _does not_ create a reply and will not be part of the quoted tweet's thread.  If you want to do that, you can't use the retweet/quote button.  You have to reply to the tweet, manually include a link to it, _and_ be sure to mention the author.

* When you quote a tweet, the author is notified; however, unlike a retweet, they won't be notified when people like or retweet your quote, unless you also mention them.

* Due to the nature of Twitter, it's common for a tweet to end up on many people's timelines simultaneously and attract many similar replies within a short span of time.  It's polite to check the existing replies to a popular tweet, or a tweet from a popular person, before giving your two cents.

* It's generally considered rude to barge into the middle of a conversation between two other people, especially if they seem to know each other much better than you know them, and especially if you're being antagonistic.  There are myriad cases where this may be more or less appropriate, and no hard and fast rules.  You're a passerby overhearing two people talking on the street; act accordingly.

* When you quote or publicly mention someone for the sake of criticizing them, be aware that you're exposing them to all of your followers, some of whom may be eager for an argument.  If you have a lot of followers, you might inadvertently invite a dogpile.

## Hashtags

Hashtags are a `#` character followed by some number of non-whitespace characters.

* Exactly _which_ characters may appear in a hashtag is somewhat inconsistent, and has quietly changed at least once.

* The only real point to hashtags is that you can click on them in clients to jump directly to search results.

* Hashtags can appear in the "trending" widget, but so can any other regular text.

* There is no reason to tag a bunch of random words in your tweets.  No one is searching Twitter for `#funny`.  Doing this makes you look like an extremely out-of-touch marketer.

* Twitter also supports "cashtags", which are prefixed with a `$` instead and are generally stock symbols.  I only even know this because it makes shell and Perl code look goofy.


## Media

A tweet may have _one_ embedded attachment.

* You may explicitly include a set of up to four images _or_ a video _or_ a poll.  You cannot combine this within a single tweet.  Brands™ have access to a handful of other embedded gizmos.

* If you include images or a video, you will lose 24 characters of writing space, because a direct link to the images/video will be silently added to the end of your tweet.  This is for the sake of text-only clients, e.g. people using Twitter over SMS, so they can see that there's an attachment and possible view it in a browser.

* Including a poll will not append a link, but curiously, you'll still lose 24 characters.  It's possible this is a client bug, but it happens in both Web and Android Twitter.

* Alternative clients may not support new media types at first.  In particular, people who used TweetDeck were frequently confused right after polls were launched, because TweetDeck showed only the tweet text and no indication that a poll had ever been there.  If this happens again in the future, consider mentioning when you're using a new feature.

* If you don't include an explicit attachment, Twitter will examine the links in your tweet, in _reverse_ order.  If you link to a tweet, that tweet will be quoted in yours.  If you link to a website that supports Twitter "cards" (small brief descriptions of a site, possibly with images), that card will be attached.  There can only be one attachment, so as soon as Twitter finds something it can use, it stops looking.

* Quoted tweets are always just tweets that include links to other tweets.  If the link is the last thing to appear in the tweet text, official clients _will not show_ the link.  This can be extremely confusing if you try to link to two tweets — the first one will be left as a regular link, and the second one will be _replaced_ by a quoted tweet, so at a glance it looks like you linked to a tweet and it was also embedded.  A workaround for this is just to add text after the final link, so it's not the last thing in the tweet and thus isn't hidden.

* Twitter cards may be associated with a Twitter account.  On Android Twitter (not Web Twitter!), replying to a tweet with a card will also include the `@handle` for the associated account.  For example, replying to a tweet that links to a YouTube video will prefill `@YouTube`.  This is pretty goofy, since YouTube itself didn't _make_ the video, and it causes replies to notify the person even though the original link doesn't.

* Uploaded media may be flagged as "sensitive", which generally means "pornographic".  This will require viewers to click through a warning to see the media, unless they're logged in and have their account set to skip the warning.  Flagged media also won't appear in the sidebar on profile pages for people who have the warning enabled.

* The API supports marking individual tweets as containing sensitive media, but official clients _do not_ — instead, there's an account setting that applies to everything you upload from that point forward.  Media may also be flagged by other users as sensitive.  Twitter also has some sort of auto-detection for sensitive media, which I only know about because it sometimes thinks photos of my hairless cats are pornographic.

* If _your own_ tweets have "sensitive" media attached, _you_ will have to click through the warning, even if you have the warning disabled.  A Twitter employee tells me this is so you're aware when your own tweets are flagged, but the message still tells you to disable the warning in account settings, so this is mostly just confusing.


## Blocking and muting

* A blocked user cannot view your profile.  They can, of course, use a different account, or merely log out.  This is entirely client-side, too, so it's possible that some clients don't even support this "feature".

* A blocked user cannot like or retweet your tweets.  (I believe blocking may cause any existing likes to be undone, but I'm not clear on this.)

* A blocked user cannot follow you.  If you block someone who's already following you, they'll be forced to immediately unfollow.  Likewise, you cannot follow a blocked user.

* A blocked user's tweets won't appear on your timeline, or in any thread.  As of fairly recently, their tweets won't appear in search results, either.  However, if you view the profile of someone who's retweeted a blocked user, you **will** still see that retweet.

* A blocked user **can** see your tweets, if someone they follow retweets you.

* A blocked user **can** mention or reply to you, though you won't be notified either by the tweet itself or by any retweets/likes.  However, if someone else replies to them, your `@handle` will be prefilled, and you'll be notified.  Also, other people viewing your tweets will still see their replies threaded.

* A blocked user **can** link to your tweets — however, rather than an embedded quote, their tweet will have a gray "this tweet is unavailable" box attached.  This effect is retroactive.  However (I think?), if a quoted tweet can't be shown, the _link_ to the tweet is left visible, so people can still click it to view the tweet manually.

* Muting has two different effects.  If you mute someone you're _following_, their tweets won't appear in your timeline, but you'll still get notifications from them.  This can be useful if you set your phone to only buzz on notifications from people you follow.  If you mute someone you're _not following_, nothing they do will send you notifications.  Either way, their tweets will still be visible in threads and search results.

* It's trivial to tell whether someone's blocked you, since their profile will tell you.  However, it's _impossible_ to know for sure if someone has muted you or is just manually ignoring you, since being muted doesn't actually prevent you from doing anything.

* You can block and mute someone at the same time, though this has no special effect.  If you unblock them, they'll just still be muted.

* Tweeting screenshots of "you have been blocked" is getting pretty old and we can probably stop doing it.


## Search

* I _believe_ all of Twitter's advanced search options are exposed on the [advanced search page](https://twitter.com/search-advanced).  All of them are shorthand for using a prefix in your search query; for example, "from these accounts" just becomes something like `from:username`.

* Search applies to _unshortened_ links, so you can find links to a website just by searching for its URL.  However, because Twitter displays links without a protocol (`http://`), you have to leave it off when searching.  Be aware that people who mention your work without mentioning _you_ might be saying unkind things about it.

* As a side effect, you can search for _quotes_ of a given user's tweets by searching for `twitter.com/username/status`, because all tweet URLs begin with that prefix.  This will also include any tweets from that user that have photos or video attached, because attaching media appends a photo URL, but you can fix that by adding `-from:username`.

* Searching for `to:foo` will only find tweets that _begin with_ `@foo`; dot-replies and other mentions are not included.  Searching for `@foo` will find mentions as well as tweets from that person.  To find only someone's mentions, you can search for `@foo -from:foo`.  You can combine this with the above trick to find quotes as well.

* `from:` only applies to the handle a user had _when the tweet was made_.  If someone changes their handle, you still need to use their old handle to find their old tweets.

* Some clients, such as TweetDeck, support showing live feeds of search results right alongside your timeline and notifications.  It's therefore possible for people to keep an eye on a live stream of everyone who's talking about them, even when their `@handle` isn't mentioned.  Bear this in mind when grumbling, especially about people whose attention you'd prefer to avoid.

* Namesearch — that is, look for mentions of you or your work that don't actually `@`-mention you — with caution.  Liking or replying amicably to tweets that compliment you is probably okay.  Starting arguments with people who dislike your work is rude and kind of creepy, and certainly not likely to improve anyone's impression of you.


## Locked accounts

* You may set your account to private, which will hide your tweets from the general public.  Only people who follow you will be able to see your tweets.  Twitter calls this "protected", but since it shows a lock icon next to your handle, everyone calls it "locked".

* Specifically: your banner, avatar, display name, and bio (including location, website, etc.) are still public.  The _number_ of tweets, follows, followers, likes, and lists you have are also public.  Your actual tweets, media, follows, followers, lists, etc. are all hidden.

* When you lock your account, any existing followers will remain.  Anyone else will only be able to send a follow _request_, which you can then approve or deny.  You can force anyone to unfollow you at any time (whether locked or not) by blocking and then unblocking them.  Or just blocking them.

* It's unclear whether denying a follow request actually notifies the requester in any way.  Come to think of it, I'm not sure _approving_ a follow request notifies the requester, either, except that your tweets will start appearing on their timeline.

* If you _unlock_ your account, any pending follow requests are automatically accepted.

* There is (to my knowledge) no way to see a list of all the locked accounts you've tried to follow but that haven't yet accepted.

* No one can retweet a locked account, not even followers.

* Quoting doesn't work with locked account; the quoted tweet will only show the "unavailable" message, even if a locked account quotes itself.  Clicking the tweet link will still work, of course.

* Locked accounts never create notifications for people who aren't following them.  A locked account can like, retweet, quote, follow, etc. as usual, and the various numbers will go up, but only their followers will be notified.

* If a locked account likes a bunch of your tweets (or retweets, etc.), and then you follow them, the notifications will not be created retroactively.

* Locked accounts do not appear in the lists of who liked or retweeted a tweet (except, of course, when viewed by someone following them).

* While a locked account's own follows and followers are hidden, a locked account **will still appear publicly** in the following/follower lists of other unlocked accounts.  There is no blessed way to automatically cross-reference this, but be aware that the _existence_ of a locked account is still public.  In particular, if you follow someone who keeps an eye on their follower count, they can just look at their own list of followers to find you.

* Anyone can still mention a locked account, whether or not they follow it, and it'll receive notifications.

* Open DMs ("receive direct messages from anyone") work as normal for locked accounts.  A locked account can send DMs to anyone with open DMs, and a locked account may turn on open DMs to receive DMs from anyone.

* Replies to a locked account are **not** protected in any way.  If a locked account participates in a thread, its own tweets will be hidden from non-followers, but any public tweets will be left in.  Also, anyone can search for mentions of a locked account to find conversations it's participated in, and may be able to infer what the locked account was saying from context.


## Other clients

I've mentioned issues with non-primary clients throughout, but a couple more things to be aware of:

* The official API doesn't support a number of Twitter features, including polls, ads, and DMs with multiple participants.  Clients that use the API (i.e. clients not made by Twitter) thus cannot support these features.

* Even TweetDeck, which is maintained by Twitter, frequently lags behind in feature support.  TweetDeck had the original (client-side-only) implementation of muting, but even after Twitter added it as a real feature, TweetDeck was never changed to make use of it.  So TweetDeck's muting is separate from Twitter's muting.
