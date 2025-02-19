title: The NSA is trying to create a virtual clone of me
date: 2016-03-03 18:47
modified: 2016-03-19 19:11
category: articles
tags: tech

**update 2016-03-19:** I believe the account described below _is_ run by a real human being, but for the sake of their privacy I'm not going to tell you why.  I'm leaving this post up, though, because it's an interesting story and also this was a hecka creepy thing to do.

----

[@softfennec](https://twitter.com/softfennec) and [@orezpraw](https://twitter.com/orezpraw) brought to my attention the following tweet, which I have to reconstruct from memory for reasons that will be clear in a moment:

> I like to think I'm okay at math, but then I stumble into Math SE and it's Latin to me. [http://math.stackexchange.com/q/1665383/58532](http://math.stackexchange.com/q/1665383/58532)

What a hilarious joke!  I liked it so much that it turns out I'd already made it myself:

> i like to think i'm ok at math but then i stumble into math.SE and it is basically lorem ipsum to me [http://math.stackexchange.com/q/1665383/58532](http://math.stackexchange.com/q/1665383/58532)
>
> — [@eevee](https://twitter.com/eevee/status/701478886375350275), Feb 21 at 10:49am

<!-- more -->

It seems there's a Twitter account that has been copying my tweets, along with the tweets of half a dozen other tech people who follow me.  I don't mean stealing our jokes; I mean _only_ tweeting paraphrases of our tweets, even fairly mundane ones.  It's a shame that I can't show you the account in full, because after an hour of our trying to figure out what was going on, I finally made a public tweet about this — and the account instantly vanished.  A couple people verified by user id that the account was actually deleted, not just renamed.

archive.org has two snapshots, both from 2013, but [this one](https://web.archive.org/web/20131217160207/https://twitter.com/tilapya_) is fairly telling — it reads as perfectly normal, _but the bio is mine!_  There's also a [recent copy](https://archive.is/bxnPe) on archive.is, from Feb 28, where you can see a rewording of a tweet I made about a page down:

> i have acquired ingredients for the cheesecake i'm contractually obligated to make. i didn't know how much chocolate i'd need so i got: lots
>
> — [@eevee](https://twitter.com/eevee/status/702656586519425024), Feb 24 at 4:49pm

<!-- -->
> I have acquired ingredients for the cheesecake I’m contractually obligated to make. I didn’t know how much stuff I’d need so I got: LOTS
>
> — [@tilapya\_](https://twitter.com/tilapya_/status/703051652694040576), Feb 25 at 6:59pm (timezone unclear)

So please believe me when I stress, very very strongly, just how bizarre this is.  I'm plenty familiar with bot accounts on Twitter that try to look normal so they can be sold as fake followers.  I hate them with such a burning passion that I obsessively check on everyone who follows me so I can block/report any junk.  I've seen quite a few of them by now.

And they are always, _always_ obvious to a human being.  At worst, they're slightly _less_ obvious.  There's no reason for them to try to look real to a person, anyway, because they only need to be good enough to fool automated spam tools.  Twitter can't reasonably hand-check all of its millions of accounts.

They'll tweet obvious spam links.  They'll copy a tweet that was the middle of a thought and makes no sense on its own.  They'll Markov a little too heavily, and cut a sentence off halfway.  They'll screw up copying some non-ASCII.  They'll contradict themselves by copying text from two very different people.  Sometimes they're less obvious, but they're always obvious.

Whatever this was, it was completely different.  Because it pulled from a small circle of people, it tweeted about the same general topics.  It made repeated references to being female, to wearing contacts, to having a strong interest in milk — without ever contradicting itself.  It made followup tweets that continued a thought.  It never tweeted junk links.  It kept a consistent writing style.  It occasionally retweeted jokes that I could believe the persona found funny.

It looked like the account of an average nerd named "Nikki V."  Except that it had 1600 followers, yet never garnered a single like or retweet.  And seemingly everything it wrote was a paraphrase of someone else.

The kicker here is that it was so good, _I cannot believe it was automatic_.  You might think the above tweet was generated by some rules that fix capitalization and a little [text spinning](https://en.wikipedia.org/wiki/Article_spinning), right?  Well, I already contest that a bot is unlikely to realize "math.SE" can be reasonably written as "Math SE" instead of interpreting it as a link.  But also, consider this pair:

> i wear nothing but a shirt and sit around all day wrapped in a blanket. i'm basically a sphynx
>
> — [@eevee](https://twitter.com/eevee/status/688476540162605056), Jan 16 at 1:42pm

<!-- -->
> I wear nothing but a shirt and sit around all day wrapped in a blanket. I’m basically a puppy?
>
> — [@tilapya\_](https://twitter.com/tilapya_/status/688525157569150978), Jan 16 at 4:56pm

What kind of word list would even think to include "sphynx" and "puppy" as potentially interchangeable?  How would software know that a question mark can go on the end of that non-question?

(This blog software turns everything into curly quotes automatically, but it's worth noting that my original tweet had a plain quote, whereas this account _always_ uses curly quotes.)

Or how about these, which were both accompanied by the same screenshot of some obtuse legalese:

> this tax prep software just makes everything so easy
>
> — [@eevee](https://twitter.com/eevee/status/703658964341272576), Feb 27 at 11:12am

<!-- -->
> This tax preparation software is one reason why I want to be @avdangeles’ friend forever.
>
> — [@tilapya\_](https://twitter.com/tilapya_/status/703793015148576770), Feb 27 at 8:05pm

I don't know who @avdangeles is, but their Twitter bio indicates they're a tax lawyer.  And also one of the only two [archive.org snapshots of this account](https://web.archive.org/web/20130617165127/https://twitter.com/tilapya_) shows them tweeting at that same person in 2013!

The joke — the _sarcastic_ joke — was completely rewritten with a nod to a sensibly-chosen third party who the account appears to know.

Or take these:

> psa: please stop generating PDFs whose titles are the path to a temporary file on your server
>
> — [@eevee](https://twitter.com/eevee/status/703692217957744640), Feb 27 at 1:24pm

<!-- -->
> Federal websites should really stop generating PDFs whose titles are the path to a temporary file on their servers.
>
> — [@tilapya\_](https://twitter.com/tilapya_/status/704012009440849920), Feb 28 at 10:35am

How could an automated system possibly add the reasonable context of "Federal websites", which are known for this sort of clumsy tech oversight?  I was even talking about doing income taxes at the time, so that's not unreasonable to infer, though I was actually talking about several bank websites.

These are the only tweets I still had open in tabs when the account was deleted, but you get the idea.  I also saw several of my tweets get copied, unmodified, except that they also had an appropriate smiley added.  And these are just my own tweets that I recognized; I hadn't gotten around to comparing the others' tweets yet.

The account was _six years old_ and looked to have copied from other sources before.  I saw one case where it copied someone else's reply to a Demetri Marin tweet, but exapnded upon it:

> @DemetriMartin is there an "and" missing? third line?
>
> — [@Bob\_Lawblaw](https://twitter.com/Bob_Lawblaw/status/456512459910557697), Apr 16, 2014 at 12:20pm

<!-- -->
> @DemetriMartin Third line seems to be missing an “and”, but I love your work! I love palindromes!
>
> — [@tilapya\_](https://twitter.com/tilapya_/status/456604713207615488), Apr 16, 2014 at 6:27pm

This is extraordinarily bizarre and I am at a loss to explain it.  I can only think of two ways this could've happened:

1. An actual human being, who has enough general tech knowledge to ensure nerdy tweets still make sense, is spending an awful lot of time manually copying tweets from a small circle of tech friends.  And has been doing so for years.  And doesn't seem to be gaining anything from it.

    Granted, this _could_ just be a fake follower account, but why would someone put so much apparent _manual_ effort into it?  Those fake follower places sell _a thousand_ junk followers for ten bucks; it can't possibly be worth trying so hard just to make one of them vaguely resemble an actual person.  They even hid themselves once they were discovered; what kind of bot herder bothers to do that?

2. Alternatively, the NSA has a secret program to build an AI to simulate the perfect nerd, and it's already so good that it independently thinks of the same tweets I do, right around the same time.  Soon it will replace me, and no one will know the difference.

That's all I've got.  Any other ideas?
