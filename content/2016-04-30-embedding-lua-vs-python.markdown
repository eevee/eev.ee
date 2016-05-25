title: Embedding Lua vs Python
date: 2016-04-30 18:29
category: blog
tags: tech, python, gamedev, patreon

Nova Dasterin asks, [with money](https://www.patreon.com/eevee?ty=h):

> How about usage of Lua for game development? Love2d etc. Also http://lexaloffle.com/pico-8.php which I recently heard about.
> 
> clarification: thoughts on Lua as a 'good choice', also Lua vs Python for that subject (gamedev)

There are a couple ways I can interpret this, so I'll go with: _all of them_.

_(edit: you may be interested in a subsequent post about [the game I actually made for the PICO-8](/blog/2016/05/25/under-construction-our-pico-8-game/)!)_

<!-- more -->

## Writing an entire game in Lua or Python

This is entirely possible!  Eve Online, for example, is allegedly mostly Python.

You can use [pygame](http://www.pygame.org/hifi.html) or [cocos2d](http://python.cocos2d.org/) (built atop [pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home)) or a handful of other things.  They're libraries/frameworks rather than dedicated game development studio apps like Unity, and they leave a lot to be desired at times, but they do exist and are maintained and have little communities around them.

Somewhat more well-known is [Ren'Py](https://www.renpy.org/), a visual novel engine that uses Python mixed with a sort of Pythonesque visual novel macro language.  That's not _quite_ the same, but it's close.

As for Lua, er, I don't know.  Finding this out is pretty hard, since the Internet is flooded with information on engines with Lua _embedded_.  Maybe someone has written OpenGL or SDL bindings for Lua and sprinkled a skeleton of game stuff on top, but if so, I haven't found it.

But this is probably not what you meant anyway, since you mentioned LÖVE, which does embed Lua.


## Embedding Lua or Python

You have a game engine written in a _host_ language, and you want to write a bunch of behavior in a _guest_ language, because you secretly hate your host language but it's fast at doing math.

What you really want to do is embed a particular language _implementation_, of course — embedding Jython is going to be a much different experience from embedding CPython.  The host language is usually C or something related to C, what with C being our lingua franca (a phrase that refers to how Italian is the universal spoken language), so I assume this is about embedding liblua or CPython.

Embedding a language is a tricky problem.  If it's high-level enough to need "embedding" (rather than "linking to"), it probably has some kind of runtime, which you'll also need to embed and babysit.  At the very least, embedding a language means you have to:

- start the guest runtime
- load some guest code
- convert host data to guest data
- call some guest functions
- convert guest data back to host data

In many cases, you'll also want to expose host functions to the guest runtime, so that guest code can call back into your engine.  You might also want to expose entire new types to the guest language, e.g. a fast vector type.  That's a lot of things to worry about, and the difficulty is entirely dependent on how cooperative the guest is.

I admit I've never had the need to embed a language in C myself, so don't take any of this as gospel truth.  I've been around people who _have_, though, and hopefully I've osmotically absorbed some of their knowledge.

### Embedding Lua

I know much less about embedding Lua, but it also seems more straightforward, so it makes a good reference point.

The [Lua book](https://www.lua.org/pil/), which serves as its documentation, has a [chapter](https://www.lua.org/pil/24.html) that begins:

> Lua is an _embedded language_.

That's a pretty good start.  Indeed, Lua is so embeddable that you can just paste the entire Lua source code into your project — which I know because [SLADE has done exactly that](https://github.com/sirjuddington/SLADE/tree/master/src/External/lua).  It's a flat directory of C files totaling 640K, and nothing else is necessary.

As for actually embedding, the book [provides this example](https://www.lua.org/pil/25.html) of using a Lua script for configuration and reading `width` and `height` variables out of it:

```lua
height = 600
width = 800
```

```c
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

void load (char *filename, int *width, int *height) {
    lua_State *L = lua_open();
    luaL_openlibs(L);
    
    if (luaL_loadfile(L, filename) || lua_pcall(L, 0, 0, 0))
        error(L, "cannot run configuration file: %s", lua_tostring(L, -1));
    
    lua_getglobal(L, "width");
    lua_getglobal(L, "height");
    if (!lua_isnumber(L, -2))
        error(L, "`width' should be a number\n");
    if (!lua_isnumber(L, -1))
        error(L, "`height' should be a number\n");
    *width = (int)lua_tonumber(L, -2);
    *height = (int)lua_tonumber(L, -1);
    
    lua_close(L);
}
```

An interesting concept in embedded Lua is the _stack_, a structure that straddles C-land and Lua-land.  Invoking Lua operations from C will leave the results in the stack, where C code can then fetch them.  In the above code, `lua_getglobal` is used to put two global variables in the stack, and `lua_tonumber` retrieves them as C doubles.

Lua's own value types don't seem to be exposed to C at all, and there is no "any Lua value" type.  Instead, there are a handful of primitive types (nil, boolean, number, string, table, function, userdata, thread) and separate C functions for getting or putting a value of the equivalent C type from or onto the stack.

This means that the Lua-land garbage collector knows exactly what types are examinable by C — they're the ones on the stack — and it never has to worry about arbitrary C code holding direct references to Lua values.

----

I haven't actually used LÖVE!  I probably should sometime.  I definitely want to give PICO-8 a spin, now that I'm experimenting with pixel art.

For now, my only real experience with embedded Lua comes from tinkering with modding [Starbound](http://playstarbound.com/), where actor behavior is all defined in Lua and new actors can be dropped in alongside the stock ones.

The API isn't particularly well-documented, and it changes arbitrarily between releases.  Starbound still technically hasn't been released, so this is a _little_ forgivable, but it sure is inconvenient having to reverse-engineer the API surface to get anything done.

Starbound is closed-source, so I don't know how exactly they embed Lua.  From the point of view of a modder, every object has a list of zero or more Lua scripts attached to it, and those scripts are mashed into a single namespace.  The namespace can implement various hooks by defining global functions with specific names.  There are `self` and `storage` tables made available, but there's no use of Lua's OO-ish facilities; they're globals injected into your scripts, corresponding to the entity whose hooks are being executed right now.  The hooks back into the engine are, similarly, exposed via a few global tables of functions.

The result is rather goofy, and not what I imagine "native" Lua would look like.  If you want to, say, store the ID of your entity when it's created:

```lua
function init(virtual)
    if virtual then return end

    self.id = entity.id()
end
```

`self` is a plain global table.  `entity` is, likewise, a plain global table, but containing some API functions you can use that are specific to the entity you happen to be working with right now.

If a regular library API were implemented like this, it would seem ludicrous.  Why should it be any different just because it's part of a game engine?

This might be the hardest part of embedding any language: making it actually feel native to people who only see the guest side.  If you're going to embed a language, try writing a dummy plugin/script/whatever — _before_ you design the API — the same way you would expect to write it if the entire engine were written in the guest language.  Then embed the guest in such a way that it actually works.

To Lua's credit, it doesn't look like this ought to be particularly difficult; there's a [whole chapter on exposing custom C types to Lua](https://www.lua.org/pil/28.html), and the [salient bits](https://www.lua.org/pil/28.1.html) are pretty straightforward.

Hm.  I just don't have that much to say about embedding Lua; its own documentation lays out pretty much everything you might want to know.  It's designed for this very purpose, and it shows.


### Python

Python is a pretty nice and featureful language, and it _is_ embeddable, yet embedding it seems relatively uncommon.

I've asked around about this before, but it was many months ago and I don't remember who it was or what they said, which is super helpful.  I'll do my best!

I've used the CPython C API before (to embed C in Python), and it contrasts very sharply with the Lua API.  Where Lua's API is clearly designed for embedding, CPython's API is clearly designed for _writing CPython_.  The exposed constructs are the ones used for implementing the standard library and the C parts of third-party libraries; if you want to embed CPython, you're using the same wide array of fairly fiddly tools.

Python's [embedding documentation](https://docs.python.org/3/extending/embedding.html) doesn't have an exact analogue for the Lua config example, but I've crafted one myself:

```c
#include <Python.h>

int load(char* modname, int* width, int* height) {
    Py_Initialize();
    PyObject* py_modname = PyUnicode_DecodeFSDefault(modname);
    if (! py_modname) {
        if (PyErr_Occurred())
            PyErr_Print();
        fprintf(stderr, "Couldn't decode module name \"%s\"\n", modname);
        return 1;
    }

    PyObject* py_module = PyImport_Import(py_modname);
    // This function wraps the commonly-used Py_DECREF macro, ensuring that you
    // get the right behavior even if running on a Python that was configured
    // differently, or something?  I dunno I read that somewhere
    Py_DecRef(py_modname);

    if (! py_module) {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", modname);
        return 1;
    }

    // TODO PyLong_AsLong can actually raise a (Python-land) exception, if the
    // number is too big to fit in a C long...  and of course a long might be
    // bigger than an int!
    PyObject* py_width = PyObject_GetAttrString(py_module, "width");
    *width = (int) PyLong_AsLong(py_width);
    Py_DecRef(py_width);
    PyObject* py_height = PyObject_GetAttrString(py_module, "height");
    *height = (int) PyLong_AsLong(py_height);
    Py_DecRef(py_height);

    Py_DecRef(py_module);

    Py_Finalize();

    return 0;
}
```

This is definitely, ah, wordier.  (In fairness, I suspect the `error()` function in the Lua example is assumed to be supplied by you.)  Most notably, you have to call `Py_DecRef` all over the place, and you have to understand what's going on well enough to do it at the right times, or you'll get a memory leak that'll suck to track down.  And this was just for reading two globals; calling a function is [a bit worse](https://docs.python.org/3/extending/embedding.html#pure-embedding).

On the other hand...  from what I know of the CPython API, I can't think of any reason why you couldn't _emulate_ something like the Lua stack.  Define the stack as a structure that only exists in C; wrap the useful parts of the API in versions that interact with the stack instead; write some accessors for the stack that only expose C types instead of `PyObject*`s everywhere.  Then the stack access functions could worry about refcounting, and C code would never have to think about it.

The result would be a bit more complex than Lua's API, perhaps; Python has [a lot of built-in types](https://docs.python.org/3.6/c-api/concrete.html) and [a lot of "shapes" of types](https://docs.python.org/3.6/c-api/abstract.html) and overall just a really big API surface.  Still, if you're going to embed Python, I would definitely recommend wrapping up all the C API stuff in a simpler layer like this.  I'm actually kind of surprised such a wrapper API doesn't already exist.

That aside, there's a much bigger problem with the above code, which is that it doesn't actually work.  I compiled it in a directory alongside this `config.py` file, then ran `./a.out config`.

```python
height = 600
width = 800
```

Result: `ImportError: No module named 'config'`.

Ah.  `sys.path` is wrong.  Regular ol' Python will automatically add the current directory to `sys.path` if you do something like `python -m config`, but it seems the C API will not.  And I...  can't figure out how to fix it.  I can set the path manually to `.`, but then Python can't find any of its own built-in modules any more, and nothing works at all — even decoding a bytestring requires the standard library.  I could manually add `.` to the path after starting the interpreter, but surely that's not the right way to fix this, right?  A workaround is to run it as `PYTHONPATH=. ./a.out config`, but boy howdy is that ugly.

The problem isn't so much this particular gotcha, but the wider issue that Python is designed as if it controlled the entire process.  Its state is mostly global variables; it reads environment variables; it assumes it can look for modules as real files in standard locations.  (Lua's standard library is baked into its C, for better or worse.)

If you want to embed Python, you'll need to think about how to map features like module importing — which has a bunch of implicit behavior perfectly suited for a standalone interpreter — to something more appropriate for your application.  Where _is_ Python's standard library?  Python can import from a zip file, and my compiled program's `sys.path` even begins with `/usr/lib/python35.zip` (which doesn't exist?), so this isn't a terribly difficult problem to solve, but it's something you have to think about from the get-go that you can pretty much ignore with Lua.

Also, do you _want_ the entire standard library?  I wouldn't recommend eliminating all of it (though that [does seem to be possible](http://stackoverflow.com/q/20951624/17875)), as it's a large part of the appeal of Python, but does embedded code need to be able to [fork](https://docs.python.org/3/library/os.html) or [start threads](https://docs.python.org/3/library/threading.html) or [spawn a GUI](https://docs.python.org/3/library/tkinter.html)?  Probably not, but now you have the tricky problem of sifting through some 200 modules to figure out what's necessary and what's not.  If you don't want embedded code to be able to read or write arbitrary files, you also need to strip out some _builtins_.  Good luck.

Again, there's nothing really stopping anyone from doing all this work for you and making it available as a wrapper.  But no one has.  Maybe I'm wrong, and the comments are full of links to projects that do exactly this!  I sure hope so.  If not, and you decide to build such a thing for your own project, please share it with the world.

Other potential roadbumps that come to mind:

- You probably don't want to start and stop the interpreter all the time, since Python has a lot of default state that it would have to create and destroy repeatedly.
- Having multiple interpreters is possible, using ["sub-interpreters"](https://docs.python.org/3/c-api/init.html#sub-interpreter-support), but care is required — nothing prevents passing a `PyObject*` from one interpreter into another, for example.
- I've heard that it's difficult to use Python modules written in C from embedded Python, though I don't know the details.
- Python supports (OS) threads, so there are things to be aware of if you call into Python from different threads.  I don't know what those things are, exactly.


### Other ways to embed Python

CPython's API is not the only option.  Perhaps one of these will be more helpful.

**Boost.Python** is a common suggestion, but it's mostly intended for [embedding C++ in CPython](http://www.boost.org/doc/libs/1_60_0/libs/python/doc/html/tutorial/index.html).  It does have some support for [embedding](http://www.boost.org/doc/libs/1_60_0/libs/python/doc/html/tutorial/tutorial/embedding.html), but the second paragraph mentions "you'll need to use the Python/C API to fill in the gaps", which is not a particularly good sign.  Still, this example code is much more encouraging than the equivalent using the C API:

```cpp
object main_module = import("__main__");
object main_namespace = main_module.attr("__dict__");
object ignored = exec("result = 5 ** 2", main_namespace);
int five_squared = extract<int>(main_namespace["result"]);
```

In fact, I can rewrite my C example as something like this, which I have not bothered to test:

```cpp
#include <boost/python.hpp>

void load(string modname, int* width, int* height) {
    using namespace boost::python;

    object py_module = import(modname);

    *width = extract<int>(py_module.attr("width"));
    *height = extract<int>(py_module.attr("height"));
}
```

Certainly much better.  No reference counting in sight; the `object` wrapper type takes care of it.  Python exceptions are (partially) mapped to C++ exceptions, so the caller can worry about them.  You're not saved from the runtime concerns like where the stdlib lives, but your actual glue code is much less terrible.

----

[**Cython**](http://cython.org/) is another project originally intended for writing extension modules — it uses a modified Python syntax that compiles to C code using the Python API, and can operate on both Python and C objects interchangeably.

The good news is, [it's possible to embed the entire CPython interpreter with Cython](https://github.com/cython/cython/wiki/EmbeddingCython)!  The bad news is, the documentation appears to consist solely of a one-page wiki article, a few mailing list threads, and a demo.

I do see a glimmer of real potential here.  The part you compile is more or less _just Python_, which means you can write all your loading code _in Python_.  That reduces the amount of C or C++ glue junk you have to write to _nothing_, an infinity-percent improvement.

Unfortunately, Cython produces a binary that just directly executes the compiled module.  From what's provided, I don't see how you're supposed to produce a C API you can call at will from other C code.  So close!  If only some project had done the same thing but actually finished and documented it.

----

[**CFFI**](http://cffi.readthedocs.io/en/latest/index.html) did!

CFFI is a pretty slick library, not for writing extension modules, but for calling C library functions _from Python_.  It's kinda like [`ctypes`](https://docs.python.org/3/library/ctypes.html), but with a less atrocious API and the ability to learn the C library's API from its header files.

I found out _yesterday_ that it now also supports [embedding Python](http://cffi.readthedocs.io/en/latest/embedding.html).  It's the same general idea as with Cython: you write some Python and it gets built into a shared library.  But here, you can declare Python wrappers for C functions _and_ C wrappers for Python functions, giving you an explicit list of interfaces between the environments.  Particularly nice about this is that CFFI is already designed for wrapping C libraries, so you have a good shot at creating a Python API that actually feels Python-native.

As an added bonus, CFFI is built into [PyPy](http://pypy.org/), the JITted Python implementation, so you can use that instead of CPython if you like.

Alas, this _still_ doesn't save you from dealing with paring down and locating the stdlib.  Someone should really figure that out once and for all, then tell the rest of us.


### Conclusions

Lua is certainly the simpler option.  You don't even have to link to Lua; you can just drop the whole damn thing into your codebase and forget about it.  The API is already fairly simple to use, which leaves you lots of spare dev time for making your API not be a few bags of injected globals.

On the other hand, if you really like Python, you might be willing to deal with its few extra headaches to get it embedded.  It's not as common as Lua, but it certainly can be done.  The best option at the moment looks to be CFFI, which has some pretty clever people behind it who might be able to give you some pointers.

What a letdown.  I really wanted to root for Python here.  If only...  if only there were some other way...


## A third option: embedding _in_ Python

If you ask the `#python` IRC channel about embedding Python in an application, you will almost always get the same response: don't.

_Instead_, they'll tell you, you should _embed your application in Python_.

Now, this isn't always practical.  If your application is intended to support plugins in multiple different languages, this is perhaps not the best approach.  But _if_ you only ever intend to support Python, and _if_ you wish you could be writing Python anyway, this is entirely doable.

Remember that the biggest issue with embedding Python is that it's designed assuming it controls the entire process.  It has global state and tendrils into the system all over the place.  In contrast, your application is probably _less_ invasive, and you have complete control over it besides.  So why not hand the wheel to Python?

Build your application like a library, then call its entry point from Python using one of the C embedding gizmos, like [CFFI](http://cffi.readthedocs.io/en/latest/index.html).  You can pass Python callbacks into your C code with [`def_extern`](http://cffi.readthedocs.io/en/latest/using.html#extern-python-reference), or do the bulk of application work in Python and keep the heavy lifting in C, or whatever.

Then you can bundle and deploy the whole thing with any of the existing Python-to-executable tools: [cx\_Freeze](http://cx-freeze.sourceforge.net/), [py2exe](http://www.py2exe.org/), [py2app](https://pythonhosted.org/py2app/), [PyInstaller](http://www.pyinstaller.org/), etc.  (This isn't a thing I have to do, so I don't know which is the latest and greatest.)  Or, hell, compile all your Python in Cython's embedded mode.

This is a pretty radical departure from what people tend to mean when they say "embedding", but it has the major benefit that there's just far more C-in-Python tooling available than Python-in-C.

Alas!  You still have to worry about paring down the standard library and builtins yourself, and that's [really tricky from pure Python](http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html).  If you want arbitrary mods to be relatively safe for players to use, and you are not an **expert** on Python internals (I'm not!), you might have to stick with Lua.


## A fourth option

[Godot](http://godotengine.org/) took the rather radical approach of creating their _own_ vaguely Pythonesque language, [GDScript](http://docs.godotengine.org/en/latest/reference/gdscript.html).

Obviously this is a hell of a lot of work, especially if you've never designed a language before.  On the other hand, the control over the embedding API and native types was apparently [reason enough](https://github.com/godotengine/godot/wiki/devel_faq/aab29ff13aacc9f7be809a96de174481b65721c0#2-i-dont-believe-you-what-are-the-technical-reasons-for-the-item-above) for the Godot developers.  As I've previously mentioned, [most programming languages are bad at expressing simulation](/blog/2016/04/21/elegance/#inform-7), so a new language can be a chance to design some more appropriate syntax and types.  (I can't speak to whether GDScript has pulled this off.)

It's not unheard of, either. [RPG Maker](http://www.rpgmakerweb.com/) had its own language before switching to Ruby a few years ago.  The original Quake had [QuakeC](https://en.wikipedia.org/wiki/QuakeC), though that was dropped in favor of native libraries in later engines.  [Unreal](http://unrealengine.com/) had its own language before...  uh...  ditching it two years ago.  Hmm, maybe there's a pattern here.

One thing GDScript does have going for it is that it _kinda_ solves the problem of getting scripts to feel "native", since the language itself is just designed to be native.  In particular, scripts are associated with nodes, and everything in a script file is implicitly part of that node's _type_ (or class, if you must) in a way that plays pretty well with Godot's concept of [instancing](http://docs.godotengine.org/en/latest/tutorials/step_by_step/instancing.html).

I definitely wouldn't advise designing your own language without a _really_ good reason, especially not for just a single game.  Language design is _hard_ — most languages are still evolving to fill their gaps decades after they were first conceived.

But hey, if you do go down this road, for the love of god, please don't base your language on Java or C.  That gets you the worst of both worlds: all the introspection of a static compiled language with all the tooling of a dynamic language.


## Appendix: the languages themselves

I don't want to get into a huge language fight here.  Lua is pretty good for what it is, which is an embedded dynamic language in 640KB of ultraportable C and nothing else.  It has some goofy decisions, like using `~=` for inequality and indexing arrays from 1, but whatever.  It also has coroutines and metatypes, which is impressive.  I only have a couple real beefs with Lua, and they're mostly grievances I have with JavaScript as well:

- There's only one numeric type (`number`, double-precision floating point) and only one data structure (`table`).  Ehh.  You _can_ return multiple values from a function or iterator, but there's no real tuple type, and misusing a faux tuple will silently discard the unconsumed values.

- Reading a nonexistent variable is not an error; it produces `nil`.  Likewise (actually for the same reason), reading a nonexistent table entry silently produces `nil`.  Writing to a variable that's not declared `local` will silently create a new global.

- If a function receives too many arguments, the extras are silently ignored.  If too few, the missing ones default to `nil`.

- There's nothing like Python's `repr` built in, let alone `pprint`.  A table prints as `table: 0xa6c300`, without even delimiters around it.  This is _terrible_ — half the appeal of a dynamic runtime is the ability to inspect the state of your program from within itself, but the only data structure the language even has is opaque.

- `break` and `return` have to be the last statement in a block.  There's a trivial workaround (wrap it in a dummy `do ... end`) but it's still kind of annoying.  Also there's no `continue`.

- You need the built-in `debug` library to do a lot of useful things, like print Lua tracebacks, but the Lua book advises disabling it in production builds because it allows Lua code to do naughty things.  Indeed, Starbound doesn't have `debug`.  Trouble is, a production build of Starbound is the development environment for a mod.

These issues are compounded when Lua is embedded in a larger engine with a poorly-documented API, ahem.  Mistakes like `nil`s and typoed variable names can persist for several lines or several _functions_ before causing any obvious errors, at which point you have to reload the entity (or as is often the case with Starbound, reload _all the game assets_) for every attempted diagnosis or fix.

Contrast with Python, which is perfect in every way.

Well, er.  The biggest drawback with Python is the one I've already mentioned: it's a general-purpose language which exposes a lot of general-purpose system functionality.  If you don't want your scripts to be able to [_start a web server_](https://docs.python.org/3/library/http.server.html), you'll have to trim the language down into something more appropriate.  (On the other hand, it looks like people are [making use of sockets in Blender](http://stackoverflow.com/q/14802608/17875)...)  And what of the other things Python developers take for granted, like imports or the [`logging` module](https://docs.python.org/3/library/logging.html)?  Do you support third-party modules?  How?  Do you respect Python's environment variables?  Where does `print` go?  What do you do with all the goodies in the [`sys` module](https://docs.python.org/3/library/sys.html) — some useful, some nefarious, some a bit of both?  How do you insulate scripts from each other; an entire sub-interpreter for each one?  Did you know that CPython lets you construct, modify, and execute arbitrary bytecode?  Do you need to protect against that?  Or against using [`ctypes`](https://docs.python.org/3/library/ctypes.html) to call the CPython C API from Python code?

One other thought: Python has [syntactic async support as of 3.5](https://docs.python.org/3.5/whatsnew/3.5.html#pep-492-coroutines-with-async-and-await-syntax), which sounds like something that might be pretty useful in a game engine, but I have _no idea_ how you would actually embed code that uses it.  I'd sure be interested to hear if you got it to work, though.
