title: Python FAQ: Descriptors
date: 2012-05-23 21:16
category: articles
series: python faq
tags: python, plt

Part of my [Python FAQ][].

**How does `@property` work? Why does it call my `__getattr__`? What’s a "descriptor"?**

<!-- more -->

Python offers several ways to hook into attribute access—that is, there are several ways you can affect what happens when someone does `obj.foo` to your object.

The most boring behavior is that the object has a `foo` attribute (perhaps set in `__init__`), or the class has a `foo` method or attribute of its own.

If you need total flexibility, there are the magic methods `__getattr__` and `__getattribute__`, which can return a value depending on the attribute name.

Somewhere between these two extremes lie _descriptors_.  A descriptor handles the attribute lookup for a _single_ attribute, but can otherwise run whatever code it wants.

[Properties][property] are very simple descriptors.  If you haven't used them before, they look like this:

```python
class Whatever(object):
    def __init__(self, n):
        self.n = n

    @property
    def twice_n(self):
        return self.n * 2

    @twice_n.setter
    def twice_n(self, new_n):
        self.n = new_n / 2

obj = Whatever(2)
print obj.n  # 2
print obj.twice_n  # 4
obj.twice_n = 10
print obj.n  # 5
```

This _does some stuff_ to create a descriptor object named `twice_n`, which jumps in whenever code tries to use the `twice_n` attribute of a `Whatever` object.  In the case of `@property`, you can then have things that look like plain attributes but act like methods.  But descriptors are a bit more powerful.


## How they work

A descriptor is just an object; there's nothing inherently special about it.  Like many powerful Python features, they're surprisingly simple.  To get the descriptor behavior, only three conditions need to be met:

1. You have a new-style class.
2. It has some object as a class attribute.
3. That object's class has the appropriate special descriptor method.

Note very carefully that these conditions are in terms of **classes**.  In particular, a descriptor **will not work** if it's assigned to an _object_ instead of a class, and an object is **not** a descriptor if you assign the _object_ a function named `__get__`.  Descriptors are all about modifying behavior for classes, **not** individual objects!

Ahem.  So, about those special descriptor methods.  There are three of them, and your object can implement whichever ones it needs.  Assuming this useless setup:

```python
class OwnerClass(object):
    descriptor = DescriptorClass()

obj = OwnerClass()
```

You can implement these methods, sometimes called the "descriptor protocol":

* `__get__(self, instance, owner)` hooks into reading, for both an object and the class itself.

    `obj.descriptor` will call `descriptor.__get__(obj, OwnerClass)`.
    
    `OwnerClass.descriptor` will call `descriptor.__get__(None, OwnerClass)`.  Here, it's polite to just return `self`, so you can still get at the descriptor object like a regular class attribute.

* `__set__(self, instance, value)` hooks into writing.

    `obj.descriptor = 5` will call `descriptor.__set__(obj, 5)`.

* `__delete__(self, instance)` hooks into deletion.

    `del obj.descriptor` will call `descriptor.__delete__(obj)`.
    
    Note this is **not** the same as `__del__`; that's something different entirely.

A minor point of confusion here: the descriptor is triggered by touching attributes on `obj`, but inside these methods, `self` is the descriptor object itself, _not_ `obj`.

You can implement any combination of these you like, and whichever you implement will be triggered.  This may or may not be what you want, e.g.: if you only implement `__set__`, you won't get a write-only attribute; `obj.descriptor` will act as normal and produce your descriptor object.


## Writing a descriptor

Talking about descriptors involves juggling several classes and instances.  Let's try a simple example, instead: recreating `property`.

First, the read-only behavior.

```python
class prop(object):
    def __init__(self, get_func):
        self.get_func = get_func

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.get_func(instance)

class Demo(object):
    @prop
    def attribute(self):
        return 133

print Demo().attribute
```

This code sneaks the descriptor in using a decorator.  Remember that decorators can be rewritten as regular function calls.  The class definition is roughly equivalent to this:

```python
def getter(self):
    return 133

class Demo(object):
    attribute = prop(getter)
```

So the descriptor, `attribute`, is just an object wrapping a single function.  When code reads from `Demo().attribute`, the descriptor calls its stored function on the `Demo` instance and passes along the return value.

(The instance has to be passed in manually because the function isn't being called as a method.  If you refer to them within a class body directly, methods are just regular functions; they only get method magic added to them at the end of the `class` block.  It's complicated.)

With this implementation, code could still do `obj.attribute = 3` and the descriptor would be shadowed.  Want setter behavior, too?  No problem; add a `__set__`.

