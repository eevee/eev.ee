title: A little bit Rusty
date: 2012-11-17 23:57
category: articles
tags: rust, tech, plt

[Yelp][] had a hackathon a couple weeks ago.  These affairs are mixed blessings for me: a fixed chunk of uninterrupted time to work on a single project is _great_, but I tend to have at least a dozen ideas that I want to do all at once, none of which can be reasonably "finished" in a scant 30 hours, and most of which are obscure enough that nobody can work on them with me.

For example, during this most recent event, I wrote a roguelike.  In [Rust][].

Long-time readers may recall that I've [attempted to write a roguelike before][raidne], in Python, but fell prey to architecture astronomy.  _This_ time would be different!  Because I would only have 30 hours.  Also because static typing limits my options, thus making it easier to overcome choice paralysis.  (It's a working theory.)

But first: a bunch of people have asked what I think of Rust, and now I've actually written something approaching a real program in it, so let's start there.

<!-- more -->


## On Rust

The best way I've found to describe Rust is: C, if it were invented today, by a guy who only knows Haskell.  It's aimed at systems programming and translates to machine code about as intuitively as C, but it's memory-safe, type-safe, and built on closures and pattern matching.  It makes a lot of C tricks first-class, it's binary-compatible with C, and it tries hard to avoid all the pitfalls of C.

I'm trying very hard not to make this a full-blown tutorial (you can read the [actual Rust tutorial][Rust tutorial] if you'd like), but rather a quick overview of why I'm drawn to this language.


### Memory-safety

You cannot dereference a null pointer, free memory twice, or leak memory in Rust.

Rust has two primary pointer types.  "Boxed" pointers look like `@T` and are garbage-collected.  This is baby mode, but it frees you from ever caring about memory management at all.  Unique pointers look like `~T` and, as the name suggests, _cannot be copied_.

There is no explicit allocation or deallocation.  If you want some memory, you directly create a struct or vector or whatever, and that memory will be freed as appropriate for that pointer type.  Boxed pointers go away when no longer referenced; unique pointers go away when they go out of scope.  And there's no pointer arithmetic, so you can't cheat the system.

Rust also has "borrowed" pointers, which look like `&T` and mostly appear in function signatures.  If an argument expects a borrowed pointer, any pointer type can be passed in, and Rust will quietly convert it.  Borrowing is also the easiest way to pass a unique pointer into a function (as that would otherwise perform a copy): the program will only compile if Rust can prove that the original pointer stays untouched until the function returns.

(By the way, I'm lying.  This is a systems language, after all; you can create null pointers, you can leak memory, you can do pointer math until the cows come home.  But you have to actively try, via functions tucked away in the core library, and you have to wrap it all in an `unsafe` block—which has no semantics other than "when my program segfaults, this is why".  Also, there's a fourth pointer type `*T` which indicates a C pointer, and naturally that can be a source of problems, but you generally only see those when wrapping a C library.)


### Type-safety

Rust has very strong typing.  Even built-in numeric types have to be explicitly cast back and forth.  Pointers and structures can only be cast "upwards" to classes, never downwards or sideways.

(Again, I'm lying.  You can cast whatever you want to whatever you want, if you use an `unsafe` function in the stdlib.  But the core syntax doesn't allow it.)


### Inference and generics

Outside of function signatures and struct definitions, you rarely need to give an explicit type to Rust.  It'll usually figure out what you mean.

Unadorned integers are also type-inferred: if you pass a `4` to a function expecting a certain numeric type, Rust will infer that type for the `4`.  This even works for assigning constant numbers to variables without giving an explicit type, though of course your program won't compile if you try to pass that variable to functions expecting different types.

Generics have a syntax I can actually understand.  Also, you don't need to put all your generic code in header files and recompile it every time; as I understand it, a Rust library contains the AST for each generic function it exposes, so compiling a new variant is quick and easy.

Type inference also applies to generics, including their return values.  You very, very rarely have to qualify a generic after defining it.


### Functional features

Rust has closures.  I don't know how they made this work with a systems language; virgin sacrifices may be involved.  The syntax is a bit like Ruby blocks, and in fact there are two built-in structures for passing a closure like a Ruby block.

