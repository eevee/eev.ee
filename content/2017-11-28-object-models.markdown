title: Object models
date: 2017-11-28 21:42
category: articles
tags: tech, plt, patreon

Anonymous asks, with dollars:

> More about programming languages!

Well then!

I've written before about [what I think objects _are_]({filename}/2013-03-03-the-controller-pattern-is-awful-and-other-oo-heresy.markdown): state and behavior, which in practice mostly means _method calls_.

I suspect that the popular impression of what objects _are_, and also how they should _work_, comes from whatever C++ and Java happen to do.  From that point of view, the whole post above is probably nonsense.  If the baseline notion of "object" is a rigid definition woven tightly into the design of two massively popular languages, then it doesn't even make sense to talk about what "object" _should_ mean — it _does_ mean the features of those languages, and cannot possibly mean anything else.

I think that's a shame!  It piles a lot of baggage onto a fairly simple idea.  Polymorphism, for example, has nothing to do with _objects_ — it's an escape hatch for _static type systems_.  Inheritance isn't the only way to reuse code between objects, but it's the easiest and fastest one, so it's what we get.  Frankly, it's much closer to a speed tradeoff than a fundamental part of the concept.

We could do with more experimentation around how objects work, but that's impossible in the languages most commonly thought of as object-oriented.

Here, then, is a (very) brief run through the inner workings of objects in four very dynamic languages.  I don't think I really appreciated objects until I'd spent some time with Python, and I hope this can help someone else whet their own appetite.

<!-- more -->

## Python 3

Of the four languages I'm going to touch on, Python will look the most familiar to the Java and C++ crowd.  For starters, it actually has a `class` construct.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __div__(self, denom):
        return Vector(self.x / denom, self.y / denom)

    @property
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalized(self):
        return self / self.magnitude
```

The `__init__` method is an _initializer_, which is like a constructor but named differently (because the object already exists in a usable form by the time the initializer is called).  Operator overloading is done by implementing methods with other special `__dunder__` names.  Properties can be created with `@property`, where the `@` is syntax for applying a wrapper function to a function as it's defined.  You can do inheritance, even multiply:

```python
class Foo(A, B, C):
    def bar(self, x, y, z):
        # do some stuff
        super().bar(x, y, z)
```

Cool, a very traditional object model.

Except...  for some details.

### Some details

For one, Python objects don't have a fixed layout.  Code both inside and outside the class can add _or remove_ whatever attributes they want from whatever object they want.  The underlying storage is just a `dict`, Python's mapping type.  (Or, rather, something like one.  Also, it's possible to change, which will probably be the case for everything I say here.)

If you create some attributes at the class level, you'll start to get a peek behind the curtains:

```python
class Foo:
    values = []

    def add_value(self, value):
        self.values.append(value)

a = Foo()
b = Foo()
a.add_value('a')
print(a.values)  # ['a']
b.add_value('b')
print(b.values)  # ['a', 'b']
```

The `[]` assigned to `values` isn't a _default_ assigned to each object.  In fact, the individual objects don't know about it at all!  You can use `vars(a)` to get at the underlying storage `dict`, and you won't see a `values` entry in there anywhere.

Instead, `values` lives on the _class_, which is a value (and thus an object) in its own right.  When Python is asked for `self.values`, it checks to see if `self` has a `values` attribute; in this case, it doesn't, so Python _keeps going_ and asks the _class_ for one.

Python's object model is secretly **prototypical** — a class acts as a prototype, as a shared set of fallback values, for its objects.

In fact, this is also how method calls work!  They aren't syntactically special at all, which you can see by separating the attribute lookup from the call.

```python
print("abc".startswith("a"))  # True
meth = "abc".startswith
print(meth("a"))  # True
```

Reading `obj.method` looks for a `method` attribute; if there isn't one on `obj`, Python checks the class.  Here, it finds one: it's a function from the class body.

Ah, but wait!  In the code I just showed, `meth` seems to "know" the object it came from, so it can't just be a plain function.  If you inspect the resulting value, it claims to be a "bound method" or "built-in method" rather than a function, too.  Something funny is going on here, and that funny something is the _descriptor protocol_.

### Descriptors

Python allows attributes to implement their own custom behavior when read from or written to.  Such an attribute is called a _descriptor_.  I've [written about them before]({filename}/2012-05-23-python-faq-descriptors.markdown), but here's a quick overview.

If Python looks up an attribute, finds it in a class, and the value it gets has a `__get__` method…  then _instead of_ using that value, Python will use the return value of its `__get__` method.

The `@property` decorator works this way.  The `magnitude` property in my original example was shorthand for doing this:

```python
class MagnitudeDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return (instance.x ** 2 + instance.y ** 2) ** 0.5

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    magnitude = MagnitudeDescriptor()
```

When you ask for `somevec.magnitude`, Python checks `somevec` but doesn't find `magnitude`, so it consults the class instead.  The class does have a `magnitude`, and it's a value with a `__get__` method, so Python calls that method and `somevec.magnitude` evaluates to its return value.  (The `instance is None` check is because `__get__` is called even if you get the descriptor directly from the class via `Vector.magnitude`.  A descriptor intended to work on instances can't do anything useful in that case, so the convention is to return the descriptor itself.)

You can also intercept attempts to write to or _delete_ an attribute, and do absolutely whatever you want instead.  But note that, similar to operating overloading in Python, the descriptor must be on a _class_; you can't just slap one on an arbitrary object and have it work.

This brings me right around to how "bound methods" actually work.  Functions are descriptors!  The function type implements `__get__`, and when a function is retrieved from a class via an instance, that `__get__` bundles the function and the instance together into a tiny bound method object.  It's essentially:

```python
class FunctionType:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return functools.partial(self, instance)
```

The `self` passed as the first argument to methods is not special or magical in any way.  It's built out of a few simple pieces that are also readily accessible to Python code.

Note also that because `obj.method()` is just an attribute lookup and a call, Python doesn't actually care whether `method` is a method on the _class_ or just some callable thing on the _object_.  You won't get the auto-`self` behavior if it's on the object, but otherwise there's no difference.

### More attribute access, and the interesting part

Descriptors are one of several ways to customize attribute access.  Classes can implement `__getattr__` to intervene when an attribute isn't found on an object; `__setattr__` and `__delattr__` to intervene when any attribute is set or deleted; and `__getattribute__` to implement _unconditional_ attribute access.  (That last one is a fantastic way to create accidental recursion, since any attribute access you do within `__getattribute__` will of course call `__getattribute__` again.)

Here's what I really love about Python.  It might seem like a magical special case that descriptors only work on classes, but it really isn't.  You could implement _exactly the same behavior yourself_, in pure Python, using only the things I've just told you about.  Classes are themselves objects, remember, and they are instances of `type`, so the reason descriptors only work on classes is that `type` effectively does this:

```python
class type:
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        # like all op overloads, __get__ must be on the type, not the instance
        ty = type(value)
        if hasattr(ty, '__get__'):
            # it's a descriptor!  this is a class access so there is no instance
            return ty.__get__(value, None, self)
        else:
            return value
