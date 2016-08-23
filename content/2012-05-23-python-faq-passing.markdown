title: Python FAQ: Passing
date: 2012-05-23 22:48
tags: python, tech
category: blog

Part of my [Python FAQ][].

**How do I pass by reference?  Does Python pass by reference or pass by value?**

<!-- more -->

This question is most often asked by C++ immigrants, who are used to a firm distinction between these kinds of passing and a bunch of subtle pros/cons for each.

So, then, does Python pass by reference or value?

Short answer: objects are passed as if by reference, not copied.  If you change an object in a function, it'll change in the caller.  But!  You can't _assign_ to an argument name and magically have values in the caller change.

Long answer: both, and neither.  Hmm.  This may require some context.


## References and values

In C and C++, variable declarations are really _memory_ declarations.  Consider this innocuous statement:

```c
int x;
```

This doesn't really _create_ a thing named `x`.  What it does is ensure that, at runtime, there will be some chunk of memory somewhere big enough to hold an integer, and whenever your code says `x`, it will look in that same chunk.  For all you care, that block might be in RAM or swap or hibernated or on the moon somewhere.  If you use `register`, it won't be system memory at all.  All `x` refers to here is a wink and a nod between you and your compiler, agreeing that whenever you say `x`, you mean the same _place_ as every other time you say `x`.

Enter function calls.

```c
void do_the_needful(some_bigass_struct foo) {
    /* ... */
}
```

`some_bigass_struct foo` is still a variable declaration.  At runtime, you'll have a chunk of memory the size of that struct, and anytime you say `foo` inside this function, you're guaranteed to be talking about the same chunk of memory.

Because of this, anything used as a function argument is _copied_.  When this function is called, `foo` contains a byte-for-byte copy of whatever struct was actually used as an argument.  This is pass-by-value: the function receives an equivalent value, but it has a different identity (or memory location, if you must).

Clearly this isn't going to work so well for nontrivial types.  You waste a lot of time copying this whole struct, and then your function can't even change anything and have it reflected in the caller's struct, because you only have a copy.

The C way to fix this is to pass a pointer, instead.  That's still technically passing by value, but the "value" here is a memory address.  That's only a few bytes.  And even though the pointer's identity is different, it still _points to_ the same single struct, so a function can muck about with the struct contents if it so pleases.

Along comes C++.  C++ decided that pointers were confusing, because universities were inexplicably trying to teach pointers to CS102 students who barely understood what a compiler was for, and the students weren't getting it.  Well, gosh, let's fix this by getting rid of pointers.

C++'s solution to the pass-a-bunch-of-stuff problem was to introduce _references_.

```cpp
void do_the_needful(some_bigass_struct &foo) {
    // whoa, inline comment
}
```

Now you can call `do_the_needful(bar)` without fear.  It still _looks_ like the entire struct is being passed in, but the `&` reference sigil causes `foo` to be an _alias_ for `bar`.  In other words, `foo` no longer reserves some runtime chunk of memory; it becomes another way to talk about the _same_ chunk of memory the caller has, somewhere.  And because `foo` _is_ `bar`, you can even assign to `foo` and overwrite `bar` outright—in C, you'd generally use a double pointer to do that without copying.

This is pass-by-reference: the same chunk of memory is now shared by two different variables, a feat that is impossible in C.


## Back to Python

With these (hopefully-clear) definitions, let us consider Python again.

```python
def do_the_needful(foo):
    pass

obj = SomeBigassClass()
do_the_needful(obj)
```

So, is `foo` passed by value or reference?

Again, the short answer is "neither".  But the real answer is that the question doesn't make sense for Python!  Variable names aren't fixed preallocated chunks like they are in C or C++.  Python variable names are just that: _names_.

Compare:

* In C, `int x = 3;` declares a memory chunk named `x` and writes the value `3` into it.

* In Python, `x = 3` creates a value `3` and makes `x` a name for it.  All values are objects and thus first-class entities; they can exist with several names or no name at all.

If it helps: C variables are boxes that you write values into.  Python names are tags that you put on values.  [This is a cool illustration.][illustration]

And much like in C, argument passing is just a funny way of doing assignment.  The `foo` argument in this function might as well have been assigned to with `foo = obj`; the effect would be the same.

