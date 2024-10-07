title: Let's stop copying C
date: 2016-12-01 03:51
category: blog
tags: tech, plt

Ah, C.  The best _lingua franca_ we have...  because we have no other lingua francas.  Linguae franca.  Surgeons general?

C is fairly old — 44 years, now! — and comes from a time when there were possibly more architectures than programming languages.  It works well for what it is, and what it is is a relatively simple layer of indirection atop assembly.

Alas, the popularity of C has led to a number of programming languages' taking significant cues from its design, and parts of its design are...  slightly questionable.  I've gone through some common features that probably should've stayed in C and my justification for saying so.  The features are listed in rough order from (I hope) least to most controversial.  The idea is that C fans will give up when I call it "weakly typed" and not even get to the part where I rag on braces.  Wait, crap, I gave it away.

<!-- more -->

I've listed some languages that do or don't take the same approach as C.  Plenty of the listed languages have no relation to C, and some even predate it — this is meant as a cross-reference of the landscape (and perhaps a list of prior art), not a genealogy.  The language selections are arbitrary and based on what I could cobble together from documentation, experiments, Wikipedia, and attempts to make sense of [Rosetta Code](https://rosettacode.org/).  I don't know everything about all of them, so I might be missing some interesting quirks.  Things are especially complicated for very old languages like COBOL or Fortran, which by now have numerous different versions and variants and de facto standard extensions.

"Unix shells" means some handwaved combination that probably includes bash and its descendants; for expressions, it means the `(( ... ))` syntax.  I didn't look too closely into, say, fish.  Unqualified "Python" means both 2 and 3; likewise, unqualified "Perl" means both 5 and 6.  Also some of the puns are perhaps a little too obtuse, but the first group listed is always C-like.


## Textual inclusion

`#include` is not a great basis for a module system.  It's not even a module system.  You can't ever quite tell what symbols came from which files, or indeed whether particular files are necessary at all.  And in languages with C-like header files, most headers include other headers include more headers, so who knows how any particular declaration is actually ending up in your code?  Oh, and there's the whole include guards thing.

It's a little tricky to pick on individual languages here, because ultimately even the greatest module system in the world boils down to "execute this other file, and maybe do some other stuff".  I think the true differentiating feature is whether including/importing/whatevering a file _creates a new namespace_.  If a file gets dumped into the caller's namespace, that looks an awful lot like textual inclusion; if a file gets its own namespace, that's a good sign of something more structured happening behind the scenes.

This tends to go hand-in-hand with how much the language relies on a global namespace.  One surprising exception is Lua, which can compartmentalize `require`d files quite well, but dumps everything into a single global namespace by default.

Quick test: if you create a new namespace and import another file within that namespace, do its contents end up in that namespace?

**Included:** ACS, awk, COBOL, Erlang, Forth, Fortran, most older Lisps, Perl 5 (despite that required files must return true), PHP, Unix shells.

**Excluded:** Ada, Clojure, D, Haskell, Julia, Lua (the file's return value is returned from `require`), Nim, Node (similar to Lua), Perl 6, Python, Rust.

**Special mention:** ALGOL appears to have been designed with the assumption that you could include other code by adding its punch cards to your stack.  C#, Java, OCaml, and Swift all have some concept of "all possible code that will be in this program", sort of like C with inferred headers, so imports are largely unnecessary; Java's `import` really just does aliasing.  Inform 7 has no namespacing, but does have a first-class concept of external libraries, but doesn't have a way to split a single project up between multiple files.  Ruby doesn't automatically give `require`d files their own namespace, but doesn't evaluate them in the caller's namespace either.


## Optional block delimiters

Old and busted and responsible for [gotofail](https://nakedsecurity.sophos.com/2014/02/24/anatomy-of-a-goto-fail-apples-ssl-bug-explained-plus-an-unofficial-patch/):

```c
if (condition)
    thing;
```

New hotness, which reduces the amount of punctuation overall and eliminates this easy kind of error:

```rust
if condition {
    thing;
}
```

To be fair, and unlike most of these complaints, the original idea was a sort of clever consistency: the actual syntax was merely `if (expr) stmt`, _and also_, a single statement could always be replaced by a block of statements.  Unfortunately, the cuteness doesn't make up for the ease with which errors sneak in.  If you're stuck with a language like this, I advise you _always_ use braces, possibly excepting the most trivial cases like immediately returning if some argument is `NULL`.  Definitely do not do this nonsense, which I saw in actual code not 24 hours ago.

```c
for (x = ...)
    for (y = ...) {
        ...
    }

    // more code

    for (x = ...)
        for (y = ...)
            buffer[y][x] = ...
```

The only real argument _for_ omitting the braces is that the braces take up a lot of vertical space, but that's mostly a problem if you put each `{` on its own line, and you could just not do that.

Some languages use keywords instead of braces, and in such cases it's vanishingly rare to make the keywords optional.

**Blockheads:** ACS, awk, C#, D, Erlang (kinda?), Java, JavaScript.

**New kids on the block:** Go, Perl 6, Rust, Swift.

**Had their braces removed:** Ada, ALGOL, BASIC, COBOL, CoffeeScript, Forth, Fortran (but still requires parens), Haskell, Lua, Ruby.

**Special mention:** Inform 7 has several ways to delimit blocks, none of them vulnerable to this problem.  Perl 5 requires _both_ the parentheses and the braces...  but it lets you leave off the semicolon on the last statement.  Python just uses indentation to delimit blocks in the first place, so you _can't_ have a block look wrong.  Lisps exist on a higher plane of existence where the very question makes no sense.


## Bitwise operator precedence

For [ease of transition from B](http://softwareengineering.stackexchange.com/a/194647/78705), in C, the bitwise operators `&` `|` `^` have _lower_ [precedence](http://en.cppreference.com/w/c/language/operator_precedence) than the comparison operators `==` and friends.  That means they happen _later_.  For binary math operators, this is _nonsense_.

```c
1 + 2 == 3  // (1 + 2) == 3
1 * 2 == 3  // (1 * 2) == 3
1 | 2 == 3  // 1 | (2 == 3)
```

Many other languages have copied C's entire set of operators _and_ their precedence, including this.  Because a new language is easier to learn if its rules are familiar, you see.  Which is why we still, today, have extremely popular languages maintaining compatibility with a language from 1969 — so old that it probably couldn't get a programming job.

Honestly, if your language is any higher-level than C, I'm not sure bit operators deserve to be operators at all.  Free those characters up to do something else.  Consider having a first-class bitfield type; then 99% of the use of bit operations would go away.

Quick test: `1 & 2 == 2` evaluates to 1 with C precedence, false otherwise.  Or just look at a precedence table: if equality appears _between_ bitwise ops and other math ops, that's C style.

**A bit wrong:** D, expr, JavaScript, Perl 5, PHP.

**Wisened up:** F# (ops are `&&&` `|||` `^^^`), Go, Julia, Lua (bitwise ops are new in 5.3), Perl 6 (ops are `+&` `+|` `+^`), Python, Ruby, Rust, SQL, Swift, Unix shells.

**Special mention:** C# and Java have C's precedence, but forbid using bitwise operators on booleans, so the quick test is a compile-time error.  Lisp-likes have no operator precedence.


## Negative modulo

The modulo operator, `%`, finds the remainder after division.  Thus you might think that this always holds:

```c
0 <= a % b < abs(b)
```

But no — if `a` is negative, C will produce a negative value.  (Well, since C99; before that it was unspecified, which is probably worse.)  This is so `a / b * b + a % b` is always equal to `a`.  Truncating integer division rounds _towards zero_, so the sign of `a % b` always needs to be away from zero.

I've never found this behavior (or the above equivalence) useful.  An easy example is that checking for odd numbers with `x % 2 == 1` will fail for negative numbers, which produce -1.  But the opposite behavior can be pretty handy.

Consider the problem of having `n` items that you want to arrange into rows with `c` columns.  A calendar, say; you want to include enough empty cells to fill out the last row.  `n % c` gives you the number of items on the last row, so `c - n % c` seems like it will give you the number of empty spaces.  But if the last row is _already full_, then `n % c` is zero, and `c - n % c` equals `c`!  You'll have either a double-width row or a spare row of empty cells.  Fixing this requires treating `n % c == 0` as a special case, which is unsatisfying.

Ah, but if we have positive `%`, the answer is simply...  `-n % c`!  Consider this number line for `n` = 5 and `c` = 3:

```text
-6      -3       0       3       6
 | - x x | x x x | x x x | x x - |
```

`a % b` tells you how far to count _down_ to find a multiple of `b`.  For positive `a`, that means "backtracking" over `a` itself and finding a smaller number.  For _negative_ `a`, that means continuing further away from zero.  If you look at negative numbers as the mirror image of positive numbers, then `%` on a positive number tells you how to much to file off to get a multiple, whereas `%` on a negative number tells you how much further to go to get a multiple.  `5 % 3` is 2, but `-5 % 3` is 1.  And of course, `-6 % 3` is still zero, so that's not a special case.

Positive `%` effectively lets you _choose_ whether to round up or down.  It doesn't come up often, but when it's handy, it's _really_ handy.

(I have no strong opinion on what `5 % -3` should be; I don't think I've ever tried to use `%` with a negative divisor.  Python makes it negative; Pascal makes it positive.  Wikipedia has a [whole big chart](https://en.wikipedia.org/wiki/Modulo_operation).)

Quick test: `-5 % 3` is -2 with C semantics, 1 with "positive" semantics.

**Leftovers:** C#, D, expr, Go, Java, JavaScript, OCaml, PowerShell, PHP, Rust, Scala, SQL, Swift, Unix shells, VimL, Visual Basic.  Notably, some of these languages don't even _have_ integer division.

**Paying dividends:** Dart, MUMPS (`#`), Perl, Python, R (`%%`), Ruby, Smalltalk (`\\\\`), Standard ML, Tcl.

**Special mention:** Ada, Haskell, Julia, many Lisps, MATLAB, VHDL, and others have separate `mod` (Python-like) and `rem` (C-like) operators.  CoffeeScript has separate `%` (C-like) and `%%` (Python-like) operators.


## Leading zero for octal

Octal notation like `0777` has three uses.

One: to make a file mask to pass to `chmod()`.

Two: to confuse people when they write `013` and it comes out as 11.

Three: to confuse people when they write `018` and get a syntax error.

If you absolutely must have octal (?!) in your language, it's fine to use `0o777`.  Really.  No one will mind.  Or you can go the whole distance and allow literals written in _any_ base, as several languages do.

**Gets a zero:** awk (gawk only), Clojure, Go, Groovy, Java, JavaScript, m4, Perl 5, PHP, Python 2, Unix shells.

**G0od:** ECMAScript 6, Eiffel (`0c` — cute!), F#, Haskell, Julia, Nemerle, Nim, OCaml, Perl 6, Python 3, Ruby, Rust, Scheme (`#o`), Swift, Tcl.

**Based literals:** Ada (`8#777#`), Bash (`8#777`), Erlang (`8#777`), Icon (`8r777`), J (`8b777`), Perl 6 (`:8<777>`), PostScript (`8#777`), Smalltalk (`8r777`).

**Special mention:** BASIC uses `&O` and `&H` prefixes for octal and hex.  bc and Forth allow the base used to interpret literals to be changed on the fly, via `ibase` and `BASE` respectively.  C#, D, expr, Lua, Scala, and Standard ML have no octal literals at all.  Some COBOL extensions use `O#` and `H#`/`X#` prefixes for octal and hex.  Fortran uses the slightly odd `O'777'` syntax.  


## No power operator

Perhaps this makes sense in C, since it doesn't correspond to an actual instruction on most CPUs, but in JavaScript?  If you can make `+` work for strings, I think you can add a `**`.

If you're willing to ditch the bitwise operators (or lessen their importance a bit), you can even use `^`, as most people would write in regular ASCII text.

**Powerless:** ACS, C#, Eiffel, Erlang, expr, Forth, Go.

**Two out of two stars:** Ada, ALGOL (`↑` works too), COBOL, CoffeeScript, ECMAScript 7, Fortran, F#, Groovy, OCaml, Perl, PHP, Python, Ruby, Unix shells.

**I tip my hat:** awk, BASIC, bc, COBOL, fish, Lua.

**Otherwise powerful:** APL (`⋆`), D (`^^`).

**Special mention:** Lisps tend to have a named function rather than a dedicated operator (e.g. `Math/pow` in Clojure, `expt` in Common Lisp), but since operators are regular functions, this doesn't stand out nearly so much.  Haskell uses all three of `^`, `^^`, and `**` for [typing reasons](http://stackoverflow.com/q/6400568/17875).


## C-style for loops

This construct is bad.  It very rarely matches what a human actually wants to do, which 90% of the time is "go through this list of stuff" or "count from 1 to 10".  A C-style `for` obscures those wishes.  The syntax is downright goofy, too: nothing else in the language uses `;` as a delimiter and repeatedly executes only _part_ of a line.  It's like a tuple of statements.

I said in my [previous post about iteration]({filename}/2016-11-18-iteration-in-one-language-then-all-the-others.markdown) that having an iteration protocol requires either objects or closures, but I realize that's not true.  I even disproved it in the same post.  Lua's own iteration protocol can be implemented without closures — the semantics of `for` involve keeping a persistent state value and passing it to the iterator function every time.  It could even be implemented in C!  Awkwardly.  And with a bunch of macros.  Which aren't hygenic in C.  Hmm, well.

**Loopy:** ACS, bc, Fortran.

**Cool and collected:** C#, Clojure, D, Delphi (recent), ECMAScript 6, Eiffel (recent), Go, Groovy, Icon, Inform 7, Java, Julia, Logo, Lua, Nemerle, Nim, Objective-C, Perl, PHP, PostScript, Prolog, Python, R, Rust, Scala, Smalltalk, Swift, Tcl, Unix shells, Visual Basic.

**Special mention:** Functional languages and Lisps are laughing at the rest of us here.  awk has `for...in`, but it doesn't iterate arrays in order which makes it rather less useful.  JavaScript (pre ES6) has _both_ `for...in` and `for each...in`, but both are differently broken, so you usually end up using C-style `for` or external iteration.  BASIC has an ergonomic numeric loop, but no iteration loop.  Ruby mostly uses external iteration, and its `for` block is actually expressed in those terms.


## Switch with default fallthrough

We've [been through this before]({filename}/2016-09-18-the-curious-case-of-the-switch-statement.markdown#some-objections).  Wanting completely separate code per `case` is, by far, the most common thing to want to do.  It makes no sense to have to explicitly opt _out_ of the more obvious behavior.

**Breaks my heart:** Java, JavaScript.

**Follows through:** Ada, BASIC, CoffeeScript, Go (has a `fallthrough` statement), Lisps, Ruby, Swift (has a `fallthrough` statement), Unix shells.

**Special mention:** C# and D require `break`, but require _something_ one way or the other — implicit fallthrough is disallowed except for empty `case`s.  Perl 5 historically had no `switch` block built in, but it comes with a [Switch](http://perldoc.perl.org/5.8.8/Switch.html) module, and the last seven releases have had an [experimental `given` block](http://perldoc.perl.org/perlsyn.html#Switch-Statements) which I stress is _still_ experimental.  Python has no `switch` block.  Erlang, Haskell, and Rust have pattern-matching instead (which doesn't allow fallthrough at all).


## Type first

```c
int foo;
```

In C, this isn't _too_ bad.  You get into problems when you remember that it's common for type names to be all lowercase.

```c
foo * bar;
```

Is that a useless expression, or a declaration?  It depends entirely on whether `foo` is a variable or a type.

It gets a little weirder when you consider that there are type names with spaces in them.  And storage classes.  And qualifiers.  And sometimes part of the type comes _after_ the name.

```c
extern const volatile _Atomic unsigned long long int * restrict foo[];
```

That's not even getting into the syntax for types of function pointers, which might have arbitrary amounts of stuff after the variable name.

And then C++ came along with generics, which means a type name might _also_ have other type names nested _arbitrarily deep_.

```cpp
extern const volatile std::unordered_map<unsigned long long int, std::unordered_map<const long double * const, const std::vector<std::basic_string<char>>::const_iterator>> foo;
```

And that's just a declaration!  Imagine if there were an assignment in there too.

The great thing about static typing is that I know the types of all the variables, but that advantage is somewhat lessened if I can't tell _what the variables are_.

Between type-first, function pointer syntax, Turing-complete duck-typed templates, and C++'s initialization syntax, there are several ways where [parsing C++ is ambiguous](https://en.wikipedia.org/wiki/Most_vexing_parse) or even [undecidable](http://blog.reverberate.org/2013/08/parsing-c-is-literally-undecidable.html)!  "Undecidable" here means that there exist C++ programs which cannot even be parsed into a syntax tree, because the same syntax means two different things depending on whether some expression is a _value_ or a _type_, and that question can depend on an endlessly recursive template instantiation.  ([This is also a great example of ambiguity](http://yosefk.com/c++fqa/web-vs-c++.html#misfeature-2), where `x * y(z)` could be either an expression or a declaration.)

Contrast with, say, Rust:

```rust
let x: ... = ...;
```

This is easy to parse, both for a human and a computer.  The thing before the colon _must_ be a variable name, and it stands out immediately; the thing after the colon _must_ be a type name.  Even better, Rust has pretty good type inference, so the type is probably unnecessary anyway.

Of course, languages with no type declarations whatsoever are immune to this problem.

**Most vexing:** ACS, ALGOL, C#, D (though `[]` goes on the type), Fortran, Java, Perl 6.

**Looks Lovely:** Ada, Boo, F#, Go, Python 3 (via annotation syntax and the `typing` module), Rust, Swift, TypeScript.

**Special mention:** BASIC uses trailing type sigils to indicate scalar types.


## Weak typing

Please note: [this is not the opposite of static typing]({filename}/2016-07-26-the-hardest-problem-in-computer-science.markdown#loose-typing).  Weak typing is more about the runtime behavior of _values_ — if I try to use a value of type T as though it were of type U, will it be implicitly converted?

C lets you assign pointers to `int` variables and then take square roots of them, which seems like a bad idea to me.  C++ agreed and nixed this, but also introduced the ability to make your own custom types implicitly convertible to as many other types you want.

This one is pretty clearly a spectrum, and I don't have a clear line.  For example, I don't fault Python for implicitly converting between `int` and `float`, because `int` is infinite-precision and `float` is 64-bit, so it's _usually_ fine.  But I'm a lot more suspicious of C, which lets you assign an `int` to a `char` without complaint.  (Well, okay.  Literal integers in C are `int`s, which poses a slight problem.)

I _do_ count a combined addition/concatenation operator that accepts different types of arguments as a form of weak typing.

**Weak:** JavaScript (`+`), PHP, Unix shells (almost everything's a string, but even arrays/scalars are somewhat interchangeable).

**Strong:** F#, Go (explicit numeric casts), Haskell, Python, Rust (explicit numeric casts).

**Special mention:** ACS only has integers; even fixed-point values are stored in integers, and the compiler has no notion of a fixed-point type, making it the weakest language imaginable.  C++ and Scala both allow defining implicit conversions, for better or worse.  Perl 5 is weak, _but_ it avoids most of the ambiguity by having entirely separate sets of operators for string vs numeric operations.  Python 2 is mostly strong, but that whole interchangeable bytes/text thing sure caused some ruckus.  Tcl only has strings.


## Integer division

"Hey, new programmers!" you may find yourself saying.  "Don't worry, it's just like math, see?  Here's how to use $LANGUAGE as a calculator."

"Oh boy!" says your protégé.  "Let's see what 7 ÷ 2 is!  Oh, it's 3.  I think the computer is broken."

They're right!  It _is_ broken.  I have genuinely seen a non-trivial number of people come into #python thinking division is "broken" because of this.

To be fair, C is pretty consistent about making math operations always produce a value whose type matches one of the arguments.  It's also unclear whether such division should produce a `float` or a `double`.  Inferring from context would make sense, but that's not something C is really big on.

Quick test: `7 / 2` is 3½, not 3.

**Integrous:** bc, C#, D, expr, F#, Fortran, Go, OCaml, Python 2, Ruby, Rust (hard to avoid), Unix shells.

**Afloat:** awk (no integers), Clojure (produces a rational!), Groovy, JavaScript (no integers), Lua (no integers until 5.3), Nim, Perl 5 (no integers), Perl 6, PHP, Python 3.

**Special mention:** Haskell disallows `/` on integers.  Nim, Haskell, Perl 6, Python, and probably others have separate integral division operators: `div`, `div`, `div`, and `//`, respectively.


## Bytestrings

"Strings" in C are arrays of 8-bit characters.  They aren't really strings at all, since they can't hold the vast majority of characters without some further form of encoding.  Exactly what the encoding is and how to handle it is left entirely up to the programmer.  This is a pain in the ass.

Some languages caught wind of this Unicode thing in the 90s and decided to solve this problem once and for all by making "wide" strings with 16-bit characters.  (Even C95 has this, in the form of `wchar_t*` and `L"..."` literals.)  Unicode, you see, would never have more than 65,536 characters.

Whoops, so much for that.  Now we have strings encoded as UTF-16 rather than UTF-8, so we're paying extra storage cost and we _still_ need to write extra code to do basic operations right.  Or we forget, and then later we have to track down a bunch of wonky bugs because someone typed a 💩.

Note that handling characters/codepoints is very different from handling _glyphs_, i.e. the distinct shapes you see on screen.  Handling glyphs doesn't even really make sense outside the context of a font, because fonts are free to make up whatever ligatures they want.  Remember ["diverse" emoji]({filename}/2016-04-12-apple-did-not-invent-emoji.markdown#gender-diversity)?  Those are ligatures of three to seven characters, completely invented by a font vendor.  A programming language can't reliably count the display length of that, especially when new combining behaviors could be introduced at any time.

Also, it doesn't matter _how_ you solve this problem, as long as it appears to be solved.  I believe Ruby uses bytestrings, for example, but they know their own encoding, so they can be correctly handled as sequences of codepoints.  Having a separate non-default type or methods does _not_ count, because everyone will still use the wrong thing first — sorry, Python 2.

Quick test: what's the length of "💩"?  If 1, you have real unencoded strings.  If 2, you have UTF-16 strings.  If 4, you have UTF-8 strings.  If something else, I don't know what the heck is going on.

**Totally bytes:** Go, Lua, Python 2 (separate `unicode` type).

**Comes up short:** Java, JavaScript.

**One hundred emoji:** Python 3, Ruby, Rust, Swift (even gets combining characters right!).

**Special mention:** Go's strings are explicitly arbitrary byte sequences, but iterating over a string with `for..range` decodes UTF-8 code points.  Perl 5 gets the quick test right if you put `use utf8;` at the top of the file, but Perl 5's Unicode support is such a [confusing clusterfuck](http://perldoc.perl.org/perlunicode.html) that I can't really give it a 💯.

Hmm.  This one is kind of hard to track down for sure without either knowing a lot about internals or installing fifty different interpreters/compilers.



## Increment and decrement

I don't think there are too many compelling reasons to have `++`.  It means the same as `+= 1`, which is still nice and short.  The only difference is that people can do stupid unreadable tricks with `++`.

One exception: it _is_ possible to overload `++` in ways that don't make sense as `+= 1` — for example, C++ uses `++` to advance iterators, which may do any arbitrary work under the hood.

**Double plus ungood:** ACS, awk, C#, D, Go, Java, JavaScript, Perl, Unix shells, Vala.

**Double plus good:** Lua (which doesn't have `+=` either), Python, Ruby, Rust, Swift (removed in v3).

**Special mention:** Perl 5 and PHP both allow `++` on strings, in which case it increments letters or something, but I don't know if much real code has ever used this.


## `!`

A pet peeve.  Spot the difference:

```c
if (looks_like_rain()) {
    ...
}
if (!looks_like_rain()) {
    ...
}
```

That single `!` is ridiculously subtle, which seems wrong to me when it makes an expression mean its _polar opposite_.  Surely it should stick out like a sore thumb.  The left parenthesis makes it worse, too; it blends in slightly as just noise.

It helps a bit to space after the `!` in cases like this:

```c
if (! looks_like_rain()) {
    ...
}
```

But this seems to be curiously rare.  The easy solution is to just spell the operator `not`.  At which point the other two might as well be `and` and `or`.

Interestingly enough, C95 specifies `and`, `or`, `not`, and [some others](http://en.cppreference.com/w/c/language/operator_alternative) as standard alternative spellings, though I've never seen them in any C code and I suspect existing projects would prefer I not use them.

**Not right:** ACS, awk, C#, D, Go, Groovy, Java, JavaScript, Nemerle, PHP, R, Rust, Scala, Swift, Tcl, Vala.

**Spelled out:** Ada, ALGOL, BASIC, COBOL, Erlang, F#, Fortran, Haskell, Inform 7, Lisps, Lua, Nim, OCaml, Pascal, PostScript, Python, Smalltalk, Standard ML.

**Special mention:** APL and Julia both use `~`, which is at least easier to pick out, which is more than I can say for most of APL.  bc and expr, which are really calculators, have no concept of Boolean operations.  Forth and Icon, which are not calculators, don't seem to either.  Inform 7 often blends the negation into the verb, e.g. `if the player does not have...`.  Perl and Ruby have _both_ symbolic and named Boolean operators (Perl 6 has even more), with _different precedence_ (which inside `if` won't matter); I believe Perl 5 prefers the words and Ruby prefers the symbols.  Perl and Ruby also both have a separate `unless` block, with the opposite meaning to `if`.  Python has `is not` and `not in` operators.


## Single return and out parameters

Because C can only return a single value, and that value is often an indication of failure for the sake of an `if`, "out" parameters are somewhat common.

```c
double x, y;
get_point(&x, &y);
```

It's not immediately clear whether `x` and `y` are input or output.  Sometimes they might function as both.  (And of course, in this silly example, you'd be better off returning a single `point` struct.  Or would you use a `point` out parameter because returning structs is potentially expensive?)

Some languages have doubled down on this by adding syntax to declare "out" parameters, which removes the ambiguity in the function _definition_, but makes it worse in function _calls_.  In the above example, using `&` on an argument is at least a decent hint that the function wants to write to those values.  If you have implicit out parameters or pass-by-reference or whatever, that would just be `get_point(x, y)` and you'd have no indication that those arguments are special in any way.

The vast majority of the time, this can be expressed in a more straightforward way by returning multiple values:

```python
x, y = get_point()
```

That was intended as Python, but _technically_, Python doesn't have multiple returns!  It seems to, but it's really a combination of several factors: a tuple type, the ability to make a tuple literal with just commas, and the ability to _unpack_ a tuple via multiple assignment.  In the end it works just as well.  Also this is a way better use of the comma operator than in C.

But the exact same code could appear in Lua, which has multiple return/assignment as an explicit feature...  and _no_ tuples.  The difference becomes obvious if you try to assign the return value to a single variable instead:

```python
point = get_point()
```

In Python, `point` would be a tuple containing both return values.  In Lua, `point` would be the `x` value, and `y` would be silently discarded.  I don't tend to be a fan of silently throwing data away, but I have to admit that Lua makes pretty good use of this in several places for "optional" return values that the caller can completely ignore if desired.  An existing function can even be extended to return more values than before — that would break callers in Python, but work just fine in Lua.

(Also, to briefly play devil's advocate: I once saw Python code that returned **14** values all with very complicated values, types, and semantics.  Maybe don't do that.  I think I cleaned it up to return an object, which simplified the calling code considerably too.)

It's also possible to half-ass this.  ECMAScript 6::

```javascript
function get_point() {
    return [1, 2];
}

var [x, y] = get_point();
```

It _works_, but it doesn't actually _look_ like multiple return.  The trouble is that JavaScript has C's comma operator _and_ C's variable declaration syntax, so neither of the above constructs could've left off the brackets without significantly changing the syntax:

```javascript
function get_point() {
    // Whoops!  This uses the comma operator, which evaluates to its last
    // operand, so it just returns 2
    return 1, 2;
}

// Whoops!  This is multiple declaration, where each variable gets its own "=",
// so it assigns nothing to x and the return value to y
var x, y = get_point();
// Now x is undefined and y is 2
```

This is still better than either out parameters or returning an explicit struct that needs manual unpacking, but it's not as good as comma-delimited tuples.  Note that some languages require parentheses around tuples (and also call them tuples), and I'm arbitrarily counting that as better than bracket.

**Single return:** Ada, ALGOL, BASIC, C#, COBOL, Fortran, Groovy, Java, Smalltalk.

**Half-assed multiple return:** C++11, D, ECMAScript 6, Erlang, PHP.

**Multiple return via tuples:** F#, Haskell, Julia, Nemerle, Nim, OCaml, Perl (just lists really), Python, Ruby, Rust, Scala, Standard ML, Swift, Tcl.

**Native multiple return:** Common Lisp, Go, Lua.

**Special mention:** C# has explicit syntax for `out` parameters, but it's a compile-time error to not assign to all of them, which is slightly better than C.  Forth is stack-based, and all return values are simply placed on the stack, so multiple return isn't a special case.  Unix shell functions don't return values.  Visual Basic sets a return value by assigning to the function's name (?!), so good luck fitting multiple return in there.


## Silent errors

Most runtime errors in C are indicated by one of two mechanisms: returning an error code, or segfaulting.  Segfaulting is pretty noisy, so that's okay, except for the exploit potential and all.

Returning an error code kinda sucks.  Those tend to be important, but nothing in the language actually reminds you to check them, and of course we silly squishy humans have the habit of assuming everything will succeed at all times.  Which is how I segfaulted `git` two days ago: I found a spot where it didn't check for a `NULL` returned as an error.

There are several alternatives here: exceptions, statically forcing the developer to check for an error code, or using something monad-like to statically force the developer to distinguish between an error and a valid return value.  Probably some others.  In the end I was surprised by how many languages went the exception route.

**Quietly wrong:** Unix shells.  Wow, yeah, I'm having a hard time naming anything else.  Good job, us!  And even Unix shells have `set -e`; it's just opt-in.

**Exceptional:** Ada, C++, C#, D, Erlang, Forth, Java (exceptions are even part of function signature), JavaScript, Nemerle, Nim, Objective-C, OCaml, Perl 6, Python, Ruby, Smalltalk, Standard ML, Visual Basic.

**Monadic:** Haskell (`Either`), Rust (`Result`).

**Special mention:** ACS doesn't really have many operations that can error, and those that do simply halt the script.  ALGOL apparently has something called "mending" that I don't understand.  Go tends to use _secondary_ return values, which calling code has to unpack, making them slightly harder to forget about; it also allows both the assignment and the error check together in the header of an `if`.  Lisps have _conditions_ and `call/cc`, which are different things entirely.  Lua and Perl 5 handle errors by taking down the whole program, but offer a construct that can catch that further up the stack, which is clumsy but enough to emulate `try..catch`.  PHP has exceptions, _and_ errors (which are totally different), _and_ a lot of builtin functions that return error codes.  Swift has something that looks like exceptions, but it doesn't involve stack unwinding and does require some light annotation — apparently sugar for an "out" parameter holding an error.  Visual Basic, and I believe some other BASICs, decided C wasn't bad enough and introduced the bizarre `On Error Resume Next` construct which does exactly what it sounds like.


## Nulls

The [billion dollar mistake](https://en.wikipedia.org/wiki/Tony_Hoare#Apologies_and_retractions).

I think it's considerably _worse_ in a statically typed language like C, because the whole point is that you can rely on the types.  But a `double*` might be `NULL`, which is not actually a pointer to a `double`; it's a pointer to a segfault.  Other kinds of bad pointers are possible, of course, but those are more an issue of _memory_ safety; allowing any reference to be null violates _type_ safety.  The root of the problem is treating null as a possible _value_ of any type, when really it's its own type entirely.

The alternatives tend to be either opt-in nullability or an "optional" generic type (a monad!) which eliminates null as its own value entirely.  Notably, Swift does it both ways: optional types are indicated by a trailing `?`, but that's just syntactic sugar for `Option<T>`.

On the other hand, while it's annoying to get a `None` where I didn't expect one in Python, it's not like I'm surprised.  I occasionally get a string where I expected a number, too.  The language explicitly leaves type concerns in my hands.  My real objection is to having a static type system that _lies_.  So I'm not going to list every single dynamic language here, because not only is it consistent with the rest of the type system, but they don't really have any machinery to prevent this anyway.

**Nothing doing:** C#, D, Go, Java, Nim (non-nullable types are opt _in_).

**Nullable types:** Swift (sugar for a monad).

**Monads:** F# (`Option` — though technically F# also inherits `null` from .NET), Haskell (`Maybe`), Rust (`Option`), Swift (`Optional`).

**Special mention:** awk, Tcl, and Unix shells only have strings, so in a surprising twist, they have no concept of null whatsoever.  Java recently introduced an `Optional<T>` type which explicitly may or may not contain a value, but since it's still a non-primitive, it could _also_ be `null`.  C++17 doesn't quite have the same problem with `std::optional<T>`, since non-reference values can't be null.  Inform 7's `nothing` value is an `object` (the root of half of its type system), which means any `object` variable might be `nothing`, but any value of a more specific type cannot be `nothing`.  JavaScript has _two_ null values, `null` and `undefined`.  Perl 6 is really big on static types, but claims its `Nil` object doesn't exist, and I don't know how to even begin to unpack that.  R and SQL have a more mathematical kind of `NULL`, which tends to e.g. vanish from lists.


## Assignment as expression

How common a mistake is this:

```c
if (x = 3) {
    ...
}
```

Well, I don't know, actually.  Maybe not _that_ common, save for among beginners.  But I sort of wonder whether allowing this buys us anything.  I can only think of two cases where it does.  One is with something like iteration:

```c
// Typical linked list
while (p = p->next) {
    ...
}
```

But this is only necessary in C in the first place because it has no first-class notion of iteration.  The other is shorthand for checking that a function returned a useful value:

```c
if (ptr = get_pointer()) {
    ...
}
```

But if a function returns `NULL`, that's really an error condition, and presumably you have some other way to handle that too.

What does that leave?  The only time I remotely miss this in Python (where it's illegal) is when testing a regex.  You tend to see this a lot instead.

```python
m = re.match('x+y+z+', some_string)
if m:
    ...
```

`re` treats failure as an acceptable possibility and returns `None`, rather than raising an exception.  I'm not sure whether this was the right thing to do or not, but off the top of my head I can't think of too many other Python interfaces that _sometimes_ return `None`.

**Freedom of expression:** ACS, C#, Java, JavaScript, Perl, PHP, Swift.

**Makes a statement:** Inform 7, Lua, Python, Unix shells.

**Special mention:** BASIC uses `=` for both assignment _and_ equality testing — the meaning is determined from context.  D allows variable _declaration_ as an expression, so `if (int x = 3)` is allowed, but regular assignment is not.  Functional languages generally don't have an assignment operator.  Go disallows assignment as an expression, but assignment _and_ a test can appear together in an `if` condition, and this is an idiomatic way to check success.  Ruby makes everything an expression, so assignment might as well be too.  Rust makes everything an expression, but assignment evaluates to the useless `()` value (due to ownership rules), so it's not actually useful.  Rust and Swift both have a special `if let` block that explicitly combines assignment with pattern matching, which is way nicer than the C approach.


## No hyphens in identifiers

snake\_case requires dancing on the shift key (unless you rearrange your keyboard, which is perfectly reasonable).  It slows you down slightly and leads to occasional mistakes like `snake-Case`.  The alternative is dromedaryCase, which is objectively wrong and doesn't actually solve this problem anyway.

Why not just allow hyphens in identifiers, so we can avoid this argument and use `kebab-case`?

Ah, but then it's ambiguous whether you mean an identifier or the subtraction operator.  No problem: require spaces for subtraction.  I don't think a tiny way you're allowed to make your code harder to read is really worth this clear advantage.

**Low scoring:** ACS, C#, D, Java, JavaScript, OCaml, Pascal, Perl 5, PHP, Python, Ruby, Rust, Swift, Unix shells.

**Nicely-designed:** COBOL, CSS (and thus Sass), Forth, Inform 7, Lisps, Perl 6, XML.

**Special mention:** Perl has a built-in variable called `$-`, and Ruby has a few called `$-n` for various values of "n", but these are very special cases.


## Braces and semicolons

Okay.  Hang on.  Bear with me.

C code looks like this.

```c
some block header {
    line 1;
    line 2;
    line 3;
}
```

The block is indicated _two different ways_ here.  The braces are for the _compiler_; the indentation is for _humans_.

Having two different ways to say the same thing means they can get out of sync.  They can _disagree_.  And that can be, as previously mentioned, _really bad_.  This is really just a more general form of the problem of optional block delimiters.

The only solution is to eliminate one of the two.  Programming languages exist for the benefit of humans, so we obviously can't get rid of the indentation.  Thus, we should get rid of the braces.  QED.

As an added advantage, we reclaim all the vertical space wasted on lines containing only a `}`, and we can stop squabbling about where to put the `{`.

If you accept this, you might start to notice that there are _also_ two different ways of indicating where a line ends: with semicolons for the compiler, and with _vertical_ whitespace for humans.  So, by the same reasoning, we should lose the semicolons.

Right?  Awesome.  Glad we're all on the same page.

Some languages use keywords instead of braces, but the effect is the same.  I'm not aware of any languages that use keywords instead of semicolons.

**Bracing myself:** C#, D, Erlang, Java, Perl, Rust.

**Braces, but no semicolons:** Go (ASI), JavaScript (ASI — see below), Lua, Ruby, Swift.

**Free and clear:** CoffeeScript, Haskell, Python.

**Special mention:** Lisp, just, in general.  Inform 7 has an indented style, but it still requires semicolons.  MUMPS doesn't support nesting at all, but I believe there are extensions that use dots to indicate it.

Here's some interesting trivia.  JavaScript, Lua, and Python all optionally allow semicolons at the end of a statement, but the way each language determines line continuation is very different.

JavaScript takes an "opt-out" approach: it continues reading lines until it hits a semicolon, _or_ until reading the next line would cause a syntax error.  (This approach is called _automatic semicolon insertion_.)  That leaves a few corner cases like starting a new line with a `(`, which could look like the last thing on the previous line is a function you're trying to call.  Or you could have `-foo` on its own line, and it would parse as subtraction rather than unary negation.  You might wonder why anyone would do that, but using unary `+` is one way to make `function` parse as an expression rather than a statement!  I'm not so opposed to semicolons that I want to be debugging where the language _thinks_ my lines end, so I just always use semicolons in JavaScript.

Python takes an "opt-in" approach: it assumes, by default, that a statement ends at the end of a line.  However, newlines inside parentheses or brackets are ignored, which takes care of 99% of cases — long lines are most frequently caused by function calls (which have parentheses!) with a lot of arguments.  If you _really_ need it, you can explicitly escape a newline with `\\`, but this is widely regarded as incredibly ugly.

Lua avoids the problem almost entirely.  I believe Lua's grammar is designed such that it's _almost_ always unambiguous where a statement ends, even if you have no newlines at all.  This has a few weird side effects: void expressions are syntactically forbidden in Lua, for example, so you just _can't_ have `-foo` as its own statement.  Also, you can't have code immediately following a `return`, because it'll be interpreted as a return value.  The upside is that Lua can treat newlines just like any other whitespace, but still not need semicolons.  In fact, semicolons aren't statement terminators in Lua at all — they're _their own statement_, which does nothing.  Alas, not for lack of trying, Lua does have the same `(` ambiguity as JavaScript (and parses it the same way), but I don't think any of the others exist.

Oh, and the colons that Python has at the end of its block headers, like `if foo:`?  As far as I can tell, they serve no syntactic purpose whatsoever.  Purely aesthetic.


## Blaming the programmer

Perhaps one of the worst misfeatures of C is the ease with which responsibility for problems can be shifted to the person who wrote the code.  "Oh, you segfaulted?  I guess you forgot to check for `NULL`."  If only I had a computer to take care of such tedium for me!

Clearly, computers can't be expected to do everything for us.  But they can be expected to do quite a bit.  Programming languages are built _for humans_, and they ought to eliminate the sorts of rote work humans are bad at whenever possible.  A programmer is already busy thinking about the actual problem they want to solve; it's no surprise that they'll sometimes forget some tedious detail the language forces them to worry about.

So if you're designing a language, don't just copy C.  Don't just copy C++ or Java.  Hell, don't even just copy Python or Ruby.  Consider your target audience, consider the problems they're trying to solve, and try to get as much else out of the way as possible.  If the same "mistake" tends to crop up over and over, look for a way to modify the language to reduce or eliminate it.  And be sure to look at a lot of languages for inspiration — even ones you hate, even weird ones no one uses!  A lot of clever people have had a lot of other ideas in the last 44 years.

----

I hope you enjoyed this accidental cross-reference of several dozen languages!  I enjoyed looking through them all, though it was _incredibly_ time-consuming.  Some of them look pretty interesting; maybe give them a whirl.

Also, dammit, now I'm [thinking about language design]({filename}/2015-02-28-sylph-the-programming-language-i-want.markdown) again.
