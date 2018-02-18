title: Tech wishes for 2018
date: 2018-02-18 13:03
category: blog
tags: tech, patreon

Anonymous asks, via money:

> What would you like to see happen in tech in 2018?
> 
> (answer can be technical, social, political, combination, whatever)

Hmm.

<!-- more -->

## Less of this

I'm not really qualified to speak in depth about either of these things, but let me put my foot in my mouth anyway:

### The Blockchain™

Bitcoin was a neat idea.  No, really!  Decentralization is cool.  Overhauling our terrible financial infrastructure is cool.  Hash functions are cool.

Unfortunately, it seems to have devolved into mostly a get-rich-quick scheme for nerds, and by nearly any measure it's turning into a spectacular catastrophe.  Its "success" is measured in how much a bitcoin is worth _in US dollars_, which is pretty close to an admission from its own investors that its only value is in converting back to "real" money — all while that same "success" is making it _less_ useful as a distinct currency.

Blah, blah, everyone already knows this.

What concerns me slightly more is the gold rush hype cycle, which is putting cryptocurrency and "blockchain" in the news and lending it all legitimacy.  People have raked in _millions of dollars_ on ICOs of novel coins I've never heard mentioned again.  (Note: again, that value is measured _in dollars_.)  Most likely, none of the investors will see any return whatsoever on that money.  They _can't_, really, unless a coin actually takes off _as a currency_, and that seems at odds with speculative investing since everyone either wants to hoard or ditch their coins.  When the coins have no value themselves, the money can only come from other investors, and eventually the hype winds down and you run out of other investors.

I fear this will hurt a _lot_ of people before it's over, so I'd like for it to be over as soon as possible.

----

That said, the hype itself has gotten way out of hand too.  First it was the obsession with "blockchain" like it's a revolutionary technology, but hey, _Git_ is a fucking blockchain.  The novel part is the way it handles distributed _consensus_ (which in Git is basically left for you to figure out), and that's uniquely important to currency because you want to be pretty sure that money doesn't get duplicated or lost when moved around.

But now we have startups trying to use blockchains for website backends and file storage and who knows what else?  Why?  What advantage does this have?  When you say "blockchain", I hear "single Git repository" — so when you say "email on the blockchain", I have an aneurysm.

