title: Perls of Wisdom
date: 2011-07-22 16:17:00
modified: 2011-07-23 12:52:00
category: blog
tags: perl, tech

Ha, ha!  A hilarious and original pun.

I've had several conversations now about Perl 5's level of deadness and Perl 6's level of disastrousness.  So here is a followup, which surely won't get as much attention because it's not as potentially inflammatory.

<!-- more -->

## To recap

What does "dead" mean?  I have no idea.  And neither does anyone else.  Everyone agrees that it's a bad thing for their pet language to be called, but I can't really find a definition that applies to, say, COBOL but not Ruby.  The best we have is, er, "like COBOL".

Let's be more precise then: I feel Perl has a dire problem on its hands, and as a developer raised by Perl, this saddens me.

(An aside: one acquaintance told me he doesn't think I even like Perl, having seen me complain about it a bit too frequently.  I had to think about this.  I suppose I like Perl, but I don't _enjoy_ it, which is precisely what frustrates me here.  I want to like Perl, but I don't know that Perl wants me to like it.)

## The Problem

The Problem isn't even so much the language itself.  I fear a dark cloud of insulation hangs over the Perl community.  I submit the following.

* Recall that Perl 5.8 went five and a half years before another major revision.  That's nearly a quarter of Perl's entire lifetime, and it happened _while_ PHP and Ruby and Python were eroding Perl's Web development niche.  The new release cycle is a breath of fresh air, but there have still been few major improvements.

* I just worked for a Perl shop for four years.  I have friends involved with Perl.  I lurk in #perl.  Somehow, I'm still missing out on interesting Perl developments that others imply are happening.  I could definitely better educate myself, but the bigger issue is: if someone with a foot in Perl is oblivious to these things, what chance do those outside the community have?

* Consider the use of `open` with bareword filehandles.  Unlike some other warts (blockless `map` and `grep`, _ugh_), I'm hard-pressed to find a Perl developer who'll defend bareword filehandles.  The #perl bot's "usual stuff" quote includes "use lexical filehandles" as its third bullet point, immediately after `strict` and `warnings`.  It's universally agreed that this is a misfeature and should be avoided.

    Yet even a proposal to remove them from a small part of the Perl documentation is [contentious][barewords in open]!  brian d foy (who I believe is the documentation maintainer in some capacity?) argues that bareword filehandles should remain in the _tutorial_ on `open` because, ultimately, new users will find them simpler and existing users need to know about them.

* There's a worrying trend in how both the Perl 5 and 6 communities respond to criticisms of the process or language.  Detractors will gripe about the lack of some feature or the lack of a blessed Perl 6 interpreter.  Perl 5 will respond with links to CPAN; Perl 6 will explain that the idea of a "finished" language is absurd.  Such responses are perfectly rational and correct.

    _However_, they don't address what the detractor actually wants: first-class support in core, or a guarantee of reasonable Perl 6 spec compatibility.  The Perl community treats these gripes as engineering problems to be worked around, but they're actually a sticky emotional thing: how people _feel_ about Perl.

    The misunderstanding hints at a deep disconnect within the Perl community.  Are you announcing to the world why they _should_ use Perl, or merely that they _could_ use Perl?  The latter is a programming issue, easily resolved with more CPAN modules.  The former is a human issue, dealing with people and their expectations.

From where I'm standing, it _looks like_ the Perl community has taken Perl's usability and success somewhat for granted due to their own close involvement, and thus forgotten to address the needs of those outside the community.  Do the core Perl maintainers care that most other languages have, say, a nice object system built in?  When the response is generally just "use Moose", it sounds as if nobody close to Perl thinks there's even a problem.

Or perhaps that's just the impression I get.  I freely admit I'm pulling this out of my ass based on personal anecdotes and a foggy memory of blog posts read over the course of years; I could be wildly off-base.  But what is the ultimate goal here?  To make Perl better for the people using Perl, or to make Perl better for everyone?

## Fixing Perl 5

Advertising Perl like with Iron Man is helpful, but only so much.  When people aren't using Perl because of some legitimate beef with it, you can't counter with a workaround.  Admit that Perl does have shortcomings, sympathize with the problem, explain what could be done or is being done to fix it.  I'd rather know someone considers a product flawed and still uses it than know he uses a product and is oblivious to its obvious flaws.

I don't know.  People are hard.  Find someone else to figure that out.  Let's do the language.

### Get rid of all this crap

The Perl community has a long list of things you Should Not Do in Perl, and even a decent list of CPAN modules you Should Not Use.  Unfortunately, the interpreter (and often the documentation) are oblivious to these hard-earned lessons, leaving every novice free to commit atrocious sins anew.  The well-known problem of ancient Perl tutorials floating to the top of Google rankings makes this an even more urgent problem.

A few things have been deprecated or removed recently, which is great, but they tend to be insane and ancient features that few people have even heard of like pseudo-hashes or `$[`.  That's a start, but `$[` is not exactly on the top ten list of beginner pitfalls.  If Perl wants to be used for new software, it should help me to make that _good_ software.

So let's ditch all this garbage.  Disable it under `strict`, bitch about it under `warnings`, add a third pragma everyone has to remember; whatever accomodations you have to make for backwards compatibility, make them.

* `-w`, if it's still there.  I think the docs spend more time advising against it than explaining it.
* `chop()`.  I can't recall ever seeing this used deliberately.
* `dump()`, unless it's still useful?  I don't think it works with most platforms' default ulimits, and its stated use case is...  arcane.
* The built-in socket functions.  `IO::Socket` is a core module.
* Indirect object syntax.  I thought this had already been removed, but I don't see it in the perldeltas.  It makes the grammar much more ambiguous and masks common errors like missing a comma or semicolon.
* Global filehandles, besides the built-ins.
* `<*.foo>` syntax.  Doesn't do anything that `glob()` can't do, and is a strange and confusing overloading of an already unusual operator.
* `$|` and friends.  Probably only deserving of a warning that you should be using `IO::Handle`.
* Two-arg `open()`.  At least ditch _one_-arg `open()`.
* One-arg `system()`.  Okay, you can't really remove that—but it would be nice to spit out a warning by default if `system()` is called with one arg containing shell characters.
* C-style `for` loops.  No, really.  I think I saw one used in the guts of Moose once, or maybe DBIC, but nowhere else.  They're just a potential pitfall for C converts.  Simple ones are clearer as iterating blocks with a range; complex ones ought to be a more explicit `while`.

I'm sure some of these are contentious, and I'm missing some very good reasons why they ought to be supported.  (Note that TMTOWTDI is not a compelling reason for something to exist!  If there are two ways to do something and one of them sucks, don't keep it around just to proclaim how flexible your language is.)  I'm not particularly attached to this list; it's off the top of my head.  More important is that Perl's maintainers be _willing_ to drop or at least heavily warn about the features that make for bad code and ultimately hurt Perl's reputation.

Modules are more complicated.  Both `base` and `parent`, for example, are core modules.  Which should I use?  `base` warns me not to use it, but if I just run across it in someone else's code, I wouldn't know that.  Should `base` warn about its use if the caller is under `use feature :5.16`?  Are there a significant number of similarly discouraged modules?

If I may be so bold, it would be fantastic for the Perl interpreter to warn that the initial file it runs isn't using `strict` or `warnings`.  Can we do that?  That would be great.  It shouldn't be easy to remain oblivious to such critically useful tools.

### Better indicate gotchas

`warnings` is a funny beast.  Here are some things it complains about, but allows:

* Recursing more than 100 times.
* Reading from or writing to a closed file, or writing to a read-only file, etc.
* Escaping from a loop, function, `eval`, or other construct with e.g. `goto`.
* Overflowing `gmtime`.

Here are some things that Perl always complains about, but allows:

* Using `elseif`.
* Supplying a value where the lexer expects an operator.

Here are some things that are always silently allowed:

* A wide variety of failing i/o operations.

The priorities are a little backwards here.  Perl allows or merely warns about some things that are extremely unlikely to make any sense.  I'd much prefer Perl to stop me when I'm clearly doing something stupid, instead of trying very hard to continue operating in a useless state.  `autodie` will intercept the i/o problems, and there are ways to make certain warnings fatal, if you want to add even more complex boilerplate to the top of _every file_.

Or maybe...  we can go furtherer.

### use Modern::Perl

We have a lot of pragmas that try to fix things about Perl, and meta-pragmas (like `Modern::Perl` and `common::sense`) that turn on various other pragmas.  Good grief.

We also have `use feature` now.  So how about this: add a bunch more features, so that `use feature :5.20` will:

* Enable `strict` and `warnings`.
* Make some of the more insane warnings fatal, like `malloc`.
* Enable `autodie`.
* Enable C3.
* Load `IO::Handle`.
* Enable `utf8`.

It could also disable a bunch of the junk listed above, like the special variables that `IO::Handle` replaces.  Then you'd be set with the best Perl has to offer you, with just one line, already built into the interpreter.

### Give me an object system

Perl has a remarkably inventive meta-object system; you can create any kind of object system you want.  While cool and interesting, it's not very practically useful, and the overwhelming majority of objects are just blessed hashrefs created with some helper module.  When a core feature of your language needs third-party help to be usable for simple tasks, it's time to rethink the feature.

The above is a funny way to describe Perl's OO support, but it segues nicely into my biggest gripe with said support: because Perl has only a factory for making object systems, and no single blessed object system, _little of the core language is object-oriented_.

Filehandles are still globs (or globrefs, or scalarrefs to globrefs or something).  You can make them kinda objecty by loading `IO::Handle`...  er, or `IO::File`, or maybe `FileHandle`.  Rather little code actually seems to do this, instead using the dozens of global i/o functions.

Data and structures are likewise not objects, so there are more global functions for working with those, often interspersed with code using other structures that have methods.  I could tie, but that still causes a noticable slowdown, and it actually solves the _opposite_ problem by making an object look more like a not-object.

1. Create an actual, blessed (zing!) object system, probably based on blessed hashrefs.  I see stevan has [proposed a MOP][mop]; he is clever, do what he says.  (This is the sort of thing that needs more advertising!  I had no idea of this until mithaldu waved it in my face after my previous post.)

2. `localtime`, `gmtime`, `caller`, various `get*` functions, and so forth should _absolutely not_ return lengthy lists; have them return simple objects.

3. Perhaps define a set of methods on built-in refs.  Probably just reuse the tie names, or something; filehandles already have an API in the form of `IO::Handle`.  Let me do `$hashref->keys`.  Blessed refs should ignore all this.  It might be too late for this to be useful.

### More data structures

Once you have an object system, you can build in a couple more basic data structures.  Yes, yes, I know, there's CPAN.  But it's nice to be able to whip up something as dead simple as a _set_ without having to consult CPAN and evaluate all my options and whatever.  The presence of a module in core doesn't prevent CPAN from doing better, either.

I'd kind of like to see:

* Sets!  Hashes with junk values work, yes, but they make you write some weird stuff like `map { $_ => 1 } @values`.  They also limit you to only strings.  Speaking of:

* Hashes with arbitrary keys.  There are workarounds for this.  They all suck.

* Iterators.  These already appear ad-hoc in a lot of CPAN modules as 0-arity closures and similar; it'd be nice to have this as a first-class thing.  Potentially this would allow for fixing the wacky state `each` attaches to a hash.

Careful readers may notice and complain that the above are all built into Python.  You are right!  This is a thing I like about Python!  _Steal it!_

### EXCEPTION HANDLING

I don't know how to put this delicately: Perl's exception handling is abysmal.  It starts off looking just quirky, but after you've made four attempts at getting `$SIG{__DIE__}` to wrap exceptions in objects that remember stack traces _but only once_ only to discover that Moose throws string exceptions that already contain the entire stack trace, and oh by the way Template Toolkit has its own exception class hierarchy that tries to re-wrap yours and then gets re-re-wrapped, you might also be ready to strangle something.

1. **Make them objects.**  The only reason exception handling gets mentioned after OO is so I can say this.  I don't care about the performance of exceptions; they're exceptional.  They need to be _useful_ before anything else.  They should capture stack traces automatically (perhaps as `caller` objects...).  For bonus points, they should be able to remember their pads so I can have a better idea of the state of my program when it exploded.  And I should be able to check for particular built-in or otherwise well-known kinds of errors without having to rely on _string matching_.  Make them stringify to the old format for some half-assed backwards compatibility.

    (An aside: to my knowledge, it's not actually possible to identify a built-in warning inside `$SIG{__WARN__}`; the last approach I saw involved parsing the headers in `perldiag` into a list of regexps.  It would be nice to, uh, improve this.)

2. `eval`'s default behavior is to quietly swallow an exception and stick it in a weird global, where I can go get it if I really want to.  This is very silly; doing `On Error Resume Next` out of the box is neither useful nor particularly safe.  The use of a global also causes a number of subtle problems, which modules like `Try::Tiny` exist partly just to work around.  Give me a new block that actually catches errors; combine it with `when` so I can smart-match them.

3. Lemme `return` from the enclosing _function_ within such a block.  I do this in Python kinda rarely, but enough that I realize I miss it in Perl.

4. I repeat: make `autodie` a default, or associate it with `strict`, or bolt it onto `use feature`, or anything.  Besides backwards compatibility, there's very little reason why I wouldn't want to know when opening a file failed miserably.

    "Hey, Perl, do this."  "OK, done, no problem."  "What?  Nothing happened."  "Oh yeah none of that actually worked, but I _tried_ successfully."

### A running theme

I shouldn't have to replace large chunks of the language to make it reasonably usable.  The modernest of Perl invokes `autobox` to apply magic to data, `IO::Handle` to wrap globrefs, `autodie` to wrap a lot of I/O builtins, `IO::Socket` instead of the built-in socket functions, Moose instead of explicit `bless`, `DateTime` and friends over the built-in time functions, and so on.  Perl has become a glue even for itself.

I suppose in a way that's an attractive idea: build your own programming language.  But I'm assuming that Perl wants to attract new blood, and when new blood sees a feature provided in the core language, it's unlikely to double-check that there's a better replacement module somewhere.  Sometimes new blood won't check even if a feature _isn't_ provided in the core language.

So if I may say anything at all it is merely: **be sane by default**.

### Update the documentation

Perl has pretty solid documentation, actually.  It's just got a whole lot of cobwebs, as well.  I hear of occasional little fixes, but something more serious needs to be done here.

1. The documentation isn't very helpful for beginners.  The online perldoc index points me to perlintro, which is an extremely quick once-over that devotes more space to regex syntax than Perl operators.  Perhaps Modern Perl could be distilled down to a more thorough introduction.

2. There is _a lot_ of duplicated stuff here.  Data structures are covered in perlreftut, perllol, perlref, perldsc.  OO is covered in perlboot, perltoot, perltooc, perlobj.  Surely we only need one tutorial and one reference.

3. Advanced topics aren't covered terribly well.  There's a variety of module, package, symbol table, function, scoping, and OO stuff strewn about perlmod and perlsub and perlref, but a lot of glob behavior I've had to figure out by trial and error.  Closures are briefly mentioned, but not in great detail; I'm actually not sure whether named subs act as closures, though surely they must.  These perhaps aren't the most common features to research, but they're powerful enough to deserve some first-class explanation.  Exception handling is, I believe, only covered at all in the `eval` function documentation.  Two-phase garbage collection is covered in perlobj.

4. perltie is just awful, at least for filehandles.  It only explains a handful of the tied methods, claims the support is "partial" but doesn't say what's missing, and was generally useless when I actually needed to implement a tied filehandle class.  How does `OPEN` work?  The manual doesn't even mention what _arguments_ it takes; I had to source-dive existing modules.  (The docs for `Tie::Handle` claim that `OPEN` is passed the object and the filename.  But this is outright wrong; `OPEN` receives whatever was passed to `open()`!)

5. As much as the Perl community stresses the value of CPAN, the Perl documentation makes little mention of non-core modules except to wave the user vaguely in CPAN's direction.  Moose, the championed solution to all problems, isn't mentioned _anywhere_.

6. Similarly, it's very difficult to even figure out what Perl can do out of the box, because its core modules are difficult to identify and read about.  perldoc.perl.org has a module index, but it's split into 26 pages by first letter.  `Module::CoreList` and `corelist` are helpful, but I have to actually run them locally; I don't get an online list.  And both of these suffer from the same problem of actually listing _every module_, rather than every "distribution".  `Module::Build` consumes some 24 lines, 14 of which are just platform support for various OSes.

    No wonder so many new Perl developers do pathname manipulation manually.  How are they going to find `File::*`?

7. Partly due to age, and partly due to some of the above, the Perl documentation just has some completely insane things in it.  Some of it is ancient and questionable code; some of it is inexcusably nuts.  These are things I've run across in the past few days; I haven't done an exhaustive search here.

    * perltoot shows code examples that set `@ISA` directly (without declaring it, as there's no `strict`), explains obscure object models like blessed arrayrefs and _closures_, shows how to add base classes to `UNIVERSAL`, and demonstrates the slightly insane `Alias` module.

    * perltooc is a slow descent into madness, starting with fully-qualified package globals and ending with a lexical hash of class-slash-prototype data used by several hybrid object/class methods.  I'm unsure why this topic even deserves such a lengthy page to itself.

    * perlboot _starts out_ by defining functions in other packages and then calling them directly, then shows how to do this dynamically using soft references.  It also assigns directly to `@ISA`, without `strict`.

    * perlref states that you "might also think of closure as a way to write a subroutine template without using eval()."  perldiag explains how to silence the duplicate format warning, by creating the second format with `eval`.

    * From perlfaq7:

        > Note that some languages provide anonymous functions but are not capable of providing proper closures: the Python language, for example.

        This hasn't been true since, what, 2.1?  What is this even doing here?  The same file has some quirky syntax like `$$name{WIFE}` and, for some reason, explains scoping in more detail than the core documentation.

I'm not sure how to approach this.  There's a lot of good content in the Perl docs, but it comes from several different eras and not all of it is arranged well.

It might be best to just identify the handful of things that need better coverage and give them new pages.  Transplant and update chunks of code from existing pages, then remove whatever's left over and not useful.

The documentation is the first line of defense against crappy Perl and the loss of potential converts; it should fucking **sparkle**.

## Fixing Perl 6

I think I just told Perl 5 that it should be more like Perl 6, hm.  Well, anyway.

I snuck this onto my last post, but I'll repeat it here: I suspect a big problem with Perl 6's perception is that it's unique in having a rather big and complete-looking spec out of the gate.  Its implementors treat this as a rough direction to build towards, but the very existence of a spec means that the rest of the world thinks _Perl 6 isn't done until something mostly complies with the spec_.  As the spec is still free to expand to fill in vague areas or cover new ideas or discovered shortcomings, this is basically doomed from the beginning.

And so I propose that the Perl 6 spec be carved down into a fairly specific and reasonable milestone, and then an interpreter that complies with _that_ can be released.  It'll match something written down, so it can be blessed as "sort of a finished thing", and everyone will have a clear idea of what it's capable of.  Once that's finished, a more expansive subset of the spec can be created as the next milestone, and the process repeats until you're done and have released Perl τ.

### Rakudo's status

I complained that it's not obvious what Rakudo actually does and doesn't do.  pmichaud responded:

> The current lead article on rakudo.org is "Rakudo Star 2011.04 released".  The fifth paragraph of that article says "There are some key features of Perl 6 that Rakudo Star does not yet handle appropriately", followed by the list of Perl 6 features known not to work.

> I admit there may be better ways to display this information in greater detail, such as the chart you link to.  But I'm personally burned out on writing web scripts and the like, and I know there are plenty of people who can do a better job than me.  So I'm hoping someone else will pick up that task.

This is true; rakudo.org does mention _missing_ features.  But as a potential user who may know very little about Rakudo or even Perl 6, that doesn't tell me a lot about its _implemented_ features.  I can try to write some software in Rakudo, but I'll end up playing whack-a-mole with the spec, which I probably don't want to read in its entirety anyway.

Even without a big colorful feature matrix (though it would be _awesome_), a page briefly summarizing what Rakudo can already do would be phenomenally helpful.  Follow it up with some example programs that cover a variety of useful tasks and features.  I know these things already exist, because they're all over Planet Perl Six!  Show the world the work you've been doing and plaster working code all over Rakudo's homepage.

---

Most important of all, I think, is to admit that Perl _might have_ a bit of a popularity decline on its hands.  What can be done about that?  Is Perl's future growth more or less important than backwards compatibility, historical reasons, thorough documentation, or even TMTOWTDI?

...

Don't look at me; I have no idea.

---

**Addendum**: The very first comment I got about this post was the following:

    > wow
    > as an uneducated code monkey, i don't even consider perl as a webdev language at all
    > like, php is quick and easy and makes it easy to shoot yourself
    > asp/.net is this microsoft thing that a lot of people use
    > flex is this adobe thing that less people use
    > when i think of "perl" i think of "more powerful than bash for stuff"
    > (that is just my perception, though)

This was from an IRC channel that mentions Perl Web development with some regularity.  I am _concerned_.

---

**Addendum Sat Jul 23, 2011**: There are a couple obvious omissions from the above list of Perl 5 things to fix, though with less-than-obvious solutions.

* Function calling/returning conventions.  Much like the object support, Perl more allows you to invent your own calling conventions than actually providing you with one.  CPAN modules meant to fix this are generally weird/awkward, slow, or both.  More than anything else, I think this is a problem that can only be solved well in core.

    One subtle problem is that of passing/returning lists; passing lists loses the runtime "odd number of elements" warning, and returning an arbitrarily-sized list is potentially slow since the operation is always a copy.  A new kind of sub might be able to optimize around this problem.  Or maybe we should just always return arrayrefs now that core functions treat arrayrefs like arrays.

* Speaking of, with core functions treating arrayrefs just like arrays, we're not too far off from just having arrays act as opaque containers.  With the two becoming increasingly interchangeable, I actually kind of worry that newcomers will find the distinction even harder to grasp.  `@array` can't be up and changed without breaking virtually all existing code, though, so I wonder what can be reasonably done about this.  Maybe in the far-off future, sigils will vanish entirely and tutorials will use `my $foo = [1..3];` as the canonical way to create an array.

* Fix string-vs-bytes handling.  Well, maybe.  I'm ashamed to admit I don't even quite grok how this works at the moment, as the support has changed somewhat in every major release of Perl since 5.8, and with the continued backwards compatibility it's difficult to even notice a difference.  With the last big Perl Web project I did, I just kind of held my breath and assumed it would all work; thanks to Catalyst's effort, it kind of did.  But I'm not very _confident_ about that.

    Despite the obvious massive problems with the porting effort, I still think Python 3 is the only language to have gotten this right.  For those not familiar: the `str` class in Python 3 is Unicodey (i.e., a character is a Unicode codepoint), but all I/O by default yields `bytes` (where a character or slice just gives you integers).  You can convert back and forth easily enough with `str.encode()` and `bytes.decode()`, and printing a `str` to a byte-y medium like a terminal or file will encode to UTF-8 by default, but otherwise Python will explode at you if you try to casually mingle the two.

* Template Toolkit blows, man.  Someone invent something better.  Yeah, I know, this isn't part of Perl core, but TT makes Web development look clunky and 90s.  It's great for really dumb templates, but it tries very hard to be richer than that and doesn't do so well.

[mop]: https://github.com/stevan/p5-mop/blob/master/proposal/p5-mop.md
[barewords in open]: http://www.learning-perl.com/?p=235
