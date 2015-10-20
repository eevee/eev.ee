title: Don't use pickle — use Camel
date: 2015-10-15 10:44
category: blog
tags: tech, python, making things

Don't use `pickle`.  Don't use `pickle`.  _Don't use `pickle`._

The problems with Python's `pickle` module are extensively documented (and repeated).  It's unsafe by default: [untrusted pickles can execute arbitrary Python code](https://www.cs.uic.edu/~s/musings/pickle.html).  Its automatic, magical behavior shackles you to the internals of your classes in non-obvious ways.  You can't even easily tell _which_ classes are baked forever into your pickles.  Once a pickle breaks, figuring out why and where and how to fix it is an utter nightmare.

Don't use `pickle`.

So we keep saying.  But people keep using `pickle`.  Because we don't offer any real alternatives.  Oops.

You can fix `pickle`, of course, by writing a bunch of `__setstate__` and `__reduce_ex__` methods, and maybe using the `copyreg` module that you didn't know existed, and oops that didn't work, and it's trial and error figuring out which types you actually need to write this code for, and all you have to do is overlook _one_ type and all your rigor was for nothing.

What about [PyYAML](http://pyyaml.org/)?  Oops, same problems: it's dangerous by default, it shackles you to your class internals, it's possible to be rigorous but hard to enforce it.

Okay, how about that thing [Alex Gaynor told me to do at PyCon](https://www.youtube.com/watch?v=7KnfGDajDQw&t=1292), where I write custom `load` and `dump` methods on my classes that just spit out JSON?  Sure, you can do that.  But if you want to serialize a _nested_ object, then you have to manually call `dump` on it, and it has to _not_ do the JSON dumping itself.  There's also the slight disadvantage that all the knowledge about what the data _means_ is locked in your application, in code — if all you have to look at is the JSON itself, there's no metadata besides "version".  You can't even tell if your codebase can still load a document without, well, just trying to load it.  We're really talking about rolling ad-hoc _data formats_ here, so I think that's a shame.

But I have good news: _I have solved all of your problems_.

<!-- more -->


## YAML

YAML has earned itself something of a bad rap, which is also a shame.  YAML is actually a pretty great format, but it's fighting an uphill battle.  [The YAML specification](http://www.yaml.org/spec/1.2/spec.html) is clearly intended for implementors and is _horrible_ as a reference, yet there is no reference guide for someone seeking to _use_ YAML rather than implement it.  The language bindings tend to be atrocious — [PyYAML's documentation](http://pyyaml.org/wiki/PyYAMLDocumentation) is a single massive page on a Trac wiki, and both it and the Ruby implementation (and probably others) allow `load` to do arbitrary bad things.  And JSON came along at just the right time to eat YAML's lunch, even though JSON is utterly hostile to human beings.

But YAML has one particularly appealing feature that few data formats have: _metadata_.  Every value in a YAML document has a type, and you can _explicitly indicate those types within YAML_.  That is, when you see this:

```yaml
- 1
- 2
- apple
```

It actually, canonically, means this:

```yaml
!!seq [
    !!int "1",
    !!int "2",
    !!str "apple",
]
```

An identifier beginning with `!` is called a _tag_, and it declares the type of the following value.  Tags that begin with `!!` are used for YAML's own native types, and occasionally co-opted by libraries like PyYAML, ahem.

Perhaps you already see where I'm going with this.  Consider the `Table` example from [Alex Gaynor's talk](https://www.youtube.com/watch?v=7KnfGDajDQw&t=1292).  It has some serialization logic baked in, and looks like this:

```python
# v1: tables are always square
class Table(object):
    def __init__(self, size):
        self.size = size

    def dump(self):
        return json.dumps({
            "version": 1,
            "size": self.size,
        })

    @classmethod
    def load(cls, data):
        assert data["version"] == 1
        return cls(data["size"])
```

Which produces this JSON:

```json
{
    "version": 1,
    "size": 25
}
```

That's not much to go on to tell a casual reader that this is intended to be a table.  But what if you could use YAML's tagging and serialize it like this, instead:

```yaml
!table
size: 25
```

Well _now you can_!


## Introducing Camel

I've spent long enough telling people to roll their own serialization rather than use `pickle`, so I've rolled it for you.  `camel` is a tiny library that wraps PyYAML, hides all its bad design decisions from you, and lets you register your own types in a useful way.  Let's try that table class again.

```python
# v1: tables are always square
class Table(object):
    def __init__(self, size):
        self.size = size


from camel import CamelRegistry
my_types = CamelRegistry()


@my_types.dumper(Table, 'table', version=1)
def _dump_table(table):
    return dict(
        size=table.size,
    )

@my_types.loader('table', version=1)
def _load_table(data, version):
    return Table(data["size"])
```

Rather than being global state that's entagled with the library itself, your serialization code is registered in an object that you can scope however you want.  Then when the time comes to use it:

```python
from camel import Camel
table = Table(25)
print(Camel([my_types]).dump(table))
```

```yaml
!table;1
size: 25
```

Amazing.  And you can, of course, nest custom objects arbitrarily-deeply in collections or even each other, and all the right things should happen.  You can even return a list or dict containing _other_ custom types, as long as the return value itself is something YAML understands natively.

Now if we change our class a bit:

```python
# v2: tables can be rectangles
class Table(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
```

All we need to do is change our functions:

```python
@my_types.dumper(Table, 'table', version=2)
def _dump_table(table):
    return dict(
        height=table.height,
        width=table.width,
    )


@my_types.loader('table', version=1)
def _load_table_v1(data, version):
    edge = data["size"] ** 0.5
    return Table(data["size"])


@my_types.loader('table', version=2)
def _load_table_v2(data, version):
    return Table(data["height"], data["width"])
```

And use it the same way as before:

```python
from camel import Camel
table = Table(5, 7)
print(Camel([my_types]).dump(table))
```

```yaml
!table;2
height: 5
width: 7
```

But old data continues to work, too.

I wrote some [more extensive documentation](http://camel.readthedocs.org/en/latest/camel.html) on this already, so I'll direct you that way rather than copy/paste all the examples.


## Look at all these amazing benefits

It's not a gigantic fucking security hole, because it doesn't call arbitrary functions with arbitrary arguments or execute arbitrary code.  It will only call the functions you give it.  The only types recognized by default are dead simple Python types that map to built-in YAML types.

Your serialization code is explicit and versioned.  It includes the names of your types, so anyone doing a major refactoring (and, hopefully, `grep`ing around for where types are used) will easily find them.  You can always tell exactly which types are sitting in data somewhere, so there are no pickle time bombs.  And if you ever truly want to throw a type away, all you have to do is write a trivial loader that "loads" into a dummy object.

You have to pick your own YAML tags, rather than having module paths baked into your data.  That paves the way to sharing serialized objects with other languages, or even standardizing a small format.

This is all just functions working with Python objects, so you can write all the tests you want without having to care about YAML at all.

And best of all, you won't have to pay someone like me to spend the better part of two weeks fixing pickles in five-year-old database tables when you try to upgrade SQLAlchemy and discover that third party libraries don't go out of their way to preserve pickle compatibility across four major versions!


## Caveats

Python 2 `str` are serialized exactly the same way as Python 3 `bytes`.  It's not pretty.  Sorry.  Actually I'm not sorry, it's 2015, what are you doing, use Unicode strings already.

Camel is backed by PyYAML, which is kinda slow and kinda memory-hungry.  On the other hand, manual control over serialization means you're much less likely to accidentally pickle a hundred kilobytes of configuration that some lazy-loaded property happened to point to, so maybe it all evens out.

You have to write some code.  The horror.  Trust me, it's _way_ better than the code you have to write to fix pickles after-the-fact.

This hasn't actually been used in production yet — I haven't actually had a need for this _myself_ since leaving Yelp.  But the entire library is a single file, less than 400 lines long.  What could _possibly_ go wrong?


## Go use it already

It's on [PyPI](https://pypi.python.org/pypi/camel), [GitHub](https://github.com/eevee/camel), and [ReadTheDocs](http://camel.readthedocs.org/en/latest/).

Also, I wrote a [condensed guide to _all_ of YAML's syntax](http://camel.readthedocs.org/en/latest/yamlref.html) that's hopefully much easier to digest than the spec.  I've often wished such a thing exists, and now it does.

Enjoy!  Let me know how it works for you.