Bitcoin seems to have sparked imagination in large part because it's decentralized, but I'd argue it's actually a pretty _bad_ example of a decentralized network, since _people keep forking it_.  The ability to fork is a feature, sure, but the trouble here is that the Bitcoin family has no notion of _federation_ — there is _one_ canonical Bitcoin ledger and it has no notion of communication with any other.  That's what you want for currency, not necessarily other applications.  (Bitcoin also _incentivizes_ [frivolous forking](https://gizmodo.com/atari-is-launching-a-cryptocurrency-because-thats-just-1823042620) by giving the creator an initial pile of coins to keep and sell.)

And federation is much more interesting than decentralization!  Federation gives us email and the web.  Federation means I can set up my own instance with my own rules and _still_ be able to meaningfully communicate with the rest of the network.  Federation has some amount of tolerance for changes to the protocol, so such changes are more flexible and rely more heavily on consensus.

Federation is fantastic, and it feels like a massive tragedy that this rekindled interest in decentralization is mostly focused on peer-to-peer networks, which do little to address our current problems with centralized platforms.

And hey, you know what else is federated?  ***Banks***.


### AI

Again, the tech is cool and all, but the marketing hype is getting way out of hand.

Maybe what I really want from 2018 is less marketing?

For one, I've seen a _huge_ uptick in uncritically referring to any software that creates or classifies creative work as "AI".  Can we…  can we not.  It's not AI.  Yes, yes, nerds, I don't care about the hair-splitting about the nature of intelligence — you _know_ that when we hear "AI" we think of a human-like self-aware intelligence.  But we're applying it to stuff like a weird dog generator.  Or to whatever neural network a website threw into production this week.

And this is _dangerously_ misleading — we already had massive tech companies scapegoating The Algorithm™ for the poor behavior of their software, and now we're talking about those algorithms as though they were self-aware, untouchable, untameable, unknowable entities of pure chaos whose decisions we are arbitrarily bound to.  Ancient, powerful gods who exist just outside human comprehension or law.

It's weird to see this stuff appear in consumer products so quickly, too.  It feels quick, anyway.  The latest iPhone can unlock via facial recognition, right?  I'm sure a lot of effort was put into ensuring that the same person's face would always be recognized…  but how confident are we that _other_ faces _won't_ be recognized?  I admit I don't follow all this super closely, so I may be imagining a non-problem, but I _do_ know that humans are remarkably bad at checking for negative cases.

Hell, take the recurring problem of major platforms like Twitter and YouTube classifying anything mentioning "bisexual" as pornographic — because the word is also used as a porn genre, and someone threw a list of porn terms into a filter without thinking too hard about it.  That's just a _word list_, a fairly simple thing that any human can review; but suddenly we're confident in opaque networks of inferred details?

I don't know.  "Traditional" classification and generation are much more comforting, since they're a set of fairly abstract rules that can be examined and followed.  Machine learning, as I understand it, is less about rules and much more about pattern-matching; it's _built out of_ the fingerprints of the stuff it's trained on.  Surely that's just begging for tons of edge cases.  They're practically _made of_ edge cases.

----

I'm reminded of a point I saw made a few days ago on Twitter, something I'd never thought about but should have.  TurnItIn is a service for universities that checks whether students' papers match any others, in order to detect cheating.  But this is a _paid_ service, one that _fundamentally hinges_ on its corpus: a large collection of existing student papers.  So students pay money to attend school, where they're _required_ to let their work be given to a third-party company, which then profits off of it?  What kind of a goofy business model is this?

And my thoughts turn to machine learning, which is fundamentally different from an algorithm you can simply copy from a paper, because it's all about the training data.  And to get good results, you need a _lot_ of training data.  Where is that all coming from?  How many for-profit companies are setting a neural network loose on the web — on millions of people's work — and then turning around and selling the result as a product?

This is really a question of how intellectual property works in the internet era, and it continues our proud decades-long tradition of just kinda doing whatever we want without thinking about it too much.  Nothing if not consistent.


## More of this

A bit tougher, since computers are pretty alright now and everything continues to chug along.  Maybe we should just quit while we're ahead.  There's some real pie-in-the-sky stuff that would be nice, but it certainly won't happen within a year, and may never happen except in some horrific Algorithmic™ form designed by people that don't know anything about the problem space and only works 60% of the time but is treated as though it were bulletproof.

### Federation

The giants are getting more giant.  Maybe too giant?  Granted, it could be much worse than Google and Amazon — it could be Apple!

Amazon has its own delivery service and brick-and-mortar stores now, as well as providing the plumbing for vast amounts of the web.  They're not doing anything particularly outrageous, but they kind of _loom_.

Ad company Google just put ad blocking in its majority-share browser — albeit for the ambiguously-noble goal of only blocking _obnoxious_ ads so that people will be less inclined to install a _blanket_ ad blocker.

Twitter is kind of a nightmare but no one wants to leave.  I keep trying to [use Mastodon](https://mastodon.social/@eevee) as well, but I always forget about it after a day, whoops.

Facebook sounds like a _total_ nightmare but no one wants to leave that either, because normies don't use anything else, which is itself direly concerning.

IRC is rapidly bleeding mindshare to Slack and Discord, both of which are far better at the things IRC sadly never tried to do and absolutely terrible at the exact things IRC excels at.

The problem is the same as ever: there's no incentive to interoperate.  There's no fundamental technical reason why Twitter and Tumblr and MySpace and Facebook can't intermingle their posts; they just don't, because why would they bother?  It's extra work that makes it easier for people to _not_ use your ecosystem.

I don't know what can be done about that, except that hope for a really big player to decide to play nice out of the kindness of their heart.  The really big federated success stories — say, the web — mostly won out because they came along _first_.  At this point, how does a federated social network take over?  I don't know.


### Social progress

I… don't really have a solid grasp on what's happening in tech socially at the moment.  I've drifted a bit away from the _industry_ part, which is where that all tends to come up.  I have the vague sense that things are improving, but that might just be because the Rust community is the one I hear the most about, and it puts a lot of effort into being inclusive and welcoming.

So… more projects should be like Rust?  Do whatever Rust is doing?  And not so much what Linus is doing.


### Open source funding

I haven't heard this brought up much lately, but it would still be nice to see.  The Bay Area _runs_ on open source and is raking in zillions of dollars on its back; pump some of that cash back into the ecosystem, somehow.

I've seen a couple open source projects on Patreon, which is fantastic, but feels like a very _small_ solution given how much money is flowing through the commercial tech industry.


### Ad blocking

Nice.  Fuck ads.

One might wonder where the money to host a website comes from, then?  I don't know.  Maybe we should loop this in with the above thing and find a more informal way to pay people for the stuff they make when we find it useful, without the financial and cognitive overhead of A Transaction or Giving Someone My Damn Credit Card Number.  You know, something like Bitco—  ah, fuck.


### Year of the Linux Desktop

I don't know.  What are we working on at the moment?  Wayland?  Do Wayland, I guess.  Oh, and hi-DPI, which I hear sucks.  And please fix my sound drivers so PulseAudio stops blaming them when it fucks up.