```

You can even trivially prove to yourself that this is what's going on by skipping over `type`'s behavior:

```python
class Descriptor:
    def __get__(self, instance, owner):
        print('called!')

class Foo:
    bar = Descriptor()

Foo.bar  # called!
type.__getattribute__(Foo, 'bar')  # called!
object.__getattribute__(Foo, 'bar')  # ...
```

And that's not all!  The mysterious `super` function, used to exhaustively traverse superclass method calls even in the face of diamond inheritance, can _also_ be expressed in pure Python using these primitives.  You could write your own superclass calling convention and use it exactly the same way as `super`.

This is one of the things I really like about Python.  Very little of it is truly magical; virtually everything about the object model exists in the _types_ rather than the _language_, which means virtually everything can be _customized_ in pure Python.

### Class creation and metaclasses

A very brief word on all of this stuff, since I could talk forever about Python and I have three other languages to get to.

The `class` block itself is fairly interesting.  It looks like this:

```python
class Name(*bases, **kwargs):
    # code
```

I've said several times that classes are objects, and in fact the `class` block is one big pile of syntactic sugar for calling `type(...)` with some arguments to create a new `type` object.

The Python documentation has a [remarkably detailed description of this process](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation), but the gist is:

- Python determines the type of the new class — the _metaclass_ — by looking for a `metaclass` keyword argument.  If there isn't one, Python uses the "lowest" type among the provided base classes.  (If you're not doing anything special, that'll just be `type`, since every class inherits from `object` and `object` is an instance of `type`.)

- Python executes the class body.  It gets its own local scope, and any assignments or method definitions go into that scope.

- Python now calls `type(name, bases, attrs, **kwargs)`.  The name is whatever was right after `class`; the `bases` are position arguments; and `attrs` is the class body's local scope.  (This is how methods and other class attributes end up on the class.)  The brand new type is then assigned to `Name`.

Of course, you can mess with most of this.  You can implement `__prepare__` on a metaclass, for example, to use a custom mapping as storage for the local scope — including any _reads_, which allows for some interesting shenanigans.  The only part you _can't_ really implement in pure Python is the scoping bit, which has a couple extra rules that make sense for classes.  (In particular, functions defined within a `class` block don't close over the class body; that would be nonsense.)

### Object creation

Finally, there's what actually happens when you create an object — including a class, which remember is just an invocation of `type(...)`.

Calling `Foo(...)` is implemented as, well, _a call_.  Any type can implement calls with the `__call__` special method, and you'll find that `type` itself does so.  It looks something like this:

```python
# oh, a fun wrinkle that's hard to express in pure python: type is a class, so
# it's an instance of itself
class type:
    def __call__(self, *args, **kwargs):
        # remember, here 'self' is a CLASS, an instance of type.
        # __new__ is a true constructor: object.__new__ allocates storage
        # for a new blank object
        instance = self.__new__(self, *args, **kwargs)
        # you can return whatever you want from __new__ (!), and __init__
        # is only called on it if it's of the right type
        if isinstance(instance, self):
            instance.__init__(*args, **kwargs)
        return instance
