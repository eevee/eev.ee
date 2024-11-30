title: Cython versus CFFI
date: 2013-09-13 20:01
category: articles
tags: python, sanpera, tech

_(This article has been translated into [Russian](http://www.everycloudtech.com/cython-gainst-cffi) by <a href="http://www.everycloudtech.com/" rel="nofollow">Everycloudtech</a>—thanks!)_

I have a hilariously unfinished Python module I work on from time to time named [sanpera](https://github.com/eevee/sanpera).  It's an imaging library for Python, with the vain hope that it might replace PIL someday.  But this isn't about sanpera.

sanpera happens to be powered by [ImageMagick][].  I distinguish this from being an "ImageMagick wrapper", as it explicitly has nothing resembling the ImageMagick API, because said API is insane.  But this isn't about ImageMagick, either.

Using ImageMagick requires binding Python to C, and that's what this is about.  There are several ways to use C libraries from Python:

* **Writing an extension module** means the Python API is defined in C, so the library is used exactly as it was intended: with C code.  Unfortunately this requires writing _a lot_ of C, as well as _a lot_ of careful Python refcounting.  My C is passable, but I've done far more reading it than writing it, so this is not an appealing option.

* **ctypes** is a standard-library module that can load shared libraries and call functions from them without the use of a C compiler or any new C code.  Convenient, especially if you hate dependencies (in which case why are you binding to C?), but all the ctypes-powered code I've read has been tedious and fiddly and ugly.

* **Cython**, a spiritual port/evolution/fork/something of the older Pyrex, is a language similar to Python that translates to C and then compiles into an extension module.  Cython code can define Python classes and functions, but also call C functions and perform other C operations directly.  Code with C semantics is translated fairly directly to C; code with Python semantics is translated to appropriate use of the CPython API; and Cython fills in all the bits to translate between the two.

I went with Cython because it looked interesting, it seemed to reduce the number of translation layers I'd have to care about, and it would even let me write hot loops (this _is_ an imaging library) in C without actually writing any C.  Plus, since it's not actually Python code, it can compile to _both_ Python 2 and Python 3 extension modules with very little effort on my part.

Here's what Cython looks like:

<!-- more -->

```cython
@classmethod
def read(type cls, bytes filename not None):
    cdef libc.stdio.FILE* fh = libc.stdio.fopen(<char*>filename, "rb")
    if fh == NULL:
        cpython.exc.PyErr_SetFromErrnoWithFilename(IOError, filename)

    cdef c_api.ImageInfo* image_info = c_api.CloneImageInfo(NULL)
    cdef MagickException exc = MagickException()
    cdef int ret

    cdef Image self = cls()

    try:
        # Force reading from this file descriptor
        image_info.file = fh

        self._stack = c_api.ReadImage(image_info, exc.ptr)
        exc.check()

        # Blank out the filename so IM doesn't try to write to it later
        self._stack.filename[0] = <char>0
    finally:
        c_api.DestroyImageInfo(image_info)

        ret = libc.stdio.fclose(fh)
        if ret != 0:
            cpython.exc.PyErr_SetFromErrnoWithFilename(IOError, filename)

    self._post_init()
    return self
```

(Wow, it's even syntax-highlighted.  Impressive.)

Clearly Python-inspired, with C bits sprinkled around.  `cdef` for a statically-typed variable declaration, static types on function arguments, comparisons to `NULL`, brief dipping into the Python C API when useful.  Certainly easier than writing plain C, especially when dealing with ImageMagick's...  idiosyncracies.  But I can't easily use some features like `with`, and so my code is sprinkled with pointer-freeing `finally`s and manual conversion of ImageMagick exceptions into Python ones.

This was all well and good, and I tinkered with the library every so often, wrestling the underlying API more than getting many features implemented.

Then [PyPy][] started to gain in popularity.  PyPy didn't originally _have_ a C API, being not written in C and all.  More recent releases have a C API emulation layer, and Cython even has support for targeting it, but it's [full of caveats](http://docs.cython.org/src/userguide/pypy.html) that do not fill me with confidence.  I do like PyPy, and not supporting it would be a shame, but navigating the quirks of two different memory models is exactly the kind of thing I was trying to _avoid_ by using Cython in the first place.

Lucky for me, several PyPy fans _strongly advised_ that I port to CFFI.  This is yet another way to bind to C libraries, with an interface borrowed from Lua, which sure sounds impressive to me.  It's based on the same underlying library (libffi) as ctypes, but is more amenable to PyPy for reasons beyond my comprehension, and gets its C interface definitions by parsing C header files so I don't have to translate them all to pretty clunky Python.

That sounded like a _whole lot of work_, but I didn't want to write more Cython code that I might be porting later, so I avoided working on sanpera at all for a while.  Until I finally sat down and gave CFFI a whirl over the past few days.

```python
@classmethod
def read(cls, filename):
    with open(filename, "rb") as fh:
        image_info = blank_image_info()
        image_info.file = ffi.cast("FILE *", fh)

        with magick_try() as exc:
            ptr = ffi.gc(
                lib.ReadImage(image_info, exc.ptr),
                lib.DestroyImageList)
            exc.check(ptr == ffi.NULL)

    return cls(ptr)
```

Which brings me to what this post is _actually_ about: my experience porting a modest amount of Cython to CFFI.


## Porting effort

You can eyeball-diff the Cython and CFFI implementations above to get an idea of what was involved.  For the most part this was a matter of tediously and mechanically removing `cdef` and type annotations, copying the C function definitions from the original headers into a file for CFFI to parse, and replacing the reference to `c_api` with the new `lib` object CFFI spits out.

I actually did this one module at a time, with moderate success; my Cython code _mostly_ interacted by going through Python interfaces, which continued to work fine after those Python interfaces were ported to CFFI.  And of course it's all using the same library in the same process, so the library doesn't know or care about my hybrid monstrosity sitting above it.

There were a few places that took more effort, and this is where CFFI started to shine.  Notice that the `try`/`finally` is completely gone in the above code; it's been replaced by `ffi.gc`, which adds a little Python-land wrapper to a C pointer and gives it a destructor.  When the wrapper is destroyed, the pointer is freed.  Of course, in the non-refcounted land of PyPy that I'm actually trying to port to, it's completely arbitrary when this actually happens—but most of my pointers are stored inside Python objects anyway so they'll likely go away at the same time.

Writing Python code meant `with` actually works, too, and I ported my crappy exception wrapper into a tiny `contextmanager`.  ImageMagick handles errors by passing pointers to `ExceptionInfo` structs around, and writing into them when something goes wrong; the object returned from `magick_try` is just a thin container for such a pointer.  When the `with` block ends, if the struct contains an error, it's converted to a Python error and raised.  Between `with` and `ffi.gc`, a lot of the memory-managing cruft went away, and I'm left with something that actually looks like Python code.

The CFFI version also passes a pointer directly to the constructor, rather than building an object manually (or using an awkwardly-named factory function, as I did elsewhere).  This was a restriction of Cython: no function exposed to Python can accept C-specific types as arguments, and `__init__` is necessarily exposed to Python.  Anytime I needed an object initially populated with C fields, I had to create it empty with `Class.__new__(Class)` and then assign attributes manually.  But in CFFI, pointers are just Python objects like anything else, so I can pass them around freely.  This simplified my life a great deal, especially with common post-setup code like the `self._post_init()` above, which was easy to forget to call.

## Dealing with typedefs

ImageMagick uses `typedef` for most of its numeric types, and the actual concrete type depends on how ImageMagick was configured.  CFFI can't deal with this, because it needs to know the sizes of types to interact with C calling conventions.  Pointers to structs of unknown size are fine, because they're ultimately _pointers_ and those are always a known size, but if I don't know whether I have a `float` or a `double` then I have a bit of a problem.

The main offender is `Quantum`, which holds the value of a single channel in a pixel; depending on the build it might be an `unsigned char`, `unsigned long`, or `long long double` that ranges from 0 to 1 (?!).  Luckily `Quantum` only really exists as a field in a pixel structure, so there was room for a hack: I wrote tiny wrappers in C that converted a pixel to an array of 0–1 `double`s and back, and left the pixel struct as an opaque type.  CFFI was more than happy to compile them for me and expose them to Python code the same way as the rest of the library.

## Pointer arithmetic

Pointers in CFFI can be dereferenced by indexing, much like C (and ctypes): `ptr[0]` is the spiritual equivalent of `*ptr`.

But part of ImageMagick's API requires pointer _incrementing_.  In Cython this had to be done by a dedicated function, `inc(ptr)`, which would be compiled to `ptr++`.  In ctypes, well...  you can always dereference with an increasing index, but an actual increment appears to be...  [cumbersome](http://stackoverflow.com/a/6801160/17875).

I was about to write another C wrapper just to return `ptr + 1` and I thought to try the obvious thing: `ptr += 1`.

Which works.  Huh.  Neat.

## Compilation

Cython generates **a lot** of C.  Like...  **a lot**.  `sanpera.image` is 30K of Cython, and it becomes 607K of C.  That takes a little while to build.  It's only some 9 seconds to build all of sanpera from scratch on my machine, and there are partial builds as you might expect, but it's a bit of a bump in the road when I'm trying to cycle quickly between writing code and running tests.

Oh, and I have to compile manually after every change.  And sometimes the translation fails, and Cython's error messages aren't great at times.  And sometimes the compile fails, and I have to debug generated C code.  And sometimes Python segfaults, and I am very sad about that.

On the other hand, CFFI still has to compile some boilerplate code and the little wrappers I wrote, but it does so automatically when needed, and it only takes about a second.  I've gotten a few C errors, but they've been pretty straightforward and usually are mistakes in my declarations.  Definitely much nicer.

One downside: CFFI claims a _parse_ error when you use a C type that hasn't been declared yet, and lays the blame on the _next_ token with no mention of the name it didn't recognize.  This was not obvious at first.

## Speed

I admit I was dreading finding out that my library was some 10× slower, but this was hard to measure before I'd ported most of it.

* CPython 2.7 + Cython: 2.0s
* CPython 2.7 + CFFI: 2.7s
* PyPy 2.1 + CFFI: 4.3s

That's the time it takes, from a warm start, to run the test suite.  (Which is hilariously broken at the moment, but it's equally broken in all three cases.)

I guess that's not too awful a drop, considering I was running _compiled C code_ before, but I'd still like to work on improving it.  (Only 49 tests actually run, for crying out loud.)  And while PyPy's performance is pretty lousy, it didn't work _at all_ before, so this is a stark improvement.  :)

## Overall

I put this off for way too long, but it ended up being much easier than I expected, and way less ugly than any of the ctypes code I've read.  Using a CFFI-wrapped library is a delight so far, and I expect this will get me much more motivated to work on sanpera in the future—at least if Wand doesn't beat me to the mindshare.


## Epilogue: Loading the library

I'm saving this for last because it's really just griping about ImageMagick and has nothing to do with CFFI.

ImageMagick is fucking insane, let's make that clear.  You probably know that it claims super-generic CLI names like `convert` and `identify`, but that's just the tip of the iceberg.  Large chunks of the core API, including such basic functions as `ReadImage`, are themselves the implementations of parts of the CLI utilities—you actually cannot ask ImageMagick to read an image from a filename without trying to parse out all the `png:foobar.jpg[20x20]` cruft.  Oh and it's written like 1991 C, the function and type names are un-namespaced `CamelCaps`, none of the types are documented, most of the numeric types are actually typedefs that vary depending on how it was compiled, and a lot of the interesting stuff exists only in macros.

But what haunted my very first foray into CFFI was merely finding the library and its headers.  ImageMagick headers don't live in standard locations; they're usually installed in a subdirectory of `/usr/include` (which varies by platform and configuration, of course), and inside _that_ is a `magick/` directory that actually contains the headers.  The library used to be fairly easy to find, but now it has some combination of up to three types of suffix in the name, again depending on how it was compiled.

This is all ostensibly because ImageMagick can be compiled with different bit-depths, and they want to support having multiple different flavors of the library installed side-by-side, but the resulting confusion makes it awkward to use the library at _all_.

The easy way to get all the right paths is `pkg-config`, but I can only take that for granted on Linux and perhaps other not-Mac Unix flavors, so in the interest of being multicultural I set out to find a robust fallback.  (The Cython approach just relied on `pkg-config` and spat out a useless error message if it weren't available; lame!)

First attempt: happy day!  ImageMagick ships with and installs a program called `Magick-config`, which is like `pkg-config` but specific to ImageMagick.  Whew, that was easy.

Then I had a look, and it turns out `Magick-config` is just a one-page shell script that calls `pkg-config`.  Why does this even exist, then?  Who the fuck knows.

Second attempt: ImageMagick also installs some configuration files, which are promised to contain some compile-time information.  Excellent; I'll just find those.  Except ImageMagick looks for them in each of half a dozen places that are different on every platform—and the most likely home contains the ImageMagick _version_, which I don't know until I've found the configuration files.

Okay, okay.  Luckily the `convert` program has a shoddy interface to these configuration files; `convert -list configure` will spit out all the juicy details.  So I tried that, and it worked well.  Sort of.

Turns out this file will _only_ tell me how ImageMagick itself was built, not how to link to it.  It contains an include path which happens to match one on my machine, but somehow I suspect it's not necessarily intended to.  And of course the name of the library itself doesn't appear anywhere.

At this point I gave up and I'll have to revisit it later.  I know I can ignore the headers and just look for the library on OS X, which is certainly _easier_.  The related Wand library, which also seeks to wrap ImageMagick, is currently just [flailing wildly](https://github.com/dahlia/wand/blob/0.3.3/wand/api.py#L40) until it finds a library that actually exists.  (Oh, and they have these very specific [instructions for installing ImageMagick on Windows](http://docs.wand-py.org/en/0.3.5/guide/install.html#install-imagemagick-on-windows) which involve setting a specific environment variable so ImageMagick can even find its own files.)


[ImageMagick]: http://imagemagick.org/
[PyPy]: http://www.pypy.org/
