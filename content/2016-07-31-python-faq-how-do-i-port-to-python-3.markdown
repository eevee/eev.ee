title: Python FAQ: How do I port to Python 3?
date: 2016-07-31 22:25
category: blog
tags: tech, python, unicode

_Part of my [Python FAQ]({filename}2011-07-22-python-faq.markdown), which is doomed to never be finished._

Maybe you have a Python 2 codebase.  Maybe you'd like to make it work with Python 3.  Maybe you really wish someone would write a comically long article on how to make that happen.

I have good news!  You're already reading one.

(And if you're not sure why you'd want to use Python 3 in the first place, perhaps you'd be interested in the companion article [which delves into exactly that question]({filename}2016-07-31-python-faq-why-should-i-use-python-3.markdown)?)

<!-- more -->


## Don't be intimidated

This article _is_ quite long, but don't take that as a sign that this is necessarily a Herculean task.  I'm trying to cover every issue I can ever recall running across, which means a lot of small gotchas.

I've ported several codebases from Python 2 to Python 2+3, and most of them have gone pretty smoothly.  If you have modern Python 2 code that handles Unicode responsibly, you're already halfway there.

However...  if you still haven't ported by now, almost _eight years_ after Python 3.0 was first released, chances are you have either a lumbering giant of an app or ancient and weird 2.2-era code.  Or, perish the thought, a lumbering giant consisting largely of weird 2.2-era code.  In that case, you'll want to clean up the more obvious issues one at a time, then go back and start worrying about actually running parts of your code on Python 3.

On the other hand, if your Python 2 code is pretty small and you've just never gotten around to porting, good news!  It's not that bad, and much of the work can be done automatically.  Python 3 is ultimately the same language as Python 2, just with some sharp bits filed off.


## Making some tough decisions

We say "porting from 2 to 3", but what we usually mean is "porting code from 2 to both 2 and 3".  That ends up being more difficult (and ugly), since rather than writing either 2 or 3, you have to write the common subset of 2 and 3.  As nifty as some of the features in 3 are, you can't actually use any of them if you have to remain compatible with Python 2.

The first thing you need to do, then, is decide exactly which versions of Python you're targeting.  For 2, your options are:

- **Python 2.5+** is possible, but very difficult, and this post doesn't really discuss it.  Even something as simple as exception handling becomes painful, because the only syntax that works in Python 3 was first introduced in Python 2.6.  I wouldn't recommend doing this.

- **Python 2.6+** used to be fairly common, and is well-tread ground.  However, Python 2.6 reached end-of-life in 2013, and some common libraries have been dropping support for it.  If you want to preserve Python 2.6 compatibility for the sake of making a library more widely-available, well, I'd urge you to reconsider.  If you want to preserve Python 2.6 compatibility because you're running a proprietary app on it, you should stop reading this right now and go upgrade to 2.7 already.

- **Python 2.7** is the last release of the Python 2 series, but is guaranteed to be supported until at least 2020.  The major focus of the release was backporting a lot of minor Python 3 features, making it the best possible target for code that's meant to run on both 2 and 3.

- There is, of course, also the choice of **dropping Python 2 support**, in which case this process will be much easier.  Python 2 is still very widely-used, though, so library authors probably won't want to do this.  App authors do have the option, but unless your app is trivial, it's much easier to maintain Python 2 support during the port — that way you can port iteratively, and the app will still function on Python 2 in the interim, rather than being a 2/3 hybrid that can't run on either.

Most of this post assumes you're targeting Python 2.7, though there are mentions of 2.6 as well.

You also have to decide which version of Python _3_ to target.

- **Python 3.0 and 3.1** are forgettable.  Python 3 was still stabilizing for its first couple minor versions, and from what I hear, compatibility with both 2.7 and 3.0 is a huge pain.  Both versions are also past end-of-life.

- **Python 3.2 and 3.3** are a common minimum version to target.  Python 3.3 reinstated support for `u'...'` literals (redundant in Python 3, where normal strings are already Unicode), which makes supporting both 2 and 3 _much_ easier.  I bundle it with Python 3.2 because the [latest version that stable PyPy supports](https://morepypy.blogspot.com/2014/10/pypy3-240-released.html) is 3.2, _but_ it also supports `u'...'` literals.  You'll support the biggest surface area by targeting that, a sort of 3.2½.  (There's an [alpha PyPy supporting 3.3](https://morepypy.blogspot.com/2016/05/pypy33-v52-alpha-1-released.html), but as of this writing it's not released as stable yet.)

- **Python 3.4 and 3.5** add shiny new features, but you can only really use them if you're dropping support for Python 2.  Again, I'd suggest targeting Python 2.7 + Python 3.2½ first, then dropping the Python 2 support and adding whatever later Python 3 trinkets you want.

Another consideration is what attitude you want your final code to take.  Do you want Python 2 code with enough band-aids that it also works on Python 3, or Python 3 code that's carefully written so it still works on Python 2?  The differences are subtle!  Consider code like `x = map(a, b)`.  `map` returns a list in Python 2, but a lazy iterable in Python 3.  Which way do you want to port this code?

```python
# Python 2 style: force eager evaluation, even on Python 3
x = list(map(a, b))

# Python 3 style: use lazy evaluation, even on Python 2
try:
    from future_builtins import map
except ImportError:
    pass
x = map(a, b)
```

The answer may depend on which Python you primarily use for development, your target audience, or even case-by-case based on how `x` is used.

Personally, I'd err on the side of preserving Python 3 semantics and porting them to Python 2 when possible.  I'm pretty used to Python 3, though, and you or your team might be thrown for a loop by changing Python 2's behavior.

At the very least, prefer `if PY2` to `if not PY3`.  The former stresses that Python 2 is the special case, which is increasingly true going forward.  Eventually there'll be a Python 4, and perhaps even a Python 5, and those future versions will want the "Python 3" behavior.


## Some helpful tools

The good news is that you don't have to do all of this manually.

[`2to3`](https://docs.python.org/2/library/2to3.html) is a standard library module (since 2.6) that automatically modifies Python 2 source code to change some common Python 2 constructs to the Python 3 equivalent.  (It also doubles as a framework for making arbitrary changes to Python code.)

Unfortunately, it ports 2 to 3, not 2 to 2+3.  For libraries, it's possible to rig `2to3` to run automatically on your code just before it's installed on Python 3, so you can keep writing Python 2 code — but `2to3` isn't perfect, and this makes it impossible to develop with your library on Python 3, so Python 3 ends up as a second-class citizen.  I wouldn't recommend it.

The more common approach is to use something like [`six`](https://pythonhosted.org/six/), a library that wraps many of the runtime differences between 2 and 3, so you can run the same codebase on both 2 and 3.

Of course, that still leaves you making the changes yourself.  A more recent innovation is the [python-future](http://python-future.org/) project, which combines both of the above.  It has a `future` library of renames and backports of Python 3 functionality that goes further than `six` and is designed to let you write Python 3-esque code that still runs on Python 2.  It also includes a `futurize` script, based on the `2to3` plumbing, that rewrites your code to target 2+3 (using python-future's library) rather than just 3.

The nice thing about python-future is that it explicitly takes the stance of writing code against Python 3 semantics and backporting them to Python 2.  It's _very_ dedicated to this: it has a `future.builtins` module that includes not only easy cases like `map`, but also entire pure-Python reimplementations of types like `bytes`.  (Naturally, this adds some significant overhead as well.)  I do like the overall attitude, but I'm not totally sold on all the changes, and you might want to leaf through them to see which ones you like.

`futurize` isn't perfect, but it's probably the best starting point.  The `2to3` design splits the various edits into a variety of "fixers" that each make a single style of change, and `futurize` works the same way, inheriting many of the fixers from `2to3`.  The nice thing about `futurize` is that it groups the fixers into "stages", where stage 1 (`futurize --stage1`) only makes fairly straightforward changes, like fixing the `except` syntax.  More importantly, it doesn't add any dependencies on the `future` library, so it's useful for making the easy changes even if you'd prefer to use `six`.  You're also free to choose individual fixes to apply, if you discover that some particular change breaks your code.

Another advantage of this approach is that you can tackle the porting piecemeal, which is great for very large projects.  Run one fixer at a time, starting with the very simple ones like updating to `except ... as ...` syntax, and convince yourself that everything is fine before you do the next one.  You can make some serious strides towards 3 compatibility just by eliminating behavior that already has cromulent alternatives in Python 2.

If you expect your Python 3 port to take a _very long time_ — say, if you have a large project with numerous developers and a frantic release schedule — then you might want to prevent older syntax from creeping in with a tool like [autopep8](https://pypi.python.org/pypi/autopep8), which can automatically fix some deprecated features with a much lighter touch.  If you'd like to automatically enforce that, say, `from __future__ import absolute_import` is at the top of every Python file, that's a bit beyond the scope of this article, but I've had [pre-commit](http://pre-commit.com/) + [`reorder_python_imports`](https://libraries.io/github/asottile/reorder_python_imports) thrust upon me in the past to fairly good effect.

Anyway!  For each of the issues below, I'll mention whether `futurize` can fix it, the name of the responsible fixer, and whether `six` has anything relevant.  If the name of the fixer begins with `lib2to3`, that means it's part of the standard library, and you can use it with `2to3` without installing python-future.

Here we go!


## Things you shouldn't even be doing

These are ancient, ancient practices, and even Python 2 programmers may be surprised by them.  Some of them are arguably outright bugs in the language; others are just old and forgotten.  They generally have equivalents that work even in older versions of Python 2.

### Old-style classes

```python
class Foo:
    ...
```

In Python 3, this code creates a class that inherits from `object`.  In Python 2, it creates a completely different kind of thing entirely: an "old-style" class, which worked a little differently from built-in types.  The differences are generally subtle:

* Old-style classes don't support `__getattribute__`, `__slots__`

* Old-style classes don't correctly support data descriptors, i.e. the assignment behavior of `@property`.

* Old-style classes had a `__coerce__` method, which would attempt to turn a value into a built-in numeric type before performing a math operation.

* Old-style classes didn't use the C3 MRO, so in the case of diamond inheritance, a class could be skipped entirely by `super()`.

* Old-style instances check the instance for a special method name; new-style instances check the _type_.  Additionally, if a special method isn't found on an old-style instance, the lookup falls back to `__getattr__`; this is not the case for new-style classes (which makes proxying more complicated).

That last one is the only thing old-style classes can do that new-style classes _cannot_, and if you're relying on it, you have a bit of refactoring to do.  (The really curious thing is that there [doesn't seem to be a particularly good reason for the limitation on new-style classes](http://lucumr.pocoo.org/2014/8/16/the-python-i-would-like-to-see/), and it doesn't even make things faster.  Maybe that'll be fixed in Python 4?)

If you have no idea what any of that means or why you should care, chances are you're either not using old-style classes at all, or you're only using them because you forgot to write `(object)` somewhere.  In that case, `futurize --stage2` will happily change `class Foo:` to `class Foo(object):` for you, using the `libpasteurize.fixes.fix_newstyle` fixer.  (Strictly speaking, this is a Python _2_ compatibility issue, since the old syntax still works fine in Python 3 — it just means something else now.)


### `cmp`

Python 2 originally used the C approach for sorting.  Given two things `A` and `B`, a comparison would produce a negative number if `A < B`, zero if `A == B`, and a positive number if `A > B`.  This was the only way to customize sorting; there's a `cmp()` built-in function, a `__cmp__` special method, and `cmp` arguments to `list.sort()` and `sorted()`.

This is a little cumbersome, as you may have noticed if you've ever tried to do custom sorting in Perl or JavaScript.  Even a case-insensitive sort involves repeating yourself.  Most custom sorts will have the same basic structure of `cmp(op(a), op(b))`, when the only thing you really care about is `op`.

```python
names.sort(cmp=lambda a, b: cmp(a.lower(), b.lower()))
```

But more importantly, the C approach is flat-out wrong for some types.  Consider sets, which use comparison to indicate subsets versus supersets:

```python
{1, 2} < {1, 2, 3}  # True
{1, 2, 3} > {1, 2}  # True
{1, 2} < {1, 2}  # False
{1, 2} <= {1, 2}  # True
```

So what to do with `{1, 2} < {3, 4}`, where none of the three possible answers is correct?

Early versions of Python 2 added "rich comparisons", which introduced methods for all six possible comparisons: `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, and `__ge__`.  You're free to return `False` for all six, or even `True` for all six, or return `NotImplemented` to allow deferring to the other operand.  The `cmp` argument became `key` instead, which allows mapping the original values to a different item to use for comparison:

```python
names.sort(key=lambda a: a.lower())
```

(This is faster, too, since there are fewer calls to the lambda, fewer calls to `.lower()`, and no calls to `cmp`.)

----

So, fixing all this.  Luckily, Python 2 supports all of the new stuff, so you don't need compatibility hacks.

To replace simple implementations of `__cmp__`, you need only write the appropriate rich comparison methods.  You could even do this the obvious way:

```python
class Foo(object):
    def __cmp__(self, other):
        return cmp(self.prop, other.prop)

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    ...
```

You would also have to change the use of `cmp` to a manual `if` tree, since `cmp` is gone in Python 3.  I don't recommend this.

A lazier alternative would be to use [`functools.total_ordering`](https://docs.python.org/2/library/functools.html#functools.total_ordering) (backported from 3.0 into 2.7), which generates four of the comparison methods, given a class that implements `__eq__` and one other:

```python
@functools.total_ordering
class Foo(object):
    def __eq__(self, other):
        return self.prop == other.prop

    def __lt__(self, other):
        return self.prop < other.prop
```

There are a couple problems with this code.  For one, it's still pretty repetitive, accessing `.prop` four times (and imagine if you wanted to compare several properties).  For another, it'll either cause an error or do entirely the wrong thing if you happen to compare with an object of a different type.  You should return `NotImplemented` in this case, but `total_ordering` doesn't handle that correctly until Python 3.4.  If those bother you, you might enjoy my own [`classtools.keyed_ordering`](http://classtools.readthedocs.io/en/latest/#classtools.keyed_ordering), which uses a `__key__` method (much like the `key` argument) to generate all six methods:

```python
@classtools.keyed_ordering
class Foo(object):
    def __key__(self):
        return self.prop
```

Replacing uses of `key` arguments _should_ be straightforward: a `cmp` argument of `cmp(op(a), op(b))` becomes a `key` argument of `op`.  If you're doing something more elaborate, there's a [`functools.cmp_to_key`](https://docs.python.org/2/library/functools.html#functools.cmp_to_key) function (also backported from 3.0 to 2.7), which converts a `cmp` function to one usable as a `key`.  (The implementation is much like the first `Foo` example above: it involves a class that calls the wrapped function from its comparison methods, and returns `True` or `False` depending on the return value.)

Finally, if you're using `cmp` directly, don't do that.  If you really, _really_ need it for something other than Python's own sorting, just use an `if`.

The only help `futurize` offers is in `futurize --stage2`, via `libfuturize.fixes.fix_cmp`, which adds an import of `past.builtins.cmp` if it detects you're using the `cmp` function anywhere.


### Comparing incompatible types

Python 2's use of C-style ordering also means that _any_ two objects, of _any_ types, must be either equal or occur in some defined order.  Python's answer to this problem is to sort on the names of the types.  So `None < 3 < "1"`, because `"NoneType" < "int" < "str"`.

Python 3 removes this fallback rule; if two values don't know how to compare against each other (i.e. both return `NotImplemented`), you just get a `TypeError`.

This might affect you in subtle ways, such as if you're sorting a list of objects that _may_ contain `None`s and expecting it to silently work.  The fix depends entirely on the type of data you have, and no automated tool can handle that for you.  Most likely, you didn't mean to be sorting a heterogenous list in the first place.

Of course, you could always sort on `type(x).__name__`, but I don't know why you would do that.


### The `sets` module

Python 2.3 introduced its set types as `Set` and `ImmutableSet` in the `sets` module.  Since Python 2.4, they've been built-in types, `set` and `frozenset`.  The `sets` module is gone in Python 3, so just use the built-in names.


### Creating exceptions

Python 2 allows you to do this:

```python
raise RuntimeError, "an error happened at runtime!!"
```

There's not really any good reason to do this, since you can just as well do:

```python
raise RuntimeError("an error happened at runtime!!")
```

`futurize --stage1` will rewrite the two-arg form to a regular object creation via the `libfuturize.fixes.fix_raise` fixer.  It'll also fix this alternative way of specifying an exception type, which is so bizarre and obscure that I did not know about it until I read the fixer's source code:

```python
raise (((A, B), C), ...)  # equivalent to `raise A` (?!)
```

Additionally, exceptions act like sequences in Python 2, but not in Python 3.  You can just operate on the `.args` sequence directly, in either version.  Alas, there's no automated way to fix this.


### Backticks

Did you know that `` `x` `` is equivalent to `repr(x)` in Python 2?  Yeah, most people don't.  It's super weird.  `futurize --stage1` will fix this with the `lib2to3.fixes.fix_repr` fixer.


### `has_key`

Very old code may still be using `somedict.has_key("foo")`.  `"foo" in somedict` has worked since Python 2.2.  What are you doing.  `futurize --stage1` will fix this with the `lib2to3.fixes.fix_has_key` fixer.


### `<>`

`<>` is equivalent to `!=` in Python 2!  This is an ancient, _ancient_ holdover, and there's no reason to still be using it.  `futurize --stage1` will fix this with the `lib2to3.fixes.fix_ne` fixer.

(You could also use `from __future__ import barry_as_FLUFL`, which restores `<>` in Python 3.  It's an easter egg.  I'm joking.  Please don't actually do this.)


## Things with easy Python 2 equivalents

These aren't necessarily ancient, but they have an alternative you can just as well express in Python 2, so there's no need to juggle 2 and 3.

### Other ancient builtins

`apply()` is gone.  Use the built-in syntax, `f(*args, **kwargs)`.

`callable()` was briefly gone, but then came back in Python 3.2.

`coerce()` is gone; it was only used for old-style classes.

`execfile()` is gone.  Read the file and pass its contents to `exec()` instead.

`file()` is gone; Python 3 has multiple file types, and a hierarchy of interfaces defined in the `io` module.  Occasionally, code uses this as a synonym for `open()`, but you should really be using `open()` anyway.

`intern()` has been moved into the `sys` module, though I have no earthly idea why you'd be using it.

`raw_input()` has been renamed to `input()`, and the old ludicrous `input()` is gone.  If you really need `input()`, please stop.

`reduce()` has been moved into the `functools` module, but it's there in Python 2.6 as well.

`reload()` has been moved into the `imp` module.  It's unreliable garbage and you shouldn't be using it anyway.

`futurize --stage1` can fix several of these:

- `apply`, via `lib2to3.fixes.fix_apply`
- `intern`, via `lib2to3.fixes.fix_intern`
- `reduce`, via `lib2to3.fixes.fix_reduce`

`futurize --stage2` can also fix `execfile` via the `libfuturize.fixes.fix_execfile` fixer, which imports `past.builtins.execfile`.  The 2to3 fixer uses an `open()` call, but the true correct fix is to use a `with` block.

`futurize --stage2` has a couple of fixers for `raw_input`, but you can just as well import `future.builtins.input` or `six.moves.input`.

Nothing can fix `coerce`, which has no equivalent.  Curiously, I don't see a fixer for `file`, which is trivially fixed by replacing it with `open`.  Nothing for `reload`, either.


### Catching exceptions

Historically, the way to say "if there's a `ValueError`, store it in `e` and run some code" was:

    :::python
    try:
        ...
    except ValueError, e:
        ...

Unfortunately, that's very easy to confuse with the syntax for catching two different types of exception:

    :::python
    except (ValueError, TypeError):
        ...

If you forget the parentheses, you'll only catch `ValueError`, and the exception will be assigned to a variable called, er, `TypeError`.  Whoops!

Python 3.0 introduced clearer syntax, which was also backported to Python 2.6:

    :::python
    except ValueError as e:
        ...

Python 3.0 finally removed the old syntax, so you _must_ use the `as` form.  `futurize --stage1` will fix this with the `lib2to3.fixes.fix_except` fixer.

As an additional wrinkle, the extra variable `e` is deleted at the end of the block in Python 3, but _not_ in Python 2.  If you _really_ need to refer to it after the block, just assign it to a different name.

(The reason for this is that captured exceptions contain a traceback in Python 3, and tracebacks contain the locals for the current frame, and those locals will contain the captured exception.  The resulting cycle would keep _all_ local variables alive until the cycle detector dealt with it, at least in CPython.  Scrapping the exception as soon as it's been dealt with was a simple way to keep this from accidentally happening all over the place.  It usually doesn't make sense to refer to a captured exception after the `except` block, anyway, since the variable may or may not even exist, and that's generally weird and bad in Python.)


### Octals

It's not uncommon for a new programmer to try to zero-pad a set of numbers:

```python
a = 07
b = 08
c = 09
d = 10
```

Of course, this will have the rather bizarre result that `08` is a `SyntaxError`, even though `07` works fine — because numbers starting with a `0` are parsed as octal.

This is a holdover from C, and it's fairly surprising, since there's virtually no reason to ever use octal.  The only time I can _ever_ remember using it is for passing file modes to `chmod`.

Python 3.0 requires octal literals to be prefixed with `0o`, in line with `0x` for hex and `0b` for binary; literal integers starting with only a `0` are a syntax error.  Python 2.6 supports both forms.

`futurize --stage1` will fix this with the `lib2to3.fixes.fix_numliterals` fixer.

### `pickle`

If you're using the `pickle` module (which you [shouldn't be]({filename}/release/2015-10-15-dont-use-pickle-use-camel.markdown)), and you intend to pass pickles back and forth between Python 2 and Python 3, there's a small issue to be aware of.  `pickle` has several different ["protocol" versions](https://docs.python.org/3/library/pickle.html#pickle-protocols), and the default version used in Python 3 is protocol 3, which Python 2 _cannot read_.

The fix is simple: just find where you're calling `pickle.dump()` or `pickle.dumps()`, and pass a `protocol` argument of 2.  Protocol 2 is the highest version supported by Python 2, and you probably want to be using it anyway, since it's much more compact and faster to read/write than Python 2's default, protocol 0.

You may be already using `HIGHEST_PROTOCOL`, but you'll have the same problem: the highest protocol supported in any version of Python 3 is unreadable by Python 2.

----

A somewhat bigger problem is that if you pickle an instance of a user-defined class on Python 2, the pickle will record all its attributes as bytestrings, because that's what they are in Python 2.  Python 3 will then dutifully load the pickle and populate your object's `__dict__` with keys like `b'foo'`.  `obj.foo` will then not actually exist, because `obj.foo` looks for the string `'foo'`, and `'foo' != b'foo'` in Python 3.

Don't use pickle, kids.

It's possible to fix this, but also a huge pain in the ass.  If you don't know how, you _definitely_ shouldn't be using pickle.


## Things that have a `__future__` import

Occasionally, the syntax changed in an incompatible way, but the new syntax was still backported and hidden behind a [`__future__` import](https://docs.python.org/3/reference/simple_stmts.html#future) — Python's mechanism for opting into syntax changes.  You have to put such an import at the top of the file, optionally after a docstring, like this:

```python
"""My super important module."""
from __future__ import with_statement
```

### `print` is now a function

Ugh!  Parentheses!  Why, Guido, why?

The reason is that the `print` statement has _incredibly_ goofy syntax, unlike anything else in the language:

```python
print >>a, b, c,
```

You might not even _recognize_ the `>>` bit, but it lets you print to a file other than `sys.stdout`.  It's baked specifically into the `print` syntax.  Python 3 replaces this with a straightforward [built-in function](https://docs.python.org/3/library/functions.html#print) with a couple extra bells and whistles.  The above would be written:

```python
print(b, c, end='', file=a)
```

It's slightly more verbose, but it's also easier to tell what's going on, and that teeny little comma at the end is now a more obvious keyword argument.

`from __future__ import print_function` will forget about the `print` statement for the rest of the file, and make the builtin `print` function available instead.  `futurize --stage1` will fix all uses of `print` and add the `__future__` import, with the `libfuturize.fixes.fix_print_with_import` fixer.  (There's also a `2to3` fixer, but it doesn't add the `__future__` import, since it's unnecessary in Python 3.)

A word of warning: _do not_ just use `print` with parentheses without adding the `__future__` import.  This may appear to work in stock Python 2:

```python
print("See, what's the problem?  This works fine!")
```

However, that's parsed as the `print` statement followed by an expression in parentheses.  It becomes more obvious if you try to print two values:

```python
print("The answer is:", 3)
# ("The answer is:", 3)
```

Now you have a comma inside parentheses, which is a tuple, so the old `print` statement prints its `repr`.


### Division always produces a float

Quick, what's the answer here?

```python
5 / 2
```

If you're a normal human being, you'll say 2.5 or 2½.  Unfortunately, if you're like Python and have been afflicted by C, you might say the answer is 2, because this is "integer division" — a bizarre and alien concept probably invented because CPUs didn't have FPUs when C was first invented.

Python 3.0 decided that maybe contorting fundamental arithmetic to match the inadequacies of 1970s hardware is not the best idea, and so it changed division to always produce a float.

Since Python 2.6, `from __future__ import division` will alter the division operator to always do true division.  If you want to do floor division, there's a separate `//` operator, which has existed for ages; you can use it in Python 2 with or without the `__future__` import.

Note that true division _always_ produces a float, even if the result is integral: `6 / 3` is 2.0.  On the other hand, floor division uses the same typing rules as C-style division: `5 // 2` is 2, but `5 // 2.0` is 2.0.

`futurize --stage2` will "fix" this with the `libfuturize.fixes.fix_division` fixer, but unfortunately that just adds the `__future__` import.  With the `--conservative` option, it uses the `libfuturize.fixes.fix_division_safe` fixer instead, which imports `past.utils.old_div`, a forward-port of Python 2's division operator.

The trouble here is that the new `/` always produces a float, and the new `//` always floors, but the old `/` sometimes did one and sometimes did the other.  `futurize` can't just replace all uses of `/` with `//`, because `5/2.0` is 2.5 but `5//2.0` is 2.0, and it can't generally know what types the operands are.

You might be best off fixing this one manually — perhaps using `fix_division_safe` to find all the places you do division, then changing them to use the right operator.

Of course, the `__div__` magic method is gone in Python 3, replaced explicitly by `__floordiv__` (`//`) and `__truediv__` (`/`).  Both of those methods already exist in Python 2, and `__truediv__` is even called when you use `/` in the presence of the `future` import, so being compatible is a simple matter of implementing all three and deferring to one of the others from `__div__`.


### Relative imports

In Python 2, if you're in the module `foo.bar` and say `import quux`, Python will look for a `foo.quux` before it looks for a top-level `quux`.  The former behavior is called a _relative_ import, though it might be more clearly called a _sibling_ import.  It's troublesome for several reasons.

- If you have a sibling called `quux`, and there's also a top-level or standard library module called `quux`, you can't import the latter.  (There used to be a `py.std` module for providing indirect access to the standard library, for this very reason!)

- If you import the top-level `quux` module, and then _later_ add a `foo.quux` module, you'll suddenly be importing a different module.

- When reading the source code, it's not clear which imports are siblings and which are top-level.  In fact, the modules you get depend on the module you're _in_, so moving or renaming a file may change its imports in non-obvious ways.

Python 3 eliminates this behavior: `import quux` always means the top-level module.  It also adds syntax for "explicit relative" or "absolute relative" (yikes) imports: `from . import quux` or `from .quux import somefunc` explicitly means to look for a sibling named `quux`.  (You can also use `..quux` to look in the parent package, three dots to look in the grandparent, etc.)

The explicit syntax is supported since Python 2.5.  The old sibling behavior can be _disabled_ since Python 2.5 with `from __future__ import absolute_import`.

`futurize --stage1` has a `libfuturize.fixes.fix_absolute_import` fixer, which attempts to detect sibling imports and convert them to explicit relative imports.  If it finds any sibling imports, it'll also add the `__future__` line, though honestly you should make an effort to to put that line in _all_ of your Python 2 code.

It's possible for the `futurize` fixer to guess wrong about a sibling import, but in general it works pretty well.

(There _is_ one case I've run across where simply replacing `import sibling` with `from . import sibling` didn't work.  Unfortunately, it was Yelp code that I no longer have access to, and I can't remember the precise details.  It involved having several sibling imports inside a `__init__.py`, where the siblings also imported from each other in complex ways.  The sibling imports worked, but the explicit relative imports failed, for some really obscure timing reason.  It's even possible this was a 2.6 bug that's been fixed in 2.7.  If you see it, please let me know!)


## Things that require some effort

These problems are a little more obscure, but many of them are also more difficult to fix automatically.  If you have a massive codebase, these are where the problems start to appear.

### The grand module shuffle

A whole bunch of modules were deleted, merged, or removed.  A full list is in [PEP 3108](https://www.python.org/dev/peps/pep-3108/), but you'll never have heard of most of them.  Here are the ones that might affect you.

- `__builtin__` has been renamed to `builtins`.  Note that this is a module, _not_ the `__builtins__` attribute _of_ modules, which is exactly why it was renamed.  Incidentally, you should be using the `builtins` module rather than `__builtins__` anyway.  Or, wait, no, just don't use either, please don't mess with the built-in scope.

- `ConfigParser` has been renamed to `configparser`.

- `Queue` has been renamed to `queue`.

- `SocketServer` has been renamed to `socketserver`.

- `cStringIO` and `StringIO` are gone; instead, use `StringIO` or `BytesIO` from the `io` module.  Note that these also exist in Python 2, but are pure-Python rather than the C versions in current Python 3.

- `cPickle` is gone.  Importing `pickle` in Python 3 now gives you the C implementation automatically.

- `cProfile` is gone.  Importing `profile` in Python 3 gives you the C implementation automatically.

- `copy_reg` has been renamed to `copyreg`.

- `anydbm`, `dbhash`, `dbm`, `dumbdm`, `gdbm`, and `whichdb` have all been merged into a `dbm` package.

- `dummy_thread` has become `_dummy_thread`.  It's an implementation of the `_thread` module that doesn't actually do any threading.  You should be using `dummy_threading` instead, I guess?

- `httplib` has become `http.client`.  `BaseHTTPServer`, `CGIHTTPServer`, and `SimpleHTTPServer` have been merged into a single `http.server` module.  `Cookie` has become `http.cookies`.  `cookielib` has become `http.cookiejar`.

- `repr` has been renamed to `reprlib`.  (The module, not the built-in function.)

- `thread` has been renamed to `_thread`, and you should really be using the `threading` module instead.

- A whole mess of top-level Tk modules have been combined into a `tkinter` package.

- The contents of `urllib`, `urllib2`, and `urlparse` have been consolidated and then split into `urllib.error`, `urllib.parse`, and `urllib.request`.

- `xmlrpclib` has become `xmlrpc.client`.  `DocXMLRPCServer` and `SimpleXMLRPCServer` have been merged into `xmlrpc.server`.

`futurize --stage2` will fix this with the somewhat invasive `libfuturize.fixes.fix_future_standard_library` fixer, which uses a mechanism from `future` that adds aliases to Python 2 to make all the Python 3 standard library names work.  It's an interesting idea, but it didn't actually work for all cases when I tried it (though now I can't recall what was broken), so YMMV.

Alternative, you could manually replace any affected imports with imports from [`six.moves`](https://pythonhosted.org/six/#module-six.moves), which provides aliases that work on either version.

Or as a last resort, you can just sprinkle `try ... except ImportError` around.


### Built-in iterators are now lazy

`filter`, `map`, `range`, and `zip` are all lazy in Python 3.  You can still iterate over their return values (once), but if you have code that expects to be able to index them or traverse them more than once, it'll break in Python 3.  (Well, not `range`, that's fine.)  The lazy equivalents — `xrange` and the functions in `itertools` — are of course gone in Python 3.

In either case, the easiest thing to do is force eager evaluation by wrapping the call in `list()` or `tuple()`, which you'll occasionally need to do in Python 3 regardless.

For the sake of consistency, you may want to import the lazy versions from the standard library [`future_builtins`](https://docs.python.org/2/library/future_builtins.html) module.  It only exists in Python 2, so be sure to wrap the import in a `try`.

`futurize --stage2` tries to address this with several of `lib2to3`'s fixers, but the results aren't particularly pleasing: calls to all four are unconditionally wrapped in `list()`, even in an obviously safe case like a `for` block.  I'd just look through your uses of them manually.

A more subtle point: if you pass a string or tuple to Python 2's `filter`, the return value will be the same type.  Blindly wrapping the call in `list()` will of course change the behavior.  Filtering a _string_ is not a particularly common thing to do, but I've seen someone complain about it before, so take note.

Also, Python 3's `map` stops at the shortest input sequence, whereas Python 2 extends shorter sequences with `None`s.  You can fix this with `itertools.zip_longest` (which in Python 2 is `izip_longest`!), but honestly, I've never even seen anyone pass multiple sequences to `map`.

Relatedly, `dict.iteritems` (plus its friends, `iterkeys` and `itervalues`) is gone in Python 3, as the plain `items` (plus `keys` and `values`) is already lazy.  The `dict.view*` methods are also gone, as they were only backports of Python 3's normal behavior.

Both `six` and `future.utils` contain functions called `iteritems`, etc., which provide a lazy iterator in both Python 2 and 3.  They also offer `view*` functions, which are closer to the Python 3 behavior, though I can't say I've ever seen anyone actually use `dict.viewitems` in real code.

Of course, if you explicitly want a list of dictionary keys (or items or values), `list(d)` and `list(d.items())` do the same thing in both versions.


### `buffer` is gone

The `buffer` type has been replaced by `memoryview` (also in Python 2.7), which is similar but not identical.  If you've even heard of either of these types, you probably know more about the subtleties involved than I do.  There's a `lib2to3.fixes.fix_buffer` fixer that blindly replaces `buffer` with `memoryview`, but `futurize` doesn't use it in either stage.


### Several special methods were renamed

Where Python 2 has `__str__` and `__unicode__`, Python 3 has `__bytes__` and `__str__`.  The trick is that `__str__` should return the native `str` type for each version: a bytestring for Python 2, but a Unicode string for Python 3.  Also, you almost certainly don't want a `__bytes__` method in Python 3, where `bytes` is no longer used for text.

Both six and python-future have a `python_2_unicode_compatible` class decorator that tries to do the right thing.  You write only a single `__str__` method that returns a _Unicode_ string.  In Python 3, that's all you need, so the decorator does nothing; in Python 2, the decorator will rename your method to `__unicode__` and add a `__str__` that returns the same value encoded as UTF-8.  If you need different behavior, you'll have to roll it yourself with `if PY2`.

----

Python 2's `next` method is more appropriately `__next__` in Python 3.  The easy way to address this is to call your method `__next__`, then alias it with `next = __next__`.  _Be sure_ you never call it directly as a method, only with the built-in `next()` function.

Alternatively, `future.builtins` contains an alternative `next` which always calls `__next__`, but on Python 2, it falls back to trying `next` if `__next__` doesn't exist.

`futurize --stage1` changes all use of `obj.next()` to `next(obj)` via the `libfuturize.fixes.fix_next_call` fixer.  `futurize --stage2` renames `next` methods to `__next__` via the `lib2to3.fixes.fix_next` fixer (which also fixes calls).  Note that there's a remote chance of false positives, if for some reason you happened to use `next` as a regular method name.

----

Python 2's `__nonzero__` is Python 3's `__bool__`.  Again, you can just alias it manually.  Or `futurize --stage2` will rename it with the `lib2to3.fixes.fix_nonzero` fixer.

Renaming it will of course break it in Python 2, but `futurize --stage2` also has a `libfuturize.fixes.fix_object` fixer that imports python-future's own `builtins.object`.  The replacement `object` class has a few methods for making Python 3's `__str__`, `__next__`, and `__bool__` work on Python 2.

This is one of the mildly invasive things python-future does, and it may or may not sit well.  Up to you.

----

`__long__` is completely gone, as there is no `long` type in Python 3.

`__getslice__`, `__setslice__`, and `__delslice__` are gone.  Instead, slice objects are passed to `__getitem__` and friends.  On the off chance you use these, you'll have to do something clever in the `item` methods to defer to your slice logic on Python 3.

`__oct__` and `__hex__` are gone; `oct()` and `hex()` now consult `__index__`.  I seriously doubt this will impact anyone.

`__div__` is gone, as mentioned previously.


### Unbound methods are gone; function attributes renamed

Say you have this useless class.

```python
class Foo(object):
    def bar(self):
        pass
```

In Python 2, `Foo.bar` is an "unbound method", a type that's generally unseen and unexposed other than as `types.MethodType`.  In Python 3, `Foo.bar` is just a regular function.

Offhand, I can only think of one time this would matter: if you want to get at attributes on the function, perhaps for the sake of a method decorator.  In Python 2, you have to go through the unbound method's `.im_func` attribute to get the original function, but in Python 3, you already have the original function and can get the attributes directly.

If you're doing this anywhere, an easy way to make it work in both versions is:

```python
method = Foo.bar
method = getattr(method, 'im_func', method)
```

As for bound methods (the objects you get from accessing methods but not calling them, like `[].append`), the `im_self` and `im_func` attributes have been renamed to `__self__` and `__func__`.  Happily, these names also work in Python 2.6, so no compatibility hacks are necessary.

`im_class` is completely _gone_ in Python 3.  Methods have no interest in which class they're attached to.  They _can't_, since the same function could easily be attached to more than one class.  If you're relying on `im_class` somehow, for some reason...  well, don't do that, maybe.

Relatedly, the `func_*` function attributes have been renamed to dunder names in Python 3, since assigning function attributes is a fairly common practice and Python doesn't like to clog namespaces with its own builtin names.  `func_closure`, `func_code`, `func_defaults`, `func_dict`, `func_doc`, `func_globals`, and `func_name` are now `__closure__`, `__code__`, etc.  (Note that `func_doc` and `func_name` were already aliases for `__doc__` and `__name__`, and `func_defaults` is much more easily inspected with [the `inspect` module](https://docs.python.org/3/library/inspect.html).)  The new names are **not** available in Python 2, so you'll need to do a `getattr` dance, or use [the `get_function_*` functions from `six`](https://pythonhosted.org/six/#object-model-compatibility).


### Metaclass syntax has changed

In Python 2, a metaclass is declared by assigning to a special name in the class body:

```python
class Foo(object):
    __metaclass__ = FooMeta
    ...
```

Admittedly, this doesn't make a lot of sense.  The metaclass affects how a class is created, and the class body is evaluated as part of that creation, so this is sort of a goofy hack.

Python 3 changed this, opening the door to a few new neat tricks in the process, which you can find out about in [the companion article]({filename}2016-07-31-python-faq-why-should-i-use-python-3.markdown).

```python
class Foo(object, metaclass=FooMeta):
    ...
```

The catch is finding a way to express this idea in both Python 2 and Python 3 — the old syntax is ignored in Python 3, and the new syntax is a syntax error in Python 2.

It's a bit of a pain, but the `class` statement is really just a lot of sugar for calling the `type()` constructor; after all, Python classes are just instances of `type`.  All you have to do is manually create an instance of your metaclass, rather than of `type`.

Fortunately, other people have already made this work for you.  `futurize --stage2` will fix this using the `libfuturize.fixes.fix_metaclass` fixer, which imports `future.utils.with_metaclass` and produces the following:

```python
from future.utils import with_metaclass

class Foo(with_metaclass(object)):
    ...
```

This creates an intermediate dummy class with the right metaclass, which you then inherit from.  Classes use the same metaclass as their parents, so this works fine in any Python.

If you don't want to depend on python-future, the same function exists in the `six` module.


### Re-raising exceptions has different syntax

`raise` with no arguments does the same thing in Python 2 and Python 3: it re-raises the exception currently being handled, preserving the original traceback.

The problem comes in with the three-argument form of `raise`, which is for preserving the traceback while raising a _different_ exception.  It might look like this:

```python
try:
    some_fragile_function()
except Exception as e:
    raise MyLibraryError, MyLibraryError("Failed to do a thing: " + str(e)), sys.exc_info()[2]
```

`sys.exc_info()[2]` is, of course, the only way to get the current traceback in Python 2.  You may have noticed that the three arguments to `raise` are the same three things that `sys.exc_info()` returns: the type, the value, and the traceback.

Python 3 introduces exception _chaining_.  If something raises an exception from within an `except` block, Python will _remember_ the original exception, attach it to the new one, and show _both_ exceptions when printing a traceback — including both exceptions' types, messages, and where they happened.  So to wrap and rethrow an exception, you don't need to do anything special at all.

```python
try:
    some_fragile_function()
except Exception:
    raise MyLibraryError("Failed to do a thing")
```

For more complicated handling, you can also explicitly say `raise new_exception from old_exception`.  Exceptions contain their associated tracebacks as a `__traceback__` attribute in Python 3, so there's no need to muck around getting the traceback manually.  If you really want to give an explicit traceback, you can use the `.with_traceback()` method, which just assigns to `__traceback__` and then returns `self`.

```python
raise MyLibraryError("Failed to do a thing").with_traceback(some_traceback)
```

It's hard to say what it even means to write code that works "equivalently" in both versions, because Python 3 handles this problem largely automatically, and Python 2 code tends to have a variety of ad-hoc solutions.  Note that you _cannot_ simply do this:

```python
if PY3:
    raise MyLibraryError("Beep boop") from exc
else:
    raise MyLibraryError, MyLibraryError("Beep boop"), sys.exc_info()[2]
```

The first `raise` is a syntax error in Python 2, and the second is a syntax error in Python 3.  `if` won't protect you from parse errors.  (On the other hand, you can hide `.with_traceback()` behind an `if`, since that's just a regular method call and will parse with no issues.)

`six` has [a `reraise` function](https://pythonhosted.org/six/#six.reraise) that will smooth out the differences for you (probably by using `exec`).  The drawback is that it's of course Python 2-oriented syntax, and on Python 3 the final traceback will include more context than expected.

Alternatively, there's a [`six.raise_from`](https://pythonhosted.org/six/#six.raise_from), which is designed around the `raise X from Y` syntax of Python 3.  The drawback is that Python 2 has no obvious equivalent, so you just get `raise X`, losing the old exception and its traceback.

There's no clear right approach here; it depends on how you're handling re-raising.  Code that just blindly raises new exceptions doesn't need any changes, and will get exception chaining for free on Python 3.  Code that does more elaborate things, like implementing its own form of chaining or storing `exc_info` tuples to be re-raised later, may need a little more care.


### Bytestrings are sequences of integers

In Python 2, `bytes` is a synonym for `str`, the default string type.  Iterating or indexing a `bytes`/`str` produces 1-character `str`s.

```python
list(b'hello')  # ['h', 'e', 'l', 'l', 'o']
b'hello'[0:4]  # 'hell'
b'hello'[0]  # 'h'
b'hello'[0][0][0][0][0]  # 'h' -- it's turtles all the way down
```

In Python 3, `bytes` is a specialized type for handling binary data, _not text_.  As such, iterating or indexing a `bytes` produces _integers_.

```python
list(b'hello')  # [104, 101, 108, 108, 111]
b'hello'[0:4]  # b'hell'
b'hello'[0]  # 104
b'hello'[0][0][0][0]  # TypeError, since you can't index 104
```

If you have explicitly binary data that want to be `bytes` in Python 3, this may pose a bit of a problem.  Aside from just checking the version explicitly and making heavy use of `chr`/`ord`, there are two approaches.

One is to use `bytearray` instead.  This is like `bytes`, but mutable.  More importantly, since it was introduced as a new type in Python 2.6 — _after_ Python 3.0 came out — it has the same iterating and indexing behavior as Python 3's `bytes`, even in Python 2.

```python
bytearray(b'hello')[0]  # 104, on either Python 2 or 3
```

The other is to _slice_ rather than index, since slicing always produces a new iterable of the same type.  If you want to extract a single character from a `bytes`, just take a one-element slice.

```python
b'hello'[0]  # 104
b'hello'[0:1]  # b'h'
```


## Things that are just a royal pain in the ass

### Unicode

Saving the best for last, almost!

Honestly, if your Python 2 code is already careful with Unicode — working with `unicode` internally, and encoding/decoding only at the "boundaries" of your code — then you shouldn't have too many problems.  If your code is not so careful, you should really try to make it a little more careful before you worry about Python 3, since Python 3's whole jam is to force you to be careful.

See, in Python 2, you can combine bytestrings (`str`) and text strings (`unicode`) more or less freely.  Python will automatically try to convert between the two using the "default encoding", which is generally `ascii`.  Python 3 makes text strings the default string type, demotes bytestrings, and forbids ever converting between them.

Most obviously, Python 2's `str` and `unicode` have been renamed to `bytes` and `str` in Python 3.  If you happen to be using the names anywhere, you'll probably need to change them!  `six` offers [`text_type`](https://pythonhosted.org/six/#six.text_type) and [`binary_type`](https://pythonhosted.org/six/#six.binary_type), though you can just use `bytes` to mean the same thing in either version.  python-future also has backports for both Python 3's `bytes` and `str` types, which seems like an extreme approach to me.  Changing `str` to mean a text type even in Python 2 might be a good idea, though.

`b''` and `u''` work the same way in either Python 2 or 3, but unadorned strings like `''` are always the `str` type, which has different behavior.  There is a `from __future__ import unicode_literals`, which will cause unadorned strings to be `unicode` in Python 2, and this _might_ work for you.  However, this prevents you from writing literal "native" strings — strings of the same type Python uses for names, keyword arguments, etc.  Usually this won't matter, since Python 2 will silently convert between bytes and text, but it's caused me the occasional problem.

The right thing to do is just explicitly mark every single string with either a `b` or `u` sigil as necessary.  That just, you know, sucks.  But you should be doing it even if you're not porting to Python 3.

`basestring` is completely gone in Python 3.  `str` and `bytes` have no common base type, and their semantics are different enough that it rarely makes sense to treat them the same way.  If you're using `basestring` in Python 2, it's probably to allow code to work on either form of "text", and you'll only want to use `str` in Python 3 (where `bytes` are completely unsuitable for text).  [`six.string_types`](https://pythonhosted.org/six/#six.string_types) provides exactly this.  `futurize --stage2` also runs the `lib2to3.fixes.fix_basestring` fixer, but this _replaces_ `basestring` with `str`, which will almost certainly _break_ your code in Python.  If you intend to use stage 2, definitely audit your uses of `basestring` first.

As mentioned above, bytestrings are sequences of integers, which may affect code trying to work with explicitly binary data.

Python 2 has both `.decode()` and `.encode()` on both bytes and text; if you try to encode bytes or decode text, Python will try to implicitly convert to the right type first.  In Python 3, only text has an `.encode()` and only bytes have a `.decode()`.

Relatedly, Python 2 allows you to do some cute tricks with "encodings" that aren't really encodings; for example, `"hi".encode('hex')` produces `'6869'`.  In Python 3, encoding _must_ produce bytes, and decoding _must_ produce text, so these sorts of text-to-text or bytes-to-bytes translations aren't allowed.  You can still do them explicitly with the `codecs` module, e.g. `codecs.encode(b'hi', 'hex')`, which also works in Python 2, despite being undocumented.  (Note that Python 3 specifically requires bytes for the hex codec, alas.  If it's any consolation, there's a `bytes.hex()` method to do this directly, which you can't use anyway if you're targeting Python 2.)

Python 3's `open` decodes as UTF-8 by default (a vast oversimplification, but _usually_), so if you're manually decoding after reading, you'll get an error in Python 3.  You could explicitly open the file in binary mode (preserving the Python 2 behavior), or you could use [`codecs.open`](https://docs.python.org/3/library/codecs.html#codecs.open) to decode transparently on read (preserving the Python 3 behavior).  The same goes for writing.

`sys.stdin`, `sys.stdout`, and `sys.stderr` are all text streams in Python 3, so they have the same caveats as above, with the additional wrinkle that you didn't actually open them yourself.  Their `.buffer` attribute gives a handle opened in binary mode (Python 2 behavior), or you can adapt them to transcode transparently (Python 3 behavior):

```python
if six.PY2:
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
```

A text-mode file's `.tell()` in Python 3 still returns a number that can be passed back to `.seek()`, but the number is not necessarily meaningful, and in particular can't be used to estimate progress through a file.  (Python uses a few very high bits as flags to indicate the state of the decoder; if you mask them off, what's left is _probably_ the byte position in the file as you'd expect, but this is pretty definitively a hack.)

Python 3 likes to treat filenames as text, but most of the functions in `os` and `os.path` will accept _either_ text or bytes as their arguments (and return a value of the same type), so you should be okay there.

`os.environ` has text keys and values in Python 3.  If you direly need bytes, you can use `os.environb` (and `os.getenvb()`).

I think that covers most of the obvious basics.  This is a whole sprawling topic that I can't hope to cover off the top of my head.  I've seen it be both fairly painful and completely pain-free, depending entirely on the state of the Python 2 codebase.

Oh, one final note: there's a module for Python 2 called [unicode-nazi](https://pypi.python.org/pypi/unicode-nazi) (sorry, I didn't name it) that will produce a warning anytime a bytestring is implicitly converted to a text string, or vice versa.  It might help you root out places you're accidentally slopping types back and forth, which will certainly break in Python 3.  I've only tried it on a comically large project where it found _thousands_ of violations, including plenty in surprising places in the standard library, so it may or may not be of any practical help.


## Things that are not actually gone

### String formatting with `%`

There's a widespread belief that `str % ...` is deprecated, since there's a newer and shinier `str.format()` method.

Well, it's not.  It's not gone; it's not deprecated; it still works just fine.  I don't like to use it, myself, since it's easy to make accidentally ambiguous — `"%s" % foo` can crash if `foo` is a tuple! — but it's not going anywhere.  In fact, as of Python 3.5, [`bytes` and `bytearray` support `%`](https://docs.python.org/3/whatsnew/3.5.html#pep-461-percent-formatting-support-for-bytes-and-bytearray) but _not_ `.format`.

### `optparse`

[`argparse`](https://docs.python.org/3/library/argparse.html) is certainly better, but the `optparse` module still exists in Python 3.  It _has_ been deprecated since Python 3.2, though.


## Things that are preposterously obscure but that I have seen cause problems nonetheless

### Tuple unpacking

A little-used feature of Python 2 is tuple unpacking in function arguments:

```python
def foo(a, (b, c)):
    print a, b, c

x = (2, 3)
foo(1, x)
```

This syntax is gone in Python 3.  I've rarely seen anyone use it, except in two cases.  One was a parsing library that relied pretty critically on using it in every parsing function you wrote; whoops.

The other is when sorting a dict's items:

```python
sorted(d.items(), key=lambda (k, v): k + v)
```

In Python 3, you have to write that as `lambda kv: kv[0] + kv[1]`.  Boo.

### `long` is gone

Python 3 merged its `long` type with `int`, so now there's only one integral type, called `int`.

Python 2 promotes `int` to `long` pretty much transparently, and `long`s aren't very common in the first place, so it's fairly unlikely that this will make a difference.  On the off chance you're type-checking for integers with `isinstance(x, (int, long))` (and really, why are you doing that), you can just use [`six.integer_types`](https://pythonhosted.org/six/#six.integer_types) instead.

Note that `futurize --stage2` applies the `lib2to3.fixes.fix_long` fixer, which blindly renames `long` to `int`, leaving you with inappropriate code like `isinstance(x, (int, int))`.

_However..._

I _have_ seen some very obscure cases where a hand-rolled binary protocol would encode `int`s and `long`s _differently_.  My advice would be to not do that.

Oh, and a little-known feature of Python 2's syntax is that you can have `long` _literals_ by suffixing them with an `L`:

```python
123  # int
123L  # long
```

You can write `1267650600228229401496703205376` directly in Python 2 code, and it'll automatically create a `long`, so the only reason to do this is if you explicitly need a `long` with a small value like 1.  If that's the case, something has gone catastrophically wrong.


### `repr` changes

These should really only affect you if you're using `repr`s as expected test output (or, god forbid, as cache keys or something).  Some notable changes:

- Unicode strings have a `u` prefix in Python 2.  In Python 3, of course, Unicode strings are just _strings_, so there's no prefix.

- Conversely, bytestrings have a `b` prefix in Python 3, but not in Python 2 (though the `b` prefix is allowed in source code).

- Python 2 escapes all non-ASCII characters, even in the `repr` of a Unicode string.  Python 3 only escapes control characters and codepoints considered non-printing.

- Large integers and explicit `long`s have an `L` suffix in Python 2, but not in Python 3, where there is no separate `long` type.

- A `set` becomes `set([1, 2, 3])` in Python 2, but `{1, 2, 3}` in Python 3.  The set literal syntax is allowed in source code in Python 2.7, but the `repr` wasn't changed until 3.0.

- `float`s stringify to the shortest possible representation that has the same underlying value — e.g., `str(1.1)` is `'1.1'` rather than `'1.1000000000000001'`.  This change was backported to Python 2.7 as well, but _I have seen it break tests_.


### Hash randomization

Python has traditionally had a predictable hashing mechanism: `repr(dict(a=1, b=2, c=3))` will always produce the same string.  (On the same platform with the same Python version, at least.)  Unfortunately this opens the door to an obscure DoS exploit that was known to Perl long ago: if you know a web application is written in Python, you can construct a query string that will become a dict whose keys all go in the same hash bucket.  If your query string is long enough and you send enough requests, you can tie up all the Python processes in dealing with hash collisions.

The fix is hash _randomization_, which seeds the hashing algorithm in such a way that items are bucketed differently every time Python runs.  It's available in Python 2.7 via an environment variable or the `-R` argument, but it wasn't turned on by default until Python 3.3.

The fear was that it might break things.  Naturally, it has broken things.  Mostly, `repr`s in tests.  But it also changes the iteration order of dicts between Python runs.  I have seen code using dicts whose keys _happened_ to always be sorted in alphabetical or insertion order before, but with hash randomization, the keys were of course in a different order every time the code ran.  The author assumed that Python had somehow broken dict sorting (which it has never had).


### `nonlocal`

Python 3 introduces the `nonlocal` keyword, which is like `global` except it looks through _all_ outer scopes in the expected order.  It fixes this mild annoyance:

```python
def make_function():
    counter = 0
    def function():
        nonlocal counter
        counter += 1  # without 'nonlocal', this declares a new local!
        print("I've been called", counter, "times!")
    return function
```

The problem is that any use of assignment within a function automatically creates a new local, and locals are known statically for the entire body of the function.  (They actually affect how functions are compiled, in CPython.)  So without `nonlocal`, the above code would see `counter += 1`, but `counter` is a _new local_ that has never been assigned a value, so Python cannot possibly add 1 to it, and you get an `UnboundLocalError`.

`nonlocal` tells Python that when it sees an assignment of a name that exists in some outer scope, it should reuse that outer variable rather than shadowing it.  Great, right?  Purely a new feature.  No problem.

Unfortunately, I've worked on a codebase that needed this feature in Python 2, and decided to fake it with a class...  _named `nonlocal`_.

```python
def make_function():
    class nonlocal:
        counter = 0
    def function():
        nonlocal.counter += 1  # this alters an outer value in-place, so it's fine
        print("I've been called", counter, "times!")
    return function
```

The class here is used purely as a dummy container.  Assigning to an _attribute_ doesn't create any locals, because it's equivalent to a method call, so the operand must already exist.  This is a slightly quirky approach, but it works fine.

Except that, of course, `nonlocal` is a keyword in Python 3, so this becomes complete gibberish.  It's _such_ gibberish that (if I remember correctly) `2to3` actually _cannot parse it_, even though it's perfectly valid Python 2 code.

I don't have a magical fix for this one.  Just, uh, don't name things `nonlocal`.


### List comprehensions no longer leak

Python 2 has the slightly inconsistent behavior that loop variables in a generator expression (`(...)`) are scoped to the generator expression, but loop variables in a list comprehension (`[...]`) belong to the enclosing scope.

The only reason is in implementation details: a list comprehension acts like a `for` loop, which has the same behavior, whereas a generator expression actually creates a generator internally.

Python 3 brings these cases into line: loop variables in list comprehensions (or dict or set comprehensions) are also scoped to the comprehension itself.

I cannot imagine any possible reason why this would affect you negatively, and yet, I can swear I've seen it happen.  I wish I could remember where, because I'm sure it's an exciting story.


### `cStringIO.h` is gone

`cStringIO.h` is a private and undocumented C interface to Python 2's `cStringIO.StringIO` type.  It was removed in Python 3, or at least is somewhere I can't find it.

This was one of the reasons Thrift's Python 3 port [took almost 3 years](https://issues.apache.org/jira/browse/THRIFT-1857): Thrift has a "fast" C module that makes use of this private interface, and it's not obvious how to replace it.  I think they ended up just having the module not exist on Python 3, so Python 3 will just be mysteriously slower.


## Some troublesome libraries

[MySQLdb](http://mysql-python.sourceforge.net/) is some ancient, clunky, noncompliant, underdocumented trash, much like the database it connects to.  It's nigh abandoned, though it still promises Python 3 support in the MySQLdb 2.0 vaporware.  I would suggest not using MySQL, but barring that, try [mysqlclient](https://github.com/PyMySQL/mysqlclient-python), a fork of MySQLdb that continues development and adds Python 3 support.  (The same people also maintain an earlier project, [pymysql](https://github.com/PyMySQL/PyMySQL), which strives to be a pure-Python drop-in replacement for MySQLdb — it's not quite perfect, but its existence is interesting and it's sure easier to read than MySQLdb.)

At a glance, [Thrift](https://github.com/apache/thrift) still hasn't had a release since it merged Python 3 support, eight months ago.  It's some enterprise nightmare, anyway, and bizarrely does code generation for a bunch of dynamic languages.  Might I suggest just using the pure-Python [thriftpy](https://github.com/eleme/thriftpy), which parses Thrift definitions on the fly?

[Twisted](https://twistedmatrix.com/) is, ah, large and complex.  Parts of it now support Python 3; parts of it do not.  If you need the parts that don't, well, maybe you could [give them a hand](http://twistedmatrix.com/trac/wiki/ContributingToTwistedLabs)?

[M2Crypto](https://pypi.python.org/pypi/M2Crypto) is [working on it](https://gitlab.com/m2crypto/m2crypto/issues/114), though I'm pretty sure most Python crypto nerds would advise you to use [`cryptography`](https://pypi.python.org/pypi/cryptography) instead.


## And so on

You may find any number of other obscure compatibility problems, just as you might when upgrading from 2.6 to 2.7.  The Python community has a lot of clever people willing to help you out, though, and they've probably even seen your super duper niche problem before.

Don't let that, or this list of gotchas in general, dissaude you!  Better to start now than later; even fixing an integer division gets you one step closer to having your code run on Python 3 as well.