```

Again, you can trivially confirm this by asking any type for its `__call__` method.  Assuming that type doesn't implement `__call__` itself, you'll get back a bound version of `type`'s implementation.

```python-console
>>> list.__call__
<method-wrapper '__call__' of type object at 0x7fafb831a400>
```

You can thus implement `__call__` in your own metaclass to completely change how subclasses are created — including skipping the creation altogether, if you like.

And...  there's a bunch of stuff I haven't even touched on.

### The Python philosophy

Python offers something that, on the surface, looks like a "traditional" class/object model.  Under the hood, it acts more like a prototypical system, where failed attribute lookups simply defer to a superclass or metaclass.

The language also goes to almost _superhuman_ lengths to expose all of its moving parts.  Even the prototypical behavior is an implementation of `__getattribute__` somewhere, which you are free to completely replace in your own types.  Proxying and delegation are easy.

Also very nice is that these features "bundle" well, by which I mean a library author can do all manner of convoluted hijinks, and a consumer of that library doesn't have to see any of it or understand how it works.  You only need to inherit from a particular class (which has a metaclass), or use some descriptor as a decorator, or even learn any new syntax.

This meshes well with Python culture, which is pretty big on the principle of least surprise.  These super-advanced features tend to be tightly confined to single simple features (like "makes a [weak attribute](http://classtools.readthedocs.io/en/latest/#classtools.weakattr)") or cordoned with DSLs (e.g., defining a form/struct/database table with a class body).  In particular, I've never seen a metaclass in the wild implement its own `__call__`.

I have mixed feelings about that.  It's probably a good thing overall that the Python world shows such restraint, but I wonder if there are some very interesting possibilities we're missing out on.  I implemented a metaclass `__call__` myself, just once, in an entity/component system that strove to minimize fuss when communicating between components.  It never saw the light of day, but I enjoyed seeing some new things Python could do with the same relatively simple syntax.  I wouldn't mind seeing, say, an object model based on composition (with no inheritance) built atop Python's primitives.


## Lua

Lua doesn't have an object model.  Instead, it gives you a handful of very small primitives for building your own object model.  This is pretty typical of Lua — it's a very powerful language, but has been carefully constructed to be very small at the same time.  I've never encountered anything else quite like it, and "but it starts indexing at 1!" really doesn't do it justice.

The best way to demonstrate how objects work in Lua is to build some from scratch.  We need two key features.  The first is **metatables**, which bear a passing resemblance to Python's metaclasses.

### Tables and metatables

The _table_ is Lua's mapping type and its primary data structure.  Keys can be any value other than `nil`.  Lists are implemented as tables whose keys are consecutive integers starting from 1.  Nothing terribly surprising.  The dot operator is sugar for indexing with a string key.

```lua
local t = { a = 1, b = 2 }
print(t['a'])  -- 1
print(t.b)  -- 2
t.c = 3
print(t['c'])  -- 3
```

A metatable is a table that can be associated with another value (usually another table) to change its behavior.  For example, operator overloading is implemented by assigning a function to a special key in a metatable.

```lua
local t = { a = 1, b = 2 }
--print(t + 0)  -- error: attempt to perform arithmetic on a table value

local mt = {
    __add = function(left, right)
        return 12
    end,
}
setmetatable(t, mt)
print(t + 0)  -- 12
```

Now, the interesting part: one of the special keys is `__index`, which is consulted when the base table is _indexed_ by a key it doesn't contain.  Here's a table that claims every key maps to itself.

```lua
local t = {}
local mt = {
    __index = function(table, key)
        return key
    end,
}
setmetatable(t, mt)
print(t.foo)  -- foo
print(t.bar)  -- bar
print(t[3])  -- 3
```

`__index` doesn't have to be a function, either.  It can be yet another table, in which case that table is simply indexed with the key.  If the key still doesn't exist and _that_ table has a metatable with an `__index`, the process repeats.

With this, it's easy to have several unrelated tables that act as a single table.  Call the base table an _object_, fill the `__index` table with functions and call it a _class_, and you have half of an object system.  You can even get _prototypical inheritance_ by chaining `__index`es together.

At this point things are a little confusing, since we have at least three tables going on, so here's a diagram.  Keep in mind that Lua doesn't actually have anything called an "object", "class", or "method" — those are just convenient nicknames for a particular structure we might build with Lua's primitives.

```text
                    ╔═══════════╗        ...
                    ║ metatable ║         ║
                    ╟───────────╢   ┌─────╨───────────────────────┐
                    ║ __index   ╫───┤ lookup table ("superclass") │
                    ╚═══╦═══════╝   ├─────────────────────────────┤
  ╔═══════════╗         ║           │ some other method           ┼─── function() ... end
  ║ metatable ║         ║           └─────────────────────────────┘
  ╟───────────╢   ┌─────╨──────────────────┐
  ║ __index   ╫───┤ lookup table ("class") │
  ╚═══╦═══════╝   ├────────────────────────┤
      ║           │ some method            ┼─── function() ... end
      ║           └────────────────────────┘
┌─────╨─────────────────┐
│ base table ("object") │
└───────────────────────┘
```

Note that a metatable is _not_ the same as a class; it defines behavior, not methods.  Conversely, if you try to use a class directly as a metatable, it will probably not do much.  (This is pretty different from e.g. Python, where operator overloads are just methods with funny names.  One nice thing about the Lua approach is that you can keep interface-like functionality separate from methods, and avoid clogging up arbitrary objects' namespaces.  You could even use a dummy table as a key and completely avoid name collisions.)

Anyway, code!

```lua
local class = {
    foo = function(a)
        print("foo got", a)
    end,
}
local mt = { __index = class }
-- setmetatable returns its first argument, so this is nice shorthand
local obj1 = setmetatable({}, mt)
local obj2 = setmetatable({}, mt)
obj1.foo(7)  -- foo got 7
obj2.foo(9)  -- foo got 9
```

Wait, wait, hang on.  Didn't I call these _methods_?  How do they get at the object?  Maybe Lua has a magical `this` variable?

### Methods, sort of

Not quite, but this is where the other key feature comes in: **method-call syntax**.  It's the lightest touch of sugar, just enough to have method invocation.

```lua
-- note the colon!
a:b(c, d, ...)

