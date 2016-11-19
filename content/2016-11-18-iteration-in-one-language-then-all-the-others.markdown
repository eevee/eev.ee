title: Iteration in one language, then all the others
date: 2016-11-18 19:48
category: blog
tags: tech, plt

You [may have noticed]({filename}/2016-09-18-the-curious-case-of-the-switch-statement.markdown) that I like comparing features across different languages.  I hope you like it too, because I'm doing it again.

<!-- more -->

## Python

I'm most familiar with Python, and iteration is one of its major concepts, so it's a good place to start and a good overview of iteration.  I'll dive into Python a little more deeply, then draw parallels to other languages.

Python only has one form of iteration loop, `for`.  (Note that all of these examples are written for Python 3; in Python 2, some of the names are slightly different, and fewer things are lazy.)

```python
for value in sequence:
    ...
```

`in` is also an operator, so `value in sequence` is also the way you test for containment.  This is either very confusing or very satisfying.

When you need indices, or specifically a range of numbers, you can use the built-in [`enumerate`](https://docs.python.org/3/library/functions.html#enumerate) or [`range`](https://docs.python.org/3/library/functions.html#range) functions.  `enumerate` works with lazy iterables as well.

```python
# This makes use of tuple unpacking to effectively return two values at a time
for index, value in enumerate(sequence):
    ...

# Note that the endpoint is exclusive, and the default start point is 0.  This
# matches how list indexing works and fits the C style of numbering.
# 0 1 2 3 4
for n in range(5):
    ...

# Start somewhere other than zero, and the endpoint is still exclusive.
# 1 2 3 4
for n in range(1, 5):
    ...

# Count by 2 instead.  Can also use a negative step to count backwards.
# 1 3 5 7 9
for n in range(1, 11, 2):
    ...
```

`dict`s (mapping types) have several methods for different kinds of iteration.  Additionally, iterating over a `dict` directly produces its keys.

```python
for key in mapping:
    ...

for key in mapping.keys():
    ...

for value in mapping.values():
    ...

for key, value in mapping.items():
    ...
```

Python distinguishes between an **iterable**, any value that can be iterated over, and an **iterator**, a value that performs the actual work of iteration.  Common iterable types include `list`, `tuple`, `dict`, `str`, and `set`.  `enumerate` and `range` are also iterable.

Since Python code rarely works with iterators directly, and many iterable types also function as their own iterators, it's common to hear "iterator" used to mean an iterable.  To avoid this ambiguity, and because the words are fairly similar already, I'll refer to iterables as **containers** like the Python documentation sometimes does.  Don't be fooled — an object doesn't actually need to contain anything to be iterable.  Python's `range` type is iterable, but it doesn't physically contain all the numbers in the range; it generates them on the fly as needed.

The fundamental basics of iteration are built on these two ideas.  Given a container, ask for an iterator; then repeatedly advance the iterator to get new values.  When the iterator runs out of values, it raises `StopIteration`.  That's it.  In Python, those two steps can be performed manually with the [`iter`](https://docs.python.org/3/library/functions.html#iter) and [`next`](https://docs.python.org/3/library/functions.html#next) functions.  A `for` loop is roughly equivalent to:

```python
_iterator = iter(container)
_done = False
while not _done:
    try:
        value = next(_iterator)
    except StopIteration:
        _done = True
    else:
        ...
```

An iterator can only move forwards.  Once a value has been produced, it's lost, at least as far as the iterator is concerned.  These restrictions are occasionally limiting, but they allow iteration to be used for some unexpected tasks.  For example, iterating over an open file produces its lines — even if the "file" is actually a terminal or pipe, where data only arrives once and isn't persistently stored anywhere.

### Generators

A more common form of "only forwards, only once" in Python is the **generator**, a function containing a `yield` statement.  For example:

```python
def inclusive_range(start, stop):
    val = start
    while val <= stop:
        yield val
        val += 1

# 6 7 8 9
for n in inclusive_range(6, 9):
    ...
```

Calling a generator function doesn't execute its code, but immediately creates a _generator iterator_.  Every time the iterator is advanced, the function executes until the next `yield`, at which point the yielded value is returned as the next value and the function _pauses_.  The next iteration will then resume the function.  When the function returns (or falls off the end), the iterator stops.

Since the values here are produced by running code on the fly, it's of course impossible to rewind a generator.

[The underlying protocol](https://docs.python.org/3/library/stdtypes.html#typeiter) is straightforward.  A container must have an `__iter__` method that returns an iterator, corresponding to the `iter` function.  An iterator must have a `__next__` method that returns the next item, corresponding to the `next` function.  If the iterator is exhausted, `__next__` must raise [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration).  An iterator must also have an `__iter__` that returns _itself_ — this is so an iterator can be used directly in a `for` loop.

The above inclusive range generator might be written out explicitly like this:

```python
class InclusiveRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        return InclusiveRangeIterator(self)

class InclusiveRangeIterator:
    def __init__(self, incrange):
        self.incrange = incrange
        self.nextval = incrange.start

    def __iter__(self):
        return self

    def __next__(self):
        if self.nextval > self.incrange.stop:
            raise StopIteration

        val = self.nextval
        self.nextval += 1
        return val
```

This might seem like a lot of boilerplate, but note that the iterator state (here, `nextval`) can't go on `InclusiveRange` directly, because then it'd be impossible to iterate over the same object twice at the same time.  (Some types, like files, do act as their own iterators because they can't meaningfully be iterated in parallel.)

Even Python's internals work this way.  Try `iter([])` in a Python REPL; you'll get a `list_iterator` object.

In truth, it _is_ a lot of boilerplate.  User code usually uses this trick:

```python
class InclusiveRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        val = self.start
        while val <= self.stop:
            yield val
            val += 1
```

Nothing about this is special-cased in any way.  Now `__iter__` is a generator, and calling a generator function returns an iterator, so all the constraints are met.  It's a really easy way to convert a generator function into a type.  If this class were named `inclusive_range` instead, it would even be backwards-compatible; consuming code wouldn't even have to know it's a class.

### Reversal

But why would you do this?  One excellent reason is to add support for other sequence-like operations, like reverse iteration support.  An iterator can't be reversed, but a _container_ might support being iterated in reverse:

```python
fruits = ['apple', 'orange', 'pear']
# pear, orange, apple
for value in reversed(fruits):
    ...
```

Iterating a lazy container doesn't always make sense, but when it does, it's easy to implement by returning an iterator from [`__reversed__`](https://docs.python.org/3/reference/datamodel.html#object.__reversed__).

```python
class InclusiveRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        val = self.start
        while val <= self.stop:
            yield val
            val += 1

    def __reversed__(self):
        val = self.stop
        while val >= self.start:
            yield val
            val -= 1
```

Note that Python does _not_ have "bi-directional" iterators, which can freely switch between forwards and reverse iteration on the fly.  A bidirectional iterator is useful for cases like doubly-linked lists, where it's easy to get from one value to the next _or previous_ value, but not as easy to start from the beginning and get the tenth item.

Iteration is often associated with **sequences**, though they're not quite the same.  In Python, a sequence is a value that can be indexed in order as `container[0]`, `container[1]`, etc.  (Indexing is implemented with [`__getitem__`](https://docs.python.org/3/reference/datamodel.html#object.__getitem__).)  All sequences are iterable; in fact, if a type implements indexing but not `__iter__`, the `iter` function will automatically try indexing it from zero instead.  `reversed` does the same, though it requires that the type implement [`__len__`](https://docs.python.org/3/reference/datamodel.html#object.__len__) as well so it knows what the last item is.

Much of this is codified more explicitly in the abstract base classes in [`collections.abc`](https://docs.python.org/3/library/collections.abc.html), which also provide default implementations of common methods.

_Not_ all iterables are sequences, and not every value that can be indexed is a sequence!  Python's mapping type, `dict`, uses indexing to fetch the value for a key; but a `dict` has no defined order and is not a sequence.  However, a `dict` can still be iterated over, producing its keys (in arbitrary order).  A `set` can be iterated over, producing its values in arbitrary order, but it cannot be indexed at all.  A type could conceivably use indexing for something more unusual and not be iterable at all.

### A common question

It's not really related to iteration, but people coming to Python from Ruby often ask why `len()` is a built-in function, rather than a method.  The same question could be asked about `iter()` and `next()` (and other Python builtins), which more or less delegate directly to a "reserved" `__dunder__` method anyway.

I believe the _technical_ reason is simply the order that features were added to the language in very early days, which is not very interesting.

The _philosophical_ reason, imo, is that Python does not reserve method names for fundamental operations.  All `__dunder__` names are reserved, of course, but everything else is fair game.  This makes it obvious when a method is intended to add support for some language-ish-level operation, even if you don't know what all the method names are.  Occasionally a third-party library invents its own `__dunder__` name, which is a little naughty, but the same reasoning applies: "this is a completely generic interface that some external mechanism is expected to use".

This approach also avoids a namespacing problem.  In Ruby, a `Rectangle` class might want to have `width` and `length` attributes...  but the presence of `length` means a `Rectangle` looks like it functions as a sequence!  Since "interface" method names aren't namespaced in any way, there is _no way_ to say that you don't mean the same thing as `Array.length`.

It's a minor quibble, since everything's dynamically typed anyway, so the real solution is "well don't try to iterate a rectangle then".  And Python does use `keys` as a method name in some obscure cases.  Oh, well.

### Some cute tricks

The distinction between sequences and iterables can cause some subtle problems.  A lot of code that only needs to loop over items can be passed, e.g., a generator.  But this can take some conscious care.  Compare:

```python
# This will NOT work with generators, which don't support len() or indexing
for i in range(len(container)):
    value = container[i]
    ...

# But this will
for i, value in enumerate(container):
    ...
```

`enumerate` also has a subtle, unfortunate problem: it cannot be combined with `reversed`.  This has bit me more than once, surprisingly.

```python
# This produces a TypeError from reversed()
for i, value in reversed(enumerate(container)):
    ...

# This almost works, but the index goes forwards while the values go backwards
for i, value in enumerate(reversed(container)):
    ...
```

The problem is that `enumerate` can't, in general, reverse itself.  It counts up from zero as it iterates over its argument; reversing it means _starting_ from one less than the number of items, but it doesn't yet know how many items there are.  But if you just want to run over a list or other sequence backwards, this feels very silly.  A trivial helper can make it work:

```python
def revenum(iterable, end=0):
    start = len(iterable) + end
    for value in iterable:
        start -= 1
        yield start, value
```

I've run into other odd cases where it's frustrating that a generator doesn't have a length or indexing.  This especially comes up if you make heavy use of _generator expressions_, which are a very compact way to write a one-off generator.  (Python also has list, set, and dict "comprehensions", which have the same syntax but use brackets or braces instead of parentheses, and are evaluated immediately instead of lazily.)

```python
def get_big_fruits():
    fruits = ['apple', 'orange', 'pear']
    return (fruit.upper() for fruit in fruits)

# Roughly equivalent to:
def get_big_fruits():
    fruits = ['apple', 'orange', 'pear']
    def genexp():
        for fruit in fruits:
            yield fruit.upper()
    return genexp()
```

If you had _thousands_ of fruits, doing this could save a little memory.  The caller is _probably_ just going to loop over them to print them out (or whatever), so using a generator expression means that each uppercase name only exists for a short time; returning a list would mean creating a lot of values all at once.

Ah, but now the caller wants to know how _many_ fruits there are, with minimal fuss.  Generators have no length, so that won't work.  Turning this generator expression into a class that also has a `__len__` would be fairly ridiculous.  So you resort to some slightly ugly trickery.

```python
# Ugh.  Obvious, but feels really silly.
count = 0
for value in container:
    count += 1

# Better, but weird if you haven't seen it before.  Creates another generator
# expression that just yields 1 for every item, then sums them up.
count = sum(1 for _ in container)
```

Or perhaps you want the first big fruit?  Well, `[0]` isn't going to help.  This is one of the few cases where using `iter` and `next` directly can be handy.

```python
# Oops!  If the container is empty, this raises StopIteration, which you
# probably don't want.
first = next(iter(container))

# Catch the StopIteration explicitly.
try:
    first = next(iter(container))
except StopIteration:
    # This code runs if there are zero items
    ...

# Regular loop that terminates immediately.
# The "else" clause only runs when the container ends naturally (i.e. NOT if
# the loop breaks), which can only happen here if there are zero items.
for value in container:
    first = value
    break
else:
    ...

# next() -- but not __next__()! -- takes a second argument indicating a
# "default" value to return when the iterator is exhausted.  This only makes
# sense if you were going to substitute a default value anyway; doing this and
# then checking for None will do the wrong thing if the container actually
# contained a None.
first = next(iter(container), None)
```

Other tricks with `iter` and `next` include skipping the first item (or any number of initial items, though consider [`itertools.islice`](https://docs.python.org/3/library/itertools.html#itertools.islice) for more complex cases):

```python
it = iter(container)
next(it, None)  # Use second arg to ignore StopIteration
for value in it:
    # Since the first item in the iterator has already been consumed, this loop
    # will start with the second item.  If the container had only one or zero
    # items, the loop will get StopIteration and end immediately.
    ...
```

Iterating two (or more) items at a time:

```python
# Obvious way: call next() inside the loop.
it = iter(container)
for value1 in it:
    # With an odd number of items, this will raise an uncaught StopIteration!
    # Catch it or provide a default value.
    value2 = next(it)
    ...

# Moderately clever way: abuse zip().
# zip() takes some number of containers and iterates over them pairwise.  It
# stores an iterator for each container.  When it's asked for its next item, it
# in turn asks all of its iterators for their next items, and returns them as a
# set.  But by giving it the same exact iterator twice, it'll end up advancing
# that iterator twice and returning two consecutive items.
# Note that zip() stops early as soon as an iterator runs dry, so if the
# container has an odd number of items, this will silently skip the last one.
# If you don't want that, use itertools.zip_longest instead.
it = iter(container)
for line1, line2 in zip(it, it):
    ...

# Far too clever way: exactly the same as above, but written as a one-liner.
# zip(iter(), iter()) would create two separate iterators and break the trick.
# List multiplication produces a list containing the same iterator twice.
# One advantage of this is that the 2 can be a variable.
for value1, value2 in zip(*[iter(container)] * 2):
    ...
```

Wow, that got pretty weird towards the end.  Somehow this turned into Stupid Python Iterator Tricks.  Don't worry; I know far less about these other languages.


## C

C is an extreme example with no iterator protocol whatsoever.  It barely even supports sequences; arrays are just pointer math.  All it has is the humble C-style `for` loop:

```c
int[] container = {...};
for (int i = 0; i < container_length; i++) {
    int value = container[i];
    ...
}
```

Unfortunately, it's really the best C can do.  C arrays don't know their own length, so no matter what, the developer has to provide it some other way.  Even without that, a built-in iterator protocol is impossible — iterators require persistent state (the current position) to be bundled alongside code (how to get to the next position).  That pretty much means one of two things: closures or objects.  C has neither.


## Lua

Lua has two forms of `for` loop.  The first is a simple numeric loop.

```lua
-- 1 3 5 7 9 11
for value = 1, 11, 2 do
    ...
end
```

The three values after the `=` are the start, end, and step.  They work similarly to Python's `range()`, except that everything in Lua is always _inclusive_, so `for i = 1, 5` will count from 1 to 5.

The generic form uses `in`.

```lua
for value in iterate(container) do
    ...
end
```

`iterate` isn't a special name here, but most of the time a generic `for` will look like this.

See, Lua doesn't have objects.  It has enough tools that you can build objects fairly easily, but the core language has no explicit concept of objects or method calls.  An iterator protocol needs to bundle state and behavior somehow, so Lua uses closures for that.  But you still need a way to get that closure, and that means calling a function, and a plain value can't have functions attached to it.  So iterating over a table (Lua's single data structure) looks like this:

```lua
for key, value in pairs(container) do
    ...
```

`pairs` is a built-in function.  Lua also has an `ipairs`, which iterates over consecutive keys and values starting from key 1.  (Lua starts at 1, not 0.  Lua also represents sequences as tables with numeric keys.)

Lua does have a way to _associate_ "methods" with values, which is how objects are made, but `for` loops almost certainly came first.  So iteration is almost always over a function call, not a bare value.

Also, because objects are built out of tables, having a default iteration behavior for all tables would mean having the same default for all objects.  Nothing's stopping you from using `pairs` on an object now, but at least that looks deliberate.  It's easy enough to give objects iteration methods and iterate over `obj:iter()`, though it's slightly unfortunate that every type might look slightly different.  Unfortunately, Lua has no truly generic interface for "this can produce a sequence of values".

The iteration protocol is really just calling a function repeatedly to get new values.  When the function returns `nil`, the iteration ends.  (That means `nil` can never be part of an iteration!  You can work around this by returning _two_ values and making sure the first one is something else that's never `nil`, like an index.)  The manual explains the [exact semantics of the generic `for`](http://www.lua.org/manual/5.2/manual.html#3.3.5) with Lua code, a move I wish every language would make.

```lua
-- This:
for var_1, ···, var_n in explist do block end

-- Is equivalent to this:
do
    local _func, _state, _lastval = explist
    while true do
        local var_1, ···, var_n = _func(_state, _lastval)
        if var_1 == nil then break end
        _lastval = var_1
        block
    end
end
```

Important to note here is the way multiple-return works in Lua.  Lua doesn't have tuples; multiple assignment is a distinct feature of the language, and multiple return works exactly the same way as multiple assignment.  If there are too few values, the extra variables become `nil`; if there are too many values, the extras are silently discarded.

So in the line `local _func, _state, _lastval = explist`, the "state" value `_state` and the "last loop value" `_lastval` are both _optional_.  Lua doesn't use them, except to pass them back to the iterator function `_func`, and they aren't visible to the `for` loop body.  An iterator can thus be _only_ a function and nothing else, letting `_state` and `_lastval` be `nil` — but they can be a little more convenient at times.  Compare:

```lua
-- Usual approach: return only a closure, completely ignoring state and lastval
local function inclusive_range(start, stop)
    local nextval = start
    return function()
        if nextval > stop then
            return
        end
        local val = nextval
        nextval = nextval + 1
        return val
    end
end

-- Alternative approach, not using closures at all.  This is the function we
-- return; each time it's called with the same "state" value and whatever it
-- returned last time it was called.
-- This function could even be written exactly a method (a la Python's
-- __next__), where the state value is the object itself.
local function inclusive_range_iter(stop, prev)
    -- "stop" is the state value; "prev" is the last value we returned
    local val = prev + 1
    if val > stop then
        return
    end
    return val
end
local function inclusive_range(start, stop)
    -- Return the iterator function, and pass it the stop value as its state.
    -- The "last value" is a little weird here; on the first iteration, there
    -- is no last value.  Here we can fake it by subtracting 1 from the
    -- starting number, but in other cases, it might make more sense if the
    -- "state" were a table containing both the start and stop values.
    return inclusive_range_iter, stop, start - 1
end

-- 6 7 8 9 with both implementations
for n in inclusive_range(6, 9) do
    ...
end
```

Lua doesn't have generators.  Surprisingly, it has fully-fledged _coroutines_ — call stacks that can be paused at any time.  Lua sometimes refers to them as "threads", but only one can be running at a time.  Effectively they're like Python generators, except you can call a function which calls a function which calls a function which eventually `yield`s, and the _entire_ call stack from that point up to the top of the coroutine is paused and preserved.

In Python, the mere presence of `yield` causes a function to become a generator.  In Lua, since any function might try to yield the coroutine it's currently in, a function has to be explicitly called as a coroutine using functions in the `coroutine` library.

But this post is about iterators, not coroutines.  Coroutines don't function as iterators, but Lua provides a `coroutine.wrap()` that takes a function, turns it into a coroutine, and returns a function that resumes the coroutine.  That's enough to allow a coroutine to be turned into an iterator.  The Lua book even has [a section about this](https://www.lua.org/pil/9.3.html).

```lua
local function inclusive_range(start, stop)
    local val = start
    while val <= stop do
        coroutine.yield(val)
        val = val + 1
    end
end
-- Unfortunately, coroutine.wrap() doesn't have any way to pass initial
-- arguments to the function it wraps, so we need this dinky wrapper.
-- I should clarify that the ... here is literal syntax for once.
local function iter_coro(entry_point, ...)
    local args = {...}
    return coroutine.wrap(function()
        entry_point(unpack(args))
    end)
end

# 6 7 8 9
for n in iter_coro(inclusive_range, 6, 9) do
    ...
end
```

So, that's cool.  Lua doesn't do a lot for you — unfortunately, list processing tricks can be significantly more painful in Lua — but it has some pretty interesting primitives that compose with each other remarkably well.


## Perl 5

Perl has a very straightforward C-style `for` loop, which looks and works exactly as you might expect.  `my`, which appears frequently in these examples, is just local variable declaration.

```perl
for (my $i = 0; $i < 10; $i++) {
    ...
}
```

Nobody uses it.  Everyone uses the iteration-style `for` loop.  (It's occasionally called `foreach`, which is extra confusing because both `for` and `foreach` can be used for both kinds of loop.  Nobody actually uses the `foreach` keyword.)

```perl
for my $value (@container) {
    ...
}
```

The iteration loop can be used for numbers, as well, since Perl has a `..` inclusive range operator.  For iterating over an array with indexes, Perl has the slightly odd `$#array` syntax, which is the index of the last item in `@array`.  Creating something like Python's `enumerate` is a little tricky in Perl, because you can't directly return a list of lists, and the workaround doesn't support unpacking.  It's complicated.

```perl
for my $i (1..10) {
    ...
}

for my $index (0..$#array) {
    my $value = $array[$index];
    ...
}
```

A hash (Perl's mapping "shape") can't be iterated directly.  Or, well, it can, but the loop will alternate between keys and values because Perl is weird.  Instead you need the [`keys`](http://perldoc.perl.org/functions/keys.html) or [`values`](http://perldoc.perl.org/functions/values.html) built-in functions to get the keys or values as regular lists.  (These functions also work on arrays as of Perl 5.12.)

```perl
for my $key (keys %container) {
    ...
}
```

For iterating over both keys and values at the same time, Perl has an [`each`](http://perldoc.perl.org/functions/each.html) function.  The behavior is a little weird, since every call to the function advances an internal iterator inside the hash and returns a new pair.  If a loop using `each` terminates early, the next use of `each` may silently start somewhere in the middle of the hash, skipping a bunch of its keys.  This is probably why I've never seen `each` actually used.

```perl
while (my ($key, value) = each %container) {
    ...
}
```

Despite being very heavily built on the concept of lists, Perl doesn't have an explicit iterator protocol, and its support for lazy iteration in general is not great.  When they're used at all, lazy iterators tend to be implemented as ad-hoc closures or callable objects, which require a `while` loop:

```perl
my $iter = custom_iterator($collection);
while (my $value = $iter->()) {
    ...
}
```

### Here be dragons

It _is_ possible to sorta-kinda fake an iterator protocol.  If you're not familiar, Perl's variables come in several different "shapes" — hash, array, scalar — and it's possible to "tie" a variable to a backing object which defines the operations for a particular shape.  It's a little like operator overloading, except that Perl also has operator overloading and it's a completely unrelated mechanism.  In fact, you could use operator overloading to make your object return a tied array when dereferenced as an array.  I am talking gibberish now.

Anyway, the trick is to tie an array and return a new value for each consecutive fetch of an index.  Like so:

```perl
use v5.12;
package ClosureIterator;

# This is the tie "constructor" and just creates a regular object to store
# our state
sub TIEARRAY {
    my ($class, $closure) = @_;
    my $self = {
        closure => $closure,
        nextindex => 0,
    };
    return bless $self, $class;
}

# This is called to fetch the item at a particular index; for an iterator,
# only the next item is valid
sub FETCH {
    my ($self, $index) = @_;

    if ($index == 0) {
        # Always allow reading index 0, both to mean a general "get next
        # item" and so that looping over the same array twice will work as
        # expected
        $self->{nextindex} = 0;
    }
    elsif ($index != $self->{nextindex}) {
        die "ClosureIterator does not support random access";
    }

    $self->{nextindex}++;
    return $self->{closure}->();
}

# The built-in shift() function means "remove and return the first item", so
# it's a good fit for a general "advance iterator"
sub SHIFT {
    my ($self) = @_;
    $self->{nextindex} = 0;
    return $self->{closure}->();
}

# Yes, an array has to be able to report its own size...  but luckily, a for
# loop fetches the size on every iteration!  As long as this returns
# increasingly large values, such a loop will continue indefinitely
sub FETCHSIZE {
    my ($self) = @_;
    return $self->{nextindex} + 1;
}

# Most other tied array operations are for modifying the array, which makes no
# sense here.  They're deliberately omitted, so trying to use them will cause a
# "can't locate object method" error.


package main;

# Create an iterator that yields successive powers of 2
tie my @array, 'ClosureIterator', sub {
    # State variables are persistent, like C statics
    state $next = 1;
    my $ret = $next;
    $next *= 2;
    return $ret;
};

# This will print out 1, 2, 4, 8, ... 1024, at which point the loop breaks
for my $i (@array) {
    say $i;
    last if $i > 1000;
}
```

This transparently works like any other array...  sort of.  You can loop over it (forever!); you can use `shift` to pop off the next value; you can stop a loop and then continue reading from it later.

Unfortunately, this is just plain weird, even for Perl, and I very rarely see it used.  Ultimately, Perl's array operations come in a set, and this is an array that pretends not to be able to do half of them.  Even Perl developers are likely to be surprised by an array, a fundamental "shape" of the language, with quirky behavior.

The biggest problem is that, as I said, Perl is heavily built on lists.  Part of that design is that `@array`s are very eager to spill their contents into a surrounding context.  Naïvely passing an array to a function, for example, will expand its elements into separate arguments, losing the identity of the array itself (and losing any tied-ness).  Interpolating an array into a string automatically space-separates its elements.

Unlike a `for` loop, these operations only ask the array for its size _once_ — so rather than printing an infinite sequence, they'll print a completely arbitrary prefix of it.  In the case above, spilling a fresh array will read one item; spilling the array after the example loop will read eleven items.  So while a tied array works nicely with a `for` loop, it's at odds with the most basic rules of Perl syntax.

Also, Perl's list-based nature means it's attracted a lot of [list-processing utilities](http://search.cpan.org/~pevans/Scalar-List-Utils-1.46/lib/List/Util.pm) — but these naturally expect to receive a spilled list of arguments and cannot work with a lazy iterator.

I found multiple mentions of the [`List::Gen`](http://search.cpan.org/~asg/List-Gen-0.974/lib/List/Gen.pm) module while looking into this.  I'd never heard of it before and I've never seen it used, but it _tries_ to fill this gap (and makes use of array tying, among other things).  It's a bit weird, and its source code is extremely weird, and it took me twenty minutes to figure out how it was using `<...>` as a quoting construct.

(`<...>` in Perl does filename globbing, so it's usually seen as `<*.txt>`.  The same syntax is used for reading from a filehandle, which makes this confusing and ambiguous, so it's generally discouraged in favor of the built-in `glob` function which does the same thing.  Well, it turns out that `<...>` must just _call_ `glob()` at Perl-level, because `List::Gen` manages to co-opt this syntax simply by exporting its own `glob` function.  Perl is magical.)


## Perl 6

Perl 6, a mad experiment to put literally every conceivable feature into one programming language, naturally has a more robust concept of iteration.

At first glance, many of the constructs are similar to those of Perl 5.  The C-style `for` loop still exists for some reason, but has been disambiguated under the `loop` keyword.

```perl6
loop (my $i = 1; $i <= 10; $i++) {
    ...
}

# More interestingly, loop can be used completely bare for an infinite loop
loop {
    ...
}
```

The `for` block has slightly different syntax and a couple new tricks.

```perl6
# Unlike in Perl 5, $value is automatically declared and scoped to the block,
# without needing an explicit 'my'
for @container -> $value {
    ...
}

for 1..10 -> $i {
    ...
}

# This doesn't iterate in pairs; it reads two items at a time from a flat list!
for 1..10 -> $a, $b {
    ...
}
```

Not apparent in the above code is that ranges are lazy in Perl 6, as in Python; the elements are computed on demand.  In fact, Perl 6 supports a range like `1..Inf`.

Loop variables are also _aliases_.  By default they're read-only, so this appears to work like Python...  but Perl has always had a C-like language-level notion of "slots" that Python does not, and it becomes apparent if the loop variable is made read-write:

```perl6
my @fruits = «apple orange pear»;
for @fruits -> $fruit is rw {
    # This is "apply method inplace", i.e. shorthand for:
    # $fruit = $fruit.uc;
    # Yes, you can do that.
    $fruit .= uc;
}
say @fruits;  # APPLE ORANGE PEAR
```

For iterating with indexes, there's a curious idiom:

```perl6
# ^Inf is shorthand for 0..Inf, read as "up to Inf".
# Z is the zip operator, which interleaves its arguments' elements into a
# single flat list.
# This makes use of the "two at a time" trick from above.
for ^Inf Z @array -> $index, $value {
    ...
}
```

Iterating hashes is somewhat simpler; hashes have methods, and the `.kv` method returns the keys and values.  (It actually returns them in a flat list _interleaved_, which again uses "two at a time" syntax.  If you only use a single loop variable, your loop iterations will alternate between a key and a value.  Iterating a hash directly produces _pairs_, which are a first-class data type in Perl 6, but I can't find any syntax for directly unpacking a pair within a loop header.)

```perl6
for %container.kv -> $key, value {
    ...
}

# No surprises here
for %container.keys -> $key {
    ...
}
for %container.values -> $value {
    ...
}
```

Perl 6 is very big on laziness, which is perhaps why it took fifteen years to see a release.  It has the same _iterable_ versus _iterator_ split as Python.  Given a container (iterable), ask for an iterator; given an iterator, repeatedly ask for new values.  When the iterator is exhausted, it returns the `IterationEnd` sentinel.  Exactly the same ideas.  I'm not clear on the precise semantics of the `for` block and can't find a simple reference, but they're probably much like Python's...  plus a thousand special cases.

### Generators, kinda

Perl 6 also has its own version of generators, though with a few extra twists.  Curiously, generators are a _block_ called `gather`, rather than a kind of function — this means that a one-off `gather` is easier to create, but a `gather` factory must be explicitly wrapped in a function.  `gather` can even take a single expression rather than a block, so there's no need for separate "generator expression" syntax as in Python.

```perl6
sub inclusive-range($start, $stop) {
    return gather {
        my $val = $start;
        while $val <= $stop {
            take $val;
            $val++;
        }
    };
}

# 6 7 8 9
for inclusive-range(6, 9) -> $n {
    ...
}
```

Unlike Python's `yield`, Perl 6's `take` is dynamically scoped — i.e., `take` can be used anywhere in the call stack, and it will apply to the most recent `gather` caller.  That means arbitrary-depth coroutines, which seems like a big deal to me, but [the documentation](https://docs.perl6.org/language/control#gather/take) mentions it almost as an afterthought.

The documentation also says `gather/take` "can generate values lazily, depending on context," but neglects to clarify _how_ context factors in.  The code I wrote above turns out to be lazy, but this ambiguity inclines me to use the explicit `lazy` marker everywhere.

Ultimately it's a pretty flexible feature, but has a few quirks that make it a bit clumsier to use as a straightforward generator.  Given that the default behavior is an eagerly-evaluated block, I _think_ the original intention was to avoid the slightly unsatisfying pattern of "`push` onto an array every iteration through a loop" — instead you can now do this:

```perl6
my @results = gather {
    for @source-data -> $datum {
        next unless some-test($datum);
        take process($datum);
    }
};
```

Using a simple (syntax-highlighted!) `take` puts the focus on the value being taken, rather than the details of putting it where it wants to go and how it gets there.  It's an interesting idea and I'm surprised I've never seen it demonstrated this way.

With `gather` and some abuse of Perl's exceptionally compactable syntax, I can write a much shorter version of the infinite Perl 5 iterator above.

```perl6
my @powers-of-two = lazy gather take (state $n = 1) *= 2 for ^Inf;

# Binds to $_ by default
for @powers-of-two {
    # Method calls are on $_ by default
    .say;
    last if $_ > 1000;
}
```

It's definitely shorter, I'll give it that.  Leaving off the `lazy` in this case causes an infinite loop as Perl tries to evaluate the entire list; using a `$` instead of a `@` produces a "Cannot `.elems` a lazy list" error; using `$` without `lazy` prints a `...`-terminated representation of the infinite list and then hangs forever.  I don't quite understand the semantics of stuffing a list into a scalar (`$`) variable in Perl 6, and to be honest the list/array semantics seem to be far more convoluted than Perl 5, so I have no idea what's going on here.  Perl 6 has a lot of fascinating toys that are very easy to use incorrectly.

### Nuts and bolts

Iterables and iterators are encoded explicitly as the [`Iterable`](https://docs.perl6.org/type/Iterable) and [`Iterator`](https://docs.perl6.org/type/Iterator) roles.  An `Iterable` has an `.iterator` method that should return an `Iterator`.  An `Iterator` has a `.pull-one` method that returns the next value, or the `IterationEnd` sentinel when the iterator is exhausted.  Both roles offer several other methods, but they have suitable default implementations.

`inclusive-range` might be transformed into a class thusly:

```perl6
class InclusiveRangeIterator does Iterator {
    has $.range is required;
    has $!nextval = $!range.start;

    method pull-one() {
        if $!nextval > $!range.stop {
            return IterationEnd;
        }

        # Perl people would probably phrase this:
        # ++$!nextval
        # and they are wrong.
        my $val = $!nextval;
        $!nextval++;
        return $val;
    }
}

class InclusiveRange does Iterable {
    has $.start is required;
    has $.stop is required;

    # Don't even ask
    method new($start, $stop) {
        self.bless(:$start, :$stop);
    }

    method iterator() {
        InclusiveRangeIterator.new(range => self);
    }
}

# 6 7 8 9
for InclusiveRange.new(6, 9) -> $n {
    ...
}
```

Can we use `gather` to avoid the need for an extra class, just as in Python?  We sure can!  The only catch is that Perl 6 iterators don't also pretend to be iterables (remember, in Python, `iter(it)` should produce `it`), so we need to explicitly return a `gather` block's iterator.

```perl6
class InclusiveRange does Iterable {
    has $.start is required;
    has $.stop is required;

    # Don't even ask
    method new($start, $stop) {
        self.bless(:$start, :$stop);
    }

    method iterator() {
        gather {
            my $val = $!start;
            while $val <= $!stop {
                take $val;
                $val++;
            }
        }.iterator;  # <- this is important
    }
}
```

For sequences, Perl 6 has the [`Seq`](https://docs.perl6.org/type/Seq) type.  Curiously, even an infinite lazy `gather` is still a `Seq`.  Indexing and length are _not_ part of `Seq` — both are implemented as [separate methods](https://docs.perl6.org/language/subscripts#Methods_to_implement_for_positional_subscripting).

Curiously, even though Perl 6 became much stricter overall, the indexing methods don't seem to be part of a role; you only need define them, much like Python's `__dunder__` methods.  In fact, the preceding examples, `does Iterator` isn't necessary at all; the `for` block will blindly try to call an `iterator` method and doesn't much care where it came from.

I'm sure there are _plenty_ of cute tricks possible with Perl 6, but, er, I'll leave those as an exercise for the reader.


## Ruby

Ruby is a popular and well-disguised Perl variant, if Perl just went completely all-in on Smalltalk.  It has no C-style `for`, but it does have an infinite `loop` block and a very Python-esque `for`:

```ruby
for value in sequence do
    ...
end
```

Nobody uses this.  No, really, [the core language documentation](http://ruby-doc.org/core-2.3.1/doc/syntax/control_expressions_rdoc.html#label-for+Loop) outright says:

> The `for` loop is rarely used in modern ruby programs.

Instead, you'll probably see this:

```ruby
sequence.each do |value|
    ...
end
```

It doesn't look it, but this is completely backwards from everything seen so far.  All of these other languages have used _external_ iterators, where an object is repeatedly asked to produce values and calling code can do whatever it wants with them.  Here, something very different is happening.  The entire `do ... end` block acts as a _closure_ whose argument is `value`; it's passed to the `each` method, which calls it once for each value in the sequence.  This is an _internal_ iterator.

"Pass a block to a function which can then call it a lot" is a built-in syntactic feature of Ruby, so these kinds of iterators are fairly common.  The upside is that they look almost like a custom block, so they fit naturally with the language.  The downside is that all of these block-accepting methods are implemented _on `Array`_, rather than as generic functions: `bsearch`, `bsearch_index`, `collect`, `collect!`, `combination`, `count`, `cycle`, `delete`, `delete_if`, `drop_while`, `each`, `each_index`, `fetch`, `fill`, `find_index`, `index`, `keep_if`, `map`, `map!`, `permutation`, `product`, `reject`, `reject!`, `repeated_combination`, `repeated_permutation`, `reverse_each`, `rindex`, `select`, `select!`, `sort`, `sort!`, `sort_by!`, `take_while`, `uniq`, `uniq!`, `zip`.  Some of those, as well as a number of additional methods, are provided by the [`Enumerable`](https://ruby-doc.org/core-2.3.1/Enumerable.html) mixin which can express them in terms of `each`.  I suppose the other upside is that any given type can provide its own more efficient implementation of these methods, if it so desires.

I guess that huge list of methods answers most questions about how to iterate over indices or in reverse.  The only bit missing is that `..` range syntax exists in Ruby as well, and it produces `Range` objects which also have an `each` method.  If you don't care about each index, you can also use the cute `3.times` method.

Ruby blocks are a fundamental part of the language and built right into the method-calling syntax.  Even `break` is defined in terms of blocks, and it works with an argument!

```ruby
# This just doesn't feel like it should work, but it does.  Prints 17.
# Braces are conventionally used for inline blocks, but do/end would work too.
primes = [2, 3, 5, 7, 11, 13, 17, 19]
puts primes.each { |p| break p if p > 16 }
```

`each()` doesn't need to do anything special here; `break` will just cause its return value to be 17.  Somehow.  (Honestly, this is the sort of thing that makes me wary of Ruby; it seems so ad-hoc and raises so many questions.  A language keyword that changes the return value of a different function?  Does the inside of `each()` know about this or have any control over it?  How does it actually work?  Is there any opportunity for cleanup?  I have no idea, and [the documentation](http://ruby-doc.org/core-2.3.1/doc/syntax/control_expressions_rdoc.html#label-break+Statement) doesn't seem to think this is worth commenting on.)

### Using blocks

Anyway, with block-passing as a language feature, the "iterator protocol" is pretty straightforward: just write a method that takes a block.

```ruby
def each
    for value in self do
        yield value
    end
end
```

Be careful!  Though it's handy for iteration, that `yield` is **not** the same as Python's `yield`.  Ruby's `yield` calls the passed-in block — _yields_ control to the caller — with the given value(s).

I pulled a dirty trick there, because I expressed `each` in terms of `for`.  So how does `for` work?  Well, ah, it just delegates to `each`.  Oops!

How, then, do you write an iterator completely from scratch?  The obvious way is to use `yield` repeatedly.  That gives you something that looks rather a lot like Python, though it doesn't actually pause execution.

```ruby
class InclusiveRange
    # This gets you a variety of other iteration methods, all defined in
    # terms of each()
    include Enumerable

    def initialize(start, stop)
        @start = start
        @stop = stop
    end
    def each
        val = @start
        while val <= @stop do
            yield val
            val += 1
        end
    end
end

# 6 7 8 9
# A `for` loop would also work here
InclusiveRange.new(6, 9).each do |n|
    ...
end
```

### Enumerators

Well, that's nice for creating a whole collection type, but what if I want an ad-hoc custom iterator?  Enter the [`Enumerator`](https://ruby-doc.org/core-2.3.1/Enumerator.html) class, which allows you to create...  ah, enumerators.

Note that the relationship between `Enumerable` and `Enumerator` is _not_ the same as the relationship between "iterable" and "iterator".  Most importantly, neither is really an interface.  `Enumerable` is a set of common iteration methods that any collection type may want to have, and it expects an `each` to exist.  `Enumerator` is a generic collection type, and in fact mixes in `Enumerable`.  Maybe I should just show you some code.

```ruby
def inclusive_range(start, stop)
    Enumerator.new do |y|
        val = start
        while val <= stop do
            y.yield val
            val += 1
        end
    end
end

# 6 7 8 9
inclusive_range(6, 9).each do |n|
    puts n
end
```

`Enumerator` turns a block into a fully-fledged data stream.  The block is free to do whatever it wants, and whenever it wants to emit a value, it calls `y.yield value`.  The `y` argument is a "yielder" object, an opaque magic type; `y.yield` is a regular method call, unrelated to the `yield` keyword.  (`y << value` is equivalent; `<<` is Ruby's "append" operator.  And also, yes, bit shift.)

The amazing bit is that you can do this:

```ruby
# 6
puts inclusive_range(6, 9).first
```

`Enumerator` has all of the `Enumerable` methods, one of which is `first`.  So, that's nice.

The _really_ amazing bit is that if you stick some debugging code into the block passed to `Enumerator.new`, you'll find that...  the values are produced lazily.  That call to `first()` doesn't generate the full sequence and then discard everything after the first item; it only generates the first item, then stops.

(Beware!  The values are produced lazily, but many `Enumerable` methods are eager.  I'll get back to this in a moment.)

Hang on, didn't I say `yield` doesn't pause execution?  Didn't I also say the above `yield` is just a method call, not the keyword?

I did!  And I wasn't lying.  The really truly amazing bit, which I've seen _shockingly_ little excitement about while researching this, is that under the hood, this is all using [`Fiber`](https://ruby-doc.org/core-2.3.1/Fiber.html)s.  Coroutines.

`Enumerator.new` takes a block and turns it into a coroutine.  Every time something wants a value from the enumerator, it resumes the coroutine.  The yielder object's `yield` method then calls `Fiber.yield()` to pause the coroutine.  It works just like Lua, but it's designed to work with existing Ruby conventions, like the piles of internal iteration methods developers expect to find.

So `Enumerator.new` can produce Python-style generators, albeit in a slightly un-native-looking way.  There's also one other significant difference: an `Enumerator` can _restart itself_ for each method called on it, simply by calling the block again.  This code will print 6 three times:

```ruby
ir = inclusive_range(6, 9)
puts ir.first
puts ir.first
puts ir.first
```

For something like an inclusive range object, that's pretty nice.  For something like a file, maybe not so nice.  It also means you need to be sure to put your setup code _inside_ the block passed to `Enumerator.new`, or funny things will happen when the block is restarted.

### Something like generators

But wait, there's more.  Specifically, this common pattern, which pretty much lets you ignore `Enumerator.new` entirely.

```ruby
def some_iterator_method
    # __method__ is the current method name.  block_given? is straightforward.
    return enum_for(__method__) unless block_given?

    # An extremely accurate simulation of a large list.
    (1..1000).each do |item|
        puts "having a look at #{item}"
        # Blocks are invisible to `yield`; this will yield to the block passed
        # to some_iterator_method.
        yield item if item.even?
    end
end

# having a look at 1
# having a look at 2
# 2
puts some_iterator_method.first
```

Okay, bear with me.

First, `some_iterator_method()` is called.  It doesn't have a block attached, so `block_given?` is false, and it returns `enum_for(...)`, whatever that does.  Then `first()` is called on the result, and that produces a single element and stops.

The above code has no magic yielder object.  It uses the straightforward `yield` keyword.  Why doesn't it loop over the entire range from 1 to 1000?

Remember, `Enumerator` uses coroutines under the hood.  One neat thing coroutines can do is _pause code that doesn't know it's in a coroutine_.  Python's generators pause themselves with `yield`, and the mere presence of `yield` turns a function into a generator; but in Lua or Ruby or any other language with coroutines, any function can pause at any time.  You can even make a closure that pauses, then pass that closure to another function which calls it, without that function ever knowing anything happened.

(This arguably has some considerable _downsides_ as well — it becomes difficult to know when or where your code might pause, which makes reasoning about the order of operations much harder.  That's why Python and some other languages opted to implement async IO with an `await` keyword — anyone reading the code knows that it can _only_ pause where an `await` appears.)

(Also, I'm saying "pause" here instead of "yield" because Ruby has really complicated the hell out of this by already having a `yield` keyword that does something totally different, _and_ naming its coroutine pause function `yield`.)

Anyway, that's exactly what's happening here.  `enum_for` returns an `Enumerator` that wraps the whole method.  (It doesn't need to know `self`, because `enum_for` is actually a method inherited from `Object`, goodness gracious.)  When the `Enumerator` needs some items, it calls the method a second time with its _own_ block, running in a coroutine, just like a block passed to `Enumerator.new`.  Eventually the method emits a value using the regular old `yield` keyword, and that value reaches the block created by `Enumerator`, and that block _pauses the call stack_.  It doesn't matter that `Range.each` is eager, because its iteration is still happening in code somewhere, and that code is part of a call stack in a coroutine, so it can be paused.  Eventually the coroutine is no longer useful and gets thrown away, so the eager `each` call simply stops midway through its work, unaware that anything unusual ever happened.

In fact, despite being an `Object` method, `enum_for` isn't special at all.  It can be expressed in pure Ruby very easily:

```ruby
def my_enum_for(receiver, method)
    # Enumerator.new creates a coroutine-as-iteration-source, as above.
    Enumerator.new do |y|
        # All it does is call the named method with a trivial block.  Every
        # time the method produces a value with the `yield` keyword, we pass it
        # along to the yielder object, which pauses the coroutine.
        # This is nothing more than a bridge between "yield" in the Ruby block
        # sense, and "yield" in the coroutine sense.
        receiver.send method do |value|
            y.yield value
        end
    end
end
```

So, that's pretty neat.  Incidentally, several built-in methods like `Array.each` and `Enumerable.collect` act like this, returning an `Enumerator` if called with no arguments.

### Full laziness

I mentioned above that while an `Enumerator` fetches items lazily, many of the methods are eager.  To clarify what I mean by that, consider:

```ruby
inclusive_range(6, 9000).collect {
    |n|
    puts "considering #{n}"
    "a" * n
}.first(3)
```

`collect()` is one of those common `Enumerable` methods.  You might know it by its other name, `map()`.  Ruby is big on multiple names for the same thing: one that everyone uses in practice, and another that people who don't use Ruby will actually recognize.

Even though this code ultimately only needs three items, and even though there's all this coroutine machinery happening under the hood, this _still_ evaluates the entire range.  Why?

The problem is that `collect()` has always returned an _array_, and is generally expected to continue doing so.  It has no way of knowing that it's about to be fed into `first`.  Rather than violate this API, Ruby added a new method, `Enumerable.lazy`.  This stops after three items:

```ruby
inclusive_range(6, 9000).lazy.collect {
    |n|
    puts "considering #{n}"
    "a" * n
}.first(3)
```

All this does is return an [`Enumerator::Lazy`](https://ruby-doc.org/core-2.3.1/Enumerator/Lazy.html) object, which has lazy implementations of various methods that would usually do a full iteration.  Methods like `first(3)` are still "eager" (in the sense that they just return an array), since their results have a fixed finite size.

This seems a little clunky to me, since the end result is still an object with a `collect` method that doesn't return an array.  I suspect the real reason is just that `Enumerator` was added first; even though the coroutine support was already there, `Enumerator::Lazy` only came along later.  Changing _existing_ eager methods to be lazy can, ah, [cause problems]({filename}/2016-07-31-python-faq-how-do-i-port-to-python-3.markdown).

The only built-in type that seems to have _interesting_ `lazy` behavior is `Range`, which can be infinite.

```ruby
# Whoops, infinite loop.
(1..Float::INFINITY).select { |n| n.even? }.first(5)
# 2 4 6 8 10
(1..Float::INFINITY).lazy.select { |n| n.even? }.first(5)
```

### A loose end

I think the only remaining piece of this puzzle is something I stumbled upon but can't explain.  `Enumerator` has a [`next` method](https://ruby-doc.org/core-2.3.1/Enumerator.html#method-i-next), which returns the next value or raises `StopIteration`.

Wow, that sounds awfully familiar.

But I can't find anything in the language or standard library that _uses_ this, with one single and boring exception: [the `loop` construct](https://ruby-doc.org/core-2.3.1/Kernel.html#method-i-loop).  It catches `StopIteration` and exits the block.

```ruby
enumerator = [1, 2, 3].each
loop do
    while true do
        puts enumerator.next
    end
end
```

On the fourth call, `next()` will be out of items, so it raises `StopIteration`.  Removing the `loop` block makes this quite obvious.

That's it.  That's the only use of it in the language, as far as I can tell.  It seems almost...  vestigial.  It's also a little weird, since it keeps the current iteration state inside the `Enumerator`, unlike any of its other methods.  But it's also the only form of external iteration that I know of in Ruby, and that's handy to have sometimes.


## And, uh, so on

I intended to foray into a few more languages, including some recent lower-level friends like C++/Rust/Swift, but this post somehow spiraled out of control and hit _nine thousand words_.  No one has read this far.

Handily, it turns out that the above languages pretty much cover the basic ways of approaching iteration; if any of this made sense, other languages will probably seem pretty familiar.

- C++'s [iteration protocol](http://www.cplusplus.com/reference/iterator/)(s) has existed for a long time in the form of `++it` to advance an iterator and `*it` to read the current item, though this was usually written manually in a C-style `for` loop, and loops were generally terminated with an explicit endpoint.

    C++11 added the range-based `for`, which does basically the same stuff under the hood.  Idiomatic C++ is inscrutible, but maybe you can make sense of [this project](https://github.com/klmr/cpp11-range/) which provides optionally-infinite iterable ranges.

- Rust has an entire (extremely well-documented) [`iter` module](https://doc.rust-lang.org/stable/std/iter/index.html) with numerous iterators and examples of how to create your own.  The core of the [`Iterator` trait](https://doc.rust-lang.org/stable/std/iter/trait.Iterator.html) is just a `next` method which returns `None` when exhausted.  It also has a lot of handy Ruby-like chainable methods, so working directly with iterators is more common in Rust than in Python.

- Swift also has (well-documented) [simple `next`-based iterators](https://developer.apple.com/reference/swift/iteratorprotocol), though these return `nil` when exhausted, which means (like Lua) that an iterator cannot produce `nil` as a value.  (This isn't the case with Rust, where `next` returns an `Option<T>` — a valid `None` would be returned as `Some(None)`.)

I could probably keep finding more languages indefinitely, so I'm gonna take a break from this now.
