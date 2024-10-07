title: Python FAQ: Why should I use Python 3?
date: 2016-07-31 22:24
category: blog
tags: tech, python, unicode, patreon


_Part of my [Python FAQ]({filename}2011-07-22-python-faq.markdown), which is doomed to never be finished._

The short answer is: because it's the actively-developed version of the language, and you should use it for the same reason you'd use 2.7 instead of 2.6.

If you're here, I'm guessing that's not enough.  You need something to sweeten the deal.  Well, friend, I have got a whole _mess_ of sugar cubes just for you.

And once you're convinced, you may enjoy the companion article, [_how_ to port to Python 3]({filename}2016-07-31-python-faq-how-do-i-port-to-python-3.markdown)!  It also has some more details on the diffences between Python 2 and 3, whereas this article doesn't focus too much on the features removed in Python 3.

<!-- more -->

## Some background

If you aren't neck-deep in Python, you might be wondering what the fuss is all about, or why people keep telling you that Python 3 will set your computer on fire.  (It won't.)

Python 2 is a good language, but it comes with some considerable baggage.  It has two integer types; it may or may not be built in a way that completely mangles 16/17 of the Unicode space; it has a confusing mix of lazy and eager functional tools; it has a standard library that takes "batteries included" to [lengths beyond your wildest imagination](https://docs.python.org/2/library/sgi.html); it boasts strong typing, then casually insists that `None < 3 < "2"`; overall, it's just full of little dark corners containing weird throwbacks to the days of Python 1.

(If you're really interested, Nick Coghlan has written an exhaustive treatment of the slightly different question of [why Python 3 was created](http://python-notes.curiousefficiency.org/en/latest/python3/questions_and_answers.html).  This post is about why Python 3 is _great_, so let's focus on that.)

Fixing these things could break existing code, whereas virtually all code written for 2.0 will still work on 2.7.  So Python decided to fix them all at once, producing a not-quite-compatible new version of the language, Python 3.

Nothing like this has really happened with a mainstream programming language before, and it's been a bit of a bumpy ride since then.  Python 3 was (seemingly) designed with the assumption that everyone would just port to Python 3, drop Python 2, and that would be that.  Instead, it's turned out that most libraries want to continue to run on _both_ Python 2 and Python 3, which was considerably difficult to make work at first.  Python 2.5 was still in common use at the time, too, and it had none of the helpful backports that showed up in Python 2.6 and 2.7; likewise, Python 3.0 didn't support `u''` strings.  Writing code that works on both 2.5 and 3.0 was thus a ridiculous headache.

The porting effort also had a dependency problem: if your library or app depends on library A, which depends on library B, which depends on C, which depends on D...  then none of those projects can even _think_ about porting until D's porting effort is _finished_.  Early days were very slow going.

Now, though, things are looking brighter.  [Most popular libraries work with Python 3](http://py3readiness.org/), and those that don't are working on it.  Python 3's Unicode handling, one of its most contentious changes, has had many of its wrinkles ironed out.  Python 2.7 consists largely of backported Python 3 features, making it much simpler to target 2 and 3 with the same code — and both 2.5 and 2.6 are no longer supported.

Don't get me wrong, Python 2 will still be around for a while.  A lot of large applications have been written for Python 2 — think websites like Yelp, YouTube, Reddit, Dropbox — and porting them will take some considerable effort.  I happen to know that at least one of those websites was still running 2.6 last year, years after 2.6 had been discontinued, if that tells you anything about the speed of upgrades for big lumbering software.

But if you're just getting started in Python, or looking to start a new project, there aren't many reasons not to use Python 3.  There are still _some_, yes — but unless you have one specifically in mind, they probably won't affect you.

I keep having Python beginners tell me that all they know about Python 3 is that some tutorial tried to ward them away from it for vague reasons.  (Which is ridiculous, since _especially_ for beginners, Python 2 and 3 are fundamentally not that different.)  Even the #python IRC channel has a few people who react, ah, somewhat passive-aggressively towards mentions of Python 3.  Most of the technical hurdles have long since been cleared; it seems like one of the biggest roadblocks now standing in the way of Python 3 adoption is the community's desire to sabotage itself.

I think that's a huge shame.  Not many people seem to want to stand up for Python 3, either.

Well, here I am, standing up for Python 3.  I write all my new code in Python 3 now — because **Python 3 is great and you should use it.**  Here's why.


## Hang on, let's be real for just a moment

None of this is going to 💥blow your mind💥.  It's just a programming language.  I mean, the biggest change to Python 2 in the last decade was probably the addition of the `with` statement, which is _nice_, but hardly an earth-shattering innovation.  The biggest changes in Python 3 are in the same vein: they should smooth out some points of confusion, help avoid common mistakes, and maybe give you a new toy to play with.

Also, if you're writing a library that needs to stay compatible with Python 2, you won't actually be able to use any of this stuff.  Sorry.  In that case, the best reason to port is so application authors _can_ use this stuff, rather than citing your library as the reason they're trapped on Python 2 forever.  (But hey, if you're starting a brand new library that will blow everyone's socks off, do feel free to make it Python 3 exclusive.)

Application authors, on the other hand, can _go wild_.


## Unicode by default

Let's get the obvious thing out of the way.

In Python 2, there are two string types: `str` is a sequence of bytes (which I would argue makes it _not a string_), and `unicode` is a sequence of Unicode codepoints.  A literal string in source code is a `str`, a bytestring.  Reading from a file gives you bytestrings.  Source code is assumed ASCII by default.  It's an 8-bit world.

If you happen to be an English speaker, it's very easy to write Python 2 code that seems to work perfectly, but chokes horribly if fed anything outside of ASCII.  The right thing involves carefully specifying encodings everywhere and using `u''` for virtually all your literal strings, but that's very tedious and easily forgotten.

Python 3 reshuffles this to put full Unicode support front and center.

Most obviously, the `str` type is a real text type, similar to Python 2's `unicode`.  Literal strings are still `str`, but now that makes them Unicode strings.  All of the "structural" strings — names of types, functions, modules, etc. — are likewise Unicode strings.  Accordingly, [identifiers](https://docs.python.org/3/reference/lexical_analysis.html#identifiers) are allowed to contain any Unicode "letter" characters.  `repr()` no longer escapes printable Unicode characters, though there's a new `ascii()` (and corresponding `!a` format cast and `%a` placeholder) that does.  Unicode completely pervades the language, for better or worse.

And just for the record: this is way better.  It is _so much_ better.  It is incredibly better.  Do you know how much non-ASCII garbage I type?  Every single em dash in this damn post was typed by hand, and Python 2 would merrily choke on them.

Source files are now assumed to be UTF-8 by default, so adding an em dash in a comment will no longer break your production website.  (I have seen this happen.)  You're still free to specify another encoding explicitly if you want, using a [magic comment](https://docs.python.org/3/tutorial/interpreter.html#source-code-encoding).

There is no attempted conversion between bytes and text, as in Python 2; `b'a' + 'b'` is a `TypeError`.  Some modules require you to know what you're dealing with: [`zlib.compress`](https://docs.python.org/3/library/zlib.html#zlib.compress) only accepts `bytes`, because zlib is defined in terms of bytes; [`json.loads`](https://docs.python.org/3/library/json.html#json.loads) only accepts `str`, because JSON is defined in terms of Unicode codepoints.  Calling `str()` on some bytes will defer to `repr`, producing something like `"b'hello'"`.  (But see `-b` and `-bb` below.)  Overall it's pretty obvious when you've mixed bytes with text.

Oh, and two huge problem children are fixed: both [the `csv` module](https://docs.python.org/3/library/csv.html) and [`urllib.parse`](https://docs.python.org/3/library/urllib.parse.html) (formerly `urlparse`) can handle text.  If you've never tried to make those work, trust me, this is miraculous.

I/O does its best to make everything Unicode.  On Unix, this is a little hokey, since the filesystem is explicitly bytes with no defined encoding; Python will trust the various locale environment variables, which on most systems will make everything UTF-8.  The default encoding of text-mode file I/O is derived the same way and thus usually UTF-8.  (If it's not what you expect, run `locale` and see what you get.)  Files opened in binary mode, with a `'b'`, will still read and write bytes.

Python used to come in "narrow" and "wide" builds, where "narrow" builds actually stored Unicode as UTF-16, and this distinction could leak through to user code in subtle ways.  On a narrow build, `unichr(0x1F4A3)` raises `ValueError`, and the length of `u'💣'` is 2.  Surprise!  Maybe your code will work on someone else's machine, or maybe it won't.  Python 3.3 eliminated narrow builds.

I think those are the major points.  For the most part, you should be able to write code as though encodings don't exist, and the right thing will happen more often.  And the wrong thing will immediately explode in your face.  It's good for you.

If you work with binary data a lot, you might be frowning at me at this point; it _was_ a bit of a second-class citizen in Python 3.0.  I think things have improved, though: a number of APIs support both bytes and text, the bytes-to-bytes codec issue has largely been resolved, we have `bytes.hex()` and `bytes.fromhex()`, `bytes` and `bytearray` both support `%` now, and so on.  They're listening!

Refs: [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#text-vs-data-instead-of-unicode-vs-8-bit); myriad mentions all over the documentation


## Backported features

Python 3.0 was released shortly after Python 2.6, and a number of features were then backported to Python 2.7.  You can use these if you're only targeting Python 2.7, but if you were stuck with 2.6 for a long time, you might not have noticed them.

- Set literals:

        :::python
        {1, 2, 3}

- Dict and set comprehensions:

        :::python
        {word.lower() for word in words}
        {value: key for (key, value) in dict_to_invert.items()}

- Multi-`with`:

        :::python
        with open("foo") as f1, open("bar") as f2:
            ...

- `print` is now a function, with a couple bells and whistles added: you can change the delimiter with the `sep` argument, you can change the terminator to whatever you want (including nothing) with the `end` argument, and you can force a flush with the `flush` argument.  In Python 2.6 and 2.7, you still have to opt into this with `from __future__ import print_function`.

- The string representation of a float now uses the shortest decimal number that has the same underlying value — for example, `repr(1.1)` was `'1.1000000000000001'` in Python 2.6, but is just `'1.1'` in Python 2.7 and 3.1+, because both are represented the same way in a 64-bit float.

- `collections.OrderedDict` is a dict-like type that remembers the order of its keys.

    Note that you _cannot_ do `OrderedDict(a=1, b=2)`, because the constructor still receives its keyword arguments in a regular dict, losing the order.  You have to pass in a sequence of 2-tuples or assign keys one at a time.

- `collections.Counter` is a dict-like type for counting a set of things.  It has some pretty handy operations that allow it to be used like a multiset.

- The entire [`argparse` module](https://docs.python.org/3/library/argparse.html) is a backport from 3.2.

- `str.format` learned a `,` formatting specifier for numbers, which always uses commas and groups of three digits.  This is wrong for many countries, and the correct solution involves using the `locale` module, but it's useful for quick output of large numbers.

- `re.sub`, `re.subn`, and `re.split` accept a `flags` argument.  Minor, but, _thank fucking God_.

Ref: [Python 2.7 release notes](https://docs.python.org/3/whatsnew/2.7.html#python-3-1-features)




## Iteration improvements

### Everything is lazy

Python 2 has a lot of pairs of functions that do the same thing, except one is eager and one is lazy: `range` and `xrange`, `map` and `itertools.imap`, `dict.keys` and `dict.iterkeys`, and so on.

Python 3.0 eliminated all of the lazy variants and instead made the default versions lazy.  Iterating over them works exactly the same way, but no longer creates an intermediate list — for example, `range(1000000000)` won't eat all your RAM.  If you need to index them or store them for later, you can just wrap them in `list(...)`.

Even better, the `dict` methods are now "[views](https://docs.python.org/3/library/stdtypes.html#dict-views)".  You can keep them around, and they'll reflect any changes to the underlying dict.  They also act like sets, so you can do `a.keys() & b.keys()` to get the set of keys that exist in both dicts.

Refs: [dictionary view docs](https://docs.python.org/3/library/stdtypes.html#dict-views); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#views-and-iterators-instead-of-lists)

### Unpacking

Unpacking got a huge boost.  You could always do stuff like this in Python 2:

```python
a, b, c = range(3)  # a = 0, b = 1, c = 2
```

Python 3.0 introduces:

```python
a, b, *c = range(5)  # a = 0, b = 1, c = [2, 3, 4]
a, *b, c = range(5)  # a = 0, b = [1, 2, 3], c = 4
```

Python 3.5 additionally allows use of the `*` and `**` unpacking operators in literals, or multiple times in function calls:

```python
print(*range(3), *range(3))  # 0 1 2 0 1 2

x = [*range(3), *range(3)]  # x = [0, 1, 2, 0, 1, 2]
y = {*range(3), *range(3)}  # y = {0, 1, 2}  (it's a set, remember!)
z = {**dict1, **dict2}  # finally, syntax for dict merging!
```

Refs: [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#new-syntax); [PEP 3132](https://www.python.org/dev/peps/pep-3132); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#pep-448-additional-unpacking-generalizations); [PEP 448](https://www.python.org/dev/peps/pep-0448)

### `yield from`

`yield from` is an extension of `yield`.  Where `yield` produces a single value, `yield from` yields an entire sequence.

```python
def flatten(*sequences):
    for seq in sequences:
        yield from seq

list(flatten([1, 2], [3, 4]))  # [1, 2, 3, 4]
```

Of course, for a simple example like that, you could just do some normal `yield`ing in a `for` loop.  The magic of `yield from` is that it can also take another generator or other lazy iterable, and it'll effectively pause the current generator until the given one has been exhausted.  It also takes care of passing values back _into_ the generator using `.send()` or `.throw()`.

```python
def foo():
    a = yield 1
    b = yield from bar(a)
    print("foo got back", b)
    yield 4

def bar(a):
    print("in bar", a)
    x = yield 2
    y = yield 3
    print("leaving bar")
    return x + y

gen = foo()
val = None
while True:
    try:
        newval = gen.send(val)
    except StopIteration:
        break
    print("yielded", newval)
    val = newval * 10

# yielded 1
# in bar 10
# yielded 2
# yielded 3
# leaving bar
# foo got back 50
# yielded 4
```

Oh yes, and you can now `return` a value from a generator.  The return value becomes the result of a `yield from`, or if the caller isn't using `yield from`, it's available as the argument to the `StopIteration` exception.

A small convenience, perhaps.  The real power here isn't in the use of generators as lazy iterators, but in the use of generators as _coroutines_.

A coroutine is a function that can "suspend" itself, like `yield` does, allowing other code to run until the function is resumed.  It's _kind of_ like an alternative to threading, but only one function is actively running at any given time, and that function has to delierately relinquish control (or end) before anything else can run.

Generators could do this already, more or less, but only one stack frame deep.  That is, you can `yield` from a generator to suspend it, but if the generator calls another function, that other function has no way to suspend the generator.  This is still useful, but significantly less powerful than the coroutine functionality in e.g. Lua, which lets any function yield anywhere in the call stack.

With `yield from`, you can create a whole chain of generators that `yield from` one another, and as soon as the one on the _bottom_ does a regular `yield`, the _entire chain_ will be suspended.

This laid the groundwork for making the `asyncio` module possible.  I'll get to that later.

Refs: [docs](https://docs.python.org/3/reference/expressions.html#yieldexpr); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#pep-380); [PEP 380](https://www.python.org/dev/peps/pep-0380)


## Syntactic sugar

### Keyword-only arguments

Python 3.0 introduces "keyword-only" arguments, which _must_ be given by name.  As a corollary, you can now accept a list of args _and_ have more arguments afterwards.  The full syntax now looks something like this:

```python
def foo(a, b=None, *args, c=None, d, **kwargs):
    ...
```

Here, `a` and `d` are required, `b` and `c` are optional.  `c` and `d` _must_ be given by name.

```python
foo(1)                      # TypeError: missing d
foo(1, 2)                   # TypeError: missing d
foo(d=4)                    # TypeError: missing a
foo(1, d=4)                 # a = 1, d = 4
foo(1, 2, d=4)              # a = 1, b = 2, d = 4
foo(1, 2, 3, d=4)           # a = 1, b = 2, args = (3,), d = 4
foo(1, 2, c=3, d=4)         # a = 1, b = 2, c = 3, d = 4
foo(1, b=2, c=3, d=4, e=5)  # a = 1, b = 2, c = 3, d = f, kwargs = {'e': 5}
```

This is extremely useful for functions with a lot of arguments, functions with _boolean_ arguments, functions that accept `*args` (or may do so in the future) but also want some options, etc.  I use it a lot!

If you want keyword-only arguments, but you don't want to accept `*args`, you just leave off the variable name:

```python
def foo(*, arg=None):
    ...
```

Refs: [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#new-syntax); [PEP 3102](https://www.python.org/dev/peps/pep-3102)


### Format strings

Python 3.6 (not yet out) will finally bring us string interpolation, more or less, using the `str.format()` syntax:

```python
a = 0x133
b = 0x352
print(f"The answer is {a + b:04x}.")
```

It's pretty much the same as `str.format()`, except that instead of a position or name, you can give an entire expression.  The formatting suffixes with `:` still work, the special built-in conversions like `!r` still work, and `__format__` is still invoked.

Refs: [docs](https://docs.python.org/3.6/reference/lexical_analysis.html#f-strings); [Python 3.6 release notes](https://docs.python.org/3.6/whatsnew/3.6.html#pep-498-formatted-string-literals); [PEP 498](https://www.python.org/dev/peps/pep-0498)


### `async` and friends

Right, so, about coroutines.

Python 3.4 introduced [the `asyncio` module](https://docs.python.org/3/library/asyncio.html), which offers building blocks for asynchronous I/O (and bringing together the myriad third-party modules that do it already).

The design is based around coroutines, which are really generators using `yield from`.  The idea, as I mentioned above, is that you can create a stack of generators that all suspend at once:

```python
@coroutine
def foo():
    # do some stuff
    yield from bar()
    # do more stuff

@coroutine
def bar():
    # do some stuff
    response = yield from get_url("https://eev.ee/")
    # do more stuff
```

When this code calls `get_url()` (not actually a real function, but see [`aiohttp`](https://pypi.python.org/pypi/aiohttp)), `get_url` will send a request off into the æther, _and then `yield`_.  The entire stack of generators — `get_url`, `bar`, and `foo` — will all suspend, and control will return to whatever first called `foo`, which with `asyncio` will be an "event loop".  

The event loop's entire job is to notice that `get_url` yielded some kind of "I'm doing a network request" thing, remember it, and resume other coroutines in the meantime.  (Or just twiddle its thumbs, if there's nothing else to do.)  When a response comes back, the event loop will resume `get_url` and send it the response.  `get_url` will do some stuff and return it up to `bar`, who continues on, none the wiser that anything unusual happened.

The magic of this is that you can call `get_url` several times, and instead of having to wait for each request to completely finish before the next one can even start, you can do other work while you're waiting.  No threads necessary; this is all one thread, with functions cooperatively yielding control when they're waiting on some external thing to happen.

Now, notice that you do have to use `yield from` each time you call another coroutine.  This is nice in some ways, since it lets you see exactly when and where your function might be suspended out from under you, which can be important in some situations.  There are also arguments about why this is bad, and I don't care about them.

However, `yield from` is a _really weird_ phrase to be sprinkling all over network-related code.  It's meant for use with iterables, right?  Lists and tuples and things.  `get_url` is only _one thing_.  What are we yielding from it?  Also, what's this `@coroutine` decorator that doesn't actually do anything?

Python 3.5 smoothed over this nonsense by introducing explicit syntax for these constructs, using new `async` and `await` keywords:

```python
async def foo():
    # do some stuff
    await bar()
    # do more stuff

async def bar():
    # do some stuff
    response = await get_url("https://eev.ee/")
    # do more stuff
```

`async def` clearly identifies a coroutine, even one that returns immediately.  (Before, you'd have a generator with no `yield`, which isn't actually a generator, which causes some problems.)  `await` explains what's actually happening: you're just waiting for another function to be done.

`async for` and `async with` are also available, replacing some particularly clumsy syntax you'd need to use before.  And, handily, you can only use any of these things within an `async def`.

The new syntax comes with corresponding new special methods like `__await__`, whereas the previous approach required doing weird things with `__iter__`, which is what `yield from` ultimately calls.

I could fill a whole post or three with stuff about `asyncio`, and can't possibly give it justice in just a few paragraphs.  The short version is: there's built-in syntax for doing network stuff in parallel without threads, and that's cool.

Refs for `asyncio`: [docs](https://docs.python.org/3/library/asyncio.html) (`asyncio`); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#asyncio); [PEP 3156](https://www.python.org/dev/peps/pep-3156)

Refs for `async` and `await`: [docs](https://docs.python.org/3/reference/expressions.html#await) (`await`); [docs](https://docs.python.org/3/reference/compound_stmts.html#coroutines) (`async`); [docs](https://docs.python.org/3/reference/datamodel.html#coroutines) (special methods); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#pep-492-coroutines-with-async-and-await-syntax); [PEP 492](https://www.python.org/dev/peps/pep-0492)


### Function annotations

Function arguments and return values can have annotations:

```python
def foo(a: "hey", b: "what's up") -> "whoa":
    ...
```

The annotations are accessible via the function's `__annotations__` attribute.  They have no special meaning to Python, so you're free to experiment with them.

Well...

You _were_ free to experiment with them, but the addition of the `typing` module ([mentioned below](#typing)) has hijacked them for type hints.  There's no clear way to attach a type hint _and_ some other value to the same argument, so you'll have a tough time making function annotations part of your API.

There's still no hard requirement that annotations be used exclusively for type hints (and it's not like Python does anything with type hints, either), but the original PEP suggests it would like that to be the case someday.  I guess we'll see.

If you want to see annotations preserved for other uses as well, it would be a really good idea to do some creative and interesting things with them as soon as possible.  Just saying.

Refs: [docs](https://docs.python.org/3/reference/compound_stmts.html#function-definitions); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#new-syntax); [PEP 3107](https://www.python.org/dev/peps/pep-3107)


### Matrix multiplication

Python 3.5 learned a new infix operator for matrix multiplication, spelled `@`.  It doesn't do anything for any built-in types, but it's supported in NumPy.  You can implement it yourself with the `__matmul__` special method and its `r` and `i` variants.

Shh.  Don't tell anyone, but I suspect there are fairly interesting things you could do with an operator called `@` — some of which have nothing to do with matrix multiplication at all!

Refs: [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#pep-465-a-dedicated-infix-operator-for-matrix-multiplication); [PEP 465](https://www.python.org/dev/peps/pep-0465)

### Ellipsis

`...` is now valid syntax everywhere.  It evaluates to the `Ellipsis` singleton, which does nothing.  (This exists in Python 2, too, but it's only allowed when slicing.)

It's not of much _practical_ use, but you can use it to indicate an unfinished stub, in a way that's clearly not intended to be final but will still parse and run:

```python
class ReallyComplexFiddlyThing:
    # fuck it, do this later
    ...
```

Refs: [docs](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#changed-syntax)


## Enhanced exceptions

A slightly annoying property of Python 2's exception handling is that if you want to do your own error logging, or otherwise need to get at the traceback, you have to use the slightly funky `sys.exc_info()` API and carry the traceback around separately.  As of Python 3.0, exceptions automatically have a `__traceback__` attribute, as well as a `.with_traceback()` method that sets the traceback and returns the exception itself (so you can use it inline).

This makes some APIs a little silly — `__exit__` still accepts the exception type _and_ value _and_ traceback, even though all three are readily available from just the exception object itself.

A much more annoying property of Python 2's exception handling was that custom exception handling would lose track of where the problem actually occurred.  Consider the following call stack.

    :::text
    A
    B
    C
    D
    E

Now say an exception happens in `E`, and it's caught by code like this in `C`.

    :::python
    try:
        D()
    except Exception as e:
        raise CustomError("Failed to call D")

Because this creates and raises a new exception, the traceback will _start_ from this point and not even mention `E`.  The best workaround for this involves manually creating a traceback between `C` and `E`, formatting it as a string, and then _including that_ in the error message.  Preposterous.

Python 3.0 introduced _exception chaining_, which allows you to do this:

    :::python
    raise CustomError("Failed to call D") from e

Now, if this exception reaches the top level, Python will format it as:

    :::pytb
    Traceback (most recent call last):
    File C, blah blah
    File D, blah blah
    File E, blah blah
    SomeError

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
    File A, blah blah
    File B, blah blah
    File C, blah blah
    CustomError: Failed to call D

The best part is that you don't need to explicitly say `from e` at all — if you do a plain `raise` while there's already an active exception, Python will automatically chain them together.  Even internal Python exceptions will have this behavior, so a broken exception handler won't lose the original exception.  (In the implicit case, the intermediate text becomes "During handling of the above exception, another exception occurred:".)

The chained exception is stored on the new exception as either `__cause__` (if from an explicit `raise ... from`) or `__context__` (if automatic).

If you direly need to hide the original exception, Python 3.3 introduced `raise ... from None`.

Speaking of exceptions, the error messages for missing arguments have been improved.  Python 2 does this:

    :::pytb
    TypeError: foo() takes exactly 1 argument (0 given)

Python 3 does this:

    :::pytb
    TypeError: foo() missing 1 required positional argument: 'a'

Refs:

* Exception chaining and `__traceback__`: [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#changes-to-exceptions); [PEP 3134](https://www.python.org/dev/peps/pep-3134)
* `raise ... from None`: [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#pep-409-suppressing-exception-context); [PEP 409](https://www.python.org/dev/peps/pep-0409)


## Cooler classes

### `super()` with no arguments

You can call `super()` with no arguments.  It Just Works.  Hallelujah.

Also, you can call `super()` with no arguments.  That's so great that I could probably just fill the rest of this article with it and be satisfied.

Did I mention you can call `super()` with no arguments?

Refs: [docs](https://docs.python.org/3/library/functions.html#super); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#builtins); [PEP 3135](https://www.python.org/dev/peps/pep-3135/)

### New metaclass syntax and kwargs for classes

Compared to that, everything else in this section is going to sound really weird and obscure.

For example, `__metaclass__` is gone.  It's now a keyword-only argument to the `class` statement.

```python
class Foo(metaclass=FooMeta):
    ...
```

That doesn't sound like much, right?  Just some needless syntax change that makes porting harder, right??  Right???  Haha nope watch this because it's amazing but it barely gets any mention at all.

```python
class Foo(metaclass=FooMeta, a=1, b=2, c=3):
    ...
```

You can include _arbitrary keyword arguments_ in the `class` statement, and they will be passed along to the metaclass call as keyword arguments.  (You have to catch them in both `__new__` and `__init__`, since they always get the same arguments.)  (Also, the `class` statement now has the general syntax of a function call, so you can put `*args` and `**kwargs` in it.)

This is pretty slick.  Consider SQLAlchemy, which uses a metaclass to let you declare a table with a class.

```python
class SomeTable(TableBase):
    __tablename__ = 'some_table'
    id = Column()
    ...
```

Note that SQLAlchemy has you put the name of the table in the clumsy `__tablename__` attribute, which it invented.  Why not just `name`?  Well, because then you couldn't declare a column called `name`!  Any "declarative" metaclass will have the same problem of separating the actual class contents from configuration.  Keyword arguments offer an easy way out.

```python
# only hypothetical, alas
class SomeTable(TableBase, name='some_table'):
    id = Column()
    ...
```

Refs: [docs](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#changed-syntax); [PEP 3115](https://www.python.org/dev/peps/pep-3115/)

### `__prepare__`

Another new metaclass feature is the introduction of the `__prepare__` method.

You may have noticed that the body of a class is just a regular block, which can contain whatever code you want.  Before decorators were a thing, you'd actually declare class methods in two stages:

```python
class Foo:
    def do_the_thing(cls):
        ...
    do_the_thing = classmethod(do_the_thing)
```

That's not magical class-only syntax; that's just regular code assigning to a variable.  You can put `if`s and `for`s and `while`s and `del`s inside a class body, too; you just don't see it very often because there aren't very many useful reasons to do it.

A class body is a kind of weird pseudo-scope.  It can create locals, and it can read values from outer scopes, but methods don't see the class body as an outer scope.  Once the class body reaches its end, any remaining locals are passed to the `type` constructor and become the new class's attributes.  (This is why, for example, you can't refer to a class directly within its own body — the class doesn't and can't exist until _after_ the body has executed.)

All of this is to say: `__prepare__` is a new hook that returns the dict the class body's locals go into.

Maybe that doesn't sound particularly interesting, but consider: the value you return doesn't have to be an actual `dict`.  It can be anything that understands `__setitem__`.  You could, say, use an `OrderedDict`, and keep track of the order your attributes were declared.  That's useful for declarative metaclasses, where the order of attributes may be important (consider a C struct).

But you can go further.  You might allow more than one attribute of the same name.  You might do something special with the attributes _as soon as they're assigned_, rather than at the end of the body.  You might predeclare some attributes.  `__prepare__` is passed the class's kwargs, so you might alter the behavior based on those.

For a nice practical example, consider the new [`enum` module](https://docs.python.org/3/library/enum.html), which I briefly mention later on.  One drawback of this module is that you have to specify a value for every variant, since variants are defined as class attributes, which must have a value.  There's an [example of automatic numbering](https://docs.python.org/3/library/enum.html#autonumber), but it still requires assigning a dummy value like `()`.  Clever use of `__prepare__` would allow lifting this restriction:

```python
# XXX: Should prefer MutableMapping here, but the ultimate call to type()
# raises a TypeError if you pass a namespace object that doesn't inherit
# from dict!  Boo.
class EnumLocals(dict):
    def __init__(self):
        self.nextval = 1

    def __getitem__(self, key):
        if key not in self and not key.startswith('_') and not key.endswith('_'):
            self[key] = self.nextval
            self.nextval += 1
        return super().__getitem__(key)

class EnumMeta(type):
    @classmethod
    def __prepare__(meta, name, bases):
        return EnumLocals()

class Colors(metaclass=EnumMeta):
    red
    green
    blue

print(Colors.red, Colors.green, Colors.blue)
# 1 2 3
```

Deciding whether this is a good idea is left as an exercise.

This is an exceptionally obscure feature that gets very little attention — it's not even mentioned explicitly in the 3.0 release notes — but there's nothing else like it in the language.  Between `__prepare__` and keyword arguments, the `class` statement has transformed into a much more powerful and general tool for creating all kinds of objects.  I almost wish it weren't still called `class`.

Refs: [docs](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#changed-syntax); [PEP 3115](https://www.python.org/dev/peps/pep-3115/)

### Attribute definition order

If that's still too much work, don't worry: a proposal was just accepted for Python 3.6 that makes this even easier.  Now every class will have a `__definition_order__` attribute, a tuple listing the names of all the attributes assigned within the class body, in order.  (To make this possible, the default return value of `__prepare__` will become an `OrderedDict`, but the `__dict__` attribute will remain a regular dict.)

Now you don't have to do anything at all: you can always check to see what order any class's attributes were defined in.

----

Additionally, descriptors can now implement a `__set_name__` method.  When a class is created, any descriptor implementing the method will have it called with the containing class and the name of the descriptor.

I'm very excited about this, but let me try to back up.  A descriptor is a special Python object that can be used to customize how a particular class attribute works.  The built-in `property` decorator is a descriptor.

```python
class MyClass:
    foo = SomeDescriptor()

c = MyClass()
c.foo = 5  # calls SomeDescriptor.__set__!
print(c.foo)  # calls SomeDescriptor.__get__!
```

This is super cool and can be used for all sorts of DSL-like shenanigans.

Now, most descriptors ultimately want to store a value _somewhere_, and the obvious place to do that is in the object's `__dict__`.  Above, `SomeDescriptor` might want to store its value in `c.__dict__['foo']`, which is fine since Python will still consult the descriptor first.  If that weren't fine, it could also use the key `'_foo'`, or whatever.  It probably wants to use its own name _somehow_, because otherwise...  what would happen if you had two `SomeDescriptor`s in the same class?

Therein lies the problem, and one of my long-running and extremely minor frustrations with Python.  Descriptors have no way to know their own name!  There are only really two solutions to this:

1. Require the user to pass the name in as an argument, too: `foo = SomeDescriptor('foo')`.  Blech!

2. _Also_ have a metaclass (or decorator, or whatever), which can iterate over all the class's attributes, look for `SomeDescriptor` objects, and tell them what their names are.  Needing a metaclass means you can't make general-purpose descriptors meant for use in arbitrary classes; a decorator would work, but boy is that clumsy.

Both of these suck and really detract from what could otherwise be very neat-looking syntax trickery.

But now!  Now, when `MyClass` is created, Python will have a look through its attributes.  If it sees that the `foo` object has a `__set_name__` method, it'll call that method automatically, passing it both the owning class _and_ the name `'foo'`!  Huzzah!

This is so great I am so happy you have no idea.

----

Lastly, there's now an `__init_subclass__` class method, which is called when the class is _subclassed_.  A great many metaclasses exist just to do a little bit of work for each new subclass; now, you don't need a metaclass at all in many simple cases.  You want a plugin registry?  _No problem:_

```python
class Plugin:
    _known_plugins = {}

    def __init_subclass__(cls, *, name, **kwargs):
        cls._known_plugins[name] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def get_plugin(cls, name):
        return cls._known_plugins[name]

    # ...probably some interface stuff...

class FooPlugin(Plugin, name="foo"):
    ...
```

No metaclass needed at all.

Again, none of this stuff is available _yet_, but it's all slated for Python 3.6, [due out in mid-December](https://www.python.org/dev/peps/pep-0494/).  I am super pumped.

Refs: [docs](https://docs.python.org/3.6/reference/datamodel.html#class-customization) (customizing class creation); [docs](https://docs.python.org/3.6/reference/datamodel.html#descriptors) (descriptors); [Python 3.6 release notes](https://docs.python.org/3.6/whatsnew/3.6.html#pep-487-simpler-customization-of-class-creation); [PEP 520](https://www.python.org/dev/peps/pep-0520/) (attribute definition order); [PEP 487](https://www.python.org/dev/peps/pep-0487/) (`__init_subclass__` and `__set_name__`)


## Math stuff

`int` and `long` have been merged, and there is no longer any useful distinction between small and very large integers.  I've actually run into code that breaks if you give it `1` instead of `1L`, so, good riddance.  ([Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#integers); [PEP 237](https://www.python.org/dev/peps/pep-0237))

The `/` operator always does "true" division, i.e., gives you a float.  If you want floor division, use `//`.  Accordingly, the `__div__` magic method is gone; it's split into two parts, `__truediv__` and `__floordiv__`.  ([Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#integers); [PEP 238](https://www.python.org/dev/peps/pep-0238))

`decimal.Decimal`, `fractions.Fraction`, and `float`s now interoperate a little more nicely: numbers of different types hash to the same value; all three types can be compared with one another; and most notably, the `Decimal` and `Fraction` constructors can accept floats directly.  ([docs](https://docs.python.org/3/library/decimal.html) (`decimal`); [docs](https://docs.python.org/3/library/fractions.html) (`fractions`); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#decimal-and-fractions))

`math.gcd` returns the greatest common divisor of two integers.  This existed before, but was in the `fractions` module, where nobody knew about it.  ([docs](https://docs.python.org/3/library/math.html#math.gcd); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#math))

`math.inf` is the floating-point infinity value.  Previously, this was only available by writing `float('inf')`.  There's also a `math.nan`, but let's not?  ([docs](https://docs.python.org/3/library/math.html#math.inf); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#math))

`math.isclose` (and the corresponding complex version, `cmath.isclose`) determines whether two values are "close enough".  Intended to do the right thing when comparing floats.  ([docs](https://docs.python.org/3/library/math.html#math.isclose); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#pep-485-a-function-for-testing-approximate-equality); [PEP 485](https://www.python.org/dev/peps/pep-0485))


## More modules

The standard library has seen quite a few improvements.  In fact, Python 3.2 was developed with an explicit [syntax freeze](https://www.python.org/dev/peps/pep-3003/), so it consists almost entirely of standard library enhancements.  There are far more changes across six and a half versions than I can possibly list here; these are the ones that stood out to me.

### The module shuffle

Python 2, rather inexplicably, had a number of top-level modules that were named after the single class they contained, CamelCase and all.  `StringIO` and `SimpleHTTPServer` are two obvious examples.  In Python 3, the `StringIO` class lives in `io` (along with `BytesIO`), and `SimpleHTTPServer` has been renamed to `http.server`.  If you're anything like me, you'll find this deeply satisfying.

Wait, wait, there's a practical upside here.  Python 2 had several pairs of modules that did the same thing with the same API, but one was pure Python and one was much faster C: `pickle`/`cPickle`, `profile`/`cProfile`, and `StringIO`/`cStringIO`.  I've seen code (cough, older versions of Babel, cough) that spent a considerable amount of its startup time reading pickles with the pure Python version, because it did the obvious thing and used the `pickle` module.  Now, these pairs have been merged: importing `pickle` gives you the faster C implementation, importing `profile` gives you the faster C implementation, and `BytesIO`/`StringIO` are the fast C implementations in the `io` module.

Refs: [docs](https://docs.python.org/3/library/) (sort of); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#library-changes); [PEP 3108](https://www.python.org/dev/peps/pep-3108/) (exhaustive list of removed and renamed modules)

### Additions to existing modules

A number of file format modules, like [`bz2`](https://docs.python.org/3/library/bz2.html) and [`gzip`](https://docs.python.org/3/library/gzip.html), went through some cleanup and modernization in 3.2 through 3.4: some learned a more straightforward `open` function, some gained better support for the bytes/text split, and several learned to use their file types as context managers (i.e., with `with`).

`collections.ChainMap` is a mapping type that consults some number of underlying mappings in order, allowing for a "dict with defaults" without having to merge them together.  ([docs](https://docs.python.org/3/library/collections.html#collections.ChainMap); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#collections))

`configparser` dropped its ridiculous distinction between `ConfigParser` and `SafeConfigParser`; there is now only `ConfigParser`, which is safe.  The parsed data now preserves order by default and can be read or written using normal mapping syntax.  Also there's a fancier alternative interpolation parser.  ([docs](https://docs.python.org/3/library/configparser.html#configparser.ConfigParser); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#configparser))

`contextlib.ContextDecorator` is some sort of devilry that allows writing a context manager which can also be used as a decorator.  It's used to implement the `@contextmanager` decorator, so those can be used as decorators as well.  ([docs](https://docs.python.org/3/library/contextlib.html#contextlib.ContextDecorator); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#contextlib))

`contextlib.ExitStack` offers cleaner and more fine-grained handling of multiple context managers, as well as resources that don't have their own context manager support.  ([docs](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#contextlib))

`contextlib.suppress` is a context manager that quietly swallows a given type of exception.  ([docs](https://docs.python.org/3/library/contextlib.html#contextlib.suppress); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#contextlib))

`contextlib.redirect_stdout` is a context manager that replaces `sys.stdout` for the duration of a block.  ([docs](https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#contextlib))

`datetime.timedelta` already existed, of course, but now it supports being multiplied and divided by numbers or divided by other `timedelta`s.  The upshot of this is that `timedelta` finally, _finally_ has a `.total_seconds()` method which does exactly what it says on the tin.  ([docs](https://docs.python.org/3/library/datetime.html#datetime.timedelta); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#datetime-and-time))

`datetime.timezone` is a new concrete type that can represent fixed offsets from UTC.  There has long been a `datetime.tzinfo`, but it was a useless interface, and you were left to write your own actual class yourself.  `datetime.timezone.utc` is a pre-existing instance that represents UTC, an offset of zero.  ([docs](https://docs.python.org/3/library/datetime.html#datetime.timezone); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#datetime-and-time))



`functools.lru_cache` is a decorator that caches the results of a function, keyed on the arguments.  It also offers cache usage statistics and a method for emptying the cache.  ([docs](https://docs.python.org/3/library/functools.html#functools.lru_cache); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#functools))

`functools.partialmethod` is like `functools.partial`, but the resulting object can be used as a descriptor (read: method).  ([docs](https://docs.python.org/3/library/functools.html#functools.partialmethod); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#functools))

`functools.singledispatch` allows function overloading, based on the type of the first argument.  ([docs](https://docs.python.org/3/library/functools.html#functools.singledispatch); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#functools); [PEP 443](https://www.python.org/dev/peps/pep-0443))

`functools.total_ordering` is a class decorator that allows you to define only `__eq__` and `__lt__` (or any other) and defines the other comparison methods in terms of them.  Note that since Python 3.0, `__ne__` is automatically the inverse of `__eq__` and doesn't need defining.  Note also that `total_ordering` doesn't correctly support `NotImplemented` until Python 3.4.  For an even easier way to do this, consider my [`classtools.keyed_ordering`](http://classtools.readthedocs.io/en/latest/#classtools.keyed_ordering) decorator.  ([docs](https://docs.python.org/3/library/functools.html#functools.total_ordering); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#functools))

`inspect.getattr_static` fetches an attribute like `getattr` but avoids triggering dynamic lookup like `@property`.  ([docs](https://docs.python.org/3/library/inspect.html#inspect.getattr_static); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#inspect))

`inspect.signature` fetches the signature of a function as the new and more featureful `Signature` object.  It also knows to follow the `__wrapped__` attribute set by `functools.wraps` since Python 3.2, so it can see through well-behaved wrapper functions to the "original" signature.  ([docs](https://docs.python.org/3/library/inspect.html#inspect.signature); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#pep-362-function-signature-object); [PEP 362](https://www.python.org/dev/peps/pep-0362))

The `logging` module can use `str.format`-style string formatting in log formats by passing `style='{'` to `Formatter`.  Alas, this is only for assembling the final output; log messages themselves must still use `%` style.  ([docs](https://docs.python.org/3/library/logging.html#logging.Formatter); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#logging))

The `logging` module spits warnings and higher to `stderr` if logging hasn't been otherwise configured.  This means that if your app doesn't use `logging`, but it uses a library that _does_, you'll get actual output rather than the completely useless "No handlers could be found for logger 'foo'".  ([docs](https://docs.python.org/3/library/logging.html#logging.lastResort); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#logging))

`os.scandir` lists the contents of a directory while avoiding `stat` calls as much as possible, making it significantly faster.  ([docs](https://docs.python.org/3/library/os.html#os.scandir); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#pep-471-os-scandir-function-a-better-and-faster-directory-iterator); [PEP 471](https://www.python.org/dev/peps/pep-0471))

`re.fullmatch` checks for a match against the entire input string, not just a substring.  ([docs](https://docs.python.org/3/library/re.html#re.fullmatch); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#re))

`reprlib.recursive_repr` is a decorator for `__repr__` implementations that can detect recursive calls to the same object and replace them with `...`, just like the built-in structures.  Believe it or not, `reprlib` is an existing module, though in Python 2 it was called `repr`.  ([docs](https://docs.python.org/3/library/reprlib.html#reprlib.recursive_repr); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#reprlib))

`shutil.disk_usage` returns disk space statistics for a given path with no fuss.  ([docs](https://docs.python.org/3/library/shutil.html#shutil.disk_usage); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#shutil))

`shutil.get_terminal_size` tries very hard to detect the size of the terminal window.  ([docs](https://docs.python.org/3/library/shutil.html#shutil.get_terminal_size); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#shutil))

`subprocess.run` is a new streamlined function that consolidates several other helpers in the `subprocess` module.  It returns an object that describes the final state of the process, and it accepts arguments for a timeout, requiring that the process return success, and passing data as stdin.  This is now the recommended way to run a single subprocess.  ([docs](https://docs.python.org/3/library/subprocess.html#subprocess.run); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#subprocess))

`tempfile.TemporaryDirectory` is a context manager that creates a temporary directory, then destroys it and its contents at the end of the block.  ([docs](https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#tempfile))

`textwrap.indent` can add an arbitrary prefix to every line in a string.  ([docs](https://docs.python.org/3/whatsnew/3.3.html#textwrap); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#textwrap))

`time.monotonic` returns the value of a monotonic clock — i.e., it will never go backwards.  You should use this for measuring time durations within your program; using `time.time()` will produce garbage results if the system clock changes due to DST, a leap second, NTP, manual intervention, etc.  ([docs](https://docs.python.org/3/library/time.html#time.monotonic); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#time); [PEP 418](https://www.python.org/dev/peps/pep-0418/))

`time.perf_counter` returns the value of the highest-resolution clock available, but is only suitable for measuring a short duration.  ([docs](https://docs.python.org/3/library/time.html#time.perf_counter); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#time); [PEP 418](https://www.python.org/dev/peps/pep-0418/))

`time.process_time` returns the total system and user CPU time for the process, excluding sleep.  Note that the starting time is undefined, so only durations are meaningful.  ([docs](https://docs.python.org/3/library/time.html#time.process_time); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#time); [PEP 418](https://www.python.org/dev/peps/pep-0418/))

`traceback.walk_stack` and `traceback.walk_tb` are small helper functions that walk back along a stack or traceback, so you can use simple iteration rather than the slightly clumsier linked-list approach.  ([docs](https://docs.python.org/3/library/traceback.html#traceback.walk_stack); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#traceback))

`types.MappingProxyType` offers a read-only proxy to a dict.  Since it holds a reference to the dict in C, you can return `MappingProxyType(some_dict)` to effectively create a read-only dict, as the original dict will be inaccessible from Python code.  This is the same type used for the `__dict__` of an immutable object.  Note that this has existed in various forms for a while, but wasn't publicly exposed or documented; see my module [`dictproxyhack`](https://pypi.python.org/pypi/dictproxyhack) for something that does its best to work on every Python version.  ([docs](https://docs.python.org/3/library/types.html#types.MappingProxyType); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#types))

`types.SimpleNamespace` is a blank type for sticking arbitrary unstructed attributes to.  Previously, you would have to make a dummy subclass of `object` to do this.  ([docs](https://docs.python.org/3/library/types.html#types.SimpleNamespace); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#simplenamespace))

`weakref.finalize` allows you to add a finalizer function to an arbitrary (weakrefable) object from the "outside", without needing to add a `__del__`.  The `finalize` object will keep itself alive, so there's no need to hold onto it.  ([docs](https://docs.python.org/3/library/weakref.html#weakref.finalize); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#weakref))

### New modules with backports

These are less exciting, since they have backports on PyPI that work in Python 2 just as well.  But they came from Python 3 development, so I credit Python 3 for them, just like I credit NASA for inventing the microwave.

`asyncio` is covered above, but it's been backported as [`trollius`](https://pypi.python.org/pypi/trollius) for 2.6+, with the caveat that Pythons before 3.3 don't have `yield from` and you have to use `yield From(...)` as a workaround.  That caveat means that third-party `asyncio` libraries will almost certainly not work with `trollius`!  For this and other reasons, [the maintainer is no longer supporting it](http://trollius.readthedocs.io/deprecated.html).  Alas.  Guess you'll have to upgrade to Python 3, then.

`enum` finally provides an enumeration type, something which has long been desired in Python and solved in myriad ad-hoc ways.  The variants become instances of a class, can be compared by identity, can be converted between names and values (but only explicitly), can have custom methods, and can implement special methods as usual.  There's even an `IntEnum` base class whose values end up as subclasses of `int` (!), making them perfectly compatible with code expecting integer constants.  Enums have a surprising amount of power, far more than any approach I've seen before; I heartily recommend that you skim the examples in the documentation.  Backported as [`enum34`](https://pypi.python.org/pypi/enum34) for 2.4+.  ([docs](https://docs.python.org/3/library/enum.html); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#enum); [PEP 435](https://www.python.org/dev/peps/pep-0435))

`ipaddress` offers types for representing IPv4 and IPv6 addresses and subnets.  They can convert between several representations, perform a few set-like operations on subnets, identify special addresses, and so on.  Backported as [`ipaddress`](https://pypi.python.org/pypi/ipaddress) for 2.6+.  (There's also a [`py2-ipaddress`](https://pypi.python.org/pypi/py2-ipaddress), but its handling of bytestrings differs from Python 3's built-in module, which is likely to cause confusing compatibility problems.) ([docs](https://docs.python.org/3/library/ipaddress.html); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#ipaddress); [PEP 3144](https://www.python.org/dev/peps/pep-3144))

`pathlib` provides the `Path` type, representing a filesystem path that you can manipulate with methods rather than the mountain of functions in `os.path`.  It also overloads `/` so you can do `path / 'file.txt'`, which is kind of cool.  [PEP 519](https://www.python.org/dev/peps/pep-0519/) intends to further improve interoperability of `Path`s with classic functions for the not-yet-released Python 3.6.  Backported as [`pathlib2`](https://pypi.python.org/pypi/pathlib2/) for 2.6+; there's also a [`pathlib`](https://pypi.python.org/pypi/pathlib/), but it's no longer maintained, and I don't know what happened there.  ([docs](https://docs.python.org/3/library/pathlib.html); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#pathlib); [PEP 428](https://www.python.org/dev/peps/pep-0428))

`selectors` (created as part of the work on `asyncio`) attempts to wrap `select` in a high-level interface that doesn't make you want to claw your eyes out.  A noble pursuit.  Backported as [`selectors34`](https://pypi.python.org/pypi/selectors34) for 2.6+.  ([docs](https://docs.python.org/3/library/selectors.html); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#selectors))

`statistics` contains a number of high-precision statistical functions.  Backported as [`backports.statistics`](https://pypi.python.org/pypi/backports.statistics/0.1.0) for 2.6+.  ([docs](https://docs.python.org/3/library/statistics.html); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#statistics); [PEP 450](https://www.python.org/dev/peps/pep-0450))

`unittest.mock` provides multiple ways for creating dummy objects, temporarily (with a context manager or decorator) replacing an object or some of its attributes, and verifying that some sequence of operations was performed on a dummy object.  I'm not a huge fan of mocking so much that your tests end up mostly testing that your source code hasn't changed, but if you have to deal with external resources or global state, some light use of `unittest.mock` can be very handy — even if you aren't using the rest of `unittest`.  Backported as [`mock`](https://pypi.python.org/pypi/mock/) for 2.6+.  ([docs](https://docs.python.org/3/library/unittest.mock.html); Python 3.3, but no release notes)


### New modules without backports

Perhaps more exciting because they're Python 3 exclusive!  Perhaps less exciting because they're necessarily related to plumbing.

#### `faulthandler`

`faulthandler` is a debugging aid that can dump a Python traceback during a segfault or other fatal signal.  It can also be made to hook on an arbitrary signal, and can intervene even when Python code is deadlocked.  You can use the default behavior with no effort by passing `-X faulthandler` on the command line, by setting the `PYTHONFAULTHANDLER` environment variable, or by using the module API manually.

I think `-X` itself is new as of Python 3.2, though it's not mentioned in the release notes.  It's reserved for implementation-specific options; there are [a few others defined for CPython](https://docs.python.org/3/using/cmdline.html#cmdoption-X), and the options can be retrieved from Python code via [`sys._xoptions`](https://docs.python.org/3/library/sys.html#sys._xoptions).

Refs: [docs](https://docs.python.org/3/library/faulthandler.html); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#faulthandler)

#### `importlib`

`importlib` is the culmination of a whole lot of work, performed in multiple phases across numerous Python releases, to extend, formalize, and cleanly reimplement the entire import process.

I can't possibly describe everything the import system can do and what Python versions support what parts of it.  Suffice to say, it can do a lot of things: Python has built-in support for [importing from zip files](https://docs.python.org/3/library/zipimport.html), and I've seen third-party import hooks that allow transparently importing modules _written in another programming language_.

If you want to mess around with writing your own custom importer, `importlib` has a _ton_ of tools for helping you do that.  It's possible in Python 2, too, using the `imp` module, but that's a lot rougher around the edges.

If not, the main thing of interest is [the `import_module` function](https://docs.python.org/3/library/importlib.html#importlib.import_module), which imports a module by name without all the really weird semantics of `__import__`.  Seriously, don't use `__import__`.  It's so weird.  It probably doesn't do what you think.  `importlib.import_module` even exists in Python 2.7.

Refs: [docs](https://docs.python.org/3/library/importlib.html); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#using-importlib-as-the-implementation-of-import); [PEP 302](https://www.python.org/dev/peps/pep-0302/)?


#### `tracemalloc`

`tracemalloc` is another debugging aid which tracks Python's memory allocations.  It can also compare two snapshots, showing how much memory has been allocated or released between two points in time, and who was responsible.  If you have rampant memory use issues, this is probably more helpful than having Python check its own RSS.

_Technically_, `tracemalloc` can be used with Python 2.7...  but that involves patching and recompiling Python, so I hesitate to call it a backport.  Still, if you really need it, [give it a whirl](http://pytracemalloc.readthedocs.io/).

Refs: [docs](https://docs.python.org/3/library/tracemalloc.html); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#tracemalloc); [PEP 454](https://www.python.org/dev/peps/pep-0454)


#### `typing`

`typing` offers a standard way to declare _type hints_ — the expected types of arguments and return values.  Type hints are given using the function annotation syntax.

Python itself doesn't do anything with the annotations, though they're accessible and inspectable at runtime.  An external tool like [mypy](http://mypy-lang.org/) can perform static type checking ahead of time, using these standard types.  mypy is an existing project that predates `typing` (and works with Python 2), but the previous syntax relied on magic comments; `typing` formalizes the constructs and puts them in the standard library.

I haven't actually used either the type hints or mypy myself, so I can't comment on how helpful or intrusive they are.  Give them a shot if they sound useful to you.

Refs: [docs](https://docs.python.org/3/library/typing.html); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#whatsnew-pep-484); [PEP 484](https://www.python.org/dev/peps/pep-0484)


#### venv and ensurepip

I mean, yes, of course, virtualenv and pip are readily available in Python 2.  The whole point of these is that they are _bundled with_ Python, so you always have them at your fingertips and never have to worry about installing them yourself.

Installing Python should now give you `pipX` and `pipX.Y` commands automatically, corresponding to the latest stable release of pip when that Python version was first released.  You'll also get `pyvenv`, which is effectively just `virtualenv`.

There's also a module interface: `python -m ensurepip` will install pip (hopefully not necessary), `python -m pip` runs pip with a specific Python version (a feature of pip and not new to the bundling), and `python -m venv` runs the bundled copy of virtualenv with a specific Python version.

There was a time where these were completely broken on Debian, because Debian strongly opposes vendoring (the rationale being that it's easiest to push out updates if there's only _one copy_ of a library in the Debian package repository), so they just deleted `ensurepip` and `venv`?  Which completely defeated the point of having them in the first place?  I think this has been fixed by now, but it might still bite you if you're on the Ubuntu 14.04 LTS.

Refs: [`ensurepip` docs](https://docs.python.org/3/library/ensurepip.html); [`pyvenv` docs](https://docs.python.org/3/using/scripts.html#scripts-pyvenv); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#whatsnew-pep-453); [PEP 453](https://www.python.org/dev/peps/pep-0453)


#### `zipapp`

`zipapp` makes it easy to create executable zip applications, which have been a thing since 2.6 but have languished in obscurity.  Well, no longer.

This wasn't particularly difficult before: you just zip up some code, make sure there's a `__main__.py` in the root, and pass it to Python.  Optionally, you can set it executable and add a shebang line, since the ZIP format ignores any leading junk in the file.  That's basically all `zipapp` does.  (It does _not_ magically infer your dependencies and bundle them as well; you're on your own there.)

I can't find a backport, which is a little odd, since I don't think this module does anything too special.

Refs: [docs](https://docs.python.org/3/library/zipapp.html); [Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#zipapp); [PEP 441](https://www.python.org/dev/peps/pep-0441)


## Miscellaneous nice enhancements

There were a lot of improvements to language semantics that don't fit anywhere else above, but make me a little happier.

The interactive interpreter does tab-completion by default.  I say "by default" because I've been told that it was supported before, but you had to do some kind of goat blood sacrifice to get it to work.  Also, command history persists between runs.  ([docs](https://docs.python.org/3/library/site.html#rlcompleter-config); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#other-improvements))

The `-b` command-line option produces a warning when calling `str()` on a `bytes` or `bytearray`, or when comparing text to bytes.  `-bb` produces an error.  ([docs](https://docs.python.org/3/using/cmdline.html#cmdoption-b))

The `-I` command-like option runs Python in "isolated mode": it ignores all `PYTHON*` environment variables and leaves the current directory and user `site-packages` directories off of `sys.path`.  The idea is to use this when running a system script (or in the shebang line of a system script) to insulate it from any weird user-specific stuff.  ([docs](https://docs.python.org/3/using/cmdline.html#cmdoption-I); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#other-improvements))

Functions and classes learned a `__qualname__` attribute, which is a dotted name describing (lexically) where they were defined.  For example, a method's `__name__` might be `foo`, but its `__qualname__` would be something like `SomeClass.foo`.  Similarly, a class or function defined within another function will list that containing function in its `__qualname__`.  ([docs](https://docs.python.org/3/library/stdtypes.html#definition.__qualname__); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#pep-3155-qualified-name-for-classes-and-functions); [PEP 3155](https://www.python.org/dev/peps/pep-3155))

Generators signal their end by raising `StopIteration` internally, but it was also possible to raise `StopIteration` directly within a generator — most notably, when calling `next()` on an exhausted iterator.  This would cause the generator to end prematurely and silently.  Now, raising `StopIteration` inside a generator will produce a warning, which will become a `RuntimeError` in Python 3.7.  You can opt into the fatal behavior early with `from __future__ import generator_stop`.  ([Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#whatsnew-pep-479); [PEP 479](https://www.python.org/dev/peps/pep-0479))

Implicit namespace packages allow a package to span multiple directories.  The most common example is a plugin system, `foo.plugins.*`, where plugins may come from multiple libraries, but all want to share the `foo.plugins` namespace.  Previously, they would collide, and some `sys.path` tricks were necessary to make it work; now, support is built in.  (This feature also allows you to have a regular package without an `__init__.py`, but I'd strongly recommend still having one.)  ([Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#pep-420-implicit-namespace-packages); [PEP 420](https://www.python.org/dev/peps/pep-0420))

Object finalization behaves in less quirky ways when destroying an isolated reference cycle.  Also, modules no longer have their contents changed to `None` during shutdown, which fixes a long-running type of error when a `__del__` method tries to call, say, `os.path.join()` — if you were unlucky, `os.path` would have already have had its contents replaced with `None`s, and you'd get an extremely confusing `TypeError` from trying to call a standard library function.  ([Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#pep-442-safe-object-finalization); [PEP 442](https://www.python.org/dev/peps/pep-0442))

`str.format_map` is like `str.format`, but it accepts a mapping object directly (instead of having to flatten it with `**kwargs`).  This allows some fancy things that weren't previously possible, like passing a fake map that creates values on the fly based on the keys looked up in it.  ([docs](https://docs.python.org/3/library/stdtypes.html#str.format_map); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#other-language-changes))

When a blocking system call is interrupted by a signal, it returns `EINTR`, indicating that the calling code should try the same system call again.  In Python, this becomes `OSError` or `InterruptedError`.  I have never in my life seen any C or Python code that actually deals with this correctly.  Now, Python will do it for you: all the built-in and standard library functions that make use of system calls will automatically retry themselves when interrupted.  ([Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#pep-475-retry-system-calls-failing-with-eintr); [PEP 475](https://www.python.org/dev/peps/pep-0475))

File descriptors created by Python code are now flagged "non-inheritable", meaning they're closed automatically when spawning a child process.  ([docs](https://docs.python.org/3/library/os.html#fd-inheritance); [Python 3.4 release notes](https://docs.python.org/3/whatsnew/3.4.html#whatsnew-pep-446); [PEP 446](https://www.python.org/dev/peps/pep-0446))

A number of standard library functions now accept file descriptors in addition to paths.  ([docs](https://docs.python.org/3/library/os.html#files-and-directories); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#os))

Several different OS and I/O exceptions were merged into a single and more fine-grained hierarchy, rooted at `OSError`.  Code can now catch a specific subclass in most cases, rather than examine `.errno`.  ([docs](https://docs.python.org/3/library/exceptions.html#os-exceptions); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#pep-3151-reworking-the-os-and-io-exception-hierarchy); [PEP 3151](https://www.python.org/dev/peps/pep-3151))

`ResourceWarning` is a new kind of warning for issues with resource cleanup.  One is produced if a file object is destroyed, but was never closed, which can cause issues on Windows or with garbage-collected Python implementations like PyPy; one is also produced if uncollectable objects still remain when Python shuts down, indicating some severe finalization problems.  The warning is ignored by default, but can be enabled with `-W default` on the command line.  ([Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#other-language-changes))

`hasattr()` only catches (and returns `False` for) `AttributeError`s.  Previously, any exception would be considered a sign that the attribute doesn't exist, even though an unusual exception like an `OSError` usually means the attribute is computed dynamically, and that code is broken somehow.  Now, exceptions other than `AttributeError` are allowed to propagate to the caller.  ([docs](https://docs.python.org/3/library/functions.html#hasattr); [Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#other-language-changes))

Hash randomization is on by default, meaning that dict and set iteration order is different per Python runs.  This protects against some DoS attacks, but more importantly, it spitefully forces you not to rely on incidental ordering.  ([docs](https://docs.python.org/3/reference/datamodel.html#object.__hash__); [Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#porting-python-code))

List comprehensions no longer leak their loop variables into the enclosing scope.  ([Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#changed-syntax))

`nonlocal` allows writing to a variable in an enclosing (but non-global) scope.  ([docs](https://docs.python.org/3/reference/simple_stmts.html#nonlocal); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#new-syntax); [PEP 3104](https://www.python.org/dev/peps/pep-3104))

Comparing objects of incompatible types now produces a `TypeError`, rather than using Python 2's very silly fallback.  ([Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#ordering-comparisons))

`!=` defaults to returning the opposite of `==`.  ([Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#operators-and-special-methods))

Accessing a method as a class attribute now gives you a regular function, not an "unbound method" object.  ([Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#operators-and-special-methods))

The `input` builtin no longer performs an `eval` (!), removing a huge point of confusion for beginners.  This is the behavior of `raw_input` in Python 2.  ([docs](https://docs.python.org/3/library/functions.html#input); [Python 3.0 release notes](https://docs.python.org/3/whatsnew/3.0.html#builtins); [PEP 3111](https://www.python.org/dev/peps/pep-3111))


## Fast and furious

These aren't necessarily compelling, and they may not even make any appreciable difference for your code, but I think they're interesting technically.

Objects' `__dict__`s can now share their key storage internally.  Instances of the same type generally have the same attribute names, so this provides a modest improvement in speed and memory usage for programs that create a lot of user-defined objects.  ([Python 3.3 release notes](https://docs.python.org/3/whatsnew/3.3.html#pep-412-key-sharing-dictionary); [PEP 412](https://www.python.org/dev/peps/pep-0412/))

`OrderedDict` is now implemented in C, making it "4 to 100" (!) times faster.  Note that the backport in the 2.7 standard library is pure Python.  So, there's a carrot.  ([Python 3.5 release notes](https://docs.python.org/3/whatsnew/3.5.html#whatsnew-ordereddict))

The GIL was made more predictable.  My understanding is that the old behavior was to yield after some number of Python bytecode operations, which could take wildly varying amounts of time; the new behavior yields after a given duration, by default 5ms.  ([Python 3.2 release notes](https://docs.python.org/3/whatsnew/3.2.html#multi-threading))

The `io` library was rewritten in C, making it more fast.  Again, the Python 2.7 implementation is pure Python.  ([Python 3.1 release notes](https://docs.python.org/3/whatsnew/3.1.html#optimizations))

Tuples and dicts containing only immutable objects — i.e., objects that cannot possibly contain circular references — are ignored by the garbage collector.  This was backported to Python 2.7, too, but I thought it was super interesting.  ([Python 3.1 release notes](https://docs.python.org/3/whatsnew/3.1.html#optimizations))


## That's all I've got

Huff, puff.

I hope _something_ here appeals to you as a reason to at least experiment with Python 3.  It's fun over here.  Give it a try.