-- exactly equivalent to this
-- (except that `a` is only evaluated once)
a.b(a, c, d, ...)

-- which of course is really this
a["b"](a, c, d, ...)
```

Now we can write methods that actually do something.

```lua
local class = {
    bar = function(self)
        print("our score is", self.score)
    end,
}
local mt = { __index = class }
local obj1 = setmetatable({ score = 13 }, mt)
local obj2 = setmetatable({ score = 25 }, mt)
obj1:bar()  -- our score is 13
obj2:bar()  -- our score is 25
```

And that's all you need.  Much like Python, methods and data live in the same namespace, and Lua doesn't care whether `obj:method()` finds a function on `obj` or gets one from the metatable's `__index`.  _Unlike_ Python, the function will be passed `self` either way, because `self` comes from the use of `:` rather than from the lookup behavior.

(Aside: strictly speaking, _any_ Lua value can have a metatable — and if you try to index a non-table, Lua will _always_ consult the metatable's `__index`.  Strings all have the `string` library as a metatable, so you can call methods on them: try `("%s %s"):format(1, 2)`.  Numbers, strings, functions, and nil each share a type-specific metatable, and you can only change it with the `debug` library which is often unavailable, so this is of limited use.  But if you're writing Lua bindings from C, you can give your pointers metatables directly to give them methods implemented in C.)

### Bringing it all together

Of course, writing all this stuff every time is a little tedious and error-prone, so instead you might want to wrap it all up inside a little function.  No problem.

```lua
local function make_object(body)
    -- create a metatable
    local mt = { __index = body }
    -- create a base table to serve as the object itself
    local obj = setmetatable({}, mt)
    -- and, done
    return obj
end

local Dog = {
    -- this acts as a "default" value; if obj.barks is missing, __index will
    -- kick in and find this value on the class.  but if obj.barks is assigned
    -- to, it'll go in the object and shadow the value here.
    barks = 0,

    bark = function(self)
        self.barks = self.barks + 1
        print("woof!")
    end,
}

local mydog = make_object(Dog)
mydog:bark()  -- woof!
mydog:bark()  -- woof!
mydog:bark()  -- woof!
print(mydog.barks)  -- 3
print(Dog.barks)  -- 0
```

It works, but it's fairly barebones.  The nice thing is that you can extend it pretty much however you want.  I won't reproduce an entire serious object system here — lord knows there are enough of them floating around — but the implementation I have for my LÖVE games lets me do this:

```lua
local Animal = Object:extend{
    cries = 0,
}

-- called automatically by Object
function Animal:init()
    print("whoops i couldn't think of anything interesting to put here")
end

-- this is just nice syntax for adding a first argument called 'self', then
-- assigning this function to Animal.cry
function Animal:cry()
    self.cries = self.cries + 1
end

local Cat = Animal:extend{}

function Cat:cry()
    print("meow!")
    Cat.__super.cry(self)
end

local cat = Cat()
cat:cry()  -- meow!
cat:cry()  -- meow!
print(cat.cries)  -- 2
```

When I say you can extend it however you want, I mean that.  I could've implemented Python (2)-style `super(Cat, self):cry()` syntax; I just never got around to it.  I could even make it work with multiple inheritance if I really wanted to — or I could go the complete opposite direction and only implement composition.  I could implement descriptors, customizing the behavior of individual table keys.  I could add pretty decent syntax for composition/proxying.  I am trying very hard to end this section now.

### The Lua philosophy

Lua's philosophy is to...  not have a philosophy?  It gives you the bare minimum to make objects work, and you can do absolutely whatever you want from there.  Lua does have something resembling prototypical inheritance, but it's not so much a first-class feature as an emergent property of some very simple tools.  And since you can make `__index` be a function, you could avoid the prototypical behavior and do something different entirely.

The very severe downside, of course, is that you have to find or build your own object system — which can get pretty confusing very quickly, what with the multiple small moving parts.  Third-party code may also have its _own_ object system with subtly different behavior.  (Though, in my experience, third-party code tries very hard to avoid needing an object system at all.)

It's hard to say what the Lua "culture" is like, since Lua is an embedded language that's often a little different in each environment.  I imagine it has a thousand millicultures, instead.  I _can_ say that the tedium of building my own object model has led _me_ into something very "traditional", with prototypical inheritance and whatnot.  It's partly what I'm used to, but it's also just really dang easy to get working.

Likewise, while I love properties in Python and use them all the dang time, I've yet to use a single one in Lua.  They wouldn't be particularly hard to add to my object model, but having to add them myself (or shop around for an object model with them _and also_ port all my code to use it) adds a huge amount of friction.  I've thought about designing an interesting ECS with custom object behavior, too, but…  is it really worth the effort?  For all the power and flexibility Lua offers, the cost is that by the time I have something working at all, I'm too exhausted to actually _use_ any of it.


## JavaScript

JavaScript is notable for being preposterously heavily used, yet not having a `class` block.

Well.  Okay.  Yes.  [It has one _now_.]({filename}/2017-10-07-javascript-got-better-while-i-wasnt-looking.markdown)  It didn't for a very long time, and even the one it has now is sugar.

Here's a vector class again:

```javascript
class Vector {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    get magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    dot(other) {
        return this.x * other.x + this.y * other.y;
    }
}
```

In "classic" JavaScript, this would be written as:

```javascript
function Vector(x, y) {
    this.x = x;
    this.y = y;
}

