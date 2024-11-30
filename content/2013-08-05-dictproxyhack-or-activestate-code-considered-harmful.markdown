title: dictproxyhack, or: ActiveState Code considered harmful
date: 2013-08-05 20:36
category: articles
tags: python, making things, tech

This is a story of how nothing in this story is my fault.

I've got a [coworker][jrheard] who's super into [Clojure][], a Lisp-like that runs on the JVM.  In particular he's super into how it's got notions of mutability (and, thus, _immutability_) all throughout.

More than once he's lamented that Python lacks a `frozendict`—a dictionary type that can't be changed.  Dictionaries tend to crop up a lot in Python, and in a very large codebase, it's very easy to end up with this scenario:

1. Some function somewhere generates a dict that's only used by one caller.  The interface is obvious since the keys and values are created right there in one place.  No problem.
2. Other code comes along, notices this handy function, and starts using its return value.  Some of this code may pass the ad-hoc dict up to callers, too.
3. Some of that other code needs more things added to the dict, but computing the extra data is expensive, so arguments are added to the function that optionally turn on certain keys.
4. Some code needs even more things added to the dict that are outside the purview of the original function, so they add helper functions that take the ad-hoc dict and add more things to it.
5. Since this has all now happened multiple times throughout your codebase, someone addresses the problem by writing adapter code that infers the original dict from some other object describing its structure, thus saving everyone from writing all these functions that return dicts.

A lovely spaghetti dinner.  It's now nigh impossible to trace what the dict contains or where half of it came from.

Returning an object in the first place would have avoided much of this, but when you're sitting at step 1, that seems like a lot of effort just to return half a dozen things from a function you wrote to another function you wrote.  Swapping out `dict()` for `frozendict()` is easy.

My opinion on `frozendict` had never grown stronger than "I guess that would be cool", so I never sat down and wrote the class, and there must be enough subtleties that nobody else at Yelp has either.

Then today, [PEP 416][] came to my attention.  This PEP proposed adding a `frozendict` type, but was rejected last year as being largely unnecessary.  What's interesting about it is that the rejection ends with almost a footnote suggesting that perhaps `dictproxy` ought to be exposed to Python-land, instead.  And indeed this was done, and it exists in Python 3.3.

<!-- more -->


## dictproxy

`dictproxy` is the type of an object's `__dict__`, sometimes.  Usually for _truly_ immutable objects, i.e., ones implemented in C.  It's been part of Python since 2.2, albeit largely unnoticed, because who ever checks things like `type(type.__dict__)`?

Rather than being an immutable dict, `dictproxy` is an immutable _wrapper_ around an existing dict.  Changes to the underlying dict are still visible, but code that only has a `dictproxy` can neither change the underlying dict nor touch it directly in any way.  Perfect.

Except that in Pythons before 3.3, `dictproxy` doesn't have a Python-land constructor, so Python code can't actually use it.  That leaves us 2.x suckers out in the cold.

Or does it?  "Python can't do this" is often secret code for "Python can only do this with some awful `ctypes` hackery".  Let's google up some awful hackery, then.


## Enter ActiveState