`do` is syntactic sugar for passing a closure as the last argument to a function:

    :::rust
    do foo(a, b, c) |arg| {
        // ...
    }

`for` is similar, but allows the closure to return `True` or `False` to indicate whether iteration should continue.

So a foreach-style iteration is easy.

    :::rust
    for [1, 2, 3].each |n| {
        io::println(fmt!("%d", n));
    }

Hey, that looks like a method.  So, there are methods.


### Classes

Let me back up here a bit.  When I wrote the PHP article, I picked on the existence of a `private` keyword; I prefer the Perl and Python approach of indicating non-public API with a leading underscore, so that third parties using the code can dig into the internals if absolutely necessary.

But then, there's another problem besides method hiding that `private` clumsily tries to solve.  In most OO systems, method and attribute names are separated horizontally—that is, class A and class B can both have a method `foo` with no risk of collision.  But there's no vertical separation: if a class C inherits from both A and B, and their `foo` methods aren't intended to do the same thing, C will have a sticky mess on its hands.

Interfaces make this problem far worse, because _any_ interface may expect to be applied to _any_ class, and so the methods it requires can be considered as reserved, globally, throughout the _entire language_, forever.  Core Python sneaks around this problem by only defining "interfaces" in the form `__foo__`, and declaring that all such names are reserved for future use.  Third-party code is not so lucky.

Ironically enough, interfaces are dragging OO back to the bad old days of C, where every name is global and you have to use some kind of name munging to avoid possibly conflicting with whatever other libraries a program might link against.  Curses defines a function called `erase`?  No library, anywhere, ever again, can ever use that name now.  `Serializable` requires a method called `readObject`?  Same thing: no library, anywhere, ever again, can ever use that method name.