Object.defineProperty(Vector.prototype, 'magnitude', {
    configurable: true,
    enumerable: true,
    get: function() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    },
});


Vector.prototype.dot = function(other) {
    return this.x * other.x + this.y * other.y;
};
```

Hm, yes.  I can see why they added `class`.

### The JavaScript model

In JavaScript, a new type is defined in terms of a _function_, which is its constructor.

Right away we get into trouble here.  There is a very big difference between these two invocations, which I actually completely forgot about just now after spending four hours writing about Python and Lua:

```javascript
let vec = Vector(3, 4);
let vec = new Vector(3, 4);
```

The first calls the function `Vector`.  It assigns some properties to `this`, which here is going to be `window`, so now you have a global `x` and `y`.  It then returns nothing, so `vec` is `undefined`.

The second calls `Vector` with `this` set to a new empty object, then evaluates to that object.  The result is what you'd actually expect.

(You can detect this situation with the strange `new.target` expression, but I have never once remembered to do so.)

From here, we have true, honest-to-god, first-class prototypical inheritance.  The word "prototype" is even _right there_.  When you write this:

```javascript
vec.dot(vec2)
```

JavaScript will look for `dot` on `vec` and (presumably) not find it.  It then consults `vec`'s _prototype_, an object you can see for yourself by using `Object.getPrototypeOf()`.  Since `vec` is a `Vector`, its prototype is `Vector.prototype`.

I stress that `Vector.prototype` **is not** the prototype for `Vector`.  It's the prototype for _instances of_ `Vector`.

(I say "instance", but the true type of `vec` here is still just _object_.  If you want to find `Vector`, it's automatically assigned to the `constructor` property of its own `prototype`, so it's available as `vec.constructor`.)

Of course, `Vector.prototype` can itself have a prototype, in which case the process would continue if `dot` were not found.  A common (and, arguably, very bad) way to simulate single inheritance is to set `Class.prototype` to an _instance of_ a superclass to get the prototype right, then tack on the methods for `Class`.  Nowadays we can do `Object.create(Superclass.prototype)`.

Now that I've been through Python and Lua, though, this isn't particularly surprising.  I kinda spoiled it.

I suppose one difference in JavaScript is that you can tack arbitrary attributes directly onto `Vector` all you like, and they will remain _invisible_ to instances since they aren't in the prototype chain.  This is kind of backwards from Lua, where you can squirrel stuff away in the _metatable_.

Another difference is that _every single object_ in JavaScript has a bunch of properties already tacked on — the ones in `Object.prototype`.  Every object (and by "object" I mean any mapping) has a prototype, and that prototype defaults to `Object.prototype`, and it has a bunch of ancient junk like `isPrototypeOf`.

(Nit: it's possible to explicitly create an object with no prototype via `Object.create(null)`.)

Like Lua, and unlike Python, JavaScript doesn't distinguish between keys found on an object and keys found via a prototype.  Properties can be defined on prototypes with `Object.defineProperty()`, but that works just as well directly on an object, too.  JavaScript doesn't have a _lot_ of operator overloading, but some things like `Symbol.iterator` also work on both objects and prototypes.

### About this

You may, at this point, be wondering what `this` _is_.  Unlike Lua and Python (and the last language below), `this` is a special built-in value — a _context_ value, invisibly passed for every function call.

It's determined by where the function came from.  If the function was the result of an attribute lookup, then `this` is set to the object containing that attribute.  Otherwise, `this` is set to the global object, `window`.  (You can also set `this` to whatever you want via the `call` method on functions.)

This decision is made _lexically_, i.e. from the literal source code as written.  There are no Python-style bound methods.  In other words:

```javascript
// this = obj
obj.method()
// this = window
let meth = obj.method
meth()
```

Also, because `this` is reassigned on _every_ function call, it cannot be meaningfully closed over, which makes using closures within methods incredibly annoying.  The old approach was to assign `this` to some other regular name like `self` (which got syntax highlighting since it's also a built-in name in browsers); then we got `Function.bind`, which produced a callable thing with a fixed context value, which was kind of nice; and now finally we have arrow functions, which explicitly close over the current `this` when they're defined and don't change it when called.  Phew.

### Class syntax

I already showed class syntax, and it's really just one big macro for doing all the prototype stuff The Right Way.  It even prevents you from calling the type without `new`.  The underlying model is exactly the same, and you can inspect all the parts.

```javascript
class Vector { ... }

console.log(Vector.prototype);  // { dot: ..., magnitude: ..., ... }
let vec = new Vector(3, 4);
console.log(Object.getPrototypeOf(vec));  // same as Vector.prototype

// i don't know why you would subclass vector but let's roll with it
class Vectest extends Vector { ... }

