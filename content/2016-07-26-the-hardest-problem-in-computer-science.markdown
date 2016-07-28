title: The hardest problem in computer science
date: 2016-07-26 18:46
category: blog
tags: tech, plt

...is, of course, naming.

Not just naming variables or new technologies.  Oh no.  We can't even agree on names for basic concepts.

<!-- more -->

## A thousand overlapping vernaculars

Did you know that [the C specification](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf) makes frequent reference to "objects"?  Not in the OO sense as you might think — a C "object" is defined as a "region of data storage in the execution environment, the contents of which can represent values".  The spec then goes on to discuss, for example, "objects of type `char`".

"Method" is a pretty universal term, but you may encounter a C++ programmer who only knows it as "member function".  Conversely, Java may not have functions at all, depending on who you ask.  "Procedure" and "subroutine" aren't used much any more, but a procedure is a completely different construct from a function in Pascal.

Even within the same language, we get sloppy: see if you can catch a Python programmer using "property" to refer to a regular "attribute", when `property` is a special kind of attribute.

There's a difference between "argument" and "parameter", but no one cares what it is, so we all just use "argument" which abbreviates more easily.  I use the word "signature" a lot, but I rarely see anyone else use it, and sometimes I wonder if anyone understands what I mean.

A `float` is single-precision in C and double-precision in Python.  I reflexively tense up whenever someone says "word" unqualified, because it could mean any of three or four different sizes.

