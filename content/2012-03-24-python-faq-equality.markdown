title: Python FAQ: Equality
date: 2012-03-24 23:15
category: articles
series: python faq
tags: python, tech

Part of my [Python FAQ][].

**What does `is` do? Should I use `is` or `==`?**

<!-- more -->

These operators tend to confuse Python newcomers, perhaps because `is` doesn't have a clear equivalent in very many other languages.  Some particular quirks of Python's canon implementation make it difficult to figure out by experimentation, as well.

The simple answer is:

* `==` tests whether two objects have the same value.
* `is` tests whether two objects are _the same object_.

What does "the same value" mean?  It really depends on the objects' types; usually it means that both objects will respond the same way to the same operations, but ultimately the author of a class gets to decide.

On the other hand, no matter how similar two objects may look or act, `is` can always tell them apart.  Did you call `SomeClass()` twice?  Then you have two objects, and `a is b` will be `False`.

## Overloading

There's another critical, but subtle, difference: **`==` can be overloaded, but `is` cannot**.  Both the `__eq__` and `__cmp__` special methods allow a class to decide for itself what equality means.

Because those methods are regular Python code, they can do anything.  An object might not be equal to itself.  It might be equal to everything.  It might randomly decide whether to be equal or not.  It might return `True` for _both_ `==` and `!=`.

Hopefully no real code would do such things, but the point is that it _can_ happen.  `==` on an arbitrary object may be unreliable; `is` never will be.  More on why you might care about this below.

When Python sees `a == b`, it tries the following.

