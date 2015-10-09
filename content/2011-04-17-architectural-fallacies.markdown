title: Architectural Fallacies
date: 2011-04-17 02:09:00
category: blog
tags: python, tech, popular

I spend a lot of time in [#python][] and [#perl][].  Far more than is healthy, probably.  And I've noticed some patterns in the kinds of questions people ask.

There are plenty of people who have trouble expressing themselves well enough to [get answers in the first place][getting answers], but those are just communication problems.  (That's a good read if you ever ask nerds for help, by the way.)  More subtle, more insidious, and more _common_ are people who just ask questions that shouldn't be asked in the first place.

These are architectural fallacies: logical flaws in the very process of building or designing something.  They lead programmers towards solutions that are hard to understand, are inefficient, or just don't work.  And they confuse the heck out of the people trying to help.

<!-- more -->


## The XY Problem

This one [isn't mine][xy problem], but I see it _all the time_.  You can read the wiki entry, but the basic idea is:

1. User wants to do X, but doesn't know how.
2. User stumbles upon approach Y, which sounds somewhat relevant, and decides Y must be the solution to doing X.
3. User doesn't know how to do Y, either, so asks for help with Y.

Cue a lot of confusion from anyone who tries to help, since Y often sounds like a really odd thing to do, but without any context there's nothing easier to suggest.  Eventually the user will mention the original problem, which of course has a much simpler solution that has no relation to Y whatsoever.

The problem is subtle to notice, but happens all the time.  The vast majority of people asking how to do something extremely specific have fallen prey to this.  I've stopped trying to answer such questions, and instead try to extract the context right from the start.  Tell me **what** you want to do, not **how** you want to do it.  "How do I sort a list of numbers by their last digit?" is not a problem to be solved or a task to be accomplished; it's a homework question.


## The Swiss Army Rock Problem

This one _is_ mine, finally christened with a name after watching the exact same exchange happen in #python several times in the span of two days.

People very frequently come into #python asking how to use either threads or sockets.  Both of these are low-level and tricky concepts.  They're the kinds of things that take a lot of fiddling before they _appear_ to work, and even then you probably have some obscure behavior that will inevitably surprise you later.  Imagine building a house out of spaghetti; I'm sure you can immediately envision what it would look like, and your mental image doesn't seem that complicated, but the details will surely get you.

If only someone had taken care of all the gory details already, and you could benefit from that work!  Well, someone has, and it's the excellent [Twisted][] library.  So whenever someone asks how to use sockets—and literally 90% of the time it is for building an IRC bot—someone directs them to Twisted.  And whenever someone asks how to use threads, and it turns out to be for doing a lot of HTTP requests at once (again, 90% of the time), someone directs them to Twisted.  Simple, right?

Unfortunately, quite a lot of people take offense to this.  They already started using threads or sockets or both, and now they're [committed][sunk cost fallacy], dangit; why can't we just answer their question?

A little probing sometimes reveals a deeper reason, though.  Some people don't want to use Twisted because it _does too much_.

Now, I freely admit I'm not an expert on Twisted; I've only recently been digging into it myself for dywypi.  (My IRC bot.  Sigh.)  But the last way I'd describe it is _bulky_.  Twisted is actually a fantastic example of really [abstracted architecture][abstraction vs indirection]; it has whole Web servers and clients built in, sure, but they're built on top of the same components that are available for you to use for anything else.  You can start building a network application almost from scratch, doing all the parsing and connection handling yourself, or you can start from a slightly higher level that already parses lines and reconnects automatically.

But people object anyway, because Twisted is a Whole Thing, and sockets are _simple_.  This is a serious misunderstanding of what "simple" means; grains of sand are pretty damn simple, and castles are made out of them, but I wouldn't head for the beach if I wanted to build Buckingham Palace.

This is the Swiss Army Rock problem.

1. User wants to solve some problem X.
2. X requires doing common programming task Y.
3. There are libraries which take care of the gory details of Y.
4. User decides not to use these libraries, because X is "simple" and the libraries are "complicated".

The user has decided that the problem is simple, therefore only simple tools should be required to solve it.  I gave this attitude its name after summarizing it like this:

> "I want to pound a nail, but hammers do too many other things; I don't need to pull nails out."
    
> "Instead I'll just figure out how to tie this rock to the end of this stick."
    
> "Hmm, now I need to pull a nail out.  I bet if the rock had a notch in it..."


I remember being told about a UDP tracker protocol—a BitTorrent protocol for finding who has files available—that used UDP, for "high performance" and "low overhead".

For the non-nerds: most networking is built upon either TCP or UDP.  The major difference is that UDP is "throw data at the other end and hope for the best", whereas TCP is "throw data at the other end, but try again if they don't say they got it all in the right order".  You may be shocked to hear that UDP is faster, but virtually everything uses TCP instead.

So, let's stop and think about this for a moment.  BitTorrent is meant for downloading files.  To download files, you need to know who else has them.  With UDP, that list of people might come over the wire garbled or incomplete or missing entirely.

I can just imagine the conversation between the developers now.

> "Hmm, we can't be sure the list of peers was downloaded correctly."

> "That's okay, we'll just rig something to check that the list is valid, and resend it if it's not."

You know, kinda like TCP does.


## The Scarlet Programmer

I apologize for being Python-specific again, but the same could surely apply to any other language.

You see, Python doesn't have anonymous functions.  That means that this sort of thing in Perl:

```perl
do_twice(sub { print "this will print twice!" });
```

Or JavaScript:

```javascript
do_twice(function() { alert("this will show twice!") });
```

...can't be done directly in Python.  Functions have to be given names, and have to be defined on their own.  So you'd actually need to do this:

```python
def thing_to_do_twice():
    print "this will show twice!"
do_twice(thing_to_do_twice)
```

The horror!  (You can do some simple things inline in Python, and there are good reasons for this restriction, but the point stands that you can't just translate the Perl/JS/Ruby/etc. style directly to Python.)

In practice, this is very rarely a problem.  Just defining a function is pretty easy, and there are other ways to solve specific problems that would require the above approaches in other languages.  But people coming from those other languages are really really used to the way they do things, and they really really want to speak their other language with a Python dialect.

That on its own is already a bad sign; when in Rome, etc etc.  I've seen Python written by C programmers who really want Python to look like C, and the resulting mishmash doesn't look like either.  It's a pain to understand, too, even if all they do is add extra parentheses somewhere.  I have to keep double-checking in case I missed something, because surely there's a _reason_ the author used all these unnecessary things?

The real problem appears when I have this recurring conversation with someone:

    <dude> hey, how do I do anonymous functions in Python?
    <Eevee> you can't; python doesn't have them.  what are you trying to do?
    <dude> I need to pass callbacks to some library
    <Eevee> ok, you could do X or Y or Z
    <dude> but those are stupid and ugly.  I want to use anonymous functions
    <Eevee> ...they don't exist in Python
    <dude> why not?  they should

This usually goes on a bit longer, with some explanation as to why Python is the way it is and what other options the guy has.  Someone who's gone this far usually leaves unsatisfied.

What, exactly, am I expected to do here?  I didn't make Python.  I don't decide how Python works.  Even if I did, should I change my mind right now, go update Python, and roll out a new version in the next ten minutes to solve this guy's problem?

It's as if our guest believes that, if he states his case enough and/or complains loudly enough, reality itself will _bend around him_ and conform to his wishes.  His wishes that have already been considered and rejected, no less.

Please don't do this.  Sometimes tools suck, and you are free to bitch about them, but you've still got to work with what you've got.  And sometimes tools are designed a certain way for a reason; no amount of frowning at a screwdriver will make it work better on nails.  Ah, more carpentry.

Regarding the name, I, uh.  I [read a lot of Wikipedia][house of m].


### Reverse Injustification

Admittedly this is a followup from a specific case of the above, but it amazed me so much that I just have to mention it.

So, we told some guy that his particular problem could be solved by decorators.  If you're not familiar with Python, decorators are a cute little thing that lets you do this:

```python
@some_decorator(argument)
def func():
    ...
```

Which means the same as this:

```python
def func():
    ...
func = some_decorator(argument)(func)
```

So you can modify a function in some way when you define it.  This is handy for getting rid of a lot of boilerplate; a common example is that in a Web application, where every page corresponds to a function somewhere, you might want to use a decorator like `@needs_permission('can_comment')` to require a particular permission for a specific page.  Then the logic for checking permissions and rejecting people who don't have them is kept out of the main logic of the page.

Our friend decided right off the bat that he didn't like decorators.  Rather than read up on them at all, or search for other solutions to his problem, or anything productive at all, he decided to argue with us that decorators are outright _bad_ and Python should have anonymous functions (again, implying that we were supposed to do something about this).

He started from the conclusion that _we were wrong_, without really knowing much about decorators, and worked backwards fumbling for a reason why we must be wrong.  Included in his list:

* Decorators would be unnecessary if Python had anonymous functions.  (Some core Python functionality uses decorators; class methods, for example, are decorated with `@classmethod`.)
* He has to repeat the decorator for every function he wants to decorate.  (He also has to repeat the `def` keyword.  Surprise, you have to tell the computer what you want.)
* He can't put the decorator on the same line as the `def`.  (???)
* Decorators with arguments are complicated.  (They look daunting, but they're not very hard if you understand how decorators work.)

He doesn't have the precise tool he wants, so everything else must be bad for _some_ reason.

I had a similar exchange with someone else, more recently.  He ran into this slightly obscure pitfall:

```python
counter = 0
def count():
    counter = counter + 1
    print "I have been called", counter, "times!"

count()
```

This function will raise a `UnboundLocalError`, claiming that `counter` doesn't exist on line 3.  If you don't know why, try to figure it out.

...

It's because Python doesn't have variable declaration.  Instead, variables are automatically declared if they're assigned to anywhere within the enclosing scope (function, class, file).  So when Python compiles the function, it sees `counter =` and knows that this function has its own _local_ variable called `counter`.  Later, when Python tries to run the function, it needs to compute `counter + 1`.  What's `counter`?  Well, it's a variable local to this function.  But nothing has been assigned to it yet, so Python raises the `UnboundLocalError`.

There are a few ugly workarounds for this, and the most common—and probably more correct than the above—is to replace the function with a callable object that remembers its own state.  Python 3 also introduces a `nonlocal` keyword to solve the above problem; it tells Python "hey, I know I'm assigning to this variable here, but I really mean to assign to the one _outside_ this function."

The guy who had this problem had a strong functional programming background, and having discovered this behavior, he declared that Python doesn't support _closures_.  Like, at all.

Now, a closure is just a function that remembers variables which existed outside of it when it was declared.  You know, like this:

```python
def make_func():
    x = 3
    def func():
        print x
    return func

f = make_func()
f()
```

This correctly prints `3`.  Notice that you have no way of accessing or examining `x` outside of `make_func`; as far as code outside that function is concerned, it's been destroyed.  But the returned function remembers it, even though it was created outside that function.  (This might seem like the obvious way for things to work, but it's actually a very complex topic, somewhat recent, and still a surprise to programmers who have only been using e.g. C++.)

So clearly Python supports closures just fine, and the existence of `nonlocal` demonstrates that you can read and write to remembered variables all you like.  The only problem here is a quirk with how variables are declared; if you had to say `var x` to announce that `x` is a variable local to this function, the problem would evaporate.

But no.  The guy was absolutely insistent about this: Python must just not support closures.  I and a few others explained the above several times, with several examples.  He remained insistent that Python only supports closures "with object".  (Literally everything in Python is an object.)  His tool wasn't working how he expected, and thus it must be broken, so he worked backwards to invent reasons for the brokenness.

You'll get much more done if you work to learn and understand your tools, rather than blaming them for being different or scowling at them until they change.

---

Somewhere along the line, all of these people forgot that they were trying to solve a problem, and started trying to Win.  I see this a lot, inside and outside of programming.  People losing at games want to disparage the winning team, so they look better.  People who get harsh criticism on their work badmouth the critic.  Or, hell, pick anything in politics or religion.  The goal of building or doing something is lost as soon as another human being gets in the way, replaced instead by a squabble for social dominance.  What can this possibly accomplish?  Even if you Win this argument, you're no closer to solving your problem, and you've just wasted everyone's time.

I don't understand the impulse to seek out people more knowledgeable than you, ask for their guidance, and then argue with them when they don't tell you what you want to hear.

(Sometimes people will comment on the general gruffness of the regulars, and they're absolutely right.  Hackers are pretty direct and terse.  Sorry.  You're asking for free help from experts in a culture that wants more than anything to share knowledge and build cool things.  If you would rather receive pats on the back regardless of the quality of your work or ideas, perhaps try knitting or the third grade.)


## Maslow's Hammer

Programmers really like carpentry metaphors.  We like to think anything we do is anywhere near as important as building houses.  Ha ha!

This is "when all you have is a hammer, everything looks like a nail".  I was surprised to find that this sentiment [predated hacker culture][maslow's hammer], though relieved that someone else noticed.

The problem occurs when a programmer discovers a new tool that radically alters his perspective on programming.  Previous assumptions have gone out the window.  Previous rules and boundaries have been shattered. _Anything is possible now._

After successfully solving a difficult problem with ease thanks to this new tool, the programmer is now convinced that this is the best tool ever, and thus that it can solve all problems.  This is a road to disaster.

For some people, this happens with their first programming language -- often PHP.  I briefly knew a guy who tried to write IRC services in PHP, because he adored PHP and just didn't see any reason to use anything else.  Because, hey, [PHP can do anything][turing tarpit]!

For others, this happens with the jump from a low-to-medium-level language (say, Java) to a high-level language (say, Ruby).  Suddenly you can create functions on the fly, edit classes after they're created, and _change how built-in stuff behaves_!  Well, okay, those are groovy and all, but I wouldn't use an ion cannon to light a match no matter how cool an ion cannon is.

If you're unlucky, this frequently leads into an XY Problem.  If you're more unlucky, you'll get questions phrased like this:

> How can I do Y using X?

You might think this is much better, as the seeker of knowledge has already expressed his actual problem.  But no.  This isn't a statement of the actual problem; this is a statement of the asker's absolute determination to use X no matter how inappropriate it is.  The ensuing conversation will almost certainly revolve around why the asker thinks X is great and how X can do anything just fine and why do we all hate X so much anyway.

I still fondly remember starting a project with a single collaborator, possibly the first time I'd done so.  At some point he decided to add tagging support by writing a superclass that granted tagging powers, then _patching other classes_ to add it as an extra superclass.  From a different file.  So I couldn't figure out how anything was working, because `A.foo()` was called and `A` didn't have a `foo` function and I had to just search the whole codebase.  It got ridiculous enough that I just scrapped the project after he lost interest and started over.  (Thankfully it hadn't gotten very far.)


## Blaming the Platform

This and the following two make for a trilogy of related problems.  Let's see what we can find out about human nature and [our own measures of competence][dunning-kruger effect].

> hey, guys, I think I found a bug in Python:

    >>> 3 / 2
    1

I've actually seen this one several times, though usually the supposed bug is more complex.  The reasoning is confounding.  When I run across unexpected behavior, I start to suspect the following things _in this order_:

1. My expectations are wrong.
2. Fatfingering.
3. My code is buggy.
4. I didn't save the file, etc.
5. The documentation is wrong.
6. My copy of Python or some library is screwed up.
7. An electrical storm is causing very specific problems with my computer.
8. The platform is broken.

These things are arranged in this order based roughly on how many other people have checked each of them.  My expectations are usually vetted only by myself, and are generally broad and complex.  Platforms, on the other hand, are used by zillions of people all the time.  Bugs happen, yes, but with outright incorrect behavior for relatively simple operations, chances are that someone else noticed first.

Blaming the platform _first_ indicates a strange sort of egocentrism.  We assume that what we do is correct when we do it, of course, or we wouldn't have done it.  But most experts will pause and reflect when they run across strange behavior.  I think the most important part about learning and improving is _assuming from the start_ that you are wrong about a great many things, and being very eager to find out what those things are.  Alas, a lot of us cheerfully assume that we're right about everything, and each correction comes as a surprise, or even as a personal attack.  When I'm fairly sure I'm right about something, it's because I feel I've _earned_ that rightness.


## Christopher Columbus Armstrong, Esquire

During the course of digging out the context of an XY Problem or similar, the following exchange sometimes happens:

    <inquirer> I'm writing a script/function/program to do X
    <regular> why? there's already library X
    <inquirer> oh cool! I didn't know this had been done before

Here, X is something like...  matrix multiplication.  Or a binary search.  Or parsing email.  Some task that's a little complicated, but fairly common and not too hard to figure out how to do.

Dearest reader, if you needed to take a picture of your computer screen, would you get out the camera and tripod?  Or would you perhaps, for the briefest moment, consider that someone may have had this problem before and already devised a nice solution for you?

This is the situation above.  Binary search and email parsing are both built into Python itself.  Matrix operations are provided by one of its most-used libraries, numpy.  Other people had these common problems, solved them as best they could, made their solutions available to others, and took responsibility for maintaining and improving those solutions.

Faced with such common problems, how can you presume that you're the first to have them?  Does parsing email with Python really seem like it's breaking new ground?


## The Door Says "Pull"

> my code is right, but it still doesn't work

Distinct from blaming the platform, this is blaming the universe itself.  Reality has come apart at the seams; all the parts are working, but the whole does not.

Well, no.  Reality is _probably_ still chugging along here.  Rather than having faith in his program and suspecting the platform, this programmer has faith in his program _and_ the platform, and has nothing left to blame.  The result is a state of confusion.  Worse, since his program is "right", the programmer won't actually mention how any of it works or paste any of the code; the actual question will be phrased something like:

> I'm trying to call a function and it doesn't work.  any ideas?

It doesn't go, Eevee.  Make it go, Eevee.

As a brief aside: many of these strange queries reflect a confusion about how this whole "asking for help" process works.  What, exactly, can I do with the above information?  It's remotely possible that I've had a similar problem that happens to match yours, but otherwise, I can't diagnose this.  I'm trying to _debug_ your problem, remember; I'm like a detective, looking at the evidence and trying to work out what could have left that evidence behind.  With no evidence, I can't even begin to guess what your problem is.

I suppose a misunderstanding of debugging is the particular problem here, too.  Here, I'll let you know the ultimate secret behind debugging:

**Something is wrong.**

Now, now, don't roll your eyes.  I mean it.  The code you wrote is, as far as you know, correct.  The libraries you use are, as far as you know, correct.  The platform is, as far as you know, correct.  The universe is, as far as you know, still working.  So what could be the problem?

Well, the problem is: _you are wrong about one of those_.  I suspect this is the hardest hurdle to get over, but all the worst debugging problems I've had came down to it.  I'd made a very basic assumption about something working, and it turned out to be false.  I inspected all the obvious culprits, but because I didn't suspect _everything_, I had to flail for a long time before I finally stumbled upon the cause.

So when faced with a bug, be willing to throw out all of your assumptions.  Because at least one of them is wrong, and the proof is right in front of you.  It doesn't matter what you _think_ is right, because you think everything is right, and if that were the case then you wouldn't have a bug.

I hope you can appreciate the title of this one now.

> I'm pushing the door as hard as I can, but it won't open!

Your pushing is fine.  The door is fine.  But your assumption about how the door works is flawed.  And if the above is all the information you give to a stranger who tries to help, then the answers (is the door stuck?  locked?  are you pushing the right side?) are likely to be as misguided as you.

That's pretty important when asking for help, actually.  Don't filter your question down to what you suspect is the problem but know isn't.  You're just imposing your faulty assumptions on the people trying to help you.  Give as much context as might be relevant, even if you don't think it's broken; after all, _something_ is at fault, and since you're asking _you must not know what it is_.


[#perl]: irc://irc.perl.org/perl
[#python]: irc://irc.freenode.net/python
[Twisted]: http://twistedmatrix.com/trac/
[abstraction vs indirection]: http://zedshaw.com/essays/indirection_is_not_abstraction.html
[dunning-kruger effect]: http://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect
[getting answers]: http://www.mikeash.com/getting_answers.html
[house of m]: http://en.wikipedia.org/wiki/House_of_M
[maslow's hammer]: http://en.wikipedia.org/wiki/Law_of_the_instrument
[sunk cost fallacy]: http://www.skepdic.com/sunkcost.html
[turing tarpit]: http://en.wikipedia.org/wiki/Turing_tarpit
[xy problem]: http://mywiki.wooledge.org/XyProblem