Part of the problem here is that we're not actually doing computer science.  We're [doing programming](https://twitter.com/hashtag/iamdoingprogramming?src=hash), with a wide variety (hundreds!) of imperfect languages with different combinations of features and restrictions.  There are only so many words to go around, so the same names get used for vaguely similar features across many languages, and native speakers naturally attach their mother tongue's baggage to the jargon it uses.  Someone who got started with JavaScript would have a very different idea of what a "class" is than someone who got started with Ruby.  People come to Python or JavaScript and [exclaim](https://eev.ee/blog/2011/04/24/gotcha-python-scoping-closures/) that they "don't have real closures" because of a quirk of name binding.

Most of the time, this is fine.  Sometimes, it's incredibly confusing.  Here are my (least?) favorite lexical clashes.  (That was one too!)


## Arrays, vectors, and lists

In C, an array is a contiguous block of storage, in which you can put some fixed number of values of the same type.  `int[5]` describes enough space to store five `int`s, all snuggled right next to each other.  There's no such thing as a "vector".  "List" would likely be interpreted as a _linked_ list, in which each value is stored separately and has a pointer to the next one.

C++ introduced `vector`, an array that automatically expands to fit an arbitrary number of values.  There's also a standard `list` type, which is a doubly-linked list.  (The exact implementations may be anything, but the types require certain properties that make an array and a linked list the most obvious choices.)  But wait!  C++11 introduced the `initializer_list`, which is actually an array.

Lisp dialects are of course nothing _but_ lists, but under the hood, these tend to be implemented as linked lists — which is no doubt why Lisp originally handled lists in terms of heads and tails (very easy to do with linked lists), rather than random access (very easy to do with contiguous arrays).  Haskell works similarly, and additionally has a `Data.Array` module which offers fast random access.

Perl (5)'s sequence type is the array, though "type" is a little misleading here, because it's really one of Perl's handful of _shapes_ of variables.  Perl also has a distinct thing called a "list", but it's a transient _context_ that only exists while evaluating an expression, and is not a type of value.  It's weird and I can't really explain it within a single paragraph.

Meanwhile, in Python, `list` is the fundamental sequence type, but it has similar properties to a C++ vector and (in CPython) is implemented with a C array.  The standard library also offers the rarely-used `array` type, which packs numbers into C arrays to save space — a source of occasional confusion for new Python programmers coming from C, who think "array" is the thing they want.  Oh, and there's the built-in `bytearray` type, a mutable sequence of bytes, which is different from an `array` that stores bytes.

JavaScript has an `Array` type, but it's (semantically) built on top of the only data structure in JavaScript, which is a hash table with string (!) keys.  There's also a family of `ArrayBuffer` types for storing numbers in C arrays, much like Python's `array` module.

PHP's sole data structure is called `array`, but it's really an ordered hash table with string (!) keys.  It also has a thing called `list`, but it's not a type, just quirky syntax for doing deconstructing assignment.  People coming from PHP to other languages are occasionally frustrated that hash tables lose their order.

Lua likewise has only a single data structure, but is more upfront in calling its structure a "table"; there's nothing in the language called "array", "vector", _or_ "list".

While I'm at it, the names for mapping types are all over the place:

- C++: `map` (actually a binary tree; C++11's `unordered_map` is a hash table)
- JavaScript: object (!)  (though it's not a generic mapping, since the keys must be strings; there's now a `Map` type)
- Lua: table
- PHP: array (!)  (string keys only)
- Perl: hash (another "shape", somewhat misleading since a "hash" is also a different thing, and again string keys only), though the documentation likes to say "associative array" a lot
- Python: dict
- Rust: map, though it exists as two separate types, `BTreeMap` and `HashMap`


## Pointers, references, and aliases

C has pointers, which are storage addresses.  This is pretty easy for C to do, since it's all about operating on one big array of storage (more or less).  A pointer is just an index into that storage.

C++ inherited pointers from C, but chastizes you for using them.  As an alternative it introduced "references", which are exactly like pointers, except you can leave off the `*`.  This added a very strange new capability that didn't exist in C: two regular ol' local variables could refer to the same storage, so that `a = 5;` could also change the value of `b`.

And so all programming conversation was doomed forever, but more on that in a moment.

Rust has things called references, and uses the C++ reference syntax for their types, but they're really "borrowed pointers" (i.e., pointers, but opaque and subject to compile-time lifetime constraints).  It also has lesser-used "raw pointers", which use C's pointer syntax.

Perl has things called references.  Two different kinds of things, in fact.  The ones people generally refer to are "hard references", which are pretty much like C pointers, except the "address" is supposed to be opaque and can't be arbitrarily operated on.  The others are "soft references", where you use the contents of a variable as the name of another variable using much the same syntax as hard references, but this is forbidden by `use strict` so doesn't see much use (and can be done other ways anyway).  Perl _also_ has things called aliases, which work like C++ references — but they don't work on local variables, and they're not really a type, just explicit manipulation of the symbol table.  (Cool fact: Perl functions receive their arguments as aliases!  It's easy not to notice, because most people immediately assign the arguments to readable names.)

PHP has things called references, but despite PHP's prominent Perl influence, it borrowed its references from C++.  C++ declares references as part of the type, but PHP has no variable declaration whatsoever, so a variable _becomes_ a reference if it's involved in one of a handful of specific operations with a `&` involved.  The variable is then permanently "infected" with reference-ness.

Python, Ruby, JavaScript, Lua, Java, and probably several hundred other high-level languages have nothing called pointers, references, _or_ aliases.  This causes endless confusion when trying to explain the language semantics to someone with a C or C++ background, because we want to say things like "this references that" or "this points to that" which can lead them to think that there are literal references and pointers available for them to twiddle.  For this reason (and my Perl background), I like to call C++'s reference behavior "aliasing", which more clearly describes what it does and frees up the word "refer" to be used in its generic English sense.


## Pass by value, pass by reference

Speaking of references.  I've [explained this before for Python](/blog/2012/05/23/python-faq-passing/), but here's the quick(ish) version.  I maintain that this dichotomy makes no sense in [almost all](https://en.wikipedia.org/wiki/Almost_all) languages, because the very question hinges on C's idea of what a value _is_, and it's a relatively rare attitude outside of the C family.

The fundamental issue is that C has syntax to imply structure, but the semantics are all about _bytes_.  A `struct` looks and sounds like a container, a thing with a lid on it: it's wrapped in braces, and you have to use `.` to look inside it.  But C just sees a blob of bytes, not much different from an `int`, except that it lets you look at a few of those bytes at a time.  If you put one `struct` inside another, C will dump the inner's structure into the outer.  If you assign one `struct` to another, C will dutifully copy all the bytes over, same as it would for a `double`.  The boundary is illusory.  In effect, the only "true" container C has — the only form of containment that doesn't spill its contents all over the place — is the pointer!

If you pass a `struct` to or from a function, C will copy the whole thing, as with any other form of assignment.  If you want a function to modify a struct, you have to pass in a _pointer_ to it, so the function can modify the original storage and not a local copy.  If you want to pass a very large struct to a function, you should still use a pointer, or you'll waste a lot of time uselessly copying data around just to throw it away.

This is so-called "pass by value", but it's really about the underlying storage, not any semantic notion of "value".  Pass by copy, if you will.  It's similar to how forgetting to quote a variable in a shell script will cause it to be split on whitespace, or how passing an array to a function in Perl will copy all the elements.  It's nonsense.  The semantics, the diagrams of boxes that we draw, and even the very _syntax_ all imply that there's something being bundled up, but then you turn your back for a second and the language scatters your data to the wind.

C++ added references to make this sort of thing more transparent, just in case C was too easy to understand.  Now you can _appear_ to pass a `struct` "by value", but if the function is declared as taking references for arguments, it can still freely modify your data.  The function's argument becomes an alias for whatever you pass in, so even an atomic type like an `int` can be overwritten wholesale.  This is "pass by reference", perhaps better named "pass by alias".

The way Java, Python, Ruby, Lua, JavaScript, and countless other languages work is to have containers act as a single unit.  When you have a variable containing a structure, and you assign that variable to another variable, no copying is done.  Rather, both variables now refer to—  err, point to—  err...

And here's the major issue with the terminology.  Someone who's asking whether X language is by-value or by-reference has likely ingrained the C model, and takes for granted that this is how programming fundamentally works.  If I say "refer", they might think there are C++ references (alias) involved somewhere.  If I say "point", they might think the language has some form of indirection like a C pointer.  In most cases, the languages have neither, but there are only so many ways to express this concept in English.

Semantically, those languages act like values exist in their own right, and variables are merely names.  Assignment gives another name to a value.  It's tempting to explain `a = b` as "now `a` points to `b`" or "now they refer to the same object", but that introduces an indirection, implies an intermediate layer that doesn't exist in the language.  `a` and `b` both _name_ the same value.

Function calls are a form of assignment, so the arguments inside a function _name_ the same values that the caller passed in.  You can modify them in-place, if they're mutable, and the caller will see the changes, because it's the same value.  You _can't_ just reassign the variable: the variable is not an alias, and assigning to it merely makes it a name for something else instead.  This exists so far outside the dichotomy that it doesn't even have a consistent name, though I've seen it called pass by object, pass by identity, and pass by sharing.

It's entirely possible to have these passing styles in higher-level languages — as I mentioned, PHP can pass by alias using its C++-style references.  But pass by alias really exists as a response to pass by copy, and pass by copy exists because there's not really any alternative in a fairly low-level language like C.

Anything you can do with pass by copy, you can do with pass by sharing followed by an explicit copy.  Most things you can do with pass by alias, you can also do with pass by sharing, as long as you're mutating the same value via its own interface.  The exceptions are attempts to rebind the name itself, and most of _those_ are only for the sake of returning multiple values, which you can do directly in most higher-level languages.



## Loose typing

Okay, so, this is really up for interpretation, but I'm pretty sure "loose typing" is not actually a thing.  At least, I've never seen a particularly concrete definition for it, which is kind of ironic.  To recap:

- _Strong typing_ means that _values_ do not implicitly change type to fit operations performed on them.  Rust is strongly typed: comparing an `i32` with a `i64` is an error.

- _Weak typing_ means that _values_ can implicitly change type to fit operations performed on them.  JavaScript is weakly typed: `5 + "3"` will implicitly convert the string to a number and produce `8`.  (Haha, just kidding, it produces `"53"`.)  Also, C is weakly typed: you can just straight up assign `"3"` to an `int` and get some hilarious nonsense.

- _Static typing_ means that _names_ (variables) have associated types that are known before the program runs.  Java is statically typed: Java code is 70% type names by volume.

- _Dynamic typing_ means that _names_ are not given types ahead of time.  Ruby is dynamically typed: types are figured out on the fly while the program runs.

Strong–weak forms a spectrum, and static–dynamic forms a spectrum.  Languages may have both strong and weak elements, or both static and dynamic elements, though usually one is more prominent.  For example, while Go is considered statically-typed, `interface{}` acts much like dynamic typing.  Conversely, you [could argue](https://existentialtype.wordpress.com/2011/03/19/dynamic-languages-are-static-languages/) that Python is statically-typed and every variable is of type `object`, but good luck with that.

Crucially, because strong–weak concerns _values_ and static–dynamic concerns _names_, all four combinations exist.  Haskell is strong and static.  C is weak and static.  Python is strong and dynamic.  Shell is weak and dynamic.

So, then, what exactly is "loose typing"?  You'd think it would mean the same as "weak typing", but I've seen a lot of people refer to Python as "loosely typed", even though Python is mostly strong.  (Stronger than C!)

Given that I rarely see the phrase used in a non-derogatory context, my best guess is that "loosely typed" really means "doesn't have C++'s type system".  Which is kind of funny, given how flimsy C++'s type system is.  What type is a pointer to a `T`?  It's not `T*`, because that might be a null pointer (which is not a pointer to `T`) or complete garbage (which is unlikely to be a pointer to a `T`) or uninitialized (also unlikely to be a pointer to a `T`).  What's the point of static typing if your variables don't actually have to contain the type they're declared as?


## Caching

This one is most anecdotal, as it's not even a language feature.

Caching is storing the results of some computations so you don't have to compute them again later.  It's an optimization, trading memory in exchange for speed.

I think a _crucial_ property of a cache is that if the cache is emptied or destroyed or unavailable for any reason, _everything still works, just more slowly_.

And yet I've seen a number of programmers use "cache" to refer to any form of storing a value to use later.  I find this very confusing, since that's all programming _is_.

A fabulous example is a handy Python utility that shows up in a number of projects.  I know it by the name `reify`, which is how it's spelled in [Pyramid](http://pyramid.readthedocs.io/en/latest/), where I first saw it.  It does lazy initialization of an object attribute, for example:

```python
class Monster:
    def think(self):
        # do something smart

    @reify
    def inventory(self):
        return []
```

Here, `monster.inventory` doesn't actually exist until you try to read it, at which point the function is called — _once_ — and the list it returns becomes the attribute.  It's completely transparent, and once the value is created, it's a normal attribute with no indirection cost.  You can add items to it, and you'll see the same list every time.  Hence, "to make real": the attribute isn't real until you summon it into being by observing it.

This is nice for objects that deal with several related but interconnected ideas (which are thus difficult to split into multiple objects).  If part of the object takes time or space to set up, you can slap `@reify` on it, and the end user won't have to pay the cost if they don't use that functionality.

It wasn't on PyPI as a separate package for the longest time, probably because it can be implemented in a dozen lines.  When I said it "shows up in a number of projects", I meant "a number of projects have copy/pasted it from each other".

It finally showed up a couple years ago, under the name...  [cached-property](https://pypi.python.org/pypi/cached-property).  The docs even prominently show how to "invalidate" the "cache" — by mucking with object internals.

The problem I have here is that virtually every use of this decorator I have ever seen _is not a cache_.  The example above is silly, of course, but it immediately demonstrates the problem: "invalidating" `monster.inventory` would irrevocably lose the only copy of the monster's inventory.  Real uses of `@reify` tend to produce database connections and other kinds of mutable storage, where "invalidating" would be similarly destructive.  This isn't data you can just whip up again if need be.

It's _possible_ to use `@reify` to create a cache, but it's also possible to use `dict` to create a cache, so I don't find that very compelling.

I did try to make my case for renaming the project early on — especially as the maintainer wanted to add this to the standard library! — but no one else liked `reify` and the conversation degenerated into bikeshedding over an alternative name.  Naming really _is_ the hardest problem in computer science.


## Bonus: cool terminology we should use more

I love that the [Git changelog](https://github.com/git/git/blob/master/Documentation/RelNotes/2.7.0.txt) refers to commands as having "learned" new things:

> "git remote" learned "get-url" subcommand to show the URL for a given remote name used for fetching and pushing.

Relatedly, I love to see "spelled" use to explain how to write code (especially a single construct or brief expression).  Indexing is spelled `a[b]`, etc.

A function "signature" is just its interface: the arguments it takes, their names, their types, the return type, and exceptions that may be thrown.  Generally "signature" only refers to the parts that can be expressed directly in the language (and that affect call semantics), so a Python programmer likely wouldn't consider exceptions to be part of a function signature, and a C++ programmer would likewise ignore argument names.

I realize I said "semantic" a bunch of times in this post, but it doesn't see much use outside HTML — a lot of programmers seem to get really preoccupied with what the physical hardware is doing.  "Semantic" refers to what code _means_, as opposed to how it works in practice.

And my favorite, which I wish I had more excuses to use: a "nybble" is four bits.
