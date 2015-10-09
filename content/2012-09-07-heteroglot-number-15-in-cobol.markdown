title: Heteroglot: #15 in COBOL
date: 2012-09-07 23:17
tags: math, project euler, cobol
category: blog


## Introduction

Many moons ago, I started a ridiculous quest to solve every [Project Euler][] problem, in order, with a different programming language.  I called it "[heteroglot][]".

Partway through that, I gave myself the additional unwritten rule that the next language would be selected by polling the nearest group of nerds.  This has resulted in math problems solved in such wildly inappropriate languages as [vimscript][], [MUMPS][], [LOLcode][], and [XSLT][].

It's been a while since I did one of these, but I still remember that the next language I'm stuck using is COBOL.  I don't know who suggested it, but I hope he chokes on a rake.  ♥

I figure if this is interesting to me, it might be interesting to someone else.  So let's learn some math and/or COBOL.

<!-- more -->


## The math

{% img right http://projecteuler.net/project/images/p_015.gif 'Problem 15 illustration' 'Illustration of the six paths from the top-left to bottom-right of a 2×2 grid, following the grid lines.' %}

[Problem 15][]:

> Starting in the top left corner of a 2×2 grid, there are 6 routes (without backtracking) to the bottom right corner.
>
> How many routes are there through a 20×20 grid?

There are two approaches to solving this: actually _count_ every path, or invent a formula.  I'd like to spend as little time with COBOL as possible today, so let's try the latter approach.

So, find a pattern.

* In the trivial case (0×0), there's only 1 path.
* For 1×1, there are 2 paths: effectively clockwise and counter-clockwise.
* The problem already states that 2×2 has 6 paths.

Now, wait.  Before considering 3×3, bear in mind: nothing about this problem requires that the grid be _square_.  Think of some other small sizes:

* 0×1 and 0×2 also have only one path.  Naturally, any grid with either dimension of 0 will have only one possible path, because it's a straight line.
* 1×2 has 3 paths: clockwise, counter-clockwise, and through the middle in an S shape.

        @@@@    @--+    @--+
        ¦  @    @  ¦    @  ¦
        +--@    @--+    @@@@
        ¦  @    @  ¦    ¦  @
        +--@    @@@@    +--@

* Consider 1×3.  It has four horizontal grid lines, making for 4 possible paths: one for each horizontal line.

        @@@@    @--+    @--+    @--+
        ¦  @    @  ¦    @  ¦    @  ¦
        +--@    @@@@    @--+    @--+
        ¦  @    ¦  @    @  ¦    @  ¦
        +--@    +--@    @@@@    @--+
        ¦  @    ¦  @    ¦  @    @  ¦
        +--@    +--@    +--@    @@@@

Has a pattern emerged?

    · | 0   1   2   3
    --+--------------
    0 | 1   1   1   1
    1 | 1   2   3   4
    2 | 1   3   6
    3 | 1   4

Oh ho ho.  Yes, yes it has.  Tilt that table diagonally.

            1
          1   1
        1   2   1
      1   3   3   1
    1   4   6   4   1

This is Pascal's Triangle.

In retrospect, this makes perfect sense.  Consider the 3×3 grid.  Starting from the top left, there are only two possible directions to go: right, or down.  If you go right, you can only follow the possible paths for a 2×3 grid.  If you go down, you can only follow the possible paths for a 3×2 grid.  And none of them can overlap, because you started differently.

    +--+--+--+      @@@@--+--+    @
    ¦  ¦  ¦  ¦         ¦  ¦  ¦    @
    +--+--+--+         +--+--+    @--+--+--+
    ¦  ¦  ¦  ¦  =>     ¦  ¦  ¦    ¦  ¦  ¦  ¦
    +--+--+--+         +--+--+    +--+--+--+
    ¦  ¦  ¦  ¦         ¦  ¦  ¦    ¦  ¦  ¦  ¦
    +--+--+--+         +--+--+    +--+--+--+

So in the table, any given number is the sum of the number immediately to its left and immediately above it: the two solutions for the same-size grid with one fewer row or one fewer column.  That's exactly how Pascal's Triangle is created.

In the `n`th row of the triangle, the number at offset `r` (both counting from zero) is given by `nCr(n, r)`.  All I need now is to convert a grid size `a×b` to a row in the triangle.  Each triangle row is a diagonal of the original table, so you get the row number from `a + b`, and the offset is either `a` or `b`.  The answer is then `nCr(a + b, a)`.

Check against what I know: 1×1 is `nCr(2, 1) = 2`, 2×2 is `nCr(4, 2) = 6`.  0-by-anything is 1.  Lookin good.

From here I could just figure it out with a calculator, but that's cheating.  Time to find a COBOL compiler.


## The code

I'm on Arch, and the first thing I found was [OpenCOBOL][], [on the AUR][opencobol package], so I'm installing this bad boy.  Your results may vary, if for some reason you're following along.

    eevee@perushian ~ ⚘ sudo packer -S open-cobol

Now I need to learn some COBOL.  OpenCOBOL's site helpfully links this [OpenCOBOL Programmer's Guide][].  Let's see what I have here.