```python
class prop(object):
    # __init__ and __get__ same as before...

    def __set__(self, instance, value):
        self.set_func(instance, value)

    def setter(self, set_func):
        self.set_func = set_func
        return self

    def set_func(self, instance, value):
        raise TypeError("can't set me")

class Demo(object):
    _value = None

    @prop
    def readwrite(self):
        return self._value

    @readwrite.setter
    def readwrite(self, value):
        self._value = value

    @prop
    def readonly(self):
        return 133

obj = Demo()
print obj.readwrite
obj.readwrite = 'foo'
print obj.readwrite
print obj.readonly
obj.readonly = 'bar'  # TypeError!
```

Look at all this crazy stuff going on.  Take it a step at a time.

The new `__set__` method is pretty much the same as before: it calls a stored function on the given `instance`.

The `setter` method makes the `@readwrite.setter` decoration work.  It stores the function, and then returns itself—remember, it's a decorator, so whatever it returns will end up assigned to the decorated function's name, `readwrite`.  The class definition is equivalent to:

```python
def func1(self):
    return self._value

readwrite = prop(func1)

def func2(self, value):
    self._value = value

readwrite = readwrite.setter(func2)
```

Don't be fooled: it looks like there are two `readwrite` functions, but the class ends up with a _single_ object that happens to contain two functions.

I include a default setter function, `set_func`, so that properties are read-only unless the class specifies otherwise.  It's got three arguments because it's a regular method: calling it with `(instance, value)` will tack the descriptor object on as the first argument.

This is most of the way to an exact clone of Python's builtin `property` type, and it's only a handful of very short methods.


## Potential uses

Properties are an obvious use, but they're built in, so why would you care about descriptors otherwise?

Maybe you wouldn't.  It's metaprogramming, after all, so you either know you need it or can't imagine why you ever would.  I've used them a couple times, though, and I've seen them in the wild enough.  Some examples:

* Pyramid includes a nifty decorator-descriptor, `@reify`.  It acts like `@property`, except that the function is only ever called once; after that, the value is cached as a regular attribute.  This gives you lazy attribute creation on objects that are meant to be immutable.  It's handy enough that I've wished it were in the standard library more than once.

* SQLAlchemy's ORM classes rely heavily on descriptors: `SomeTableClass.column == 3` is actually using a descriptor that overloads a bunch of operators.

* If you're writing a class with a lot of properties that all do similar work, you can write your own descriptor class to factor out the logic, rather than writing a bunch of similar property functions that all call more methods.

* If you find yourself writing a `__getattr__` with a huge stack of `if`s or attribute name parsing or similar, consider writing a descriptor instead.

* Ever wonder how, exactly, `self` gets passed to a method call?  Well, methods are just these class attributes that do something special when accessed via an object...  surprise, methods are descriptors!


## Descriptors and `AttributeError`

One final gotcha.  A `__get__` method is allowed to raise an `AttributeError` if it wants to express that the attribute doesn't exist.  Python will then fall back to `__getattr__` as usual.

Consider this, then:

```python
def __get__(self, instance, owner):
    log.debg("i'm in a descriptor!")
    # do stuff...
```

`log.debg` probably doesn't exist, so that code will raise an `AttributeError`...  which Python will take to mean the descriptor is saying _it_ doesn't exist.  This is probably not what you want.  Be very careful with attribute access inside a descriptor, _especially_ for classes that also implement `__getattr__`.


## Conclusion

* `property` is cool.
* Descriptors are cool.
* They aren't hard to write, if you can keep `self` and `instance` straight.
* They only work as class attributes!


## Further reading

* The [Python documentation][descriptor docs] on descriptors.  Short, to the point, and totally useless for explaining what these things are.
* The [Python HowTo](http://docs.python.org/howto/descriptor.html) on descriptors.  Rather more useful.
* Perhaps also read up on [`__getattr__`](http://docs.python.org/reference/datamodel.html#customizing-attribute-access) and [`__getattribute__`](http://docs.python.org/reference/datamodel.html#more-attribute-access-for-new-style-classes).
* The [implementation of `reify`](https://github.com/Pylons/pyramid/blob/master/pyramid/decorator.py) is a nice example, and short enough that you may want to just paste it into your own project.


[Python FAQ]: /blog/2011/07/22/python-faq/
[descriptor docs]: http://docs.python.org/reference/datamodel.html#implementing-descriptors
[property]: http://docs.python.org/library/functions.html#property