The only promising result I bumbled across was [this ActiveState recipe](http://code.activestate.com/recipes/576540-make-dictproxy-object-via-ctypespythonapi-and-type/).

I was extremely skeptical about this, because in my experience, and everyone else's experience, code posted on ActiveState is some of the most bug-ridden hacked-together sludge on the planet.  I think [this example](http://code.activestate.com/recipes/496969-convert-string-to-hex/) from my actual browser history makes that point well enough.  (Look at the comments.)  But this seemed simple enough.  It was a quick wrapper around the C API, it had tests, it worked when I tried it, and the meat of it was only three lines.  **What could possibly go wrong?**

All I took was the `ctypes` bit:

```python
from ctypes import pythonapi, py_object
from _ctypes import PyObj_FromPtr

PyDictProxy_New = pythonapi.PyDictProxy_New
PyDictProxy_New.argtypes = (py_object,)
PyDictProxy_New.rettype = py_object

someproxy = PyObj_FromPtr(PyDictProxy_New(somedict))
```

I expanded on it considerably: I used the real type in 3.3+, I wrote a metaclass that would fool `isinstance`, I made `dictproxy` into a type rather than having a factory function, and I added fallback based on the `Mapping` ABC in the event that `ctypes` failed (as it does on PyPy).  It worked beautifully on every Python incarnation I had on hand, and some people cleverer than I gave nods of approval.

I thought this useful enough that someone else might want to use it, so I tossed it on PyPI.  Then I ran it again against Python 2.7, just for kicks.

It segfaulted.

Oops.


## Debugging

The next hour produced some fascinating symptoms.

* It wouldn't segfault within gdb.
* It wouldn't segfault in another `tmux` window.
* It wouldn't segfault in another terminal window.
* It wouldn't segfault in a _subshell_.

I couldn't get a core dump (later revealed to be caused by `systemd`, but not useful anyway).  I could only track it down as far as the `PyObj_FromPtr` call, but had no idea what the difference could be between shells.  The environments were identical in every way that matters.

`print` debugging revealed only some very minor differences.

* The addresses of Python objects just before the segfault were very large; around 12 hex digits.
* The pointer being returned from `PyDictProxy_New` just before the segfault was much smaller; around 6 hex digits.  Rarely, they were _negative_.
* Non-segfaulting runs had only small addresses.

Look at the ActiveState code again and see if you can figure it out from this.

Hm.

Hmmmmm.

Okay, here's the problem.

```python
PyDictProxy_New.rettype = py_object
```

`ctypes` function objects don't have a `rettype` attribute.  That's supposed to be `restype`.

Without a return type assigned, `ctypes` assumes everything returns a 32-bit signed int, so it was truncating the pointer being returned.  This worked _sometimes_, when allocations happened to be in the 32-bit range, but the shell I was using just happened to have won the memory allocation lottery, and it (and _only_ its Python children, for reasons I cannot explain) was allocating rather high addresses.

In fact, this bug is the only reason `PyObj_FromPtr` is necessary at all.  A return type of `py_object` means to convert to a Python object automatically!  The correct code is much simpler:

```python
from ctypes import pythonapi, py_object

PyDictProxy_New = pythonapi.PyDictProxy_New
PyDictProxy_New.argtypes = (py_object,)
PyDictProxy_New.restype = py_object

someproxy = PyDictProxy_New(somedict)
```

Interesting trivia: the original code failed on PyPy because `PyObj_FromPtr` doesn't exist.  (PyPy has no `PyObject*` pointers floating around, after all.)  The fixed code actually works on PyPy, until the last line, where it complains that `dict` is not a `py_object`.  (Fixing that wouldn't work, because...  well, no pointers, etc.)  I had to _make_ the code fail early so PyPy would fall back to the dumb approach.  Hopefully it gets the 3.3 stdlib soon.


## Blame

That's what I get for daring to assume that an ActiveState code sample could actually work correctly.  Don't make the same poor choices I did, kids; just say no to `code.activestate.com`.  Don't even click once.

I was also surprised that assigning to a bogus attribute on a `ctypes` object worked fine; C types tend to have fixed slots that yell at you when you make typos like this.  Guess not, in this case.

Also, `ctypes` developers, what the hell?  `restype`?  What is that even short for?  Resurn type?

Glad I bumbled into this early, though; I would've had a hell of a time debugging it inside a larger program.  Or, worse, someone _else's_ larger program.

If this tale has not entirely eradicated your confidence in me, you can totally find the resulting module, `dictproxyhack`, on [PyPI](https://pypi.python.org/pypi/dictproxyhack) and [my GitHub](https://github.com/eevee/dictproxyhack).



[Clojure]: http://en.wikipedia.org/wiki/Clojure
[jrheard]: https://twitter.com/jrheard
[PEP 416]: http://www.python.org/dev/peps/pep-0416/