console.log(Vectest.prototype);  // { ... }
console.log(Object.getPrototypeOf(Vectest.prototype))  // same as Vector.prototype
```

Alas, class syntax has a couple shortcomings.  You can't use the `class` block to assign arbitrary _data_ to either the type object or the prototype — apparently it was deemed too confusing that mutations would be shared among instances.  Which…  is…  how prototypes work.  How Python works.  How JavaScript itself, one of the most popular languages of all time, has worked for **twenty-two years**.  Argh.

You can still do whatever assignment you want _outside_ of the class block, of course.  It's just a little ugly, and not something I'd think to look for with a sugary class.

A more subtle result of this behavior is that a `class` block isn't _quite_ the same syntax as an object literal.  The check for data isn't a runtime thing; `class Foo { x: 3 }` fails to _parse_.  So JavaScript now has two _largely but not entirely identical_ styles of key/value block.

### Attribute access

Here's where things start to come apart at the seams, just a little bit.

JavaScript doesn't really have an attribute _protocol_.  Instead, it has two...  extension points, I suppose.

One is `Object.defineProperty`, seen above.  For common cases, there's also the `get` syntax inside a property literal, which does the same thing.  But unlike Python's `@property`, these aren't wrappers around some simple primitives; they _are_ the primitives.  JavaScript is the only language of these four to have "property that runs code on access" as a completely separate first-class concept.

If you want to intercept _arbitrary_ attribute access (and some kinds of operators), there's a _completely different_ primitive: the [`Proxy`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) type.  It doesn't let you intercept attribute access or operators; instead, it produces a wrapper object that supports interception and defers to the wrapped object by default.

It's cool to see composition used in this way, but also, extremely weird.  If you want to make your own type that overloads `in` or calling, you _have_ to return a `Proxy` that wraps your own type, rather than actually returning your own type.  It's workable, though — constructors can return whatever object they want, and proxies are transparent enough that `instanceof` already behaves correctly.  (If it didn't, you could customize `instanceof` with `Symbol.hasInstance` — which is really operator overloading, implement yet another completely different way.)

I know the design here is a result of legacy and speed — if any object could intercept _all_ attribute access, then _all_ attribute access would be slowed down everywhere.  Fair enough.  It still leaves the surface area of the language a bit…  bumpy?


### The JavaScript philosophy

It's a little hard to tell.  The original idea of prototypes was interesting, but it was hidden behind some _very_ awkward syntax.  Since then, we've gotten a bunch of extra features awkwardly bolted on to reflect the wildly varied things the built-in types and DOM API were already doing.  We have `class` syntax, but it's been explicitly designed to avoid exposing the _prototype_ parts of the model.

I admit I don't do a _lot_ of heavy JavaScript, so I might just be overlooking it, but I've seen virtually no code that makes use of any of the recent advances in object capabilities.  Forget about custom iterators or overloading call; I can't remember seeing any JavaScript in the wild that even uses properties yet.  I don't know if everyone's waiting for sufficient browser support, nobody knows about them, or nobody cares.

The model has advanced recently, but I suspect JavaScript is still shackled to its legacy of "something about prototypes, I don't really get it, just copy the other code that's there" as an object model.  Alas!  Prototypes are so good.  Hopefully `class` syntax will make it a bit more accessible, as it has in Python.


## Perl 5

Perl 5 also doesn't have an object system and expects you to build your own.  But where Lua gives you two simple, powerful tools for building one, Perl 5 feels more like a puzzle with half the pieces missing.  Clearly they were going for _something_, but they only gave you half of it.

In brief, a Perl object is a reference that has been blessed with a package.

I need to explain a few things.  Honestly, one of the biggest problems with the original Perl object setup was how many strange corners and unique jargon you had to understand just to get off the ground.

(If you want to try running any of this code, you should stick a `use v5.26;` as the first line.  Perl is very big on backwards compatibility, so you need to opt into breaking changes, and even the mundane `say` builtin is behind a feature gate.)

### References

A **reference** in Perl is sort of like a pointer, but its main use is very different.  See, Perl has the strange property that its data structures try _very hard_ to spill their contents all over the place.  Despite having dedicated syntax for arrays — `@foo` is an array variable, distinct from the single scalar variable `$foo` — it's actually impossible to _nest_ arrays.

```perl
my @foo = (1, 2, 3, 4);
my @bar = (@foo, @foo);
# @bar is now a flat list of eight items: 1, 2, 3, 4, 1, 2, 3, 4
```

The idea, I guess, is that an array is not _one thing_.  It's not a container, which happens to hold multiple things; it **is** multiple things.  Anywhere that expects a single value, such as an array element, cannot contain an array, because an array fundamentally _is not_ a single value.

And so we have "references", which are a form of indirection, but also have the nice property that they're _single values_.  They add containment around arrays, and in general they make working with most of Perl's primitive types much more sensible.  A reference to a variable can be taken with the `\` operator, or you can use `[ ... ]` and `{ ... }` to directly create references to anonymous arrays or hashes.

```perl
my @foo = (1, 2, 3, 4);
my @bar = (\@foo, \@foo);
# @bar is now a nested list of two items: [1, 2, 3, 4], [1, 2, 3, 4]
```

(Incidentally, this is the sole reason I initially abandoned Perl for Python.  Non-trivial software kinda requires nesting a lot of data structures, so you end up with references _everywhere_, and the syntax for going back and forth between a reference and its contents is tedious and ugly.)

A Perl object must be a reference.  Perl doesn't care what _kind_ of reference — it's usually a hash reference, since hashes are a convenient place to store arbitrary properties, but it could just as well be a reference to an array, a scalar, or even a sub (i.e. function) or filehandle.

I'm getting a little ahead of myself.  First, the other half: blessing and packages.

### Packages and blessing

Perl _packages_ are just namespaces.  A package looks like this:

```perl
package Foo::Bar;