It's not pass-by-value, then, because there's no copying done, and the function still has the same object as the caller.  (Python never copies anything implicitly.)  Is it pass-by-reference?  This sure sounds like C++ references so far.

```python
def increment(n):
    n = n + 1

i = 1
print(i)
increment(i)
print(i)
```

Nope; this will just print `1` twice.  Inside the function, assigning to `n` doesn't do anything to the _value_ `n` refers to; it just makes the name, `n`, refer to something else now.  So `n` will be `2`, sure, but then the function ends and `n` goes away and `i` is left unchanged because you never did anything to `i`.

This is _different_ from changing an existing value:

```python
def lengthen(n):
    n.append(2)

i = [1]
print(i)  # [1]
lengthen(i)
print(i)  # [1, 2]
```

In this case, `n` was never reassigned; instead, a method call altered the `value` directly.  It's still the _same list_, and both `n` and `i` refer to it, but the list's contents changed.

Got it?  Good, because there's one more wrinkle: operator overloading does weird things here.  You could rewrite both of these functions using `+=`, for example.  In `increment`, `i` wouldn't change, but in `lengthen`, it would!  This is because ints (and strs, tuples, and some other types) are immutable, so they implement `+=` literally: by creating a new object and assigning it.  But lists are mutable, so as a convenience shortcut, `+=` acts like `.extend()` and changes the list in-place.  This quirk has nothing to do with passing, though; these types just overloaded `+=` differently.

Anyway, um, this is definitely not pass-by-reference either.

If anything, Python is a third option: pass-by-object.


## What to do instead

So, wait, what if you _do_ want to write something like `increment`?

### Return stuff.

Much of the use of pointer/reference arguments in C and C++ is for "out parameters": the function returns some status value, and its actual results are "returned" by modifying particular arguments.

But this ain't C, so [why would we do that][php and c]?  You can just return multiple values.

```python
def foo():
    return True, "abc"

status, value = foo()
```

Or, you know, just raise exceptions on failure.  Then the caller doesn't get a nasty surprise when he forgets to check your status code.

### Use methods.

If you _really_ need to mutate the caller's values, you might want to use an object to store those values, and turn the function into a method.  Methods can mess with the invocant's attributes all they want, and this keeps the mess nicely contained.

```python
class Incrementer(object):
    def __init__(self, count):
        self.count = count

    def increment(self):
        self.count += 1

i = Incrementer(1)
print(i.count)  # 1
i.increment()
print(i.count)  # 2
```

### Use a mutable object.

As a last resort, you can always put the values into a list (or dict, object, etc.), pass that to the function, have the function mutate the list, then extract the new values on the outside.

That's gross, though.  Don't do that.


## Under the hood

If you must know!  In CPython, every Python value is actually a `PyObject*`.  So argument passing, assignment, etc. actually act fairly similarly to C, _if_ you wrote C where absolutely everything were a pointer (and there were no double pointers for cheating).

```c
void increment (int *n) {
    int newval = *n + 1;
    n = &newval;
}

int i = 1;
increment(&i);
```

This is the spiritual equivalent to the Python function above.  (Please ignore the impending segfault.)  Assigning to `n` naturally does nothing, because only the pointed-to value is shared.  But if that value were something mutable like a list, you could change it in-place.

And this is why "both" is a correct answer as well: you could say that Python is pass-by-value, where the values are pointers...  or you could say Python is pass-by-reference, where the references are copies.  Or you could say it's "pass-by-pointer".  But now you're thinking too hard about it.


## Conclusion

* Python functions can't replace what names in the caller refer to.
* Reassigning an argument name won't do anything useful.
* Python functions _can_ mutate their arguments, if the arguments are mutable.
* Nothing is implicitly copied in Python.
* Stop comparing Python so closely to C++ and you'll have a much better time.


## Further reading

* The Python documentation isn't terribly explicit about pass semantics.  The best I can find is the language reference on [calls][].
* That [illustration][] really is pretty cool.
* Pass-by-object is sometimes called pass-by-sharing.  Wikipedia [talks about it](http://en.wikipedia.org/wiki/Evaluation_strategy#Call_by_sharing).

[Python FAQ]: /blog/2011/07/22/python-faq/
[calls]: http://docs.python.org/reference/expressions.html#calls
[illustration]: http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#other-languages-have-variables
[php and c]: /blog/2012/04/09/php-a-fractal-of-bad-design/#c-influence
