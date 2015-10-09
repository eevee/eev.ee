title: Gotcha: Python, scoping, and closures
date: 2011-04-24 15:39:00
category: blog
tags: python, plt, tech

I've [touched on this kind of thing][architectural fallacies] before, but I just saw it come up again, and I think it's worth its own post not buried in an avalanche of armchair psychology.  Plus, I remembered that Blogofile does syntax highlighting.

## Closures in a loop

If you've been linked here, you've probably complained that this doesn't work as you expect:

```python
funcs = []
for i in range(4):
    def f():
        print i
    funcs.append(f)

for f in funcs:
    f()
```

The output will be `3`, repeated four times.  Gasp!  Python is totally broken!  It doesn't support closures!

Well, no.  Python supports closures all too well, and that's causing the problem here.  The issue is with _scoping_.

<!-- more -->

In Python, variables are "declared" automatically when you assign to them.  Speaking as a prolific Perl author, this saves a lot of `my` typing.  The downside is that Python still needs to know what that variable's scope should be.  For various reasons that I can only conjecture wildly about, the only constructs that introduce scopes in Python are functions.  (And files, and classes, and generator expressions, and comprehensions in Python 3.  But, you know.)

The problem, then, is that our code snippet is actually doing this:

```python
funcs = []
for i in range(4):  # `i` is actually created at the top of the enclosing function, only once
    # `i` has a new value assigned to it here
    def f():
        # Each incarnation of this function closes over the SAME VARIABLE, `i`
        print i
    funcs.append(f)
```

Closures close over _variables_, not values.  This `i` is scoped within the enclosing function like any other variable, and each iteration of the loop just assigns a new value to it.  Every `f` closes over the same variable `i`, and then we assign a new value to `i`.  At the end of the loop, when we run all the functions, they all look up the current value of `i`, which is 3, and print it.

The difference is easier to see in a language with explicit declaration, like Perl:

```perl
# The usual way:
my @funcs;
for my $i (0 .. 3) {
    # A brand new variable called $i is created here
    push @funcs, sub {
        # Each incarnation of this function closes over a DIFFERENT variable; they're just all named `$i`
        warn $i;
    };
    # $i is destroyed here
}

# What Python is doing, sorta:
my @funcs;
my $i;  # $i is created here
for $i (0 .. 3) {  # $i is assigned to here
    push @funcs, sub {
        # This is always the same variable, created outside the loop
        warn $i;
    };
}
```

