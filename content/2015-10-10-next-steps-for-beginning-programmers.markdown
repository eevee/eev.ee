title: Next steps for beginning programmers
date: 2015-10-10 19:02
category: articles
tags: tech, reference

Last month [@zandrmartin](https://twitter.com/zandrmartin) asked me on Twitter:

> i would love to read a post about things you would recommend newish programmers learn, esp those coming from a php web background [⮹](https://twitter.com/zandrmartin/status/642451301973000192)
>
> not even tutorials as such, just like 'you should learn about x and how to implement it effectively' would be great [⮹](https://twitter.com/zandrmartin/status/642451466213556224)
>
> like when you were talking about bit masks a while back, i have no idea what those are or why you'd use them, but i want to [⮹](https://twitter.com/zandrmartin/status/642461144377069568)

I've opined on this sort of thing briefly in various impermanent places, but somehow never tried to consolidate it at all.  So here you go, some stream of consciousness on being more better at computers.

<!-- more -->

## Languages

Can't really be a programmer without a programming language.

One of the worst things you can do is only learn one language.  Solving problems is much easier if you're used to approaching them from different angles, and that's much harder to do if your thinking is colored by only a single language's toolbox.  It's fine to be opinionated, but you only get to have an opinion if you know what you're turning down.

Or as the saying goes: when all you have is a hammer, everything starts to look like a nail.  So expose yourself to as many things as you can, however briefly, just to be aware of what's _possible_.  Here's a good spread:

[**Python**](https://www.python.org/) is a very good general-purpose language that blends a few different approaches.  It's good for beginners, since it has a fairly low number of confusing hoops to jump through, but it's plenty powerful enough for large serious projects as well.  Be aware that Python 2 and Python 3 are slightly incompatible, but learn Python 3 and roll your eyes at anyone who tells you otherwise.

**Shell** could mean either the Unix shell family or DOS-style batch files or Windows PowerShell®™.  Take your pick, depending on your platform.  Either way you are in for a _WORLD OF PAIN_, because shell languages are a horrible nightmare.  Awkward syntax, obscure gotchas, little real documentation because most of what you want to use isn't actually part of the language.  And oh, they're some of the very few examples of truly interpreted languages, because they're run in a single pass.  So even if you have an egregious syntax error on line 500, you'll never find out until you actually try to execute that line.  Have fun!

**C** (by which I explicitly mean _not_ C++) is the rough equivalent of a pile of rocks held together with razor wire.  It's tedious to write, extremely difficult to write _correctly_, and hard to debug.  But it's still the lingua franca (for better or worse), it continues to influence a lot of languages created even now, and if nothing else it'll give you an appreciation for virtually every other language.  Its design also offers a lot of glimpses into how these strange machines operate under the hood.

Any **ML** will hurt your brain in a good way.  You probably want Haskell, which isn't really an ML, but it's close enough.  It's a pure functional language, which means...  a lot of things that you'll learn about very quickly.  It's extremely different from any of the above languages and will force you to approach problems from a very different angle.

**Prolog** is even more different than any of the above languages — it's entirely declarative, meaning that you list facts rather than issue commands, and trust the language to figure the rest out.  It's definitely, ah, quite an experience.

This list is not exhaustive!  I would definitely recommend reading up on lots of languages even if you don't give them a shot yourself.  For historical and cultural reasons, you might also want to try out **Smalltalk** and a **Lisp** variant.  Smalltalk introduced object-oriented programming; Lisp introduced dynamic typing.  Both of them have fairly unique syntax.  You might also want to try **Rust** to cleanse your palate after using C; it's a new systems language from Mozilla that does away with a lot of C's sharp edges.  And less seriously, there's **APL**, which is at least notable for being the only programming language to have Unicode characters dedicated explicitly to it.


## Terminology

Is an arbitrary mess, which hopefully you will learn really quickly on your tour through half a dozen languages.  C++ calls everything "member", a word that is meaningless to virtually everyone else.  Most languages have "methods", but you may encounter people who consider "methods" uniquely distinct from "functions", or who think all "functions" are actually "methods".  Python has "attributes", but everyone is constantly tempted to call them "properties", which are actually something slightly different.  A "float" in C is a numeric type of a particular size, but a "float" in Python is a numeric type of a different size, and "float" may also be short for "floating-point".  Many languages have "classes", but Haskell and some others have "typeclasses", which are mostly entirely different.  C has "casts" and "conversions", but everyone mixes them up all the time, even in languages that don't have casting.  "Strong typing" is a compliment given to Python, but "weak typing" is an insult used on Python.  Perl has its own entire lexicon.  Programming language theorists barely even speak English, what with their "covariance" and "higher kinds".

So don't be afraid to ask what people mean (or think they mean) with some term.  Don't be surprised if different communities use different words, or different meanings for the same words.  And don't get _too_ attached to the terminology — the ideas are what's actually important.  (I've often seen beginners ask for help and use a lot of jargon that doesn't quite mean what they think it does, which just confuses everyone.)


## Topics

Something I frequently see new programmers trip over (but few resources address) is confusing **data and its representation**.  A common example is someone using Python 2 who sees some string printed as `u'foo'`, and asks how to "remove the u".  Of course, the "u" isn't actually part of the string — Python uses it in debug output to indicate that this is a Unicode string, the same way you'd indicate that in source code.  Similarly, `"\x20"` is only one character, `dict(x=1)` is equivalent to `{'x': 1}`, and `"\"foo\""` does not contain any backslashes.

This may sound trivial, especially to non-beginners, but it's exactly the same kind of pitfall as not understanding text versus bytes.  Text is a sequence of characters, whereas bytes are units of memory.  If you're used to ASCII, then there's no distinction here, because any one ASCII character will fit in one byte.  But plenty of other characters _don't_ fit in one byte, so we need to find a way to fit them in multiple bytes, and we call those ways character encodings.  It's really no different from how the number 500 might be stored in four bytes as `f4 01 00 00`, or as `00 00 01 f4`, or in some other order, or in some other number of bytes.

Speaking of which, another good thing for beginners to learn about is **Unicode**!  I've [written about some curiosities in Unicode]({filename}/2015-09-12-dark-corners-of-unicode.markdown) before, though that's not necessarily aimed at beginners.

Along similar lines, general **problem-solving** is always useful in programming.  I don't think you can just pick up a book and read about it, but it's good to pay attention to how you approach problems and see what gets you the furthest in the least time.  Off the top of my head:

* Question your assumptions.  If everything looks right but the code still doesn't work, you're wrong about _something_ you thought you were right about, and now you have to figure out what it is.  Start with whatever you're least confident about and work from there.  (If you conclude there's a bug in your programming language or operating system, chances are you overlooked something you did.)
* Avoid the [XY problem](http://xyproblem.info/), where you end up sidetracked by a different problem that poorly fixes your original problem, just because you think you have a better chance of figuring out how to solve it.
* Fix the source of a problem, not its fallout.  The question of "removing the u" above is a great example; if that "u" appears somewhere it shouldn't, you need to fix whatever's spitting out debug information where it shouldn't be.  I've also seen a lot of people ask how to flatten a list in Python — that is, turn `[1, 2, [3, 4]]` into `[1, 2, 3, 4]` — and the right answer is usually to avoid creating a partly-nested list in the first place.

Ah, let's see.  Less abstractly...

**Indirection** is super duper important, because programmers love to solve problems by adding indirection.  If you work with C or a similar language, indirection is everywhere in the form of pointers.  In other languages it might exist as weak references, wrapper objects, referring to objects by keys in a dict, or even just creative uses of lists.

Somewhat related is **abstraction**, which is like handwaving.

You should understand various **data structures** — not necessarily how to make them from scratch, but how they work and when to use them.  Lists (or arrays, see above about terminology), dicts (or hash tables, ahem), sets, queues, stacks, trees.  Bitfields fall under this umbrella too, as they're really just a specific way to pack a set into a very small amount of space.

If your language has them, look into **metaclasses**.  Objects and values have a type, right?  If types are a kind of value in your language, then what's _their_ type?  The answer is a metaclass, and if you're lucky you can write your own and do all kinds of confusing shenanigans.  Your work is done when you can explain why `isinstance(object, type)` _and_ `isinstance(type, object)`.


## Tools

Learn **source control**.  It is _invaluable_, even if you only use it to undo a change that you realize isn't going to work.  [Git](https://try.github.io/) is hecka popular and well-supported by [GitHub](https://github.com/), but there are others as well, like [Mercurial](https://www.mercurial-scm.org/).  If you're feeling confident you might even stick your code on GitHub or [Bitbucket](https://bitbucket.org/), where other people can see it and give you a hand.  You could even find another beginner and work on something together.

Write **tests**.  The goal of tests is to make sure that in the future, when you rejigger your code, it still works the way you want it to.  This is a huge and complex topic, but even _one_ test is a good start (and better than none).  I don't know of any good introductions to testing off the top of my head, but the documentation for the (_excellent_) py.test test runner has [lots of examples of what simple tests might look like](http://pytest.org/latest/getting-started.html#our-first-test-run).

Use a **bug tracker** to keep track of what you plan to do.  You could use the issue tracker on a host like GitHub (even if you don't actually publish your code), or you could just keep a list in a text file (but make an effort to keep it organized).  Ideally, find someone else to collaborate with, so you actually have to make an effort to communicate your plans.  It might seem like pointless effort for a small project (and it kind of is), but it's good to get used to.

Get familiar with **IRC**, because most languages and open source projects have support channels on [Freenode](http://freenode.net/).



## Homework

Some interesting exercises, again kind of off the top of my head, which should help you cram more things into your brain.

In general, the best way to learn anything is to **keep doing things you don't know how to do**.  The downside is that you spend a long time feeling like an idiot, because you're constantly bad at everything, because you keep only doing things you're bad at.  The upside is that one day you wake up and discover you're pretty okay at a whole bunch of things, and even things you're bad at now come more easily.

With that in mind, here are some things you hopefully don't know how to do, broken into individual pieces you don't know how to do.

### Write a calculator

You can do this entirely from a terminal.

1. Prompt _separately_ for a number, an operator, and another number.  One per line.  Compute the result and print it out.

2. Prompt for them all on one line, like `2 + 3`.  But `2+3` should also work.

3. Extend it to work with two _or three_ numbers, so `1+2+3` works as well.

4. Now take order of operations into account, so `1+2*3` produces 7, not 9.

5. Support negative numbers.  You have to figure out whether `-` is subtraction or negation.

6. Make it work for any number of numbers.  One number is a valid calculation, remember — `5` just evaluates to 5.

    Hint: If you have trouble, add manual support for four or five numbers first, then look at all the cases you have and see what common code you can turn into loops or functions.

7. Finally, add support for parentheses, which can be nested arbitrarily deep.

    Hint: either recursion or a stack will be very very helpful.  Try to figure it out yourself!  It's very rewarding if you do.

Write tests as you go, so you can be sure you don't break something accidentally.


### Write a text adventure

You know.  Like [Zork](https://en.wikipedia.org/wiki/Zork).  West of a white house?  Likely to be eaten by a grue?  Jeez, kids these days.

Okay well these are games that are entirely text-based.  Even the player's actions are entered as commands, not by clicking or choosing from a menu.  So you might `take rock` or `eat sandwich`.  If you've really never experienced this genre (the predecessor to point-and-click adventures!), consider playing some of [these introductory games](http://pr-if.org/play/) to get a feel for what they're like.

So, games are an excellent exercise; simulating a world is surprisingly finnicky, and most programming languages aren't particularly good at it, so you have to get a little creative if you don't want your code to be a huge mess.  Text adventures have many of the same problems to solve, but without making you worry about how to find graphics or sound.  Plus, the player's commands are an open problem — you can get as fancy as you want in trying to understand what a human might type.

Here are some possible steps, but this is pretty open-ended, so feel free to do whatever you want:

1. Make it possible to `look` (which should describe the room) and `examine (object)` (where the possible objects are mentioned in the room description).  You can even hardcode the exact commands at first.

2. `look` automatically when the game starts, as is tradition.  Make it possible to win.  The only action the player can perform right now is looking at stuff, so that's the only way they can win, but you can jazz it up a bit by e.g. only mentioning the winning object in the description of another object.  Congratulations, you've written a game!

3. Give the player an inventory, let them check it with `inventory`, and let them `take` and `drop` objects.  Be sure to deal with objects that can't be taken, like a desk or the sky.  Change the win condition so the player has to take the right object, not just look at it.

4. Spruce up your command parsing a bit.  Add some command aliases, and let the player use "the".  So if you understand `take rock`, you should also understand `t rock`, or `take the rock`.  `i` and `inv` are common aliases for `inventory`, as well.  Think about possible aliases when you add new commands in the future.

5. Make it possible for objects to contain _other_ objects.  (Hint: this is just like having an inventory.)  Now the player needs to be able to `put (object) in (other object)`, which means your parser has to get a little more clever.  Change the win condition so the player has to put a specific item in a specific container.

6. Add a second room, and let the player move between rooms.  A common way to do this is with compass directions like `go east` (or `east`, or `e`), but do whatever you want.  Now you have to make sure the player can only interact with objects in the room they're in.  Change the win condition so the player has to carry an object from one room to the other.

7. At this point your code is probably a huge mess of `if`s, so stop for a moment and think about how you might clean it up.  Are there any repetitive bits you could pull out into functions?  Are there any clusters of variables that might work better as objects?

    Ideally, you want to separate your particular game from the code that runs it.  The line is blurry, and it's up to you where to draw it, but you want to be able to make a _second_ game with the least amount of effort (and least amount of copy-pasting).

8. There are lots of things you can do from here, depending on how ambitious you feel.

    * Support other actions on objects, like eating or drinking or waving or turning.  (How do you describe what to do when a particular object is eaten?  What do you do when the player tries to eat an object that's inedible?)
    * Support objects with _states_, like a lamp that can be turned on or off, or a drawer that can be open or closed.
    * Support objects that specifically interact with each other to do something other than win the game.  Perhaps a drawer can only be opened once it's been unlocked with the right key.
    * Have a room or object's description show different text the first time the player examines it.
    * Support saving and loading the game, or undoing the last action.


### Write something with a UI

Throw it on top of one of the previous projects, even.

A UI could be anything: a Qt GUI, a terminal UI, an Android app, a client-side Web app, whatever.  The point of this exercise is that dealing with real-time user input adds all kinds of little wrinkles.  How do you make sure the user can only do things that make sense at any given time?  How do you make it possible to cancel something in the middle of doing it, or do things in any order?  How do you implement undo, or autosave?  How do you make your program flexible without overloading the user with trivial choices?


### Write something that does networking

IRC bots are basically rites of passage, and come with some new and interesting concerns.

* You're running a program that's exposed to the Internet and everyone on it.  [Some of those people are total assholes.]({filename}/2015-08-22-security-through-misanthropy.markdown)  How can you be sure those assholes don't break your program — or worse, use your program to break your computer?
* What do you do when your bot gets disconnected?  If you reconnect, how often do you retry, and when do you give up?
* What do you do if your bot gets flooded with too many commands?
* If your bot does something that involves talking over the network to something else, like finding the titles for YouTube links (and it totally should do something like that), how do you deal with a slow server?  If you're waiting too long on YouTube, other commands won't go through, or you might get disconnected from IRC!
* How do you connect your bot to more than one server at a time?
* How do you make it easy to configure your bot?

Free hint: don't use sockets.  And if your language allows, don't use threads either.  See if you can find an async library.  Python has Twisted, the newly builtin asyncio, and much more recently `async` and `await`; JavaScript is _only_ async; .NET languages have `async` and `await` built in; Perl has POE and AnyEvent but I don't know if they're any good.  I can't think of any others off the top of my head, but async programming is _reasonably_ popular lately, so there oughta be something.


### Contribute to open source

Chances are, you've used _something_ that's open source.  If you use Firefox, [Mozilla goes out of its way to help newcomers contribute](https://developer.mozilla.org/en-US/docs/Introduction).  Most of Chrome's source is available, so you could try that too.  Most programming languages are open source, and most libraries are open source as well.  All my work is open source.  GitHub has [pages for browsing through popular projects](https://github.com/explore).  Take your pick, find a bug or missing feature, and just go take a crack at it.

Besides the hands-on experience and learning to work within someone else's workflow, this will give you the chance to experience some of the gritty squishy human parts of Real World Programming™:

* Getting work done without trampling all over work someone else is doing, or having your work trampled
* Dealing with grouchy maintainers who won't just merge your damn pull request
* Working alongside people who are obviously way smarter than you and can't seem to explain anything without using a lot of words you're pretty sure they made up
* Finding out that your brilliant and elegant solution to a problem literally only works on your machine and no one else's
* Doing a lot of hard work only to be subtweeted by [jerks on Twitter](https://twitter.com/eevee)

I'm only half kidding.  Knowing how to interact with a larger organization (for varying values of "organization") is pretty helpful, especially if you want to make a career of programming, and it's not always sunshine and rainbows.


## Towards the future

The sky's the limit!  Do what you enjoy.

But while you're here, I have [a few things that could use your help](/projects/)—
