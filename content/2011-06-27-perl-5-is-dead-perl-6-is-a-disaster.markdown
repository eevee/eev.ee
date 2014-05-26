title: Perl 5 is dead, Perl 6 is a disaster
date: 2011-06-27 03:10:00
modified: 2011-07-03 18:30:00
tags: perl
category: essay


_(This article has been translated into [Bulgarian](http://www.fatcow.com/edu/perl-disaster-bl/) and [Polish](http://www.autoteiledirekt.de/science/perl-5-jest-martwy-perl-6-jest-katastrofa)—thanks!)_

---

**ADDENDUM Jul 3**: I don't know how, but this got a bit of attention.  chromatic has compared me to Barbie, szabgab wondered if I'm a troll, and several people suggested that I'm trying to justify leaving Perl for Python.

Remember, I'm a long-time Perl developer.  I'm the ideal target audience: someone who already uses your product.  In recent years I've become disillusioned with Perl, having watched several similar languages eclipse it.  I'm surely not unique in feeling this way.

So why is the reaction to downplay what I said, rather than to tell me why I _should_ want to use Perl, or to make Perl something I'd want to use again?  chromatic suggests I just haven't done my research.  But if I don't know why I should use your product, that's _your_ problem.

I did have an interesting discussion in #perl6 about this, which led to an insight.  Perl 6 is unusual, possibly even unique, in having a large spec written before an implementation.  I think some of its communication issues stem from this: outsiders see a spec and take it to mean an implementation isn't "1.0" until it reasonably matches the spec.  Implementors, on the other hand, regard the spec as merely a direction to move in.  So outsiders are waiting for a blessed 1.0 release, and think the insiders sound slow and stuffy for not giving them one.  Insiders are working on an organic thing, and think outsiders are obnoxious and impatient for wanting something absurd.

Explaining the discrepancy to people who want to use Perl 6 is technically correct, but not practically helpful.  It may be better to carve up the Perl 6 spec into discrete and useful milestones, with some [big ol' colored chart][web devout standards support] detailing what's supported by which implementations.  (I actually can't tell right now what Rakudo supports and doesn't.  rakudo.org is just a blog.)

---

I feel the need to respond to [this][article 1] [series][article 2] of [blog][article 3] [posts][article 4] [about][article 5] [Perl 6][article 6], whether it should be renamed, and what the implications are for Perl 5.

I'm a Perl guy.  I've been using Perl since I was _eleven_.  I got paid to write Perl for the past four-and-a-bit years.  Let's pretend I'm qualified to say anything here.

A confession: I wince when I call myself a "Perl guy".  I think it makes me sound crusty and obsolete.  Because Perl 5 is crusty and obsolete.

Who is using Perl for new software?  Besides a couple grumpy nerds I know personally, I haven't the slightest clue—and I sort of pay attention to Perl.  I have zero interest in Java or .NET, but I'm still dimly aware that things are _built_ with them.  I can't tell you what Perl is actually being used for besides all the cool new modules on CPAN designed to make Perl suck less.

What has happened with Perl since 5.8?  5.10 brought us the smart-match operator, the defined-or operator, and given/when.  5.12 brought us...  well, nothing.  5.14 allows `push $arrayref`.  And that's all!  There are a lot of bullet points in the [changelogs][perldelta], yes, but almost all of them are arcane things like "the ... operator" or "$, flexibility".  These are improvements, technically, but they're not anything that's going to make me jump for Perl 5 for my next project; they're just going to make existing Perl 5 work hurt less.  (And even that isn't automatically true; my previous job is at least a year into an effort to move from Perl 5.8 to Perl 5.10.  Note that Perl 5.10 is now so old it's unsupported.)

The ecosystem is moving, sure, but if you buy into that then you're still stuck with the language.  Worse, if you use any other Perl software, you probably have to work with an object system you don't use, an exception model you don't use, some kind of bundling thing you don't use, and on it goes.

I don't see anyone talk about Perl except people who are _really into Perl_ already.  It doesn't attract new blood; I certainly wouldn't point anyone towards it.  If it were a human language, we'd certainly call it dead, or at least moribund.

<!-- more -->

Perl 6, on the other hand, never got off the ground.  It's the worst kind of engineering disaster: a group of very smart people who want to build something perfect, and in the process have forgotten to build anything at all.

We have Rakudo star, and we have several other implementations, and there's active development.  All true.  Also, all true _more than a decade_ later.

Here is something I saw in #perl6 just yesterday.  'nom' is a big rewrite of Rakudo that's currently in progress.

    > for 1..20000 { $i = $i + $_ }
    > rakudo master:  2.74 sec
    > rakudo nom: 1.69 sec

Hmm.  Let's try this in Perl 5 on my machine:

    $ time perl -e 'for (1..20000) { $i = $i + $_ }'
    0.00s user 0.00s system 0% cpu 0.152 total

More than a decade of work, and the prime Perl 6 implementation is still **orders of magnitude** slower than the current family of dynamic languages, even for a simple addition loop.

Most of the conversation is still about details of the _spec_: the intricate ways that all of Perl 6's promised features might interact.  It's been this long and we don't even know how the "first" crack at the language is supposed to work.

I was excited about Perl 6.  I was excited for **years**.  It was everything I wanted in a language, because it was literally _everything_.  But its designers and implementors are off lost in the clouds somewhere, too busy trying to make every problem in Project Euler solvable in ten characters, and forgetting to actually give me a language and runtime I can use for something besides cute solutions to [math problems][].

Perl 5 and Perl 6 have both stagnated.  Neither of them is moving in a useful direction; both projects are drowning in the idealistic and increasingly abstract dreams of their existing communities.  They're not doing anything to attract newcomers, and they will continue to spiral into irrelevance, oblivious to the trap they've built themselves.

But yes, by all means, argue about the names.

We had a good run, Perl.  I'll miss you.

[article 1]: http://blogs.perl.org/users/mithaldu/2011/06/why-are-people-asking-for-a-perl-name-change-again.html
[article 2]: http://blogs.perl.org/users/alberto_simoes/2011/06/perl-perl-5-perl-6-and-names.html
[article 3]: http://www.modernperlbooks.com/mt/2011/06/perl-perl-5-perl-6-and-names.html
[article 4]: http://blogs.perl.org/users/aristotle/2011/06/bead-ivory-off-white.html
[article 5]: http://www.modernperlbooks.com/mt/2011/06/iridescent-bivalve-secretions-are-from-new-jersey-nacre-is-from-mit.html
[article 6]: http://www.dagolden.com/index.php/1492/counterfactual-perl/
[math problems]: http://justrakudoit.wordpress.com/2011/06/23/euler-5/
[perldelta]: http://perldoc.perl.org/perldelta.html

[web devout standards support]: http://www.webdevout.net/browser-support