sub quux {
    say "hi from quux!";
}

# now Foo::Bar::quux() can be called from anywhere
```

Nothing shocking, right?  It's just a named container.  A lot of the details are kind of weird, like how a package exists in some liminal quasi-value space, but the basic idea is a Bag Of Stuff.

The final piece is "blessing," which is Perl's funny name for binding a package to a reference.  A very basic class might look like this:

```perl
package Vector;

# the name 'new' is convention, not special
sub new {
    # perl argument passing is weird, don't ask
    my ($class, $x, $y) = @_;

    # create the object itself -- here, unusually, an array reference makes sense
    my $self = [ $x, $y ];

    # associate the package with that reference
    # note that $class here is just the regular string, 'Vector'
    bless $self, $class;

    return $self;
}

sub x {
    my ($self) = @_;
    return $self->[0];
}

sub y {
    my ($self) = @_;
    return $self->[1];
}

sub magnitude {
    my ($self) = @_;
    return sqrt($self->x ** 2 + $self->y ** 2);
}

# switch back to the "default" package
package main;

# -> is method call syntax, which passes the invocant as the first argument;
# for a package, that's just the package name
my $vec = Vector->new(3, 4);
say $vec->magnitude;  # 5
```

A few things of note here.  First, `$self->[0]` has nothing to do with objects; it's normal syntax for getting the value of a index 0 out of an array reference called `$self`.  (Most classes are based on hashrefs and would use `$self->{value}` instead.)  A blessed reference _is still a reference_ and can be treated like one.

In general, `->` is Perl's dereferencey operator, but its exact behavior depends on what follows.  If it's followed by brackets, then it'll apply the brackets to the thing in the reference: `->{}` to index a hash reference, `->[]` to index an array reference, and `->()` to call a function reference.

But if `->` is followed by an identifier, then it's a _method call_.  For packages, that means calling a function in the package and passing the package name as the first argument.  For objects — blessed references — that means calling a function in the _associated_ package and passing the object as the first argument.

This is a little weird!  A blessed reference is a superposition of two things: its normal reference behavior, and some _completely orthogonal_ object behavior.  Also, object behavior has no notion of methods vs data; it only knows about methods.  Perl lets you omit parentheses in a lot of places, including when calling a method with no arguments, so `$vec->magnitude` is really `$vec->magnitude()`.

Perl's blessing bears some similarities to Lua's metatables, but ultimately Perl is much closer to Ruby's "message passing" approach than the above three languages' approaches of "get me something and maybe it'll be callable".  (But this is no surprise — Ruby is a spiritual successor to Perl 5.)

All of this leads to one little wrinkle: how do you actually expose data?  Above, I had to write `x` and `y` methods.  Am I supposed to do that for every single attribute on my type?

Yes!  But don't worry, there are third-party modules to help with this incredibly fundamental task.  Take [`Class::Accessor::Fast`](http://search.cpan.org/~kasei/Class-Accessor-0.51/lib/Class/Accessor.pm), so named because it's faster than `Class::Accessor`:

```perl
package Foo;
use base qw(Class::Accessor::Fast);
__PACKAGE__->mk_accessors(qw(fred wilma barney));
```

(`__PACKAGE__` is the lexical name of the current package; `qw(...)` is a list literal that splits its contents on whitespace.)

This assumes you're using a hashref with keys of the same names as the attributes.  `$obj->fred` will return the `fred` key from your hashref, and `$obj->fred(4)` will change it to 4.

You also, somewhat bizarrely, have to _inherit from_ `Class::Accessor::Fast`.  Speaking of which,


### Inheritance

Inheritance is done by populating the package-global `@ISA` array with some number of (string) names of parent packages.  Most code instead opts to write `use base ...;`, which does the same thing.  Or, more commonly, `use parent ...;`, which…  also…  does the same thing.

Every package implicitly inherits from `UNIVERSAL`, which can be freely modified by Perl code.

A method can call its superclass method with the `SUPER::` pseudo-package:

```perl
sub foo {
    my ($self) = @_;
    $self->SUPER::foo;
}
```

However, this does a depth-first search, which means it almost certainly does the wrong thing when faced with multiple inheritance.  For a while the accepted solution involved a third-party module, but Perl eventually grew an alternative you have to opt into: C3, which may be more familiar to you as [the order Python uses](https://perldoc.perl.org/mro.html#How-does-C3-work).

```perl
use mro 'c3';

sub foo {
    my ($self) = @_;
    $self->next::method;
}
```

Offhand, I'm not actually sure how `next::method` works, seeing as it was originally implemented in pure Perl code.  I suspect it involves peeking at the caller's stack frame.  If so, then this is a very different style of customizability from e.g. Python — the MRO was never _intended_ to be pluggable, and the use of a special pseudo-package means it _isn't_ really, but someone was determined enough to make it happen anyway.

### Operator overloading and whatnot

Operator overloading looks a little weird, though really it's pretty standard Perl.

```perl
package MyClass;

use overload '+' => \&_add;

