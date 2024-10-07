title: A Rebuttal For Python 3
date: 2016-11-23 17:41
category: blog
tags: tech, yelling, python

Zed Shaw, of Learn Python the Hard Way fame, has now written [The Case Against Python 3](https://learnpythonthehardway.org/book/nopython3.html).

I'm not involved with core Python development.  The only skin I have in this game is that [I _like_ Python 3]({filename}/2016-07-31-python-faq-why-should-i-use-python-3.markdown).  It's a good language.  And one of the big factors _I've_ seen slowing its adoption is that respected people in the Python community keep grouching about it.  I've had multiple newcomers tell me they have the impression that Python 3 is some kind of unusable disaster, though they don't know exactly why; it's just something they hear from people who sound like they know what they're talking about.  Then they actually use the language, and it's fine.

I'm sad to see the Python community needlessly sabotage itself, but Zed's contribution is beyond the pale.  It's not just making a big deal about changed details that won't affect most beginners; it's complete and utter nonsense, on a platform aimed at people who can't yet recognize it as nonsense.  I am so mad.

<!-- more -->


## The Case Against Python 3

> I give two sets of reasons as I see them now. One for total beginners, and another for people who are more knowledgeable about programming.

Just to note: the two sets of reasons are largely the same ideas presented differently, so I'll just weave them together below.

> The first section attempts to explain the case against starting with Python 3 in non-technical terms so a beginner can make up their own mind without being influenced by propaganda or social pressure.

Having already read through this once, this sentence really stands out to me.  The author of a book many beginners read to learn Python in the first place is providing a number of reasons (some outright fabricated) not to use Python 3, often in terms beginners are ill-equipped to evaluate, but believes this is a defense _against_ propaganda or social pressure.


## The Most Important Reason

> Before getting into the main technical reasons I would like to discuss the one most important social reason for why you should not use Python 3 as a beginner:
>
> _THERE IS A HIGH PROBABILITY THAT PYTHON 3 IS SUCH A FAILURE IT WILL KILL PYTHON._
>
> Python 3's adoption is really only at about 30% whenever there is an attempt to measure it.

Wait, really?  Wow, that's fantastic.

I mean, it would probably be higher if the most popular beginner resources were actually teaching Python 3, but you know.

> Nobody is all that interested in finding out what the real complete adoption is, despite there being fairly simple ways to gather metrics on the adoption.

This accusatory sentence conspicuously neglects to mention what these fairly simple ways _are_, a pattern that repeats throughout.  The trouble is that it's hard to even define what "adoption" means — I write all my code in Python 3 now, but veekun is still Python 2 because it's in maintenance mode, so what does that say about adoption?  You could look at PyPI download stats, but those are thrown way off by caches and system package managers.  You could look at downloads from the Python website, but a great deal of Python is written and used on Unix-likes, where Python itself is either bundled or installed from the package manager.

> It's as simple as that. If you learn Python 2, then you can still work with all the legacy Python 2 code in existence until Python dies or you (hopefully) move on. But if you learn Python 3 then your future is very uncertain. You could really be learning a dead language and end up having to learn Python 2 anyway.

You could use Python 2, until it dies...  or you could use Python 3, which might die.  What a choice.

By some definitions, Python 2 is _already dead_ — it will not see another major release, only security fixes.  Python 3 is still actively developed, and its seventh major release is next month.  It even contains a new feature that Zed later mentions he prefers to Python 2's offerings.

It may shock you to learn that I know _both_ Python 2 _and_ Python 3.  Amazingly, two versions of the same language are much more similar than they are different.  If you learned Python 3 and then a wizard cast a spell that made it vanish from the face of the earth, you'd just have to spend half an hour reading up on what had changed from Python 2.

> Also, it's been over a decade, maybe even multiple decades, and Python 3 still isn't above about 30% in adoption. Even among the sciences where Python 3 is touted as a "success" it's still only around 25-30% adoption. After that long it's time to admit defeat and come up with a new plan.

Python 3.0 came out in 2008.  The first couple releases ironed out some compatibility and API problems, so it didn't start to gain much traction until Python 3.2 came out in 2011.  Hell, Python _2.0_ came out in 2000, so even Python 2 isn't multiple decades old.  It would be great if this trusted beginner reference could take two seconds to check details like this before using them to scaremonger.

The big early problem was library compatibility: it's hard to justify switching to a new version of the language if none of the libraries work.  Libraries could only port once their own dependencies had ported, of course, and it took a couple years to figure out the best way to maintain compatibility with both Python 2 and Python 3.  I'd say we only really hit critical mass a few years ago — for instance, Django didn't support Python 3 until 2013 — in which case that 30% is nothing to sneeze at.

> There are more reasons beyond just the uncertain future of Python 3 even decades later.

In one paragraph, we've gone from "maybe even multiple decades" to just "decades", which is a funny way to spell "eight years".


## Not In Your Best Interests

> The Python project's efforts to convince you to start with Python 3 are _not_ in your best interest, but, rather, are only in the best interests of the Python project.

It's bad, you see, for the Python project to want people to use the work it produced.

Anyway, please buy Zed Shaw's book.

Anyway, please pledge to [my Patreon](https://patreon.com/eevee).

> Ultimately though, if Python 3 were good they wouldn't need to do any convincing to get you to use it. It would just naturally work for you and you wouldn't have any problems. Instead, there are serious issues with Python 3 for beginners, and rather than fix those issues the Python project uses propaganda, social pressure, and marketing to convince you to use it. In the world of technology using marketing and propaganda is immediately a sign that the technology is defective in some obvious way.
>
> This use of social pressure and propaganda to convince you to use Python 3 despite its problems, in an attempt to benefit the Python project, is morally unconscionable to me.

Ten paragraphs in, Zed is telling me that I should be suspicious of anything that relies on marketing and propaganda.  Meanwhile, there has yet to be a single concrete reason why Python 3 is bad for beginners — just several flat-out incorrect assertions and a lot of handwaving about how inexplicably nefarious the Python core developers are.  You know, the same people who made Python 2.  But they weren't evil _then_, I guess.


## You Should Be Able to Run 2 and 3

> In the programming language theory there is this basic requirement that, given a "complete" programming language, I can run any other programming language. In the world of Java I'm able to run Ruby, Java, C++, C, and Lua all at the same time. In the world of Microsoft I can run F#, C#, C++, and Python all at the same time. This isn't just a theoretical thing. There is solid math behind it. Math that is truly the foundation of computer science.
>
> The fact that you can't run Python 2 and Python 3 at the same time is purely a social and technical decision that the Python project made with no basis in mathematical reality. This means you are working with a purposefully broken platform when you use Python 3, and I personally can't condone teaching people to use something that is fundamentally broken.

The programmer-oriented section makes clear that the solid math being referred to is Turing-completeness — the section is even titled "Python 3 Is Not Turing Complete".

First, notice a rhetorical trick here.  You can run Ruby, Java, C++, etc. at the same time, so why not Python 2 and Python 3?

But can you run Java and C# at the same time?  (I'm sure someone has _done_ this, but it's certainly much less popular than something like Jython or IronPython.)

Can you run Ruby 1.8 and Ruby 2.3 at the same time?  Ah, no, so I guess Ruby 2.3 is fundamentally and purposefully broken.

Can you run Lua 5.1 and 5.3 at the same time?  Lua is a _spectacular_ example, because Lua 5.2 made a breaking change to how the details of scope work, and it's led to a situation where a lot of programs that embed Lua haven't bothered upgrading from Lua 5.1.  Was Lua 5.2 some kind of _dark plot_ to deliberately break the language?  No, it's just slightly more inconvenient than expected for people to upgrade.

Anyway, as for Turing machines:

> In computer science a fundamental law is that if I have one Turing Machine I can build any other Turing Machine. If I have COBOL then I can bootstrap a compiler for FORTRAN (as disgusting as that might be). If I have FORTH, then I can build an interpreter for Ruby. This also applies to bytecodes for CPUs. If I have a Turing Complete bytecode then I can create a compiler for any language. The rule then can be extended even further to say that if I cannot create another Turing Machine in your language, then your language cannot be Turing Complete. If I can't use your language to write a compiler or interpreter for any other language then your language is not Turing Complete.

Yes, this is true.

> Currently you cannot run Python 2 inside the Python 3 virtual machine. Since I cannot, that means Python 3 is not Turing Complete and should not be used by anyone.

And this is completely asinine.  Worse, it's flat-out dishonest, and relies on _another_ rhetorical trick.  You only "cannot" run Python 2 inside the Python 3 VM because _no one has written a Python 2 interpreter in Python 3_.  The "cannot" is not a mathematical impossibility; it's a simple matter of the code not having been written.  Or perhaps it has, but no one cares anyway, because it would be comically and unusably slow.

I assume this was meant to be sarcastic on some level, since it's followed by a big blue box that seems unsure about whether to double down or reverse course.  But I can't tell why it was even brought up, because it has _absolutely nothing_ to do with Zed's true complaint, which is that Python 2 and Python 3 do not _coexist_ within a single environment.  Implementing language X using language Y does not mean that X and Y can now be used together seamlessly.

The canonical Python release is written in C (just like with Ruby or Lua), but you can't just dump a bunch of C code into a Python (or Ruby or Lua) file and expect it to work.  You _can_ talk to C from Python and vice versa, but defining how they communicate is a bit of a pain in the ass and requires some level of setup.

I'll get into this some more shortly.


## No Working Translator

> Python 3 comes with a tool called `2to3` which is supposed to take Python 2 code and translate it to Python 3 code.

I should point out right off the bat that this is not actually what you want to use most of the time, because you probably want to translate your Python 2 code to Python _2/3_ code.  `2to3` produces code that most likely will not work on Python 2.  [Other tools exist]({filename}/2016-07-31-python-faq-how-do-i-port-to-python-3.markdown) to help you port more conservatively.

> Translating one programming language into another is a solidly researched topic with solid math behind it. There are translators that convert any number of languages into JavaScript, C, C++, Java, and many times you have no idea the translation is being done. In addition to this, one of the first steps when implementing a new language is to convert the new language into an existing language (like C) so you don't have to write a full compiler. Translation is a fully solved problem.

This is completely fucking ludicrous.  Translating one programming language to another _is_ a common task, though "fully solved" sounds mighty questionable.  But do you know what the results look like?

I found a project called "Transcrypt", which puts Python in the browser by "translating" it to JavaScript.  I've never used or heard of this before; I just googled for something to convert Python to JavaScript.  Here's their first sample, a [demo using jQuery](http://transcrypt.org/examples#jquery_demo):

```python
def start ():
    def changeColors ():
        for div in S__divs:
            S (div) .css ({
                'color': 'rgb({},{},{})'.format (* [int (256 * Math.random ()) for i in range (3)]),
            })

    S__divs = S ('div')
    changeColors ()
    window.setInterval (changeColors, 500)
```

And here's the JavaScript code it compiles to:

```javascript
(function () {
    var start = function () {
        var changeColors = function () {
            var __iterable0__ = $divs;
            for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
                var div = __iterable0__ [__index0__];
                $ (div).css (dict ({'color': 'rgb({},{},{})'.format.apply (null, function () {
                    var __accu0__ = [];
                    for (var i = 0; i < 3; i++) {
                        __accu0__.append (int (256 * Math.random ()));
                    }
                    return __accu0__;
                } ())}));
            }
        };
        var $divs = $ ('div');
        changeColors ();
        window.setInterval (changeColors, 500);
    };
    __pragma__ ('<all>')
        __all__.start = start;
    __pragma__ ('</all>')
}) ();
```

Well, not quite.  That's actually just a small piece at the end of [the full 1861-line file](http://transcrypt.org/live/transcrypt/demos/jquery_demo/__javascript__/jquery_demo.js).

You may notice that the emitted JavaScript effectively has to _emulate_ the Python `for` loop, because JavaScript doesn't have anything that works exactly the same way.  And this is a basic, common language feature translated between two languages in the same general family!  Imagine how your code would look if you relied on gritty details of how classes are implemented.

Is this what you want `2to3` to do to your code?

Even if something has been proven to be mathematically possible, that doesn't mean it's _easy_, and it doesn't mean the results will be _pretty_ (or fast).

> The `2to3` translator fails on about 15% of the code it attempts, and does a poor job of translating the code it can handle. The motivations for this are unclear, but keep in mind that a group of people who claim to be programming language experts can't write a reliable translator from one version of their own language to another. This is also a cause of their porting problems, which adds up to more evidence Python 3's future is uncertain.
>
> ...
>
> Writing a translator from one language to another is a fully proven and fundamental piece of computer science. Yet, the 2to3 translator cannot translate code 100%. In my own tests it is only about 85% effective, leaving a large amount of code to translate manually. Given that translation is a solved problem this seems to be a decision bordering on malice rather than incredible incompetence.

The programmer-oriented section doubles down on this idea with a title of "Purposefully Crippled 2to3 Translator" — again, accusing the Python project of sabotaging everyone.  That doesn't even make _sense_; if their goal is to make everyone use Python 3 at any cost, why would they deliberately break their tool that reduces the amount of Python 2 code and increases the amount of Python 3 code?

`2to3` sucks because its job is hard.  Python is dynamically typed.  If it sees `d.iteritems()`, it might want to change that to `d.items()`, as it's called in Python 3 — but it can't always be sure that `d` is actually a `dict`.  If `d` is some user-defined type, renaming the method is wrong.

But hey, Turing-completeness, right?  It _must_ be _mathematically possible_.  And it is!  As long as you're willing to see this:

```python
for key, value in d.iteritems():
    ...
```

Get translated to this:

```python
__d = d
for key, value in (__d.items() if isinstance(__d, dict) else __d.iteritems()):
    ...
```

Would Zed be happier with that, I wonder?


## The JVM and CLR Prove It's Pointless

> Yet, for some reason, the Python 3 virtual machine can't run Python 2? Despite the solidly established mathematics disproving this, the countless examples of running one crazy language inside a Russian doll cascade of other crazy languages, and huge number of languages that can coexist in nearly every other virtual machine? That makes no sense.

This, finally, is the real complaint.  It's not a bad one, and it comes up sometimes, but...  it's not this easy.

The Python 3 VM is fairly similar to the Python 2 VM.  The problem isn't the VM, but the core language constructs and standard library.

Consider: what happens when a Python 2 old-style class instance gets passed into Python 3, which has no such concept?  It seems like a value would _have_ to always have the semantics of the language version it came from — that's how languages usually coexist on the same VM, anyway.

Now, I'm using Python 3, and I load some library written for Python 2.  I call a Python 2 function that deals with bytestrings, and I pass it a Python 3 bytestring.  Oh no!  It breaks because Python 3 bytestrings iterate as integers, whereas the Python 2 library expects them to iterate as characters.

Okay, well, no big deal, you say.  Maybe Python 2 libraries just need to be updated to work either way, before they can be used with Python 3.

But that's **exactly the situation we're in right now**.  Syntax changes are trivially fixed by `2to3` and similar tools.  It's libraries that cause the subtler issues.

The same applies the other way, too.  I write Python 3 code, and it gets an `int` from some Python 2 library.  I try to use the `.to_bytes` method on it, but that doesn't exist on Python 2 integers.  So my Python 3 code, written and intended purely for Python 3, now has to deal with Python 2 integers as well.

Perhaps "primitive" types should convert automatically, on the boundary?  Okay, sure.  What about the Python 2 `buffer` type, which is C-backed and replaced by `memoryview` in Python 3?

Or how about this very fundamental problem: names of methods and other attributes are `str` in both versions, but that means they're bytestrings in Python 2 and text in Python 3.  If you're in Python 3 land, and you call `obj.foo()` on a Python 2 object, what happens?  Python 3 wants a method with the _text_ name `foo`, but Python 2 wants a method with the _bytes_ name `foo`.  Text and bytes are not implicitly convertible in Python 3.  So does it error?  Somehow work anyway?  What about the other way around?

What about the standard library, which has had a number of improvements in Python 3 that don't or can't exist in Python 2?  Should Python ship two entire separate copies of its standard library?  What about modules like `logging`, which rely on global state?  Does Python 2 and Python 3 code need to set up logging separately within the same process?

There are no good solutions here.  The language would double in size and complexity, and you'd _still_ end up with a mess at least as bad as the one we have now when values leak from one version into the other.

> We either have two situations here:
>
> 1. Python 3 has been purposefully crippled to prevent Python 2's execution alongside Python 3 for someone's professional or ideological gain.
> 2. Python 3 cannot run Python 2 due to simple incompetence on the part of the Python project.

I can think of a third.


## Difficult To Use Strings

> The strings in Python 3 are very difficult to use for beginners. In an attempt to make their strings more "international" they turned them into difficult to use types with poor error messages.

Why is "international" in scare quotes?

> Every time you attempt to deal with characters in your programs you'll have to understand the difference between byte sequences and Unicode strings.

Given that I'm reading part of a book teaching Python, this would be a perfect opportunity to drive this point home by saying "Look!  Running exercise N in Python 3 doesn't work."  [Exercise 1](https://learnpythonthehardway.org/book/ex1.html), at least, works fine for me with a little extra sprinkle of parentheses:

```python
print("Hello World!")
print("Hello Again")
print("I like typing this.")
print("This is fun.")
print('Yay! Printing.')
print("I'd much rather you 'not'.")
print('I "said" do not touch this.')
```

Contrast with the _actual content_ of that exercise — at the bottom is a big red warning box telling people from "another country" (relative to where?) that if they get errors about ASCII encodings, they should put an unexplained magical incantation at the top of their scripts to fix "Unicode UTF-8", whatever that is.  I wonder if Zed has read his own book.

> Don't know what that is? Exactly.

If only there were a book that could explain it to beginners in more depth than "you have to fix this if you're foreign".

> The Python project took a language that is very forgiving to beginners and mostly "just works" and implemented strings that require _you_ to constantly know what type of string they are. Worst of all, when you get an error with strings (which is very often) you get an error message that doesn't tell you _what variable names you need to fix_.

The complaint is that this happens in Python 3, whereas it's accepted in Python 2:

```python-console
>>> b"hello" + "hello"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't concat bytes to str
```

The programmer section is called "Statically Typed Strings".  But this is not static typing.  That's [strong typing]({filename}/2016-07-26-the-hardest-problem-in-computer-science.markdown#loose-typing), a property that sets Python's type system apart from languages like JavaScript.  It's usually considered a _good_ thing, because the alternative is to silently produce nonsense in some cases, and then that nonsense propagates through your program and is hard to track down when it finally causes problems.

> If they're going to require beginners to struggle with the difference between bytes and Unicode the _least_ they could do is tell people what variables are bytes and what variables are strings.

That would be nice, but it's not like this is a new problem.  Try this in Python 2.

```python-console
>>> 3 + "hello"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

How would Python even report this error when I used literals instead of variables?  How could custom types hook into such a thing?  Error messages are hard.

By the way, did you know that several [error messages are much improved]({filename}/2016-07-31-python-faq-why-should-i-use-python-3.markdown#enhanced-exceptions) in Python 3?  Python 2 is somewhat notorious for the confusing errors it produces when an argument is missing from a method call, but Python 3 is specific about the problem, which is much friendlier to beginners.

> However, when you point out that this is hard to use they try to claim it's good for you. It is not. It's simple blustering covering for a poor implementation.

I don't know what about this is hard.  Why do you have a text string and a bytestring in the first place?  Why is it okay to refuse adding a number to a string, but not to refuse adding bytes to a string?

Imagine if one of the Python core developers were just getting into Python 2 and messing around.

```python
# -*- coding: utf8 -*-
print "Hi, my name is Łukasz Langa."
print "Hi, my name is Łukasz Langa."[::-1]
```

```text
Hi, my name is Łukasz Langa.
.agnaL zsaku�� si eman ym ,iH
```

Good luck figuring out how to fix that.

This isn't blustering.  Bytes _are not text_; they are binary data that could encode _anything_.  They happen to look like text sometimes, and you can get away with thinking they're text if you're not from "another country", but that mindset will lead you to write code that is _wrong_.  The resulting bugs will be insidious and confusing, and you'll have a hard time even reasoning about them because it'll seem like "Unicode text" is somehow a different beast altogether from "ASCII text".

[Exercise 11](https://learnpythonthehardway.org/book/ex11.html) mentions at the end that you can use `int()` to convert a number to an integer.  It's no more complicated to say that you convert bytes to a string using `.decode()`.  It shouldn't even come up unless you're explicitly working with binary data, and I don't see any reading from sockets in LPTHW.

> It's also not statically compiled as strongly as it could be, so you can't find these kinds of type errors until you run the code.

This comes a scant few paragraphs after "Dynamic typing is what makes Python easy to use and one of the reasons I advocate it for beginners."

You can't find _any_ kinds of type errors until you run the code.  Welcome to dynamic typing.

> Strings are also most frequently received from an external source, such as a network socket, file, or similar input. This means that Python 3's statically typed strings and lack of static type safety will cause Python 3 applications to crash more often and have more security problems when compared with Python 2.

On the contrary — Python 3 applications should crash _less_ often.  The problem with silently converting between bytestrings and text in Python 2 is that it _might_ fail, _depending on the contents_.  `"cafe" + u"hello"` works fine, but `"café" + u"hello"` raises a `UnicodeDecodeError`.  Python 2 makes it very easy to write code that appears to work when tested with ASCII data, but later breaks with anything else, even though the values are still the same types.  In Python 3, you get an error the first time you try to run such code, regardless of what's in the actual values.  That's the biggest reason for the change: it improves things from being intermittent _value_ errors to consistent _type_ errors.

More _security problems_?  This is never substantiated, and seems to have been entirely fabricated.


## Too Many Formatting Options

> In addition to that you will have 3 different formatting options in Python 3.6. That means you'll have to learn to read and use multiple ways to format strings that are all very different. Not even I, an experienced professional programmer, can easily figure out these new formatting systems or keep up with their changing features.

I don't know what on earth "keep up with their changing features" is supposed to mean, and Zed doesn't bother to go into details.  

Python 3 has three ways to format strings: `%` interpolation, `str.format()`, and the new `f""` strings in Python 3.6.  The `f""` strings use _the same syntax_ as `str.format()`; the difference is that where `str.format()` uses numbers or names of keyword arguments, `f""` strings just use expressions.  Compare:

```python
number = 133
print("{n:02x}".format(n=number))
print(f"{number:02x}")
```

This isn't "very different".  A frequently-used method is being promoted to syntax.

> I _really_ like this new style, and I have no idea why this wasn't the formatting for Python 3 instead of that stupid `.format` function. String interpolation is natural for most people and easy to explain.
>
> The problem is that beginner will now how to know all three of these formatting styles, and that's too many.

I could swear Zed, an experienced professional programmer, just said he couldn't easily figure out these new formatting systems.  Note also that `str.format()` has existed in Python 2 since Python 2.6 was released in 2008, so I don't know why Zed said "new formatting _systems_", plural.

This is a truly bizarre complaint overall, because the mechanism Zed likes best is the _newest_ one.  If Python core had agreed that three mechanisms was too many, we wouldn't be getting `f""` at all.  


## Even More Versions of Strings

> Finally, I'm told there is a new proposal for a string type that is both bytes and Unicode at the same time? That'd be fantastic if this new type brings back the dynamic typing that makes Python easy, but I'm betting it will end up being _yet another static type to learn_. For that reason I also think beginners should avoid Python 3 until this new "chimera string" is implemented and works reliably in a dynamic way. Until then, you will just be dealing with difficult strings that are statically typed in a dynamically typed language.

I have absolutely no idea what this is referring to, and I can't find anyone who does.  I don't see any recent [PEPs](https://www.python.org/dev/peps/) mentioning such a thing, nor anything in the last several months on [the python-dev mailing list](https://mail.python.org/mailman/listinfo/python-dev).  I don't see it in the [Python 3.6 release notes](https://docs.python.org/3.6/whatsnew/3.6.html).

The closest thing I can think of is the backwards-compatibility shenanigans for [PEP 528](https://www.python.org/dev/peps/pep-0528/) and [PEP 529](https://www.python.org/dev/peps/pep-0529/) — they switch to the Windows wide-string APIs for console and filesystem encoding, but pretend under the hood that the APIs take UTF-8-encoded bytes to avoid breaking libraries like Twisted.  That's a microscopic detail that should never matter to anyone _but_ authors of Twisted, and is nothing like a new hybrid string type, but otherwise I'm at a loss.

This paragraph really is a perfect summary of the whole article.  It speaks vaguely yet authoritatively about something that doesn't seem to exist, it doesn't bother actually investigating the thing the entire section talks about, it conjectures that this mysterious feature will be hard just because it's in Python 3, and it misuses terminology to complain about a fundamental property of Python that's always existed.


## Core Libraries Not Updated

> Many of the core libraries included with Python 3 have been rewritten to use Python 3, but have not been updated to use its features. How could they given Python 3's constant changing status and new features?

_What_ "constant changing status"?  The language makes new releases; is that bad?  The only mention of "changing" so far was with string formatting, which makes no sense to me, because the only major change has been the addition of syntax that Zed _prefers_.

> There are several libraries that, despite knowing the encoding of data, fail to return proper strings. The worst offender seems to be any libraries dealing with the HTTP protocol, which _does_ indicate the encoding of the underlying byte stream in many cases.

_In many cases_, yes.  Not in all.  Some web servers don't send back an encoding.  Some files don't _have_ an encoding, because they're images or other binary data.  HTML allows the encoding to be given inside the document, instead.  `urllib` has always returned bytes, so it's not all that unreasonable to keep doing that, rather than...  well, I'm not quite sure what this is proposing.  Return strings _sometimes_?

The [documentation for `urllib.request`](https://docs.python.org/3/library/urllib.request.html) and [`http.client`](https://docs.python.org/3/library/http.client.html) both advise using the higher-level [Requests](http://docs.python-requests.org/) library instead, in a prominent yellow box right at the top.  Requests has distinct mechanisms for retrieving bytes versus text and is vastly easier to use overall, though I don't think even it understands reading encodings from HTML.  Alas, computers.

Good luck to any beginner figuring out how to install Requests on Python 2 — but thankfully, Python 3 now comes bundled with pip, which makes installing libraries much easier.  Contrast with the beginning of [exercise 46](https://learnpythonthehardway.org/book/ex46.html), which apologizes for how difficult this is to explain, lists _four_ things to install, warns that it will be frustrating, and advises watching a _video_ to help figure it out.

> What's even more idiotic about this is Python has a really good [Chardet](https://pypi.python.org/pypi/chardet) library for detecting the encoding of byte streams. If Python 3 is supposed to be "batteries included" then fast Chardet should be baked into the core of Python 3's strings making it cake to translate strings to bytes even if you don't know the underlying encoding. ... Call the function whatever you want, but it's not magic to guess at the encoding of a byte stream, it's science. The only reason this isn't done for you is that the Python project decided that _you_ should be punished for not knowing about bytes vs. Unicode, and their arrogance means you have difficult to use strings.

Guessing at the encoding of a byte stream isn't so much science as, well, guessing.  Guessing means that [sometimes you're wrong](https://en.wikipedia.org/wiki/Bush_hid_the_facts).  Sometimes that's what you want, and I'm honestly ambivalent about having chardet in the standard library, but it's hardly _arrogant_ to not want to include a highly-fallible heuristic in your programming language.


## Conclusions and Warnings

> I have resisted writing about these problems with Python 3 for 5 versions because I hoped it would become usable for beginners. Each year I would attempt to convert some of my code and write a couple small tests with Python 3 and simply fail. If I couldn't use Python 3 reliably then there's no way a total beginner could manage it. So each year I'd attempt it, and fail, and wait until they fix it. I really liked Python and hoped the Python project would drop their stupid stances on usability.

Let us recap the usability problems seen thusfar.

- You can't add `b"hello"` to `"hello"`.
- `TypeError`s are phrased exactly the same as they were in Python 2.
- The type system is exactly as dynamic as it was in Python 2.
- There is a new formatting mechanism, using the same syntax as one in Python 2, that Zed prefers over the ones in Python 2.
- `urllib.request` doesn't decode for you, just like in Python 2.
- `档牡敤㽴` isn't built in.  Oh, sorry, I meant `chardet`.

> Currently, the state of strings is viewed as a Good Thing in the Python community. The fact that you can't run Python 2 inside Python 3 is seen as a weird kind of tough love. The brainwashing goes so far as to outright deny the mathematics behind language translation and compilation in an attempt to motivate the Python community to brute force convert all Python 2 code.
>
> Which is probably why the Python project focuses on convincing unsuspecting beginners to use Python 3. They don't have a switching cost, so if you get them to fumble their way through the Python 3 usability problems then you have new converts who don't know any better. To me this is morally wrong and is simply preying on people to prop up a project that needs a full reset to survive. It means beginners will fail at learning to code not because of their own abilities, but because of Python 3's difficulty.

Now that we're towards the end, it's a good time to say this: **Zed Shaw, your behavior here is fucking reprehensible.**

Half of what's written here is irrelevant nonsense backed by a vague appeal to "mathematics".  Instead of having even the shred of humility required to step back and wonder if there are complicating factors beyond whether something is theoretically _possible_, you have invented a variety of conflicting and malicious motivations to ascribe to the Python project.

It's fine to criticize Python 3.  The string changes force you to think about what you're doing a little more in some cases, and occasionally that's a pain in the ass.  I absolutely get it.

But you've gone out of your way to invent a _conspiracy_ out of whole cloth and promote it on your popular platform _aimed at beginners_, who won't know how obviously full of it you are.  And why?  Because you can't add `b"hello"` to `"hello"`?  Are you kidding me?  No one can even offer to _help_ you, because instead of examples of real problems you've had, you gave two trivial toys and then yelled a lot about how the whole Python project is releasing mind-altering chemicals into the air.

The Python 3 migration has been hard enough.  It's taken a lot of work from a lot of people who've given enough of a crap to help Python evolve — to make it _better_ to the best of their judgment and abilities.  Now we're finally, _finally_ at the point where virtually all libraries support Python 3, a few new ones _only_ support Python 3, and Python 3 adoption is starting to take hold among application developers.

And you show up to piss all over it, to propagate this myth that Python 3 is hamstrung to the point of unusability, because if the Great And Wise Zed Shaw can't figure it out in ten seconds then it must just be impossible.

Fuck you.

> Sadly, I doubt this will happen, and instead they'll just rant about how I don't know what I'm talking about and I should shut up.

This is because you don't know what you're talking about, and you should shut up.