(I admit that the second Perl example actually _does not_ work like Python, because Perl is extra-tricky, and implicitly localizes loop variables using some strange lexical-dynamic scope that doesn't exist anywhere else in the language.  Given that you can just say `for my $i` in the first place, I really don't think this is the right behavior.  I've been using Perl for a decade and didn't even know about it until just now.  See [note #2 in this namespaces FAQ][perl namespaces] and [perlsyn][perlsyn foreach].)

And because I can't resist the opportunity to rag on JavaScript, I must point out that it has the worst of both worlds: variables are declared (or, should be), but are function-scoped no matter where you put the declaration.  So this has the same behavior as in Python:

```javascript
var funcs = [];
for (var i = 0; i < 4; i++) {  // `i` created once, function-scoped
    var j = i;  // `j` created once, also function-scoped
    funcs.push(function() {
        // Yep, this is the same variable `j` every time
        alert(j);
    });
}
```


### The solution

Enough yammering; how do you fix this?

You have two main options here.  The fairly straightforward approach is to create a factory function.

```python
def make_f(i):
    def f():
        print i
    return f

funcs = []
for i in range(4):
    funcs.append(make_f(i))
```

Variables are function-scoped, so you'll get a new inner `i` on every call to `make_f`, and each `f` will ultimately close around a different variable.  I tend to do the above, because the alternative is a bit more obscure:

```python
funcs = []
for i in range(4):
    def f(i=i):
        print i
    funcs.append(f)
```

This relies on _another_ Python quirk that tends to surprise everyone at least once, and fighting quirks with quirks strikes me as a bad plan.  But this solves the problem because a function's defualt arguments are evaluated when the function is defined and bound to the function _by value_—just like any other kind of assignment, function call, or argument passing.  Thus the above is actually creating functions `def f(i=0):`, `def f(i=1):`, etc.  The resulting functions aren't closures at all.

(The surprise usually comes when you try to do `def f(x=[]):` and discover that `x` defaults to the _same list_ on every call.  So this approach may not work in more complex cases anyway.)


## The other problem: mutating outer variables

The problem mentioned in my [other post][architectural fallacies] was related to the above, but slightly different.  It's less common, but still trips people up, so here it is again:

```python
def outer():
    times_called = 0
    def inner():
        times_called += 1
        print "called", times_called, "times"
    return inner

f = outer()
f()
```

You'll get an `UnboundLocalError` at the `times_called += 1` line.  Why?

Again, Python scopes variables to the nearest function.  When you say `times_called = times_called + 1`, two things happen at different times:

1. When Python compiles the function, it sees `times_called =`, and declares a _new variable_, scoped within `inner`, named `times_called`.

2. When Python executes the function, it needs to compute `times_called + 1`.  Okay, well, what's `times_called`?  It's a local variable...  but, oops, it doesn't have a value yet!  Raise error.

The assignment creates a new inner variable that masks the outer variable.  To invoke Perl for clarification again (ha, what?!), you're implying this:

```perl
sub outer {
    my $times_called = 0;
    return sub {
        my $times_called;  # implicit in Python!
        $times_called += 1;
        print "called $times_called times";
    };
}
```

Of course, this will still work in Perl: variables default to `undef` which becomes 0 (with a warning) when used as a number.


### The other solution

You have a whopping _three_ options here.  The one most commonly seen in the wild is to close over a mutable value.

```python
def outer():
    times_called = [0]
    def inner():
        times_called[0] += 1
        print "called", times_called[0], "times"
    return inner
```

This works because you're never declaring a new variable.  Remember that in Python, there are three completely different kinds of assignment; they look similar, but don't really have anything to do with each other.  `name =` declares a new variable, scoped to the enclosing function (file, class, whatever), and managed by the Python virtual machine.  `obj.attr =` is sugar for `obj.__setattr__(attr, ...)`; the semantics are the responsibility of the object, and Python doesn't much care what they are.  `container[key] =` is simialarly sugar for `container.__setitem__(key, ...)`, and is also handled by the object itself.  The latter two cases don't touch Python's notion of a variable at all; they ask an object to _change itself_, in-place.  The above code only creates one variable called `times_called`, a list of one element, and mutates it.  The original code created _two_ variables, and one clobbered the other.

The downside of this is that, well, it's super ugly.  For anything beyond the most trivial cases, what you probably wanted was some kind of construct that brings together both state and behavior.  You know, an _object_.

```python
class Counter(object):
    def __init__(self):
        self.times_called = 0
    def __call__(self):
        self.times_called += 1
        print "called", self.times_called, "times"

f = Counter()
f(); f(); f()
```

Again, this mutates `self` in-place rather than creating new names.  The problem evaporates, and the code is slightly less contrived.

Luckily for the functional programming addicts, Guido has smiled upon you, and this problem is fixed in Python 3 with a new keyword.

```python
def outer():
    times_called = 0
    def inner():
        nonlocal times_called  # This says "don't declare a new var; use the outer one", just like `global`
        times_called += 1
        print "called", times_called, "times"
    return inner
```

Now you just need to wait for the world to [migrate to Python 3][python 3 wos], and you're all set.


[architectural fallacies]: /blog/2011/04/17/architectural-fallacies/#reverse-injustification
[perl namespaces]: http://perl.plover.com/FAQs/Namespaces.html.en#Notes
[perlsyn foreach]: http://perldoc.perl.org/perlsyn.html#Foreach-Loops
[python 3 wos]: http://python3wos.appspot.com/
