title: Sylph: the programming language I want
date: 2015-02-28 23:58
category: blog
tags: sylph, plt, tech, popular

Creating a programming language is apparently all the rage these days, and it's got me thinking about what I would really like to see in one.  I'm starting to suspect the things I want are either impossible or mutually incompatible, so I'd better write them down and let smarter people tell me why I can't have everything and also a pony.

I'm strongly influenced by my love of Python, my aversion to C and C++, my fascination with Rust, and the bits of Haskell I understand.  I very recently read an overview of Nim, which is part of what got my juices flowing.  Also I have a lot of fond memories of what Perl 6 could have been, so, fair warning.

This is a brain dump, not a linear narrative, so some of this might be mutually referential or causally reversed or even complete nonsense.  Please pardon the dust.

<!-- more -->


## Core goals

1. **Safety**.  The wrong thing should always be harder, or even impossible.  I don't think this will be low-enough level that you'll be allocating your own memory or otherwise susceptible to memory errors, but the [semipredicate problem](http://en.wikipedia.org/wiki/Semipredicate_problem) is a good example of an API that makes it easier to do the wrong thing than the right thing.  Languages should help me avoid mistakes.

2. **Familiarity**.  Learning the language should not require a complete upheaval of your mental model of the universe.  (Sorry, Haskell.)  Average code should be moderately comprehensible to anyone with any programming experience at all, and ideally to a lot of people with none at all.  And in a different sense, programs by different authors should look at least moderately similar, so you don't feel you have to learn the author's _style_ just to make sense of their code.  (Compare: Perl.)

3. **Convenience**.  We like to say "expressiveness" or "elegance" or "ease of use" but honestly I just want to splort out some code with as few arbitrary hurdles as possible.  Note that this is somewhat at odds with familiarity, since extreme brevity makes code more obtuse.

4. **Rigor**.  I really don't like C-derived static typing, but I _love_ being able to statically reason about code without having to run it.  That's what humans do all the time, but we have relatively primitive automated tools for doing the same.  So I would like to have lots of that, without getting stuck in the existing box of "let's add static types that look a lot like Java, well that's the best that we can do, I guess we're done here".

5. **Locality**.  A stronger and better-defined constraint than "readability".  I want to maximize how much I can know about runtime context for a given line of code, while minimizing how much stuff I have to read (or, worse, hunt down).  Brevity is part of this: an idea that seems simple to humans should ideally take less code to express.  Namespacing is another part: if I see a function name I don't recognize, I want to know where it came from as easily as possible.

6. **Dynamism**.  It's useful and I like it.  When untamed, it's at odds with locality, which is why this is listed lower.

7. **Portability**.  I don't care so much about running on VMS.  I _do_ care about being easily shipped as a single unit to Windows machines; being immune to library upgrades elsewhere on the system; being able to run on mobile platforms and JavaScript VMs; being embeddable as a scripting language; and compiling to the Z-Machine.  I don't want portability to be the lone reason that entire _huge_ problem spaces are rendered completely inaccessible.

8. **Speed**.  This is last, but I would still like to be _fast enough_, whatever that means.

(I'm sure someone will at this point object that the language is not the implementation.  Except it totally is, and besides, neither one exists yet.  Shush.)


## Gripes with existing languages

A slight diversion.  It's helpful to remember what I'm trying to fix, or what problems I'm trying to avoid.

### General

In C-family languages, type names are a completely different "kind of thing" that exist outside the language proper, vanish at runtime, and have different syntax from actual code that happens to reuse most of the same symbols for slightly different purposes.

In C++-family languages, generic types are an exponential nightmare of madness to express.  One of the nice things about Python (or even Haskell!) is that "a list" is always the same kind of thing, whereas C++ or Rust need to specialize because the underlying storage might look different.

Interfaces and multiple inheritance are usually implemented in a way that means all methods share a single global namespace.  (Counterexamples: Rust traits, Haskell typeclasses)

Unicode is hard.  Time is hard.  Serialization is hard.  Everyone is bad at all of them.


### Python

The descriptor protocol is neat, but I very frequently find myself wanting to know the name I'm "about to be assigned to".  For function decorators you already have this in the form of `__name__`, but for anything else you don't.

Magic methods work differently from other methods, in that they only work when assigned to the class and not when assigned to an instance.  It turns out there's not actually a good reason for this.

There's lots of nitpicking that could be done regarding Python...  but a lot of it either results from the rules of its dynamic runtime, or would be something to obviously not replicate.  So, sorry, this will not be the Python gripefest people sometimes ask me for.


### Nim

Namespacing is very sloppy.  Importing a module dumps the entirety of its contents into your namespace.  Method calls are just syntactic sugar: `a.b()` is exactly the same as `b(a)`, so methods are also in the globalish namespace.  Seems to rely extremely heavily on overloading.

As an example I saw some demo code that did this:

```nim
let json = %{"visitors": %visitors,
             "uniques": %uniques.len,
             "ip": %ip}
```

What the hell is `%` doing here?  Is that built-in syntax or what?

No, it turns out that's a custom operator from the standard `json` module, which polymorphically converts various values into JSON nodes.  That's cute, I guess, but if the variable here hadn't been named "json" then I would've had _absolutely no idea_ where to even look.  The short file this came from has _eight_ imports at the top; I would've had to check all of them, after figuring out that `%{` isn't language syntax.

Also the "pragma" syntax is `{.foo.}`, which looks really bizarre.  Currently a whole lot of features are implemented with pragmas so this seems to show up a lot, and often in the middle of a definition.

It looks like creating new structures requires doing e.g. `newSeq[type](size)` or `initSet[type]()`, which seems cumbersome.  I assume this is because types can't have methods, and even if they did have methods they'd live in the global namespace anyway.  So the only kinds of construction you get are literal struct building, or writing a creatively-named global constructor.  And note that these are both in the standard library; I don't know why one is "new" and the other is "init".


### Rust

Lifetimes are fantastically useful but suddenly become very awkward when dealing with recursive data structures.

It turns out I don't actually really care about pointers versus not so anything in the language that tries to make me care (like, you can't have a trait value, only a pointer to one!) is mostly just annoying.

Discovering you want to add a mutable element (like a filehandle) to a structure means you have to slap `mut`s all over the place, including for any transitive container, which by the way will probably cause all kinds of borrow errors.  `RefCell` to the rescue, at least.

I seem to have a knack for trying to write things in Rust that rely on intertangled references and mutability: first a game, then a UI library...





## Syntax

I don't really know what it'll look like, but I need to get this out of the way so I can write example code.  I'm pretty fond of Python's syntax for being relatively low on noise.  (See: locality.)  I'll be writing examples in something vaguely Python-like, but don't take that to mean I'm 100% set on anything in particular just because I wrote it down here.

That said, there are a couple fundamentals I'm pretty attached to:

- **Indentation for blocks**

    If your language has braces, then you are indenting for the sake of humans (because humans are good at noticing alignment and edges), and bracing for the sake of computers.  That's double the effort for something as mundane as where a block ends.  If they get out of sync, then your code naturally breaks in a way that's very difficult for you to detect.

    Also, braces mean that you waste an entire line at the end of every block just for a single closing brace.  If you use Allman style, you _also_ spend a line at the start of every block.  That means a lot of vertical space lost, which means less code on my screen at once.  See: locality.

    This also eliminates all possible arguments about brace style, removes the need for braceless blocks, and frees up a valuable pair of bracketing characters for other potential uses.

- **Tabs are a syntax error**

    If blocks are delimited by invisible characters then they should really only be delimited by _one kind of_ invisible character.

I have a few other vague ideas, but they're really more about features than syntax, so they'll come up below.


## Compilation and speed

There is a thing that bothers me sometimes about hot Python code.  I'm sure it bothers everyone eventually.

Some 99% of Python code I write could be ported directly to C, line by line, and compiled.  It's just math and function calls on known concrete types.  Sprinkle some type names around, pretend there's a stdlib worth mentioning, throw it at GCC, and bam!  My program is a hundred times faster.

But I _use_ Python for that other 1% of shenanigans, which let me define restricted DSLs, which let me operate on generic data easily, which let me patch third-party libraries, which let me control the environment when I'm running tests.

I value those things, certainly.  But it still bothers me, when it happens to matter, that my options are two extremes: to use a very stodgy (but fast) language or to use a very slow (but expressive) language.

The current approach is to throw JITs at existing languages, and that is a really cool area of research that I don't understand at all.  Here, though, I have a different opportunity: I'm designing a language from scratch, and I have an interest in making it amenable to static analysis.  Surely I can put that effort towards analysis that's helpful for a compiler.

Some of this will require knowing enough to unbox values and skip dynamic dispatch.  But I'm also interested in recognizing common patterns and skipping the usual overhead of language features, when possible.  More wild speculation on this later.

I don't expect to be appropriate for kernels, or AAA game engines, or any other cases where people deeply care about things like whether there's a vtable.  I _would_ like concrete operations on concrete types to have minimal overhead.  Essentially, the more the dev is willing to tell us about their code, the more we should be able to reward them by speeding it up.

On the other hand, if I ship something you could call a compiler, I _also_ want to ship a more traditional interpreter.  Compilers are things that throw away as much information about your program as possible.  They are, by their very nature, actively hostile towards development.  It'd be really nice if you didn't need to actually compile until you were ready to deploy.

## Type system

This is so complex that I actually have to use another level of subheadings.  I apologize in advance for how incoherent this might be.

### Inference

Type inference is great.  It is not great _enough_.

Rust is the static language I've most recently bumbled across, and it has left a couple of distinct impressions on me.

First: I have to explicitly declare types for every argument to every function.  But rather a lot of the time, I don't actually care about the types of some of the arguments — all I do is pass them along to another function.

In a language like Python this is a far bigger problem, since wrapper functions and delegation and other forms of proxying are extremely common.  What on Earth is the type of `*args`?

My knee-jerk reaction here is to say that argument types are also inferred, but that leaves us with very few actual concrete type annotations.  Which sounds great, but then, where do the types actually come from?

I'm hesitant to follow this train of thought, because it seems like unexplored territory, and surely there's a good reason for that.  But here I go anyway.

Consider this code:

```python
def foo(a, b, c):
    if a.startswith(b):
        c.append(a)
```

What are the types of those arguments?

If you know Python, you probably know the answer already: `a` is a string, `b` is a string (or a tuple of strings), and `c` is a list.  Also, `c` is _probably_ a list of strings.

No types appear anywhere in that code, but any Python dev knows exactly what can be passed to it.  We know `.startswith` is the name of a string method, we know what it operates on and we know that `.append` is likewise the name of a list method.

The function _might_ have been intended for methods of those names on other types, true.  But it doesn't really matter, because we can just get a little more vague and say _definitively_ that this code **will fail** if you pass an `a` that doesn't have a `startswith` method or a `c` that doesn't have an `append` method.

That's already a fairly decent assertion that will weed out most glaring type errors.  Numbers obviously won't work.  `None` won't work.  Files, bools, and other built-in types won't work.  There's nothing else in the language or standard library that has either of those method names.

We know all of this without running the code.  There's no reason we couldn't check it statically.  We'd be fooled by anything with a `__getattr__`, sure, but the vast majority of types don't support that.  And this is just stock Python, not even anything proposed for Sylph.  If you actually _did_ provide some type annotations, we'd know much more.

It seems I'm proposing something along the lines of statically inferred duck typing.

The big problem here is what happens if you make a typo, or call a method that you didn't mean to be possible.  If you let the compiler infer the argument types, it can't tell you when you make a mistake.

On the other hand, it could still complain _somewhere_ , as long as you actually call the function.  It would notice that `list` doesn't actually have a method called `apend`, or whatever.

Rather than explicitly annotate every argument throughout your entire codebase, you'd have an engine that would default to telling you about _conflicts_ between values and how you treat them.  I think I could get behind that.

### Signatures

But getting back to proxy functions.  `*args, **kwargs` is a fabulous thing, with a couple downsides.

1. It's two things, not one thing.
2. Because it's not one thing, you can't write a literal of it.

These are not massive inconveniences or anything, but if we're going down the road of static analysis, it would sure be nice to fix them.  So let's say there's a "signature" type representing all the things you can stuff into a function.

The signature type is really a family of generic types — some functions might accept any number of integers, some functions might accept exactly one string.  If you do something like this:

```python
def wrapper(*args, **kwargs):
    return f(extra, *args, **kwargs)
```

Then you know the signature type of `wrapper` is the same as the signature type of `f`, but with the type of `extra` in front.  You can statically enforce that `wrapper` only receives arguments that `f` will understand.

I guess that's not very mindblowing.  But when I first had this idea, I assumed that the signature type of a function would be available at runtime, as a property of the function.  I only now realize that this means:

### Types as values

In Python, `list` is both a type and a value.  You can instantiate it to create a new list object, and the type of that object will be `list`.  You can also inspect `list`, access properties on it, put it in a dict somewhere, and whatever else you might want to do with a value.

This isn't _too_ revolutionary.  The same idea exists in Perl (and Ruby)...  sort of.

But it doesn't exist in, say, C++.  Types (and namespaces and, to some extent, functions) are thrown away (yes, rtti, vtables, shut up) at compile time.  They exist as _program structure_, as scaffolding, as the stage on which your code will play someday in the future — they are not part of the orchestra.

Not only that, but types use a completely different _syntax_ than any of your "real" code.  They reuse some of the same symbols to mean vaguely similar things, but `char *` has very little to do with `*foo`.  (This is a big part of why C++ is a nightmare to parse: type descriptions and value expressions can appear in many of the same places syntactically, but mean radically different things.  Nothing in the grammar really distinguishes `char * text = "hi"` from `x * y = z`.  (Oh hey I bet that's why C originally required `struct` in front of all user-defined type names huh.))

What the hell was I even talking about here.  Oh, right.

Blah blah this is all really heading towards: the syntax for generics in C-family languages is fucking terrible.

I am sorry to be beating up on Rust here, I love you Rust, you are a very good try, but you're the static language I've used the most recently so you get the brunt of this.

CONSIDER this Rust code that a reasonable human being might try to write:

```rust
fn add<T>(a: T, b: T) -> T {
    return a + b;
}
```

If you try to compile that, you'll get an error like this:

    :::text
    <anon>:1:25: 1:30 error: binary operation `+` cannot be applied to type `T`

What you actually have to write is something like this:

```rust
use std::ops::Add;
fn add<T: Add>(a: T, b: T) -> T::Output {
    return a + b;
}
```

Now it typechecks correctly.

This seems a little ridiculous.  The compiler already knew that `T` had to be a type that supports addition — _it just told me that_.  So why am I spelling it out?

I got access to `T::Output` this way, but that's still something the compiler knew.  The _only_ way to support addition is to implement the stdlib `Add` trait, and the only possible result type is whatever the implementation says it is.  

The real answer is that Rust requires full types written out for all arguments and return values.  And this isn't really a huge deal.  You're right.  I know.

If you check out some Real Live Actual Rust Code from the standard library, for [the implementation of a standard hash map](http://doc.rust-lang.org/src/std/collections/hash/map.rs.html#490):

```rust
impl<K: Hash + Eq, V> HashMap<K, V, RandomState> {
    pub fn new() -> HashMap<K, V, RandomState> {
        Default::default()
    }
}
```

Now I'm getting a little sadder.  This code is 90% types.

It used to be worse: the keys of a hashmap were required to implement _four_ traits (I think?), and I went off to write a generic trie that was backed by hashmaps, and there were just angle brackets out the wazoo.

This still isn't a huge deal, I know.  But it gets me thinking.

One thing I think about is how in Python, everything is already generic.  I can write a function that operates on a list without doing anyting in particular to its elements, and it will just work, on any list.  Everything is generic already.  It doesn't even have to be a list; it can be any sequence.

(Speaking of, that's one of the downsides to static annotations, especially in a dynamic language: _people fuck them up_.  Way too many times I've seen someone ask about how to do type checking in Python so they can enforce that someone passes in a list, even though there's no reason the argument couldn't be a tuple or dict or any other kind of iterable thing.)

This is kind of meandering a lot oops.  The ultimate idea was that there should be regular expression syntax for composing types, and those resulting types should be _runtime values_.  So if you want a list of strings you can say:

```text
List<Str>
```

Or whatever.  (I'd rather not use angle brackets actually but let's pretend for now.)  And that will be a _value_, a type.  You can put it in a variable and use it anywhere you could put a type, or a value.  Like typedefs on steroids.

I suppose a plain list would be `List<Value>`, then, and there would be a handful of slotted types in there that you would be replacing when you applied angle brackets.  Which is really a lot like just having default arguments to functions.  Hm hm hm.

One catch here is that for actually generic code, you end up with expressions like `List<T>`, where `T` is meant as generic and thus is not actually a known identifier.  I suppose declaring these types is exactly what the angle-bracket annotation does in C++ and Rust!  I'll need something a little more clever to recognize when this is happening and do something useful and appropriate.

### Shape types

Something I'm dimly aware Closure Compiler (for annotating JavaScript) has: types based on the _contents_ of dicts.  So you can declare types like "a dict that has a `foo` key", or "a dict that has an `x` key with a numeric value and a `y` key with a numeric value and no other keys".

JavaScript objects literally _are_ dicts, so you don't have much choice here.  But this seems like a nice thing to have in general.  Plenty of dicts we use are not truly arbitrary — consider dicts of HTTP headers, where we reasonably expect some set of fundamental headers to exist and can't usefully do anything when they're missing.

It's also common enough to start out using a dict for some common bag of data and only realize much later that you really should've made it a class.  Being able to slap a type on there would at least document what you intend to have, and give you an inkling of an upgrade path.

This knits well with signature types, too — you can see how the type of `..., foo=4, **kwargs` might involve saying `foo` must be a number but other keys are allowed as well.

I haven't thought too much about this.  Just throwing it out there.

### Class definitions

I don't want classes.

Wait, wait, no, come back.  I don't want a thing I _call_ a class.  I don't want a `class` keyword.  I think it has way too much baggage.  People expect Java conventions and complain when they're missing.  "Why is there no `private`?  _Encapsulation!!_"  People (myself included) feel uncomfortable when the `class` keyword is used for things that [are not actually classes](/blog/2013/03/03/the-controller-pattern-is-awful-and-other-oo-heresy/).

Let's solve this problem and just not call them classes.  Call them _types_, because that's what they _are_.

Let me abruptly jump rails in a way I promise will make sense in a moment.  I love metaclasses.  The metaclass protocol in Python is super nifty and, in Python 3 especially, you can do some fascinating things with it.  The stdlib [`enum`](https://docs.python.org/3.4/library/enum.html) module is implemented with metaclasses:

```python
class Color(Enum):
    red = 1
    green = 2
    blue = 3

Color.red  # <Color.red: 1>, a singleton object
```

Magic!  I love magic.  I love constrained magic, anyway.  More on magic later.

I'm writing [a roguelike](https://github.com/eevee/flax) with an experimental [entity-component system](https://github.com/eevee/flax/blob/master/flax/component.py), and one of the things I do is define classes that implement exactly one of my interfaces:

```python
class GenericAI(Component, interface=IActor):
    ...
```

I also do wacky things so that calling `GenericAI()` doesn't actually create an object, but is used as a special initializer thing when defining entity types..  That's neat.  I can do neat things that use normal Python syntax but co-opt the semantics.

Something bothers me a little here though.  When I do `class Color(Enum):`, the thing I'm making is not actually a _class_, but an _enum_.  The superclass is called "Enum", yes, but that's really just there to attach the metaclass, because the metaclass syntax is a little foreign and clumsy and we want to insulate people from it.

It's also a little silly that the keyword is `class`, but the thing I'm making is not actually a "class" (there is no value in Python called "class", because it's a keyword!) — it's an instance of `type`, the base metaclass.

So what if we got rid of the `class` keyword entirely...  and you just used the metaclass?

```text
Type Dog(Animal):
    ...

Enum Color:
    ...
```

This would be pretty gnarly to parse so it probably wants to have a keyword in front:

```text
def Type Dog(Animal):
    ...

def Enum Color:
    ...
```

That's kind of wordy and even a bit C-like.  Function and class statements in Python are really just assignment, so maybe we want to shuffle this around a bit:

```text
Dog = new Type(Animal):
    ...

Color = new Enum:
    ...
```

Now this is getting kind of interesting.  Just by changing the syntax, it's obvious that metaclasses can be used for any kind of declaration where you want to _receive a scope as an argument_.  Consider how we might use this to replace `@property`:

```text
Foo = new Type:
    bar = new Property:
        def get(self):
            return self._bar

        def set(self, value):
            self._bar = value
```

Or even make anonymous objects:

```text
quux = new Value:
    cat = "meow"
    dog = "bark"

print(quux.cat)  # meow
print(quux.__type__)  # <Value>
```

You may notice I keep calling the base type `Value` instead of `Object`, which is in line with avoiding the name "class".

Downside: types would no longer actually know their own names, _unless_ the entire `x = new y:` syntax were parsed as a single unit and "x" were told to `y` somehow.  That seems like a hack.  On the other hand, with a little thought, maybe it could solve the problem where descriptors in general don't know their own names.

But there are some cool upsides.  For example, this solves a whole lot of the anonymous function problems in Python, _and_ removes a lot of the need for subclassing as an API.  Say you have a UI library that wants to register event handlers.  Instead of subclassing and defining `on_foo` methods, you could just do this:

```text
foo = new EventHandler:
    on-keydown = def(self):
        ...

    on-keyup = def(self):
        ...
```

Done and done.  And without a `class` keyword glaring at you, you don't have to feel dirty about doing it!

You could also define C types like this:

```text
CPoint = new StructType:
    x: int32
    y: int32
```

Wow!  You could even define methods that just defer to C functions taking that struct type as their first argument, and have a little FFI with minimal cruft or effort.

The more I think about this the more I like it.  It's kinda like exposing prototypical inheritance (which Python has!) in a more deliberate way?  Depends on the actual semantics of `new` when used with a type that's not a metatype, I suppose.

### Classes

Right, right, that was about classes.

The smart people around me seem generally agreed that inheritance is often not a good way to solve problems.  It's brittle in the face of upstream API changes, it tends to lead to having a god object somewhere up the hierarchy, and it gets really really hairy when you need to mix multiple behaviors together.

But it's sooo convenient.

What I would love to do is figure out the major problems we use inheritance to solve, explore alternative solutions to those problems, and then _make them easier_ than inheritance.

The most obvious alternative is proxying/delegation: wrap up an existing object, add your extensions, and transparently proxy anything else to the original object with `__getattr__`.  Honestly this could probably replace most uses of inheritance, with the minor downsides that it's cumbersome and it doesn't work on magic methods and it adds overhead.  But hey, this is a new language with a magical compiler that will fix all of that, right?

The other downside of proxying is that you can't actually interfere with the inner workings of the original type.  If the problem is that some of the type's internals are actually _wrong_ (or otherwise unsuitable to your purposes), you don't have much choice but to inherit.  (Or do you...?  I feel there should be something else here.)

An extension of the same idea is composition, where multiple disparate components are stitched together into a whole.  In my roguelike, there are multiple behavioral roles: "acts like a container", "can perform actions", etc.  An entity can have one implementation of whatever set of roles it supports, and it has no other state — everything lives in the implementations.  It makes the code a lot easier to reuse and provides plenty of namespacing, but it took a _lot_ of effort to get going.  This sort of approach, of populating "slots" in a composed object, could really stand to have some language support.

I recall reading a [blog post](http://www.saturnflyer.com/blog/jim/2015/02/10/the-4-rules-of-east-oriented-code-rule-1/) recently that contained the following alarming snippet:

```ruby
class Person
  def send_email
    emailer.send_email
    self
  end
end

person = Person.find(1) # get some record
person.emailer = Emailer.get # get some object to handle the emailing
person.send_email
```

Ha ha hold on.  So you have a type called `Person` which presumably represents a person.  You have a method on it that _sends email_, meaning your type now depends on an entire email and networking subsystem somewhere.  And to make that method work you _mutate_ your person to tack that email subsystem on before you call the method.

Jesus christ.

But this is kind of an awkward problem, come to think of it.  You could stick the method on the email subsystem, instead, but it has no particular reason to know anything about a `Person` or what `Person` thinks should be in an email.  Also you probably want other types to send email differently, right?

So where do those functions go, if not on those types?  Should you really have email-sending code (which, presumably, depends on template rendering and god knows what else) alongside your otherwise simple `Person` definition?  What if that same code is loaded in a codebase that doesn't actually _have_ an email subsystem, and now your static types don't exist?  If you put it somewhere else, how do you ensure that it gets loaded?

Somewhere a LISP weenie is now smirking and saying something about multiple dispatch.  Well, okay, sure, but you still have the same problem: where does the implementation actually live?

This is actually a problem I've run into a bit with [Inform](http://inform7.com/), the interactive fiction language.  Text adventure games tend to have a lot of interactions in them, which frequently produces questions like: if rubbing the lamp with the cloth summons a genie, where does that code go?  Is it a property of the lamp?  Of the cloth?  Of the very act of rubbing?

### Traits

The problem above (though not the question of where the code lives) would be solved in Rust with a trait.  Traits are like interfaces, but less terrible.  They require that an implementor define some set of methods, and may have "default" methods as well that can be overridden (or not).  Each trait your type implements goes in a separate implementation block.  The Rust By Example book has a good, erm, [example](http://rustbyexample.com/trait.html).

```rust
impl Animal for Dog {
    fn wag_tail(&self) { ... }
}
```

Each trait gets its own block, and any methods specific to the type get their own block as well.

This is very different from Java-like languages, with one massive advantage: _method names are actually namespaced_.

Compare to this Java strawman:

```java
public static final void class Dog implements Animal
{
    int get_legs_count() { ... }
    void wag_tail() { ... }
    void bark() { ... }
}
```

Pop quiz: which of those methods are part of the `Animal` interface?

Erm, oops.  You could make some vague guesses, but you can't actually know without going and looking at the `Animal` source code.  (See: locality.)

And yet, it gets worse!  What if you want to implement multiple interfaces, but two of them require methods with the same name?  What if you have an existing class, and you want to add support for an interface to it, but you already have a method with the same name as one in the interface?

Effectively, _all interface method names are global_.  They share a single giant namespace, just like C function names.  This is the problem I have with Go's implicit interfaces, too: you might happen to implement an interface _on accident_, just because you have methods of the right names.  Does implementing `length` mean you're a container type, or does it mean you're modeling snakes?

Rust treats trait method names as belonging _to the trait_, eliminating this problem.  I dig it.

Except...

In Rust, you can just call `dog.wag_tail()`.  Rust knows, statically, exactly what traits a given type has implemented.  So it can tell that `Dog` only has a single method anywhere that's called `wag_tail`, and calls that one.  If it's not obvious to the programmer where the method is coming from, the language is still static, so tooling could figure it out.

In practice method collisions tend to be uncommon, so trait methods are fully scoped, but end up just as convenient as a flat namespace.

Sylph is not (fully) statically typed.  In the general (unannotated) case, the Rust approach won't work.

I'm not quite sure how to fix this.  I've had a couple ideas swirling around, but I don't know if they're good enough.

First, a minor diversion: it's sometimes asked why `len` in Python is a function, rather than a method.  The answer is that of course it _is_ a method, called `__len__`.  The real answer is that Python pointedly and deliberately does not reserve _any_ method or attribute names (save for `__foo__`), leaving your classes pristine.  I imagine this is, at least in part, to avoid collision problems as described above.

(Strangely, no one ever asks why `getattr` and `setattr` are functions rather than methods, even though they work _exactly the same way_, merely deferring to dunder methods of the same names.  Semantically, the actual work of `getattr` is done by the default implementation everyone inherits, `object.__getattr__`!)

Here's how I might fix this minor oddity, and implement `len`, in Sylph:

```text
Container = new Type:
    def Iterable.len(self):
        return 5

...

from Iterable import len
c = Container()
print(c:len())
```

This is the most syntax I've made up at once and I feel very conspicuous but let's see what I've done here.

First, you can implement a method for a trait (here, `Iterable`) directly in the class body, by just using the trait method's fully-qualified name.  Now `Container` implicity does `Iterable`, like Go, but namespaced.  If you implement part of a trait but not all of it, your code won't compile.

Next, you can import names _from traits_, exposing the underlying method as a local function.  (I have put zero thought into modules or importing yet, so I don't know what this might actually look like.)  If this is how it goes in practice, most likely this particular import would be in the prelude anyway.

Then you create a new `Container` value.  At this point you could call `len(c)` to get its length, but we're trying to avoid that.  So instead you use lexical call syntax, which is merely sugar for doing exactly that.  `foo:bar(x, y, z)` is exactly the same as `bar(foo, x, y, z)`.  When you use the colon, the method name is **not** looked up on the object — it's taken from _local scope_.

Does this make everyone happy?  Is it even useful?  I don't know.  Seems interesting though.

### Classes as traits

I've heard some advice from Java land: don't use classes as the types of arguments.  Instead, create an interface matching what your class does, and use the interface as the type.  Then you can provide an alternative implementation without changing your API.

Well, screw that.  How about this: anywhere you could name a trait, _you can name a class instead_.

If you write a type and promise to implement some existing class `A` _as a trait_, then:

1. You _must_ implement all of `A`'s methods.
2. You _do not_ inherit any of `A`'s method implementations — no defaults.
3. You _must_ implement all the traits `A` implements.

Now you can fake out absolutely any other type, no matter how statically annotated the code is.  (Though you'd have to provide an alternative that meets whatever annotated requirements are on `A`.)

Downside: any code assuming it's going to receive an `A` might actually receive something else, so there'd still need to be at least one level of indirection on any attribute calls, and you're not ever gonna get C++-level method dispatch speed.  Maybe that's okay.  Or maybe the compiler can notice when there aren't actually any fakes for `A` and skip the indirection, or maybe it can fall back to something interpreter-like when it gets something that's not actually an `A`?

Another interesting question: how do you fake out built-in scalar types?  In Python, for example, there's nothing you can do to pass a "fake" string to `.startswith(...)`, because there's no way to emulate a string.  You can _subclass_ the string types, but all the built-in operations look at the underlying string value, so they just will not work on anything that isn't a string.

I suppose when even Python doesn't let you get away with patching something, I shouldn't be trying to go out of my way to allow it.

### Value types, mutability, type representations

Change is hard.  I don't know why we do it so often.

Probably types should be immutable by default (which is why I called the root type `Value` above).  This produces two immediate obvious problems in my mind:

1. It's a little weird if you have a custom constructor.  Your type would _look_ mutable in `__init__`, but nowhere else.
2. Sometimes someone else's code might produce immutable values that, for whatever reason, I direly need to hit with a hammer.

I don't know offhand how to solve these.  Maybe they don't need solving.  Python already has `namedtuple`, after all, and I can't recall direly needing to mutate those.  But if everything were immutable by default...  hmm.

(Note also that "mutable" is, itself, a slightly fuzzy concept.  A type may be immutable _in practice_, but want to have indexes or caches internal to itself that need writing to.  C++ has a `mutable` keyword as an escape hatch for this, and Rust likewise has the `RefCell` type.)

I suppose mutable types would want to inherit from something called `Mutable`, then?

I'm not sure these questions even quite make sense without knowing what type definitions _look like_.  Are there explicitly listed attributes?  I kinda want to say yes.  Or, rather, I might have to say yes.  If static annotations are to exist _at all_, you have to have somewhere to list the attributes a type has, so you can say what their types are supposed to be.

If you had that, you could avoid the dict for every object, too.

Speaking of.

Something that's actually very interesting about Perl 5 is the way objects work.  All they are is a namespace of functions tied to a reference to some data.  Usually the data is a hash, so you can store names and values, but it _doesn't have to be_.  Nothing is stopping you from using an array as the underlying data store.  The `URI` module actually uses a single string (the URI itself) as its data, so there's no extra storage required at all!

Very little code ever took advantage of this quirk, but it's a fascinating feature, and it vaguely reminds me of Python's `__slots__`, which turns attribute storage into (roughly) a tuple.

I don't know where I'm going with this.  I like the idea of detaching behavior from the shape of the underlying state.  (You can do that in Rust, too!  Traits can be attached to integers and pointers and all kinds of things.)

Behavior detached from shape.  Hm...  that makes me think of...

### Extending behavior

New languages often love to show off that they have all kinds of neat methods on core types, like `3.times` or `10.spawn-threads` which I swear I saw in the Perl 6 docs somewhere.

Those are great and all.  The downside is that they put a bigger burden on the core implementation, and sometimes very convenient methods might (ahem) have dependencies you wouldn't expect from the simplest types in the language.

So it would be pretty slick if you could extend types in a controlled way, _lexically_.  Ruby has a thing for this, called "refinements" — it's basically monkeypatching, except the changes aren't transitive across calls.  If you patch a type within your function or module, you can call whatever of the new methods you want, but if you call into other code, they only see the original type.

But if we're gonna be all about compositional types, maybe we could just use one of those instead.  Define whatever extra (or replaced) behavior you want in a proxy type, and (handwave, handwave) automatically wrap values of the underlying type in the proxy.

This is particularly suitable because you can't usefully override the internals of a type with refinements anyway — as soon as you call any original method on the type, your refinements vanish.  Wrapping is much closer to what you're doing than monkeypatching.

If this were made a natural enough part of the language, it might even be possible to allow attaching new "outside" state to other, immutable objects.

Consider decorators, which often want to attach _some_ sort of extra information onto a function.  In Python, you'd just stick an attribute on the function...  and hope that no other code wants to use the same attribute name, of course.

Imagine if you could use a proxy type instead.  I'm pulling this syntax out of my ass:

```text
FunctionLabel = new ProxyType<Function>:
    label: text

    print_label = def(self):
        print(self.label)
```

I don't really know how you'd apply that, or what the semantics of preserving the state would be (obviously you wouldn't want to completely lose the label as soon as it fell out of scope), or really much of any of the important details.

But this seems like a much more structured way to keep the convenience of Python's "you can assign to any attribute" in a more static way.  And it feels, at least, like it would knit well with the idea of first-class support for componentized types — what I've defined above is effectively a component of a function, just one that I want to attach from the "outside".

You _could_ instead use the `:foo` syntax with an imported regular function and function overloading.  But, well, I just don't like function overloading.  It's nice for some cases, but all the interesting problems I think of involve having foreign types register their own new behavior, and that's kind of ugly with function overloading — you're injecting a new function into another _module_.  It makes me frown.  I am frowning right now.

Anyway, another example.  Think of, say, SQLAlchemy in Python, where you can have a "metadata" object describing the schema of your database.  All that stuff is fixed at compile (import) time.  But the most convenient way to actually do anything with the metadata at _runtime_ is to assign a database connection to a property of it.  What if you could, with minimal effort, just define a wrapper that attached the database connection to the existing behavior?

I guess I'm kinda describing dependency injection now, but I would really like to be able to handwave it away with some language facilities.

This seems possibly related to the lexically-scoped method call operator, `foo:len`.

### State

Consider, if you will, a file object.

Files have a clear set of _states_.  They can, at the very least, be open or closed.  In Python, files start out open, and can transition to closed by calling the `.close()` method.  A closed file cannot be reopened.

Virtually every method of a file makes sense when the file is open, but _not_ when the file is closed.

This isn't terribly uncommon to see in mutable types.  In more complex cases, you might even have initialization that takes multiple steps, during which calling methods is (or should be) illegal.  Or you might have a type that can take one of two similar forms, and some methods may only make sense on one form or the other.

It would be super duper if we could make static assertions about this, right?  My class has possible states X Y Z, these methods require state X, this method transitions it from state Y to Z.

This _is_ already a thing, called typestate, but it doesn't exist in very many languages at all (which perhaps is a bad sign).  Do I dare dream of trying it out?  Could I just emulate it with composition somehow?

### Variant types

Well.  Obviously.

Open ones?  Not sure.

Actually...  this reminds me of a curiosity I noticed.  Say you have some family of related types, and you want to perform an operation on them that's similar, but _slightly_ different.

If you implement this operation as a _method_, you can factor out the similar bit as a separate method:

```python
class Base:
    def do_work(self):
        # work work work...
        self._different_part()
        # work work work...

class Impl(Base):
    def _different_part(self):
        # work work work...
```

Now if anyone else wants to make a new subtype, they can just implement `_different_part`.

But if you implement the operation as a _function_...

```python
def do_work(obj):
    # work work work...
    if isinstance(obj, A):
        # work work work...
    # work work work...
```

Now anyone who wants to make a new subtype is totally screwed.  There's no way to inject new behavior into that function from the _outside_, and yet, you'd want to do this in the first place to avoid injecting the behavior into the class!

"Ha ha!" you say.  "You can just use a type-overloaded function!"

Well yes!  You can.  If you have a language that does that, anyway.  But this section is about variant types, and I originally thought of this "problem" when writing some Rust and doing:

```rust
fn do_work(obj: Enum) {
    // work work work...
    match obj {
        EnumA => // work work work...
        EnumB => // work work work...
    }
    // work work work...
}
```

Whoops, same problem.  This feels vaguely like the old problem of having two subsystems that need to interact, but have no good reason to know about each other.

I'm told some language (Racket?  Clojure?) has _open_ variant types, so that other code can add new alternatives for the same type.  Those new variants are no longer first-class citizens, because they have no way to participate in any variant-switched behavior like the above.

I didn't get much further than that!  Injecting code into the middle of other functions is probably not a road I want to travel.

## Static assertions

Obviously types are a big part of that so I don't have too much left to say here.

It would be fantastic if functions could be categorized based on whether they have external dependencies, and whether they cause obvious mutation.  I don't think this is terribly hard, either.  Nim and D and C++ all have various facilities for detecting this and even partially evaluating code at compile time, though they all make it look slightly different than code that runs at runtime.  (I see Nim also has some builtins for doing I/O at compile time, which is pretty neat.)

If nothing else this would save me from trivial concerns like:

```python
foo = [bar(), bar()]
```

Whoops, now I've called it twice, even if it does the same thing twice, better use a temp.  If the function is pure, the compiler can do that for me.  Modulo noticing that the arguments haven't been mutated, I suppose.

There is some obvious need for wiggle room here; for example, if you're trying to debug a long chain of pure functions that are evaluated at compile time, it would be very helpful to stick some logging inside them.  But logging performs I/O, which is impure, which would completely change the compilation and maybe hide the problem you're trying to debug.  So I'd support little white lies like a built-in low-level logging thing that pretends to be pure — meaning calls may not happen as often as you expect or even at all, depending on the whims of the compiler.  (I think this is Haskell's `unsafePerformIO`.)

I'd actually like to have such a builtin anyway, something I can use for print-debugging that's guaranteed to always go somewhere as useful to a dev as is possible (like stderr).  Structured logging is great for coarse debugging after the fact, but I don't really want to mess with it when I just need quick-and-dirty temporary output from somewhere.

Wow this has nothing to do with static assertions.

Anyway, so, Nim has a somewhat generalized concept of this in the form of an effect system.  Exceptions are a built-in effect — a function that has `raise FooError` has the effect that it might raise `FooError`, and so does any other function that calls it, transitively (obviously stopping anywhere a function catches `FooError`).  This doesn't actively get in your way — it's not checked exceptions — but you can explicitly tag a function as not allowed to be some tag.  So...  it's more like a check for contradictions, akin to what I was saying about types above.

I see that [Nim's homepage](http://nim-lang.org/) has this snippet too:

```nim
parallel:
    var i = 0
    while i <= a.high:
        spawn f(a[i])
        spawn f(a[i+1])
        # ERROR: cannot prove a[i] is disjoint from a[i+1]
        # BUT: replace 'i += 1' with 'i += 2' and the code compiles!
        i += 1
```

That's pretty slick!  It's a proof engine.

I would _love_ a proof engine.  Types and exceptions are special cases of proving, so the same ideas could be extended to other constraints: write assertions, get compile-time errors if the compiler finds a contradiction, otherwise get runtime errors.

I don't know what the state of the art of this sort of thing is, nor do I know what kind of static constraints anyone would actually want to apply in practice.  But down this road is my ultimate dream: tell the language as much as possible about what I know should be true, and have it help me enforce that as early as possible.

Nim has a facility for expressing potential code rewrites within the language, so you can for example tell the compiler that `x * 2` is the same as `x + x`, and maybe it can optimize that better.  I wonder if something like that could be rigged for _implications_, so you can write the compiler's inferences in regular Sylph code as well — e.g., say that `if key in dict:` means the key must exist for the duration of the block unless something happens to change that.  Then you could later say that `dict[key]` can't possibly raise a `KeyError` _if_ you know that the key exists.  But then, does the compiler have to know what "the key exists" means?  Or could a type define its own arbitrary implications?

Also: I really really want to ship useful introspective tools, so at a _bare minimum_ it should be possible for the compiler to spit out a copy of your source code, annotated with everything it inferred.  Imagine!  Write your code like it's dynamic, then ask the compiler to do some inference, and it will fill in the static assertions for you, so you can't accidentally violate them later.

## Macros and extension

I'm wary of making the language _completely_ extensible.  I deathly want to avoid ending up with libraries that go overboard and produce a new language with different rules that I feel like I don't even know how to use any more.

Python has fairly limited extensibility.  But if you know the handful of flexible hooks it does have — `with`, decorators, metaclasses, descriptors, generators — then you can probably take a reasonable guess at how any given DSL is implemented.  And you know what the rules are, because it still _looks like_ Python syntax.

Ruby, on the other hand.  Yep.

Rust takes an interesting approach, requiring that the macro _invocation_ is obvious: a function call with a bang like `foo!()`, or I think there's an alternative that takes a block instead.  So no matter what the syntax looks like on the inside, at the very least you know where to look to figure out what's going on.

Nim has macros that operate on ASTs at compile-time.  So you can't extend the syntax or invent new syntax, like you can with Rust.  On the other hand you can create new _statements_, or at least new block headers.  I don't know how I feel about this, given that there's nothing to really distinguish new blocks from existing blocks, except maybe syntax highlighting.

When I was thinking about the idea of replacing Python's `class` keyword with something more flexible, it occurred to me that `def` syntax should probably be changed to resemble assignment as well.  But then, `def` could similarly be made more flexible...  only instead of capturing a scope, it would capture an AST.  You'd end up with something sort of like Nim's macro blocks, but there'd still be a keyword identifying it as such.

The curious part here is that you could implement `with` _in the language_.  You could even make a similar kind of block that can run the wrapped code more than once, or not at all — something that's impossible in Python with a single `with`.

I don't know what the syntax would look like, or how this would play with signatures, if the same syntax really were used for `def`.

Oh, one other problem it would (kind of) solve: one of the slickest test runners for Python is py.test, which lets you just write tests as `assert x == y`.  If the assertion fails, py.test will actually tell you what `x` and `y` are, and for native types will even figure out where they differ.  But to do this, it has to _rewrite_ your source code to inject temporary values it can extract later.  Something that allowed other Sylph code to receive an AST rather than a computed value would make this way easier and less hacktastic.


## Optimization

I feel there's a lot of room here.

For example, consider (Python) code like:

```python
try:
    value = some_dict[key]
except KeyError:
    value = some_dict[key] = compute_value()
return value
```

A lot of things happen here that have a lot of overhead.  If the value doesn't exist, you have to deal with an exception, _and_ then you have to find the same slot for the key a second time.  You might rewrite that like this to avoid both of those issues:

```python
return some_dict.setdefault(key, compute_value())
```

But what if `compute_value()` is relatively expensive?

When writing this code, you, the developer, now have to mentally weigh the overhead of the language constructs themselves against the effort required to run some of your own code.  The alternatives don't even look like each other, even though _semantically_ they do the same thing.

This is very silly.  You can see that the same slot in the same dict is being hit twice, and nothing changes either of them in the middle.  You can see that the exception is caught and discarded immediately.  A human being _knows_ that the first case can be rewritten as the second, yet Python does not.

What I want is a compiler smart enough, and an underlying language with enough expressive power, that the exception handling and double lookup are eliminated.  Not just that, but the _second_ example should work the same way: if `compute_value()` is known to be pure and idempotent, and the call to `setdefault()` is discovered to never use its value, then `compute_value()` doesn't need to be called in the first place.

Other thoughts along similar lines:

* A tree of `if some_string == "foo":` tests could easily be rewritten to either a dict lookup or a character-based trie.

* Format strings (`str.format`, `datetime.strftime`, etc.) are effectively tiny interpreters, but the format string is _very_ often a constant literal.  These could be reduced to customized code at compile time.  Rust does this with macros, but it would be great if it could be done more generally, without requiring the caller to care.  Nim has a neat facility for this, allowing functions to specialize what they do when called with a value known at compile time.

* If we know that a function is pure and idempotent, we can remove multiple calls to it, or even memoize it automatically.  (How would you know how much to memoize and when?  Could you really figure out statically whether the same function is called with the same arguments very often?)  Or, hell, imagine a Fibonacci implementation that precomputes the first few values at compile time.

* A function that requires integer arguments might sometimes be called with values statically known to be integers, and sometimes not.  So it would need to do runtime checks to avoid breaking constraints.  But those checks should be _skipped_ when the caller knows, statically, that it will always pass them.

## Ownership and memory management

There appear to be several schools of thought here.

1. You should use `malloc` and `free` (or `new` and `delete`) manually everywhere, come on, it's not that hard.

    These people are, of course, wrong.

2. Fuck it, use refcounting.

3. Fuck it, use garbage collection.

4. Let's build a whole notion of ownership into our type system whee

I sympathize with Rust's goals in #4, but I want to _avoid_ having to constantly appease a type system.

I don't think I'm going to get away with not having any kind of automatic memory management.  But...  it does occur to me that Rust has a pretty smart sense of lifetime and ownership.

Is it possible to take advantage of that same style of reasoning, at least sometimes, to detect when a value doesn't _need_ to be refcounted or garbage collected?  Plenty of values are only used as locals, or used briefly as arguments but not stored anywhere.  How feasible is it to skip the memory management overhead in these cases?

I'm sure there are a zillion caveats here!  But it does seem worth investigating.  Maybe it _is_ even feasible to have some notion of ownership in the language, even if it's only statically inferred.  It's the same kind of annoyance, where 99% of cases are trivial but we pay a cost everywhere for the sake of the 1%.

Somewhat relatedly, it would be nice to have multiple "views" of the same data without needing copies; string indexing, `ord()`, list slices, and whatnot shouldn't _really_ require copying.  Except when they should.  Sigh.

## Scalar types

### Null

Do I need a null?  Can I get away with having a null?

Even if I can't, I'd rather it be listed in type annotations explicitly.  It's kind of a colossal joke that in C++, one of the stereotypical grand examples of static typing, you can't actually express "a pointer to a value of type T".

"That's just `T*`!", cries someone who has fallen for my trap.  No!  `T*` does not actually have to point to a value of type T.  It can point to nothing at all!  `NULL` implicitly converts to and from any pointer type.  (`T*` could also be a pointer with a value of like, 3, which is obviously bogus, but at least you'd have to go out of your way to construct that.)  The type system cannot and will not help you.  Any pointer anywhere in your carefully annotated program might be `NULL` at any time, and if you forget to check for it when you need to, your program will probably just crash.  Oh, and be full of security holes.  Wow cool static typing is great!

(Yes, C++ has references, partly to try to solve this problem.  But you shouldn't store references in a container, string literals are still pointers, `this` is a pointer, etc.)

### Numbers

Integers should transparently auto-promote to bigints.  This sucks a bit, because obviously bigint math is slower than plain old int math.  I'm not sure how to prevent it from interfering with really critical computation without risking overflows.  But I don't know what to do about boxing, either, and I expect the solution will involve compiling two versions of functions and speculating about when and where promotion might be necessary and whatnot.  Something to chew on later, probably.

Floats should not exist.

Yeah.  You heard me.

They're impressively flexible for the amount of space they take up, sure.  They also completely break very common math like currency or simple fractions or _checking if numbers are equal_.  They're useful to have, but they're a horrible default.

Instead, the default should be big rationals — exact, infinite-precision ratios of two bigints.  (Possibly three bigints — the whole part might reasonable be separate, making them mixed fractions.)  If you write 1.33, you actually get 133/100.  If you write 4/3, you get 4/3.

I wonder if there's space for fixed-point in here, or if rationals are good enough when the denominator can just be an arbitrary power of ten.

I don't know how you'd indicate a literal float.  Maybe with a suffix, or maybe you'd just have to feed it to `float`.  It seems natural that floats would be infectious (operating on a float and a rat would produce a float), but then it's easy to implicitly lose precision, so maybe that should need an explicit conversion?

Fractional roots, logarithms, and trig functions would of course produce floats.

It does strike me that it'd be interesting to have a miniature CAS that internally represented values as a combination of arithmetic operations, roots, logs, π, and e.  (Even trig operations on simple fractional angles often produce exact answers.)  It'd simplify as best as it could and produce exact answers for operations like `(x ** 0.5) ** 2`, but otherwise you could force a float out at any time.  A neat thing, but probably better suited to a third-party library.  :)

Complex numbers ought to exist too.  Why not.

### Strings

Ugggh.

I do think the text-versus-bytes split in Python 3 is useful.  I also think it was hampered somewhat by the apparent approach of just slapping fixes on everything in the standard library.

I don't know how to deal with all the barriers between input and output, where you "should" explicitly be encoding or decoding.  I've run into more than one case (especially when working with subprocesses) where my code is 40% calls to `.encode('utf8')` all over the place.  It would be very nice if _any_ kind of source or target that required or produced bytes could have an encoding pipe tacked onto it.

Maybe that kind of pipe would be nice as a language/stdlib feature in general.  Something you insert between a producer and consumer that says it expects X and produces Y and guarantees Z.

Hm hm hm.

Something else that mildly bothers me is that programmers need to go out of their way to avoid appending to a buffer with `+=`, and instead use `str.join`, because it's faster, except it's not always, because that's how big O works.

If we have a compiler, then surely it can see in advance that we're doing a whole lot of string building, and try to compensate for that by allocating extra space.  If it runs out of extra space, it could allocate more _without copying yet_, making effectively a rope.  Then combine the pieces into a single string at the end, whatever "end" means.  Or, don't!  Ropes are neat.

This would effectively mutate the string (and strings are, of course, immutable), but as long as there's only one reference to the old string (which in the common case is plainly obvious), `a += ""` will immediately destroy the original anyway.

I would kind of like to have string interpolation, since in Python I often end up doing `.format(foo=foo, bar=bar)`.  But probably not by default, since most strings are not interpolated.  Perhaps a `$` prefix on a string would make it interpolate.

I do like Python's formatting mini-language, which is something you don't get with plain string interpolation, and something that objects can customize on themselves.  It's also handy to have formatting strings that are stored and only used for formatting _later_, so preserving that ability would be nice.

A Unicode character type, with Unicode character database properties, would be possibly a nice thing to have.

### Containers

Python has a pretty alright pile of container types.  Let's review:

| |type|shape|ordered|mutable|indexed|
|-|----|-----|-------|-------|-------|
|tuple|heterogenous|sequence|yes|no|no|
|list|homogenous|sequence|yes|yes|no|
|set|homogenous|sequence|no|yes|yes|
|frozenset|homogenous|sequence|no|no|yes|
|dict|homogenous|mapping|no|yes|yes|
|OrderedDict|homogenous|mapping|yes|yes|yes|

Hm...

I had a couple thoughts about this.

* Tuples act too much like lists, to the point that they are generally handwaved away as "immutable lists".  But this isn't right: tuples are compound record types, whereas lists are generally homoegenous.  Tuples are horizontal; lists are vertical.

    The problem is really that you can't just freeze an arbitrary builtin data structure.  I propose that this be made possible, with the freeze operator ❄.  Haha, no, I'm kidding.  Maybe.

    If lists _could_ be frozen, they could be used for return values much more easily, and perhaps wouldn't look so odd as arguments to `cursor.execute` or `str.__mod__` or other places where we know in advance that they won't be modified.

    To further drive this point home, maybe tuples shouldn't be iterable?  You'd have to iterate over a property.

* The standard library also has a `Counter` class, which is really more like a _multiset_.  It acts like a dict, yes, and it's implemented on top of one, but it's actually designed for containing some set of items that might contain duplicates.  That makes it an interesting middle ground between sets and lists.

* `OrderedDict` is weird.  I mean, ordered dicts in general are weird, but so are most implementations.  You can't sort an `OrderedDict`, for instance, nor insert a new key in a custom position.  It's not really meaningfully like a list; it just happens to remember insertion order.

    This train of thought originally led me to wonder whether there should be separate operators for _indexes_ versus _keys_, like Perl has.  Consider that iterating over a list produces its values, but iterating over a dict produces its keys!  Those are most interesting contents of their respective types, yes, but now there's no particular relationship between iteration and the `[]` operator.

    But then, I had the greatest idea.

    Sometimes, you want a bidirectional dict, right?  You have two groups of values and they map one-to-one.

    Sometimes, you want a three-way dict, right?  You have some group of interesting values, but need to look them up by either of two different properties.

    You can cobble this together with multiple dicts, and keep them synchronized yourself, certainly.

    But...  let me tell you about Inform 7.  One of its few container types is the _table_:

        :::inform7
        Table of Selected Elements
        Element     Symbol  Atomic number   Atomic weight
        text        text    number          number
        "Hydrogen"  "H"     1               1
        "Iron"      "Fe"    26              56

    You can look up any row in the table by searching any column, and retrieve other values for that row.  The syntax is even explicitly designed to make this simpler, by letting you refer to just the column names themselves when there's a "current" row.

    That's a little too implicit for me, but it did give me an idea.

    What if there were a table type, with an arbitrary set of fields, any of which could be indexed/unique/ordered?

    A dict is a table with two columns, one of which is indexed (and unique).  A list is a table with one column, not indexed.  A set is a table with one unique indexed column.  Hell, you could express multisets and multidicts in here too.

    I'm not proposing that dicts and lists actually be _removed_ in favor of a larger and more complex structure.  But this might be a useful thing to have exist, and if it does, it would be nice for it to have an API that lists and dicts and the like could emulate.

* Different data structures have different performance characteristics for different operations.  Sure.  We know this.

    But sometimes, we write code like this anyway:

        :::python
        x = [1, 2, 3]
        if 3 in x:
            ...

    Tut, tut.  That should really be a set!  It's much faster, O(1), for some value of 1.

    This seems so ridiculous.  I have a computer.  Can't it figure that out for me and use the right data structure?

    I wouldn't want that applied to any more than trivial cases, of course, but it bothers me that lists allow containment testing yet it's almost never actually what you want.

    But then, strings also allow testing for containment, and there's no such thing as an indexed string in Python.

## Syntax, revisited

With all the stuff about types and semantics out of the way, here are some other little syntactic ideas I have had.

- I really, really want to allow hyphens in variable names.  This means that you will have to put a space before infix subtraction.  I'm okay with this.  I might even want to use `/` as a path delimiter.  Heresy.

- Optional return values.  Is this even possible to express nicely?  You can do `foo, _ = ...` in Python, of course, but it's not exactly pretty, and it doesn't work very well at all if you want to embed the value in a larger expression.

    But they seem useful often enough, and our current workaround is to write wrappers that just throw information away.  Consider `re.sub` versus `re.subn`, which differ only in how much information they give you.

    This seems like such an obvious analogue to optional arguments, but I can't figure out how the syntax could work.

- In Python, you can't refer to a class inside itself (because it doesn't exist yet).  If you want the class to have some singletons as properties, you must either assign them to the class after the fact, or use a metaclass.  Likewise, you can't refer to "the current function".  I wouldn't mind having symbols for these things, since they're entirely lexically determined.

- Can `if foo == 1 or 2` possibly work?  It's a common enough error.  Perl 6 has a whole thing called _junctions_ that are simultaneously multiple values, so you can actually write `if $foo == 1 | 2`, but I don't think I want to go down that route.

    Maybe it could just be a compile-time error/warning when constant folding eliminates an entire condition like that.  (Unless it's `if False and...`, which I use for debugging.)

- It'd be slick to be able to tell if this is the first or last iteration of a loop.  I don't know how to do that without having a magical loop value.  Maybe it could be done in a library.

    Also sometimes useful is a separate block that runs only if the loop _never ran_, which is _not_ the thing Python's `for`/`else` does.

    And in templates, I frequently want to say: "do step A, then repeat step B for every item, then do step C...  but skip all of it if there are no items".  You can't do this if your list of items is actually something lazy.  Shame.

- It strikes me that a great many uses of function overloading are just to do something like this:

        :::c
        void draw_point(int x, int y);
        void draw_point(Point p);

    And then one of those functions would do nothing but convert argument types and defer to the other.

    This gets _really really bad_ in big complex GUI frameworks, where a function might have some fifteen arguments, and half of them might take multiple forms.  Now you have bunches of overloads, all of which just shuffle one or two bytes and call a different overload.

    This is very silly.  What if a function could say what it actually meant here: "I'd like my first argument to be a `Point`, but if I get two integers instead, here's how to convert them to the type I want"?

    I don't know what this would look like or if it's a great idea.  But it definitely comes up even in Python: think of all the APIs you've used that take either a single value or a sequence, or that take either a filename or an open file.

- Writing constructors or copy methods in Python is pretty tedious.  Would be nice to fix that.  Same applies to methods that spit out a new object with a minor alteration, which are gonna be far more common in a language encouraging immutable values.  (Of course the compiler could maybe handwave away the construction of a new object in many cases, right...?)

- There are a few cases where I want multiple "chunks" of arguments.  Like when I want to write a proxy function that can forward arbitrary keyword arguments but also takes arguments of its own, or for something like an HTML tag generator that may have arguments but also wants to use kwargs as attribute names.  Worth "fixing", I wonder?  Perhaps there's a way this could gel with the `new` statement block, which has to pass its enclosing namespace as arguments somehow anyway.

- Also relevant to argument passing: a common pattern is to turn on optional behavior with `arg=True`.  That reminds me of a Perl 6 behavior where you can pass `:arg` as an argument to a function (not even comma required), called an "adverb", and it doesn't need to have a value.  I think that might just be a named argument with an undefined value, though.  Having modifiers for functions seemed neat but the more I think about this the more I don't really like it so nevermind.

- Maybe it would be neat to have syntax to call a function as a command, parensless.  Like with a colon.  I sure am using colons a lot.  So within a type definition you could write `foo = slot: int` and `slot` would just be some builtin descriptor thing.

- I wonder how you could make a switch statement that doesn't suck.  Rust goes all out and has sub-syntax for match expressions.

    Also I would love to not have doubly-nested blocks on such a thing.  Should be able to stack the alternatives just like you stack `elif`s.

- I'm pretty in favor of explicit `self`, since the alternative is that you effectively have a superglobal that implicitly changes its value depending on _how the current function was called_ and I am not down with that.  But there might be a little room for experimentation here.  Like, Perl 6 allows you to separate the invocant from the rest of the arguments with a colon.  (Wow Perl 6 uses colon for a lot of things.)  I don't know how that helps you in Perl 6, but I can see how it might open the door for a sort of multiple dispatch based on a tuple of invocants, which might help with the idea of composing types...?  Throwing stuff at the wall here.

### Operators

I want operators to be first-class.  In Python, to do anything that looks like composition with operators, you have to import the `operator` module and pick the right name.  I would kinda like to be able to refer to operators as functions using, say, backslash:

```text
reduce(\+, [1, 2, 3])  # -> 6
\%(5, 2)  # -> 1
```

Speaking of backslash, it's a horrible line continuation character.  Just way too easy to overlook.  I would of course keep Python's current semantics of continuing lines inside brackets automatically, but for those rare cases where that's not good enough, how about an ellipsis?

```text
foo.bar.baz.quux ...
    .fred.wilma.method()
```

Speaking of line continuation, what if block headers automatically continued until a colon?  You could think of a block header as a bracketing construct which opens with `if` and closes with `:`.  So you could do these:

```text
if long-ass-condition and
        other-long-ass-condition:
    # ...

with mock.patch(something) as a,
        mock.patch(something-else) as b:
    # ...
```

I fear the nightmare of a syntax error you'd get if you forgot the colon, though.  Hmm.

Wait, this has nothing to do with operators.  Let's back up.  Here are the Python operators.

* The usual suspects: `-` `+` `*` `/` `%` will do the usual mathematical things.

* Boolean operators will be words: `and` `or` `not`.  Do I dare have an `xor`?  Its absence bothers me ever so slightly.

* I wonder if `=` should be an operator, or a statement?  There are people who grumble that some things in Python are not expressions, but what do they know anyway.  Making `=` a traditional operator would also conflict with named argument syntax.

* I'm sort of averse to the bitwise operators!  They have really weird precedence and they are used _incredibly_ rarely.  Mostly they seem to be used for porting number-heavy algorithms from C code.  But then they don't actually work right half the time, because algorithms dealing with bits very often expect certain overflow and negation behavior that just don't exist with infinite-precision integers.

    More bothersome but less concretely: the bitwise operators reserve a whopping _four_ characters on the keyboard.  There aren't that many characters in the first place, and giving a big handful of them to C legacy doesn't sit well.

    Imagine being able to use `|` in the Unix shell sense, where it often means list operations:

        :::text
        items = [1, 2, 3]
        def double(n): return n * 2
        print(items | double)  # [2, 4, 6]

    The bitwise ops could grow wordier names — Perl 6 calls them `+^` `+|` `+&` `+~` for, um, reasons.  Or they could just be functions or methods or something?

    Also, I note that a lot of the use of bitwise operators (even in C) is for packing and unpacking bits into and out of a number.  That's ridiculous.  You wouldn't store a struct in a single huge integer and pluck parts out of it with bit ops; why do we tolerate doing that when the fields happen to be smaller than a byte?  There should definitely be some kind of language support for this.  We're doing manual bit math just to feed the results to a compiler in 2015!

* I dig `//` for floor division.  Perl 6 also has a `%%` "is divisible by" operator, which sort of piques my interest.

Okay after that it gets more complicated.

#### Equality

I'm cool with having `==` be defined by types.  Cool?  Cool.

#### Overloading

I don't know how this ought to work.  You could do it multiple dispatch style, but then you end up with:

```text
def __add__(left: mytype, right: mytype):
    ...

def __add__(left: mytype, right: int):
    ...

def __add__(left: int, right: mytype):
    ...
```

That's a lot of noise, and probably a lot of repetition.  On the other hand, it's much simpler for the usual case of only supporting operations between values of the same type, whereas in Python you end up with:

```python
def __add__(self, other):
    if not isinstance(other, mytype):
        return NotImplemented

    # actual implementation
```

So maybe the question is about which is a more common thing to want.  Or maybe the question is really about whether I have function overloading in the first place.  More on that...  eventually.

#### New operators

This would be a pretty neat thing to have.

It would also do very invasive things to parsing.  Precedence is a nightmare.  Unless I just say that all custom operators have the same precedence, haha, suck it.

The one interesting thing that occurs to me is that, if operators can be referred to like other terms, you could do:

```text
from some-library import ↔
```

Now you always know exactly where operators come from (just like any other identifier), and you can't accidentally end up with two conflicting operators.

#### Range

The idea of a range operator does appeal to me, even though in practice I don't use ranges _that_ often.

Perl 6's range operator allows you to stick a `^` on either end, to make that end of the range exclusive.

```raku
1..4    # 1, 2, 3, 4
1..^4   # 1, 2, 3
1^..4   # 2, 3, 4
1^..^4  # 2, 3
```

That's kinda neat.  It means the default is rarely what you want, though, which is unfortunate.

## Exceptions

I like exceptions.  Without a very very strict type system (and heavy use of `Option` and `Result` types), I don't think you have much choice but to use exceptions.

That said, they leave some things to be desired.  Consider the trivial example from earlier:

```python
try:
    value = some_dict[key]
except KeyError:
    value = some_dict[key] = default_value
```

That is rather a lot of structurey-looking code to do something conceptually very simple.  (Perhaps for good reason, since exceptions are slow.)  Instead of using exceptions, we end up with helper methods instead, like `.get()` and `.setdefault()`.

I'd go so far as to say that any `try` block like the above, with only two clauses of one line each, looks "wrong".  `try` feels big and bulky, and it feels "wasted" on one or two lines.

If exception handling can actually be optimized away, though, that doesn't make a lot of sense.  So I wonder if it's feasible to have shorter syntax for very common cases like this, where you want to try a single simple operation and fall back to some default if it fails.

I don't have any ideas.  I know Ruby has `rescue`, but I'm not sure what I think of it.  I think there's also been a PEP proposing inline `raise` in Python; it didn't look great either.

I know Go has a `defer` statement that's kinda like an inline `finally` block.  Perhaps there's some inspiration to be found there.

## Concurrency

I want all the built-in IO to be asynchronous.

Dead simple rationale: it's very easy to convert async to sync (just wait on it!), but a huge pain in the ass to convert sync to async.  Exhibit A: the state of async in Python.

One consideration is that in an explicit-async system like asyncio, IO function calls need to be decorated with different syntax than any other function calls.  In Python 3 that's `yield from`; in C# there are `async` and `await`.  That infects your current function, turning it into an async function as well, and you have to do one of a few awkward things to join async functions to not async functions.

Maybe that's just inherent to the approach and not really a problem to be solved, especially in a static-ish language.  Arguably other things affect the way you call a function too, like exceptions and return values.

Anyway, async everything is easy enough to say, but what people actually want is threads.

I don't like threads.  Threads are awful.  Threads are `malloc`: low-level and sharp and error-prone.  They're a primitive, not a solution to a problem.

The question, then, is what I _can_ expose that doesn't have the safety problems of threads.

The core problem, as it always is, is shared mutable state.  You really don't want multiple threads of execution trying to twiddle the same value at the same time.  If there's anything resembling a runtime or automatic memory management, you really really _really_ don't want more than one thread looking at the same value at the same time.

Python and Ruby solve this by globally locking the entire runtime, so only one thread can touch it at a time.  This leads to much wailing and gnashing of teeth, and people proclaiming that the languages don't have "real threads".

I'd rather not lock everything, or clone the entire interpreter (like Perl does).

There are two major problems to solve here.

1. **Shared local state.**  Even if I say that values (messages?) have to be explicitly passed between threads, you're going to end up with the same value accessible to two threads simultaneously.

    Rust has a fix available for this, because it has a notion of _ownership_ built into the type system, so it can mostly-statically assert that anything you send to another thread is _moved_ there and becomes inaccessible to the originating thread.  This is neat, but I'm not interested in cloning Rust's entire type system — ownership and lifetimes are great for safety but not great for ease of banging out prototypes.

    It briefly occurs to me that memory management might know whether there are multiple references to a value (or any value it contains), but that sounds like a terrible idea.

    Another alternative: only allow sending immutable values between threads.  Then you could share whatever big complex structure you want, but you would have to use a controlled channel to actually update state in another thread.

    There's still a problem there, in the form of escape hatches — if your "immutable" type still has some form of cache or other mutable state as part of its plumbing, you've just shared mutable state across threads.  Perhaps only _truly_ immutable types would be shareable?  But then implementation details would have drastic effects on threads.

    Hmm.  What if the compiler could statically enforce that mutating escape hatches are only ever used while some kind of per-instance lock is held?  Or even add the locking itself, if you don't?  There'd still be room to screw it up, but at least you wouldn't trample your own state in bizarre ways.

2. **Shared global state.**  A big concern with threads in Python is that most type definitions are global — i.e. attached to a module, where modules are shared between all threads.  Part of the reason Python _must_ look up every method every time is that another thread could always have changed the definition in the meantime.

    This is a highly undesirable state of affairs!  Yet it would be a shame to forbid mutating existing types outright; that's much of the power of Python.

    On the other hand, no one said mutating types ought to be _easy_.  It's a relatively uncommon thing to do, so I don't mind having a little bit of boilerplate around it at runtime.  Given that, two possibilities come to mind:

    1. Mutation of global things can only be done as a form of dynamic scoping (think: `mock.patch`).  So it can only apply to your call stack, and only to your thread.

        Downside: this doesn't really make a lot of sense?  It would be inconsistent with mutating _everything else_, and if you can pass types around then you can't distinguish between global versus not anyway.

    2. Mutation of global things is thread-local, and every thread gets its own COW version of global stuff.

        I don't know if this is even really feasible without adding ridiculous overhead to everything every thread does.

    3. Fuck it, mutate whatever you want, but a lock will be briefly taken _around_ the mutation.

    Oh, and this doesn't even touch on actual user _data_ that's global.  I'm tempted to solve that problem by forbidding it, since it's always a bad idea.

This all sounds really hard!

I know Perl 6 has "hyperoperators" and various other mechanisms that reserve the right to do multiple things in parallel automatically.  Which sounds cool and all but hasn't been proven even in Perl 6, so.

## Standard library

Python has batteries included, and that's great, except that many of the batteries are from like 1970 and nobody remembers why we need them any more.

The standard library is where code goes to die.  But it's good to have a solid one.

A big consideration is that I want Sylph to be _embeddable_.  I'm told one of the very big reasons Lua is amenable to embedding is that it's trivial to disallow IO: you just don't have the `io` module.

Embedding Python, on the other hand, would require disabling the `io` module _and_ the `open` and `file` builtins, and `input`, and probably `__import__`, and then you'd have to do something about the `import` statement itself...

Plus, embedding Python suggests making _all_ of the standard library available, even the parts that are written in C.  You rarely see much Python code that has _no_ imports.

So perhaps this is something to keep in mind from the get-go.

* Builtins should be, by and large, _types_.  IO should definitely only exist as a module.  There can be some kind of output function, but even that should probably be easily redirected to...  elsewhere.

* The standard library should be partitioned into "critically useful for writing non-trivial programs" and "neat to have but not guaranteed to be available".  Rust does this with `core` vs `std` vs a handful of other first-party crates.

If the standard library is partitioned a bit, and it's possible to have multiple versions of a library installed, it may even be possible to _improve_ the standard library without being necessarily held back by that one bug we had ten versions ago that everyone now relies on.

Speaking of libraries...

- I would greatly prefer that there be a bigger distinction between "my code" and "not my code".  Python doesn't really have this; there's just one big namespace made up of a bunch of overlapped directory trees.  I kinda dig Rust's model, where some pile of modules make up a _crate_, which can be compiled as a unit into a single binary.

    Note that some Python projects _deliberately_ overlap their namespaces.  Sometimes this is done to allow third-party plugins to exist in the same root namespace; sometimes it's because a very large project broke into multiple first-party pieces.

- It's probably a good idea to specify what other libraries are required _upfront_.  I don't know how you would have optional support for a library, though.

- If you can have more than one version installed at a time, does that mean you can have more than one version loaded at a time?  Is that a good idea?

    Does this imply packages are scoped, or instantiated, or something?  Does that mean parametrized modules?

Modules in Python are a bit weird.  It's great that they're Just Objects, like everything else.  But that means the global scope is actually the `__dict__` of another object somewhere, which is bizarre.  And yet you can't customize modules easily, like adding a `__call__`, because those would have to go on the type.

There's also the ambiguity between modules and their properties — it drives me nuts when I see `from foo import bar`, where `bar` is a module!  Yet this too is useful at times, such as when a library replaces itself in `sys.modules` with some other object.  `q` does this, as does `plumbum`.

I wonder if top-level code in a module should just have the semantics of running at compile time.  You wouldn't be allowed to do IO, I suppose.  (Or maybe you would, but you'd probably regret it.)  That would let type and function definitions have the same semantics they do in Python.  If you just wanted to write a script, you could write a "main" function, the way most code is written in practice anyway.

Alas!  That would mean hello world would no longer be a single line.

### Misc

Serialization is terrible but doing it automatically is the worst.  Even C has automatic serialization.  The _worst_.

Instead there oughta be some opt-in thing where you implement an interface describing how to serialize your type, and register your type with a specific name, and you just get YAML or whatever.

Deserializing should probably be versioned, though!  Otherwise it's still doomed to be a nightmare.


## Dynamic runtime

I don't have much else to say about it that's not scattered through the preceding sections.  It's a useful thing to have, but it has a fairly high cost unless I can find a way to restrict the modifications you make.

_Most_ uses of the dynamic features in Python are either introspection (which is read-only, so not a big deal) or done at import time as some form of DSL (which could just be done at compile time).  Ideally there'd be some nicer way to solve the common problems too.  E.g., the "visitor pattern" in Python is `getattr(self, 'visit_' + node.type)`, which is pretty gnarly and could maybe be replaced with one of the dozen half-baked inside-out behavior ideas I've expressed above.

A dynamic runtime is also very convenient for writing tests, so you can stub out whatever parts of the environment you want.  But if I ship an interpreter, you can just _have_ a dynamic runtime, and run tests against the interpreter rather than a compiled binary.

That leaves...  what?  Live debugging, I suppose?

Imagine if you could statically assert that your runtime monkeypatching preserves the same argspec, though.  Dang.

## That's all I got

Yeah, uh.  This is the longest post I've ever written, 50% bigger by filesize than the PHP monstrosity.  I'll be amazed if anyone reads all this.

But if you did: hey please build this language it would be great to have  :)