> 1.3.1. “I Heard COBOL is a Dead Language!”
> Phoenician is a dead language. Mayan is a dead language. Latin is a dead language. What makes these languages dead is the fact that no one speaks them anymore. COBOL is NOT a dead language, and despite pontifications that come down to us from the ivory towers of academia, it isn’t even on life support.

> As more and more people became at least informed about programming if not downright skilled, the syntax of COBOL became one of the reasons the ivory-tower types wanted to see it eradicated.

My archaeological adventure is off to a fantastic start.

Right, well, step two: what the hell does a program look like?  I am dimly away that COBOL has a lot of wordy setup and DIVISIONs of code or data or something.  Section 2 starts to explain this setup.  The only required part of a COBOL program appears to be `PROGRAM-ID. {program-name}`, but that won't actually do anything.  So I think I'll actually need something more like this:

    IDENTIFICATION DIVISION.
    PROGRAM-ID. project-euler-15

    DATA DIVISION.
    // something to specify 20 by 20

    PROCEDURE DIVISION.
    // make it go

    END PROGRAM project-euler-15.

That last part isn't actually necessary if I'm only building one file, but I like the feeling of talking to a computer with no prepositions or particles.  Reminds me a little of [Robotic][].

At this point I like to stick my no-op program in a file and compile it, just to make sure I have _something_ valid (and also to figure out how to compile).  Here I discover several things.

* COBOL source is `.cob`.  Or `.cbl`, but that's not as funny.
* vim has built-in COBOL syntax highlighting.
* Because "indented block" is nonsense in COBOL, the shift operators (`<` and `>`) do nothing.  (The above block was indented, because my blog is all Markdown, and I had to outdent it manually.)
* Everything about the code above is wrong.  Everything.  Every single character is syntax colored as an error.

I'm having flashbacks to [MUMPS][wiki MUMPS] already.

Let's continue reading.  In §1.5, "Source Program Format", it is revealed that the compiler can run in two modes: fixed (the default) and free.  Fixed mode uses "traditional" 80-column formatting.  This rings some faint bells: COBOL is all about the columns.  What column does code need to start in?  Fuck if I know.  I can't find anywhere in the documentation for this compiler that actually explains how fixed mode _works_.

Back to the website, and I find that the _online_ [User Manual][OpenCOBOL User Manual] is not very thorough but _does_ contain an example [hello world][] program, which explicitly states that program lines must start in column 8.

And, indeed, indenting everything by 7 spaces makes vim happy.  Now I have:

```
       IDENTIFICATION DIVISION.
       PROGRAM-ID. project-euler-15

       DATA DIVISION.
      * something to specify 20 by 20

       PROCEDURE DIVISION.
      * make it go

       END PROGRAM project-euler-15.
```

Haha, and people complain that Python has significant whitespace.  You assholes.  Guess what I'm linking you next time I hear that.

At last, time to try running this thing.  The [hello world][] program comes with super simple instructions for that, too.

    ⚘ cobc -x 015.cob
    ⚘ ./015

Success!  Nothing happened.

### Do a thing

First is the seed data, which here is just the size of the grid: 20×20.  I'm gonna go out on a limb here and guess that data goes in the `DATA DIVISION`.  This handy programmer guide has a page-sized diagram of the syntax for defining data and many more pages of the clusterfuck that is record syntax, but luckily there's a much simpler way to define _constants_:

```
78 foo VALUE IS bar.
```

The `78` is a "level", an ancient incantation used to specify just how deep in the hierarchy a datum is.  In this case `78` happens to be a special level used only for constants.

Before trying to run this again, it'd be helpful to print out the constants and make sure I've actually defined them correctly.  This is done with `DISPLAY`.  (The same statement, inexplicably, also inspects command-like arguments and gets/sets environment variables.  What.)

```
       IDENTIFICATION DIVISION.
       PROGRAM-ID. project-euler-15


       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * grid size: 20 x 20
       78 width VALUE IS 20.
       78 height VALUE IS 20.


       PROCEDURE DIVISION.

       DISPLAY width
           UPON CONSOLE
       DISPLAY height
           UPON CONSOLE


       END PROGRAM project-euler-15.
```

The `UPON CONSOLE` is entirely optional but it looks like I'm hacking a mainframe so I'm including it anyway.