sub _add {
    my ($self, $other, $swap) = @_;
    ...
}
```

[`use overload`](https://perldoc.perl.org/overload.html) here is a _pragma_, where "pragma" means "regular-ass module that does some wizardry when imported".

`\&_add` is how you get a reference to the `_add` sub so you can pass it to the `overload` module.  If you just said `&_add` or `_add`, that would _call_ it.

And that's it; you just pass a map of operators to functions to this built-in module.  No worry about name clashes or pollution, which is pretty nice.  You don't even have to give references to functions that live in the package, if you don't want them to clog your namespace; you could put them in another package, or even inline them anonymously.

One especially interesting thing is that Perl lets you overload _every_ operator.  Perl has a lot of operators.  It considers some math builtins like `sqrt` and trig functions to be operators, or at least operator-y enough that you can overload them.  You can also overload the "file test" operators, such as `-e $path` to test whether a file exists.  You can overload conversions, including implicit conversion to a _regex_.  And most fascinating to me, you can overload _dereferencing_ — that is, the thing Perl does when you say `$hashref->{key}` to get at the underlying hash.  So a single object could pretend to be references of multiple different types, including a subref to implement callability.  Neat.

Somewhat related: you can overload basic operators (indexing, etc.) on basic _types_ (not references!) with the [`tie`](https://perldoc.perl.org/functions/tie.html) function, which is designed completely differently and looks for methods with fixed names.  Go figure.

You can intercept calls to nonexistent methods by implementing a function called `AUTOLOAD`, within which the `$AUTOLOAD` global will contain the name of the method being called.  Originally this feature was, I think, intended for loading binary components or large libraries on-the-fly only when needed, hence the name.  Offhand I'm not sure I ever saw it used the way `__getattr__` is used in Python.

Is there a way to intercept _all_ method calls?  I don't think so, but it _is_ Perl, so I must be forgetting something.

### Actually no one does this any more

Like a decade ago, a council of elder sages sat down and put together a whole whizbang system that covers all of it: [Moose](http://search.cpan.org/~ether/Moose-2.2009/lib/Moose.pm).

```perl
package Vector;
use Moose;

has x => (is => 'rw', isa => 'Int');
has y => (is => 'rw', isa => 'Int');

sub magnitude {
    my ($self) = @_;
    return sqrt($self->x ** 2 + $self->y ** 2);
}
```

Moose has its own way to do pretty much everything, and it's all built on the same primitives.  Moose also adds _metaclasses_, somehow, despite that the underlying model doesn't actually support them?  I'm not entirely sure how they managed that, but I do remember doing some class introspection with Moose and it was _much_ nicer than the built-in way.

(If you're wondering, the built-in way begins with looking at the hash called `%Vector::`.  No, that's not a typo.)

I really cannot stress enough just _how much stuff_ Moose does, but I don't want to delve into it here since Moose itself is not actually the language model.

### The Perl philosophy

I hope you can see what I meant with what I first said about Perl, now.  It has multiple inheritance with an MRO, but uses the wrong one by default.  It has extensive operator overloading, which looks nothing like how inheritance works, and also some of it uses a totally different mechanism with special method names instead.  It only understands methods, not data, leaving you to figure out accessors by hand.

There's 70% of an object system here with a clear general design it was gunning for, but none of the pieces really look anything like each other.  It's weird, in a distinctly Perl way.

The result is certainly flexible, at least!  It's especially cool that you can use whatever kind of reference you want for storage, though even as I say that, I acknowledge it's no different from simply subclassing `list` or something in Python.  It _feels_ different in Perl, but maybe only because it _looks_ so different.

I haven't written much Perl in a long time, so I don't know what the community is like any more.  Moose was already ubiquitous when I left, which you'd think would let me say "the community mostly focuses on the stuff Moose can do" — but even a decade ago, Moose could already do far more than I had ever seen done by hand in Perl.  It's always made a big deal out of roles (read: interfaces), for instance, despite that I'd never seen anyone care about them in Perl before Moose came along.  Maybe their presence in Moose has made them more popular?  Who knows.

Also, I wrote Perl _seriously_, but in the intervening years I've only encountered people who only ever used Perl for one-offs.  Maybe it'll come as a surprise to a lot of readers that Perl has an object model _at all_.


## End

Well, that was fun!  I hope any of that made sense.

Special mention goes to Rust, which doesn't have an object model you can fiddle with at runtime, but _does_ do things [a little differently](https://doc.rust-lang.org/book/second-edition/ch10-02-traits.html).

It's been _really_ interesting thinking about how tiny differences make a huge impact on what people do in practice.  Take the choice of storage in Perl versus Python.  Perl's massively common `URI` class uses _a string_ as the storage, nothing else; I haven't seen anything like that in Python aside from `markupsafe`, which is specifically designed as a string type.  I would guess this is partly because Perl _makes you choose_ — using a hashref is an obvious default, but you have to make that choice one way or the other.  In Python (especially 3), inheriting from `object` and getting dict-based storage is the obvious thing to do; the ability to use another type isn't quite so obvious, and doing it "right" involves a tiny bit of extra work.

Or, consider that Lua _could_ have descriptors, but the extra bit of work (especially _design_ work) has been enough of an impediment that I've never implemented them.  I don't think the object implementations I've looked at have included them, either.  Super weird!

In that light, it's only natural that objects would be so strongly associated with the features Java and C++ attach to them.  I think that makes it all the more important to play around!  Look at what Moose has done.  No, really, you should bear in mind my description of how Perl does stuff and flip through the [Moose documentation](http://search.cpan.org/~ether/Moose-2.2009/lib/Moose.pm).  It's amazing what they've built.