It struck me that what we really need instead of `private` (which, of course, doesn't help the interface problem at all) is _scoping for method names_.  Python modules, for example, are all distinct namespaces, but they can be assigned to any name (because they are first-class) and items from one namespace can be imported into another easily.  Why can't we have this kind of behavior for methods?  Instead of `__get__`, let me define a method on my class called `core:get`.  Then I can also have my own `get`, and maybe some third-party framework will have a `sprocket:get`, and so forth.  And the namespace names, just like class and module names, are themselves just incidental rather than shared globally.

I didn't follow this train of thought far enough to figure out how calling works and when it's okay to omit the namespace, but it sounded reasonable enough so far.

Anyway, it turns out that (a) Haskell already had a way better version of this same idea and called it a [type class][], and (b) Rust already had them implemented by the time I explained all this to a Rust dev I know.

So that's cool.  Here's how "classes" work in Rust.

Objects, fundamentally, are nothing more than _state_ and _behavior_.  (I don't care what your CS prof says.  Information hiding and inheritance and whatever else are not fundamental features of OO.)

In Rust, the state and behavior are separate.  Here's some state:

    :::rust
    struct Car {
        num_wheels: uint,
        gas: float,
    }

Creating a car object is easy:

    :::rust
    let car = Car { num_wheels: 4, gas: 9.0 };

(This creates the entire struct on the stack.  You could also say `@Car...` for a boxed pointer, and so on.  Method and attribute access works the same way on structs and pointers to structs.)

To give it some behavior, you can create a _trait_, which is like an "interface" if you must, except the method names are _scoped to the trait_.  The actual implementation is separate from both the struct and trait definitions.

    :::rust
    trait Vehicle {
        fn drive();
    }

    impl Car: Vehicle {
        fn drive(self) {
            if self.gas == 0.0 {
                io::println("out of gas!");
            }
            else {
                io::println("vroom vroom");
            }
        }
    }

Now you can call `car.drive()`.  If there are two traits in scope that both define a `drive` method, this will fail to compile, and you'll have to explicitly state which one you meant.  (There is, ahem, not yet syntax for actually doing this, but the idea is sound and all.)

For functionality unique to the class, you can create an anonymous trait, which is really just an implicit trait with the same name as the class.

    :::rust
    impl Car {
        fn retract_sunroof() {
            // I can't think of many operations that only apply to cars
        }
    }

Any type can be given an implementation for any trait.  (ANY type.  Structs, enums, scalar builtins, whatever.)  So I can write a serializer, define a trait for types that can be serialized, and write implementations for the builtin types and my own classes and classes from whatever other libraries I want.  No need to befriend anyone, monkeypatch anything, overload functions, or mess with your namespace.

This isn't to say that Rust has no notion of visibility; in fact, everything in a module is private by default unless explicitly marked `pub`.  (Struct _fields_ are public, though.)  But classes aren't particularly special in this regard, and in fact any code in the same module as an `impl` can call any of its methods, private or not.


### Enums

There are C-style enums, which result in a bunch of constants with increasing integer values.  But that's boring.

The other kind of enum is like a tagged union.  Here's an enum from the standard library:

    :::rust
    enum Option<T> {
        None,
        Some(T),
    }

This means: you can have a variable of type `Option<T>` and you know that it is _either_ tagged as `None` with no data associated with it, or tagged as `Some` with a variable of type `T` associated with it.  It's like Haskell's `Maybe`, except nobody is saying "monad" here.

So this is how Rust handles optional values.  To get at that stored data, you need to do a match:

    :::rust
    let maybedata = Some(123);
    match maybedata {
        Some(data)  => io::print(fmt!("found %d\n", data)),
        None        => io::print("found nothing!\n"),
    }

A particularly neat part here is that a `match` block requires, at compile time, that the match be _exhaustive_.  If I'd left off the `None` branch here, the block would be invalid.


### C pitfalls Rust avoids

Everything is immutable by default.  If you want to be able to change a value, you have to ask for it.

Vector indexing is always bounds-checked.

There are no header files.  A compiled library knows, in Rust terms, what it exposes.

Macros (which exist, btw) operate on the AST rather than being dumb text replacements.

Everything is namespaced, Python-style.  You can import a module and qualify everything in it, import a handful of particular items from a module, and rename anything you import to avoid name clashes.



## On clio

Back to that program I wrote.  [clio][] is the name of my Rust roguelike attempt; "Raidne" was the [Siren associated with improvement][Raidne the Siren] (who knew that Sirens had themes!), and "Clio" was the Muse associated with history and symbolized by scrolls.  That seemed appropriate for a game I expect to be heavily inspired by NetHack.

This was a particularly terrible endeavor not just because I was using an obscure language, but because it has no curses bindings.  So step 1 was to invent the universe.  I'd been dabbling with that on and off leading up to the hackathon.  I called the library [amulet][], because it's a Rust-y thing meant to save you from curses.  Ha HA!


### Things I learned about curses

It is terrible.  So, so terrible.

It defines like a hundred functions.  Half of them are shortcuts that don't take an invocant and operate on a global window object.  Half of them are shortcuts that move the cursor before operating.  These halves overlap, so a quarter of them are both.  Also, a vast number of these are actually macros.

I wanted to use Unicode characters, and this required using a special build of the library which defines even more variants of every function.  On the plus side, this meant that characters were passed around as structures rather than as ASCII codepoints binary-ORed with flags for appearance (e.g. bold, underlined, etc.).

Okay, well, none of this is really world-ending yet.  I wrapped bits and pieces of the library, used some example programs as inspiration, tried to mold it into something that felt native to Rust.

Then I tried to use colors.

You see, curses doesn't let you use colors directly; you must define "color pairs" and attach them to arbitrary numbers up to a limit that may vary by build or system.  Then you style a character by, again, binary-ORing a shifted pair number with the appropriate character.  Also, it's impossible to set only the foreground or background, since everything works via _pairs_, and so there are some hacks to make this work by defining color `-1` as the "default".

My impression is that this is genuinely how color settings on terminals used to work; there are, in fact, termcap entries for defining color pairs and switching to a given pair.  (There are also termcap entries for _redefining colors_, to any arbitrary RGB tuple, and they _work_!  I've yet to see a program do this, though—possibly because it's terminal-wide and would screw up a multiplexer.  Still, there's no reason a multiplexer couldn't intervene and compensate...)

After some dicking around with this, I also discovered that Arch's ncurses library is not built with 256-color support.  Fantastic.  I don't really understand how this makes any sense at all, since I'm currently typing in a vim inside tmux, and both are using 256-color themes just fine.

I started to notice that I was doing a lot more work translating curses's API into something not designed in 1970 than curses was probably doing by itself, so towards the end I veered in the direction of dropping curses entirely and just working with terminal capabilities directly.  (Given that vim and tmux are doing 256-colors despite no curses support, I assume they did the same.)

This is when I made a shocking discovery that has somehow eluded me all these years: _termcap and terminfo are part of curses_.  The specification, the files, the C interface for reading the files, even the `reset` program: it's all part of ncurses.

But this part of the story ends kind of abruptly, since I was trying to actually build something rather than just write a library.  I got color working well enough, I got Unicode working, and I dropped amulet for the time being.  (But I do intend to use caps in the future, rather than contorting to fit the "high-level" curses API.)


### Things I learned about Rust

I'd actually been excited about Rust because I thought it would let me build componentized entities much more easily, what with the ability to implement any trait on any type.

It didn't occur to me until I'd sat down that this doesn't really fit how component-entity works.  I'd need to be able to implement a trait on a particular _instance_, which doesn't make a lot of sense in a static language.

Well, still.  Off I went, hoping to avoid the pitfalls of round 1.

I don't know how much of this will make sense without some deeper familiarity with the language; again, if you're interested, the [Rust tutorial][] is a good read.

#### Perils of borrowing

I started out the evening before the hackathon, and got as far as a symbol that could walk around an enclosed area.  The first morning of hackathon proper, I kind of got stuck.

See, in Python-y style, I wanted to write a method for maps that would let me iterate over the entire grid with one loop.  Something like this:

    :::rust
    for map.each_cell |x, y, cell| {
        // draw something, probably
    }

Alas, no amount of contortion made this work.  Rust complained, every time, that I was borrowing a pointer to "mutable, aliasable" memory.  The problem was that the implementation looked like this:

    :::rust
    fn each_cell(cb: &fn(x: uint, y: uint, cell: &Cell) -> bool) {
        for self.grid.eachi |x, col| {
            for col.eachi |y, cell| {
                cb(x, y, cell)
            }
        }
    }

Rust objected to borrowing `cell`.  After much head-scratching and talking to [#rust][], I had an explanation.

At the time, I was using unique pointers for the map and grid and cells and basically everything, because it didn't seem like I had any reason to be duplicating pointers.  In the code above, `cell` is an element of a mutable vector, `self.grid`.  The issue, as I understand it, is that the caller also has a reference to `self`, and Rust cannot be absolutely certain that other code won't overwrite `self.grid[x][y]` _inside_ `cb`.  If that happened, the cell (which is a unique pointer!) would be freed, and the variable `cell` would point to free memory.

This is an unfortunate state of affairs, and I've run into it several times now when trying to write convenience iterators for a mutable grid of data.  #rust proposed that the basic `each` methods should pass copies to the callback instead of borrowing, which is unfortunate in its own way.  I don't see a particularly clean way to resolve this problem yet.  (I ended up just using nested loops.)

#### Borrowing constants

Rust supports top-level constants, which get written statically into the library.  It seemed reasonable for me to use constant structures to hold entity definitions, e.g., the floor should display as a dark gray "`·`" and be passable.

This was surprisingly awkward.

1. First, curses.  I'd rigged amulet to pretend color pairs don't exist and instead generate them as necessary for each unique pair of foreground+background it ran across.  This worked fine in simple tests, but when I added colors to my entity prototypes, they didn't work at all.

    Long story short: I was defining the color pairs _before_ initializing curses, and curses clears out all its color pairs on initialization.  Super.

2. You can't define constants as pointers; the values don't have addresses at compile time!  So my plan was to define plain structs, then store a pointer to one of them in each entity.  The only appropriate pointer type was the borrowed pointer, which is the type you get when you use the address-of operator, `&`.  This all appeared to work, until an hour or two later when I wrote some code in a completely unrelated place and got a stack explosion.

    Long story short, again: this didn't quite make sense.  I was borrowing a pointer, then storing it in a struct and returning it to somewhere.  It was a pointer to static memory, but once I'd returned the struct, Rust had no way of knowing that, and the wrong combination of operations made it extremely confused about when that pointer was meant to expire.

    The solution was to use a type of `&static/Prototype` instead of merely `&Prototype`.  The `static/` part defines a _lifetime_, something the compiler usually infers to help enforce that borrowed pointers don't outlive the original data.  `static` is the only builtin lifetime name, and it refers to any static data, i.e. constants.  This convinced Rust that I could safely borrow the original prototypes for as long as I wanted, and all was well.

    The lesson here is that storing `&T` in another structure for any length of time probably doesn't make any sense.  But `&static/T` is always kosher.

#### Minor gripes

While I appreciate having to be explicit about type conversions, it has its downsides as well.  Converting a 32-bit integer to a 16-bit integer clearly carries some risk of overflow, so having the conversion explicitly marked with `as i16` is helpful.  But converting an 8-bit integer to a 16-bit integer is absolutely harmless, and the `as i16` becomes noise that's difficult to discern at a glance from genuine problem areas.  I ran into similar problems trying to define a `Point` struct with only unsigned integers; I couldn't subtract without hellacious constructions like `(x as int - 1) as uint`.

You can't "convert" `~T` to `@T` at runtime or vice versa.  The two are stored in completely different memory pools.

Rust doesn't have very good stdlib support for boxed vectors yet.  Most functions expect and return `~[]`, and most vector methods are defined on `~[]`.  (The stdlib is still clearly a work in progress overall; there's a lot of cruft from Rust's early days as a fairly different language, and a lot of clear omissions when compared to e.g. Ruby, Python, Java.)


### Final product

There are two rooms, connected by a hallway.  You can walk between them, beat up a guy, and pick up a scroll which shows in your inventory but which you cannot use and which does nothing.  Also, you can die.

Here's the general approach I took.  The entry point looks like this:

    :::rust
    world.run(interface);

The game world runs its own main loop, and communicates to the display via an "interface", which is a trait that currently only has one implementation.  (For terminals.  Obviously.)

At the start of each turn, the world loops over every thinking actor on the map and offers it the chance to act.  (It's actually a little more complex, as there's a concept of how long actions take.  It works kinda like NetHack, though I think I had the same idea semi-independently.)  In the case of the player, this calls an interface method that asks for the next action to take, which in the terminal case blocks on keyboard input.  In the case of a monster, some pretty dumb AI generates an action.

An "action" is an object implementing the `Action` trait, which is generally executed immediately by the game world.  (Having the world execute the action rather than the actor makes my life a little easier: if the actor dies partway through, for example, cleaning it up is simpler.  And of course I'd rather _not_ have the game state advance while the UI object has control.)

Alas, I didn't get far enough to actually try building a component system, and in fact the player and AI thinking are crammed into the same function.  But I'm moderately happy with what I have so far.


## So

So.

Rust is neat.  I enjoy using it, minor toe-stubs aside.  The developers are active, clever, responsive, and helpful.  And they pass the ultimate litmus test for a new language, in that they have been _removing_ features more than they've been adding new ones lately.  :)

I also like how the game came out, as simple as it is.  It's a side project among side projects for me, so I don't know how much attention it'll get in the future, but I think I have some neat ideas for a roguelike and I'd like to see it develop into something mature and enjoyable.  Maybe I'll go into it in another post.

If you want to play clio, you'll have to compile amulet, then compile clio using `rustc clio.rc -L /path/to/amulet.git/amulet/`.  But you're really, really not missing a lot.


[#rust]: irc://irc.mozilla.org/rust
[Raidne the Siren]: http://www.mythicalcreatureslist.com/mythical-creature/Raidne
[Rust tutorial]: http://dl.rust-lang.org/doc/0.4/tutorial.html
[Rust]: http://www.rust-lang.org/
[Yelp]: http://www.yelp.com/
[amulet]: https://github.com/eevee/amulet
[clio]: https://github.com/eevee/clio
[raidne]: https://github.com/eevee/raidne
[type class]: http://en.wikipedia.org/wiki/Type_class