And, whoops, this totally doesn't work.  Unsurprisingly, the `PROCEDURE DIVISION` needs code to be in...  procedures.  I had to give up and just look at the same programs here, but the short version is, do this:

```
       PROCEDURE DIVISION.
       do-the-needful.
           DISPLAY width
               UPON CONSOLE
           DISPLAY height
               UPON CONSOLE
           .
```

Compile, run, and get `20` twice.  Off to a fabulous start.

Just need the math.

A flip through the list of statements finds me `PERFORM`, which both calls procedures and acts like a loop.  I might as well make this a real program, so let's do both and write a real function.  Sorry, procedure.

I want to implement nCr().  I need a numerator and denominator accumulator, a loop of `r` times, and some multiplication.  Seems easy enough.

The first stumbling block is, er, creating variables.  There's nothing to do that.  They all go in the `DATA DIVISION`.  _All_ of them.  In this case I want a `LOCAL-STORAGE` section, which is re-initialized for every procedure—that means it should act like a local.

I want a loop variable, a numerator, a denominator, and two arguments.

Arguments.

Hmmmm.

It is at this point that I begin to realize that COBOL procedures do not take arguments or have return values.  Everything appears to be done with globals.

There's a `CALL` statement, but it calls _subprograms_—that is, a whole other `IDENTIFICATION DIVISION` and everything.  And even that uses globals.  Also it thinks `BY VALUE` for passing means to pass a _pointer address_, and passing literals `BY REFERENCE` allows the callee to mutate that literal anywhere else it appears in the program, and various other bizarre semantics.

Let's, um, just go with the globals.  Some fumbling produces:

```
       n-choose-r.
           MOVE 1 TO numerator
           MOVE 1 TO denominator
           PERFORM VARYING i FROM 1 BY 1 UNTIL i > r
               MULTIPLY i BY denominator
               COMPUTE numerator = numerator * (n - i + 1)
           END-PERFORM
           COMPUTE n-choose-r-result = numerator / denominator
           .
```

A note on assignment in COBOL: there isn't any.  Instead, there are several different statements for different kinds of assigning.  `ADD`, `SUBTRACT`, `MULTIPLY`, and `DIVIDE` all divide a variable or a literal (but _not an expression!_) into a variable and store the result into that variable.  `MOVE` stores a variable or a literal (but, again, not an expression) into a variable.  `COMPUTE` stores an arbitrary expression into a variable.  I assume `COMPUTE`, um, came later.

Anyway, the idea here would be that you store the arguments into the `n` and `r` globals, `PERFORM` this procedure or paragraph or whatever, then get your result out of the `n-choose-r-result` global.  The globals are in the `DATA DIVISION` like this:

```
       LOCAL-STORAGE SECTION.

      * used by n-choose-r
       01 i                            USAGE IS UNSIGNED-LONG.
       01 n                            USAGE IS UNSIGNED-LONG.
       01 r                            USAGE IS UNSIGNED-LONG.
       01 numerator                    USAGE IS UNSIGNED-LONG.
       01 denominator                  USAGE IS UNSIGNED-LONG.
       01 n-choose-r-result            USAGE IS UNSIGNED-LONG.
```

(`UNSIGNED-LONG` is a 64-bit unsigned machine integer, the biggest machine number COBOL appears to have.)

Compile it, run it, and the answer is...  6.

Hmmm.

A little `DISPLAY`ing reveals that the numerator and denominator print as 688017186506670080 and 432902008176640000, respectively.  It looks like 64 bits is not enough, and I'm overflowing.  Oops.

Well.  I could set out to see if COBOL does bignums or if the whole `PIC` thing supports arbitrary precision, but I'm scared to think what I might find.  Instead, let's do some more math.

