title: Security through misanthropy
date: 2015-08-22 18:03
category: essay
tags: infosec

I love programming.  It's like playing with Lego — here are some blocks, see what you can build with them.

That sounds a bit less impressive now, but when I was a kid walking uphill both ways, I only had a very generic Lego set where all the pieces were cuboids.  If I wanted to build a house with a sloped roof, well, that was too bad.  I could cheat a little, though, by making several layers in a terrace pattern.  It wasn't actually sloped, but it did the job well enough by making creative use of the tools I had within the constraints I was given.  You might call it a _hack_.

Self-identified hackers will often lament how "hack" now has two meanings and everyone assumes the wrong one.  I think there's really only one meaning, and the "break into computers" sense is a special case.  It's not like breaking into a system is magic, or done by running `hack.exe`; it's just a creative use of the tools you have within the constraints you're given.  Like when the constraint is "your username is placed in a string of SQL" and you decide to place a couple quotation marks in your username.

So I'm always a little surprised when programmers don't _get_ security issues or how to defend against them, because to me, it requires exactly the same mindset as programming.  And I suspect the problem is a quiet assumption most people tend to make: _no one is that much of an asshole_.

That's not entirely unreasonable.  Every stranger you pass on the street _could_ be a hired assassin, but that's fairly unlikely, and we have punishments to discourage that sort of thing.  Ultimately we have to have some level of trust in other people in order to be around them at all.

And yet.

<!-- more -->

I (think I) first had this thought about Patreon, the platform that lets people give creators a few bucks a month in exchange for some kind of reward.  A lot of artists have been using it as an ad hoc paywall, where the "reward" is actually access to a bunch of artwork.  Trouble is, anyone can _declare_ support for a creator and get immediate access to the rewards, but Patreon only charges anyone at the end of the month.

I can't believe that no one saw this loophole.  It even happened a couple times to friends of mine, who would notice a new pledge for their highest tier that quietly vanished after two days.  But it was a rarity, and the setup was fairly accessible to everyone, and ultimately I assume someone over there said or thought the magic words: _no one is that much of an asshole_.

Then along came someone who _was_ that much of an asshole and wrote a Patreon scraper.  It pledged to the highest tier, grabbed all the exclusive rewards, and stuck them up on a freely-browsable website.  Daily.  For each of several _hundred_ artists.

Whoops!  Leaks are a thing, of course, but that's a little embarrassing.

"No one is that much of an asshole" may work in physical spaces (well, _somewhat_), but it completely breaks down with networked computers, which are exposed to _everyone everywhere_.  If you assume that 99.999% of people are generally good, well, that still leaves 70,000 human beings somewhere on the planet who would be all too happy to cast ruination upon your humble program.

And every single one of them can get access to it, via the power of the Internet.

And it only takes **one**.

Here's a more technical example, a story that a friend just told me but that I've heard many times before:

```irc
16:25 <_habnabit> the other day someone brought a bot in a channel that had a "hex decode" command that would translate from hex-encoded ASCII to ASCII
16:25 <eevee> oh no
16:25 <eevee> i already see where this is going
16:26 <_habnabit> i had it decode a message that contained CRLFQUIT :lol and, guess what,
16:26 <_habnabit> it rejoined (because it was a mirc script) and then i had it unban me from a channel
```

I think there are three interconnected and fundamental mistakes here.


## 1. Didn't consider failure cases

I'm sure the intention here was something along the lines of "gee whiz it would be cool if we could quickly decode messages encoded in ASCII", which sounds harmless enough.  There's a desired goal; someone wrote some code; they tried it, and it accomplished the goal.

The problem is that they only thought about whether the desired cases worked, and not about whether _undesired_ cases _didn't_ work.  In doing so, they allowed much more than they intended.  This is something we tend to overlook in any form of testing, and [not just in programming](http://www.nytimes.com/interactive/2015/07/03/upshot/a-quick-puzzle-to-test-your-problem-solving.html) — humans have a [tendency](https://en.wikipedia.org/wiki/Confirmation_bias) to test their ideas by trying to prove them _right_, not by trying to prove them _wrong_.

When I saw "ASCII", I immediately thought: _all_ of ASCII?  That includes control characters.  What havok could you wreak with a nul?  Probably not too much, just truncate a line.  Ah, but ASCII also includes newlines, and IRC is delimited by newlines...

Here is a constraint.  What creative things can you do with it?  Or, rather, what can you do that's unexpected?

We don't test for failure cases because we assume the state of the world will always be "normal", that everyone's use case is the same as ours, and that no one is out to get us.


## 2. Didn't tread carefully with a serialized format

As it turns out, this is one of the most common kinds of security flaw: dumping arbitrary user data into the string form of a structured format.  The raw IRC message would look something like this:

    PRIVMSG #channel :{response}\r\n

We might treat this like a string because it's convenient, but this is actually a serialized data structure (albeit a terrible one) for storing a sequence of strings.  You can look at this and immediately tell that spaces and newlines need to be handled with care, because they're part of the format itself.  IRC actually has no escaping mechanism (except that prefixing with a colon treats the entire rest of the line as a single argument), so there simply is no way to send a newline as part of a command.  If you just slop IRC messages together with string concatenation, you risk injecting a bogus argument and creating a malformed message...  which may do anything.

In this case, since this was a script inside an existing client and presumably used the client's own commands to send the response, I have to lay the blame on the client itself; it should definitely balk when asked to send a completely bogus message like this.

This is the same kind of problem as SQL injection, but a more apt comparison is HTTP header splitting.  Naïve CGI scripts back in the day would produce their response headers as plain text, and if those headers included any user input, a client could send data that included a newline followed by any headers of their choosing.  This isn't much of a problem now that headers tend to be set in a structured way and serialized carefully by plumbing.


## 3. Untrusted data didn't set off alarm bells

When you write a program (especially a server of some sort), you are effectively opening your hand and asking any passerby to put whatever they want in it.  Yeah, most people might give you a business card or a nickel, but one day some jackass is going to give you a hot coal.

And you should treat anything you receive as though it might be that hot coal.  What are you assuming that might not be true?  Could it contain nuls when you expected a C string?  Could it be empty when you expected a value?  Could it be megabytes when you expected a single word?

It's not just strings, either.  For the Patreon scraper, "user input" was actually a sequence of actions.  Sign up, pledge, mass download, unpledge.

Wear gloves.  Anything you don't control should be insulated.  Anything you _do_ control should be insulated too, so you get in the habit and don't have to remember whether it was okay to be sloppy in this case.


## If I have any real advice

Think of a programmer or company you just _hate_.  Put their photo on a dartboard with a few darts through it, if you must.

Then whenever you're writing a program, stop to consider — if this program was written by that dickwad, what sneaky things could you do to ruin their day?  Play with the Lego.  See what you can do that you didn't expect.  Ask some fresh eyeballs to take a look if you have to.

Because for all you know, your face is on someone _else's_ dartboard, and they're dying to see what you're building.