1. If `type(b)` is a new-style class, _and_ `type(b)` is a subclass of `type(a)`, _and_ `type(b)` has overridden `__eq__`, then the result is `b.__eq__(a)`.
2. If `type(a)` has overridden `__eq__` (that is, `type(a).__eq__` isn't `object.__eq__`), then the result is `a.__eq__(b)`.
3. If `type(b)` has overridden `__eq__`, then the result is `b.__eq__(a)`.
4. If none of the above are the case, Python repeats the process looking for `__cmp__`.  If it exists, the objects are equal iff it returns zero.
5. As a final fallback, Python calls `object.__eq__(a, b)`, which is `True` iff `a` and `b` are the same object.

If any of the special methods return `NotImplemented`, Python acts as though the method didn't exist.

Note that last step carefully: if neither `a` nor `b` overloads `==`, then `a == b` is the same as `a is b`.


## When to use which

There are actually very few cases where you want to use `is`.  The most common by far is for setting default arguments:

```python
def foo(arg=None):
    if arg is None:
        arg = []

    # ...
```

Why use `is` here?  It does read more like English, and `None` is guaranteed to be a singleton object.  A better reason is slightly more insidious: operator overloading!  If `arg` happened to overload equality, it might claim to be equal to `None`.  That would be some egregious misbehavior, sure, but no reason not to be correct when you can.

Sometimes `None` might already have a special meaning to your function—perhaps to mean `null` in JSON or SQL.  If you wrote such a function the way I did above, nobody could pass `None` to it; it would get replaced by your default.  How can you make an argument optional if `None` is a real value?  `is` can help here, too.

```python
unspecified = object()
def foo2(arg=unspecified):
    if arg is unspecified:
        arg = make_default_object()

    # ...
```

Here `unspecified` is just a dummy object containing no data and having no behavior.  The only useful property it has is that, if `arg is unspecified`, then you know `arg` _must be_ that exact same object.  It has no meaning, so it's a perfectly safe default; it won't prevent the caller from passing in some particular object you wanted to use as a sentinel.

`==` would work the same way, of course, but it has the same caveat as `arg == None`: bad overloading.  Using `is` also better expresses your `intention`, which is that you want to test for this particular object and no other.

In general, you want `==` most of the time.  `is` is only useful when you are absolutely sure you want to check that you have the same object with two different names.


## `is` and builtins

A common pitfall is to pull out the Python REPL and try something like the following:

```python
>>> 2 == 2
True
>>> 2 is 2
True
>>> "x" == "x"
True
>>> "x" is "x"
True
>>> int("133") is int("133")
True
```

Hang on, what's going on here?  Those are separate numbers and separate strings, and even separate calls to `int()`; why are they claiming to be the same object?

There are a _lot_ of strings in any given Python program containing, say, `__init__`.  (One for every constructor, in fact!)  There are also a _lot_ of small numbers, like `0` and `-1`.  Strictly speaking, every time one of these appears, Python would need to create a new object, and that eats a lot of memory.  Finding a method on a class would require comparing strings byte-by-byte, and that eats a lot of time.

So CPython (the canonical Python interpreter, written in C) has a behind-the-scenes optimization called _interning_.  Small integers and some strings are cached: the integer `2` will always refer to the same object, no matter how it comes into existence.

Interning is _not_ strictly part of the language, and other Python implementations may or may not do it.  The language allows for any immutable object to be interned, but otherwise says nothing.  For this reason, absolutely **do not use `is` on the built-in immutable types.**  The results are basically meaningless because of interning!

One last wrinkle.  When CPython compiles a chunk of code (a "compilation unit"), it has to create objects to represent literals it sees.  (Literals are objects that have native Python syntax: numbers, strings, lists that use `[]`, etc.)  In the case of numbers and strings, literals with the same value become the _same object_, whether interned or not.

With that in mind, the REPL's treatment of `is` should make more sense:

```python
# Interned ints
>>> 100 is 100
True
# Non-interned ints, but compiled together, so still the same object
>>> 99999 is 99999
True
# Non-interned ints, compiled /separately/, so different objects
>>> a = 99999
>>> b = 99999
>>> a is b
False
# Interned ints are the same object no matter where they appear
>>> a = 3
>>> b = 3
>>> c = 6 / 2
>>> a is b
True
>>> a is c
True
# Floats are never interned, but these are compiled together, so are still the
# same object
>>> 1.5 is 1.5
True
# Strings are similar to ints
>>> "foo" is "foo"
True
>>> a = "foo"
>>> b = "foo"
>>> a is b
True
>>> "the rain in spain falls mainly on the plain" is "the rain in spain falls mainly on the plain"
True
>>> a = "the rain in spain falls mainly on the plain"
>>> b = "the rain in spain falls mainly on the plain"
>>> a is b
False
# Two different lists; they're mutable so they can't be the same object
>>> [] is []
False
# Two different dicts; same story
>>> {} is {}
False
# Tuples are immutable, but their contents can be mutable, so they don't get
# the optimization either
>>> (1, 2, 3) is (1, 2, 3)
False
```

(By the way, if you really must know: CPython interns all `int`s between `-5` and `256`, inclusive.)


## Conclusion

* Most of the time, you want `==`.
* Use `arg is None` when you have a function with an argument defaulting to `None`.  That's okay, because there's only one `None`.
* For testing whether two classes, functions, or modules are the same object, `is` is okay.  Stylistic choice.
* **Never** use `is` with `str`, `int`, `float`, `complex`, or any other core immutable value type!  Interning makes the response worthless!
* Other valid uses of `is` are fairly rare and obscure, for example:
    * If I have a large tree structure and want to find the location of a subtree, `==` will recursively compare values (potentially very slow) but `is` will tell me if I've found the exact same node.
    * A caching mechanism may want to treat all objects as distinct, without having to care about or rely on how they implement `==`.  `is` can be appropriate here.
    * Demonstrating to newbies that interning exists is only possible with `is`  :)

To summarize even further: don't use `is` unless you're comparing with `None` or you really, really mean it.  And you don't.


## Further reading

* The Python Language Reference has a [data model section][Python data model] which documents the possibility of caching immutable values, [how `__eq__` works][__eq__], and [how operator overloading works][coercion] in general.
* [The Python C API][PyInt_FromLong] is the only documentation of what ints are interned.


[PyInt_FromLong]: http://docs.python.org/c-api/int.html#PyInt_FromLong
[Python FAQ]: /blog/2011/07/22/python-faq/
[__eq__]: http://docs.python.org/reference/datamodel.html#object.__eq__
[Python data model]: http://docs.python.org/reference/datamodel.html
[coercion]: http://docs.python.org/reference/datamodel.html#coercion-rules