Consider that `nCr(n, r)` for any nonnegative integers `n` and `r` is always, itself, an integer.  (This isn't too hard to prove informally, but just accepting it is enough.)  So I know:

    nCr(n, 1) = n / 1
    nCr(n, 2) = n * (n - 1) / (2 * 1)
              = n / 1 * (n - 1) / 2
    nCr(n, 3) = n * (n - 1) * (n - 2) / (3 * 2 * 1)
              = n / 1 * (n - 1) / 2 * (n - 2) / 3

I can take advantage of this to minimize the intermediate results without ever worrying about floating-point.  (Does COBOL support floating-point?  Christ, I don't want to know.)

```
       n-choose-r.
           MOVE 1 TO n-choose-r-result
           PERFORM VARYING i FROM 1 BY 1 UNTIL i > r
               COMPUTE n-choose-r-result =
                   n-choose-r-result * (n - i + 1) / i
           END-PERFORM
           .
```

This produces the answer: `000000137846528820`.

Er...  eh, close enough.  And [the internets][cobol leading zeroes] suggest it may not really be possible to avoid the leading zeroes.

Throw it at Euler and, indeed, this is correct.  Phew.  Done!  The final program is [015.cob][].


## Impression

COBOL is even more of a lumbering beast than I'd imagined; everything is global, "procedures" are barely a level above goto, and the bare metal shows through in crazy places like the possibility of changing the value of a literal (what).

On the other hand, I can see how the design maps pretty naturally _to_ bare metal, and the alternatives at the time were Fortran and ALGOL.  Ada didn't exist.  C didn't exist.  Hell, B didn't exist.  The original Lisp paper had only just been published!  In that light, COBOL is a reasonably impressive piece of work, which I will never use again if I can possibly avoid it.

One thing that slightly bewilders me is how COBOL came to _both_ have so many ways to do the same thing, yet _also_ so heavily reuse some keywords.  `DISPLAY` both prints stuff out and messes with environment variables.  `PERFORM` both calls a procedure and performs a loop.  Or calls a procedure in a loop.  And it has some pretty complex syntax for determining when the loop ends and how many times it runs and whether there's an incrementor.  It even has syntax explicitly designed for doing nested loops without actually having to nest loops.  What?

As a closing note, consider: just like MUMPS, second-hand experience tells me that there are still big high-level government/financial COBOL applications probably handling your money.  Sleep well.


## More choice quotes about COBOL

I can't resist.  This programmer's guide is _amazing_.  I know COBOL is ass-old, but this guide was published in 2009!

On endianness.

> All CPUs are capable of “understanding” big-endian format, which makes it the “most-compatible” form of binary storage across computer systems.
> 
> Some CPUs – such as the Intel/AMD i386/x64 architecture processors such as those used in most Windows PCs – prefer to process binary data stored in a little-endian format. Since that format is more efficient on those systems, it is referred to as the “native” binary format.

On working with libraries.

> Today’s current programming languages have a statement (usually, this statement is named “include” or “#include”) that performs this same function. What makes the COBOL copybook feature different than the “include” facility in current languages, however, is the fact that the COBOL COPY statement can edit the imported source code as it is being copied. This capability enables copybook libraries extremely valuable to making code reusable.

On whitespace.

> A comma character (“,”) or a semicolon (“;”) may be inserted into an OpenCOBOL program to improve readability at any spot where white space would be legal (except, of course, within alphanumeric literals). These characters are always optional. COBOL standards require that commas be followed by at least one space, when they’re used. Many modern COBOL compilers (OpenCOBOL included) relax this rule, allowing the space to be omitted in most instances.  This can cause “confusion” to the compiler if the DECIMAL POINT IS COMMA clause is used (see section 4.1.4).

On the `DISPLAY` statement.

> The specified mnemonic-name must be CONSOLE, CRT, PRINTER or any user-defined mnemonic name associated with one of these devices within the SPECIAL-NAMES paragraph (see section 4.1.4). All such mnemonics specify the same destination – the shell (UNIX) or console (Windows) window from which the program was run.


## Next up

I suppose I'm obliged to try using the first language someone suggests in the comments.  You can see what's been used so far by browsing the [existing solutions][heteroglot].  The rules therein may also be of interest.



[Project Euler]: http://projecteuler.net/about
[Problem 15]: http://projecteuler.net/problem=15
[heteroglot]: https://github.com/eevee/project-euler/tree/master/heteroglot
[vimscript]: https://github.com/eevee/project-euler/blob/master/heteroglot/008.vim
[MUMPS]: https://github.com/eevee/project-euler/blob/master/heteroglot/007.mps
[LOLcode]: https://github.com/eevee/project-euler/blob/master/heteroglot/009.lol
[XSLT]: https://github.com/eevee/project-euler/blob/master/heteroglot/014.xsl
[OpenCOBOL]: http://www.opencobol.org/
[OpenCOBOL User Manual]: http://www.opencobol.org/modules/bwiki/index.php?UserManual
[OpenCOBOL Programmer's Guide]: http://opencobol.add1tocobol.com/OpenCOBOL%20Programmers%20Guide.pdf
[opencobol package]: http://aur.archlinux.org/packages.php?ID=21860
[Robotic]: http://www.digitalmzx.net/wiki/index.php?title=Robotic
[wiki MUMPS]: http://en.wikipedia.org/wiki/MUMPS
[hello world]: http://www.opencobol.org/modules/bwiki/index.php?cmd=read&page=UserManual%2F1#content_1_1
[cobol leading zeroes]: http://www.tek-tips.com/viewthread.cfm?qid=1637735
[015.cob]: https://github.com/eevee/project-euler/blob/master/heteroglot/015.cob
