title: In which i use GitHub, and IRC is awesome
date: 2011-10-17 21:36
modified: 2013-01-11 14:28
category: articles
tags: git, tech

I just wasted way too much time migrating all of my git repositories to [GitHub][github].  It's way less janky than the [old thing][gitweb], and the guys running it seem to be acceptably hipster-nerdy.

I'm still using Redmine as a [bug tracker][], and i have a cron going that updates the [old repositories][gitweb] regularly, so commits will still appear in tickets and whatnot.  This is just a change of canon.

I _am_ considering giving GitHub Issues a shot for small new projects, just to get a feel for it.  Redmine is powerful but feels like it's targeted at my manager.  GitHub is, i must admit, very much targeted at the people on the ground doing the hacking.

Anyway, here is a story.

<!-- more -->

GitHub has push notifications for a variety of services.  One of them is IRC.  It will actually fire up a bot, connect to your server, join your channel, and spit out new commits.  This is totally awesome, except that the bot doesn't hang around (understandably), and i don't really want join/part spam surrounding every single commit.

The bot can try to notify without joining the channel, but i couldn't find a way to let a specific client punch through `+n`, and IRC server developers kind of frown on hiding joins because it leads to crazy spying from opers.  I was considering just setting #veekun `-n` and hoping for the best.

Until [habnabit][] proposed the following.

    :::text
    /mode #veekun -n
    /mode #veekun +b m:*!*@*
    /mode #veekun +e m:j:#veekun
    /mode #veekun +e m:github!*@*

This will:

* Allow anyone to talk to the channel, without being in it.
* Prevent anyone from talking in the channel at all.
* Exempt people already in the channel from the above ban.
* Exempt the github bot from the above ban.

Effectively it recreates `+n` using ban masks, then adds an exception for the bot.

This is so stupid.  I can't believe it works.  Channel matching is meant for teenaged channel warfare or keeping out a known cluster of riffraff, not recursive shenanigans like this.  I am delighted.

## If you got here by Googling how to do this

Using the above modes is a super easy way for GitHub's IRC bot to notify your channel without joining or parting.  You don't have to add explicit exceptions for new users or otherwise maintain it in any way.  It's magic.

I'm using Inspircd 2.0, but other ircds tend to have similar matching and muting.  For UnrealIRCd:

    :::text
    /mode #veekun -n
    /mode #veekun +b ~q:*!*@*
    /mode #veekun +e ~q:~c:#veekun
    /mode #veekun +e ~q:github!*@*

And, of course, change `#veekun` and `github` to the name of your channel and bot respectively.  You may also have to fix your channel's ChanServ modelock (sometimes called "mlock") to allow the `-n`.

## Closing the loophole

Other people can, technically, change to the bot's nick and babble to your channel from the outside.  This is easy to fix.

First register the bot's nick with NickServ.  You can either set its password as the hook's server password (most IRC services allow using the server password as a NickServ password), or use the ACCESS list to auto-identify connections from `*.github.com`.

Then, only allow the bot to talk to your channel if it's identified.  Replace the fourth line with this for Inspircd:

    :::text
    /mode #veekun +e m:R:github

Or this for Unreal:

    :::text
    /mode #veekun +e ~q:~R:github

If you don't have IRC services and/or don't want to futz with them, you can instead change `github!*@*` to something like `github!*@*.github.com` or even `*!*@*.github.com`, so the exception only applies to connections from GitHub servers.  But going through NickServ has the advantage that you can have anyone using the nick automatically KILLed if they don't identify for it, preventing someone from stealing the nick and blocking your notifications.


[bug tracker]: http://bugs.veekun.com/
[github]: https://github.com/eevee
[gitweb]: http://git.veekun.com/
[habnabit]: https://twitter.com/#!/habnabit
