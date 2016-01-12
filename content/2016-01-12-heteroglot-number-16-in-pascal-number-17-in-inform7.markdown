title: Heteroglot: #16 in Pascal, #17 in Inform 7
date: 2016-01-12 15:09
tags: tech, math, project euler, pascal, inform
category: blog

I was thinking about doing a problem for [heteroglot](https://github.com/eevee/project-euler/tree/master/heteroglot) — my quest to solve every [Project Euler](http://projecteuler.net/about) problem in a different programming language.  (They're adding new problems much more quickly than I'm solving them, so so far I've made _negative_ progress.)  Then I discovered I'd already done two, but never wrote about either of them.  Oops!  Here's a twofer, then.

This post necessarily gives away the answers, so **don't read this if you'd like to solve the problems yourself**.

<!-- more -->


## Problem 16 in Pascal

Pascal was the first language suggested after [the last post][heteroglot:cobol] the last post, and is actually a real programming language for once, so that's pretty nice.

### The math


[Problem 16][]:

> 2<sup>15</sup> = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

> What is the sum of the digits of the number 2<sup>1000</sup>?

If you're curious,​ the actual value of that number is 10,​715,​086,​071,​862,​673,​209,​484,​250,​490,​600,​018,​105,​614,​048,​117,​055,​336,​074,​437,​503,​883,​703,​510,​511,​249,​361,​224,​931,​983,​788,​156,​958,​581,​275,​946,​729,​175,​531,​468,​251,​871,​452,​856,​923,​140,​435,​984,​577,​574,​698,​574,​803,​934,​567,​774,​824,​230,​985,​421,​074,​605,​062,​371,​141,​877,​954,​182,​153,​046,​474,​983,​581,​941,​267,​398,​767,​559,​165,​543,​946,​077,​062,​914,​571,​196,​477,​686,​542,​167,​660,​429,​831,​652,​624,​386,​837,​205,​668,​069,​376 according to the Python CLI.  But Pascal is a more...  traditional language,​ and I don't think it has bignums built in.

This one actually had me stumped for a while, looking for some kind of pattern so I could devise an "easy" way to solve it.  The powers of 2 _mod 9_ (which you get by summing digits repeatedly until only a single digit is left) have an obvious recurring pattern of 1 2 4 8 7 5, but only summing the digits _once_ produces a sequence with no obvious pattern:

    1   2   4   8   16   32   64   128   256   512   1024   2048
    1   2   4   8    7    5   10    11    13     8      7     14

The digit sums keep wavering up and down, seemingly arbitrarily.  I tried a variety of things and none of them worked.  Then I gave up, went googling for a solution, and _still_ didn't find anything.  If there's a shortcut for solving this, I don't know what it is.

So I'll have to do it the hard way: actually compute the number and sum its digits, in a language with fixed-size integers.  I could just use [gmp][libgmp] bindings, but that doesn't seem to be keeping in the spirit of Project Euler.  I might as well do it by hand.


### The code

Here are the things I knew about Pascal, going in.

1. Delphi is actually Pascal, or something.
2. I once used a little open-source IDE, [Dev-C++](http://www.bloodshed.net/devcpp.html), that was written in Pascal.
3. It uses `begin`/`end`.
4. It's kind of on the same level as C, I think.

And so off I went to find out more things.  I don't remember where exactly, since I did this over a year ago now, but Pascal is a common-enough language that I probably got the gist just from Wikipedia.  And now I have to do it again to write this post, oops.

Just as with COBOL, the first thing I want to know isn't so much syntactic differences, but the minimal amount of boilerplate required to have a program.  This turns out to be fairly reasonable:

```pascal
program ProjectEuler16;
begin
    (* your code here *)
end.
```

I can appreciate that.  It's certainly more welcoming than the equivalent empty program in C.  Also, comments in Pascal are delimited by `(* ... *)`!  Wild.

I want to implement a quick and dirty bignum.  A real bignum would probably be in base 2³² or 2⁶⁴, where the number is broken into an array of native-word-sized "digits".  I only care about the sum of the digits in base ten, though, so I'm just going to keep an array of decimal digits the whole time.

So I need to know how to do variables.  In the case of the "main" program block, I need a separate `var` block before the main `begin`/`end`.  (I never got around to figuring out functions, but I _think_ they're structured the same way and can have their own `var` block before the function proper.)  I'll throw in a constant, too.

```pascal
program ProjectEuler16;
const
    digits = 1000;

var
    bignum: packed array[1..digits] of integer;
begin
    (* your code here *)
end.
```

Cool.  I'm glad to see Pascal has adopted Rust's approach of putting the type _last_, so you can actually see at a glance what the variable names are.

(Why am I using 1000 digits, you may wonder?  Well, 10<sup>𝑥</sup> has 𝑥 digits, and 2¹⁰⁰⁰ must be less than 10¹⁰⁰⁰ because 2 is less than 10, so 2¹⁰⁰⁰ cannot have more than 1000 digits.  You could figure out _exactly_ how many easily enough with logarithms, but this array is only a few kilobytes, so I don't care that much.)

The keyword `packed` there indicates that the compiler should cram each element into as few bytes as possible, instead of the default behavior of giving each element its own machine word.  I have no idea why I used it here, since `integer` is already 32-bit.  I guess this does halve the storage space.  But then why did I use `integer` at all for decimal digits, instead of a single-byte type?  What a buffoon.

The way you make a single-byte type is actually super interesting.  Supposedly most implementations already have it built in, but you can just do:

```pascal
type
    byte = 0..255;
```

And you'll get a type that only takes up enough bytes to fit that range.  Also, ranges are built in, if you hadn't noticed.  Cool stuff for a low-level language from _1970_.  What's your excuse, C?

Okay, so, the first thing I want the program to actually do is initialize this bignum to 1, which means all zeroes except for the last digit.  This requires a _loop_, which is pretty chill in Pascal.

```pascal
for digit := 1 to digits do begin
    bignum[digit] := 0;
end;
bignum[1] := 1;
```

I had to declare `digit` as an `integer` in my `var` block, too.  Also, assignment uses `:=`, reserving `=` solely for equality.  I think this is because Pascal derives from ALGOL, which had a more mathematical design.  Odd, then that constants use `=`?  I guess constant declarations are really about asserting equality, not so much about "assigning" anything.  Type declarations use `=`, too.

Notice that although we write numbers with the biggest place first, I'm effectively writing mine little-endian, with the ones digit in the first position in the array.  The advantage is that as I multiply and carry, I'm moving forwards through the array from 1 upwards, and don't have to think about subtracting from the array size to figure out the right place.  In a language with array indices starting from 1, I'm happy to do as little math on indices as possible.

Now I have to actually do the work, i.e., double that number a thousand times.

```pascal
for i := 1 to exponent do begin
    carry := 0;
    for digit := 1 to digits do begin
        carry := carry + bignum[digit] * base;
        bignum[digit] := carry mod number_base;
        carry := carry div number_base;
    end;
end;
```

Nothing shocking here.  The actual work is done in the `carry`.  Double the digit, add the previous carry.  Then the new digit is `carry % 10` and the new carry is `carry // 10`.  This is just long multiplication.

All that's left is to sum the digits and print the answer.

```pascal
n := 0;
for digit := 1 to digits do begin
    n := n + bignum[digit];
end;

writeln(n);
```

This produces 1366, which is correct.  The final program is [016.pas][].

### Impression

Pascal seems like a cute language.  I have a hard time even thinking of it as a systems language, since systems languages tend to be full of punctuation, whereas Pascal makes pretty heavy use of keywords.  It's strongly-typed, it has sets (including bitflags) built in, it has `for` loops over a range, a built-in file type, a polymorphic `writeln`...  does this seriously predate C and share the same problem space?  How on earth did C win out over this?  C, the language whose "library support" requires a separate language bolted on top that copy/pastes other libraries' headers into your code?

Granted, I don't know enough about Pascal from one toy program to fairly compare it to C.  Kind of curious what the story is, though.


## Problem 17 in Inform 7

[Inform 7](http://inform7.com/) is a vaguely English-like language intended to be used to write interactive fiction (i.e. text adventures, like Zork).  I picked it up a year ago for...  writing interactive fiction, and it's certainly a bit obscure, so it seemed appropriate for a heteroglot problem.

### The math

[Problem 17][]:

> If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

> If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?

> **NOTE:** Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.

There's not really a math problem here; it's just a matter of writing an algorithm that can correctly count the letters.

### The code

If you were clever, you might realize that you don't need to actually _generate_ the written-out text.  Nothing in the problem requires you to know that the number 3 is written as "three", for example, you only have to know that the number 3 is written with five letters.  Also, spaces and hyphens don't count, so you don't have to muck about with formatting, either.  And the problem thankfully stops at 1000, which avoids the problem of splitting numbers into groups of a thousand.

But if you were _even more_ clever, you might use Inform 7, for reasons that will become apparent shortly.

A valid Inform 7 program requires only one thing: a room for the player to start in.  Yes, the player.  This is a language for writing games, remember!  The smallest possible program is thus:

```inform7
X is a room.
```

Now, heteroglot has the general rule that a program should do nothing other than print the solution to standard output.  Interactive fiction games tend to be built around a turn cycle, waiting for the player's input and responding.  I don't care about any of that for the sake of this problem, so I'll put my entire solution in a block like this:

```inform7
When play begins:
    [solution here]
    end the story.
```

`when play begins` introduces a block to be run when the game starts, before the prompt is ever shown.  `end the story` ends the game.

Now I'm ready to solve the problem.

#### Cheating

I do love cheating.

```inform7
let count be 0;
repeat with n running from 1 to 1000:
    let letters be "[n in words]";
    repeat with i running from 1 to the number of characters in letters:
        if character number i in letters is in lower case:
            increment count;
say count;
```

The first thing you may notice is that Inform 7, while written sort of like English, still has the same standard constructs if you need them.  So that's nice.  Rather than functions, you have "phrases", and a number of them are built in.  You can also define your own.  This all makes the syntax a little fuzzy, but it's...  interesting to write.  Also, you have to use semicolons _between_ statements, and a period at the end of the last one; and you must indent with tabs.  Sigh.

The second thing you may notice is that I'm cheating.  Inform 7 is designed to resemble English text because its entire _job_ is to produce and parse English text, and so it's only natural that it knows how to spell out numbers.  So the simple expression `"[n in words]"` is all I need here.

(Bracketed blocks inside quotes are a remarkably powerful form of interpolation, computed _on the fly_ whenever the string is evaluated.  That is, you can give an object a description — a property defined at compile time — like `"The clock reads [time of day]."` and it'll do what you mean.  You can also embed conditionals, random choices, or your own custom tokens.  It's pretty slick.)

The only other trick is using `if ... is in lower case` to determine whether a character is actually a letter.  Spaces and hyphens, after all, are not in lower case.

Compile, run, wait about 20 seconds, and:

> 21124

> \*\*\* The End \*\*\*

> Would you like to RESTART, RESTORE a saved game, QUIT or UNDO the last command?

Close!  By using a `when play begins` block, I've even skipped the usual introductory text and the name of the starting room.  But I don't want that ending prompt.

Fixing this is admittedly a little fiddly.  You might look around and discover you can `try quitting the game`, but `try` causes the _player_ to try doing something, and more importantly asks for confirmation first.

I noticed that typing `QUIT` at that last prompt quits _without_ asking first, so I dug into the Standard Rules and discovered that this is done with a rule called the "immediately quit rule".  Rules are a whole huge thing in Inform 7, but all that's important here is that I can invoke the rule with:

```inform7
abide by the immediately quit rule.
```

Which produces:

> 21124  
> [Hit any key to exit.]

Much better.  In fact, the "hit any key" part is from the virtual machine, not my program.  To fix it—  well, hang on, I haven't talked about this at all yet.

#### Compiling and running it

So, compiling Inform 7 is actually a gigantic pain in the ass.

Inform 7 compiles to an older punctuation-heavy language called Inform 6, then compiles Inform 6 to a bytecode format which is run in an implementation of the "Z-machine" VM.  The expected workflow is to write Inform 7 in its IDE, which also has a bunch of fancy features like a generated index of all phrases and types and whatnot (including your own) and a rough map of your world and various other stuff.  I didn't want to use the IDE for this trivial program, so I went to build it myself.

The Inform 6 compiler is open source.  The IDE is open source.  The Z-machine spec is pretty well understood.  The Standard Rules and some Inform 6 glue are readily available.  Great.

The Inform _7_ compiler, `ni`, is closed-source and completely undocumented.  Not great.  It's not closed-source for any particular reason; as far as I can tell, it's just a case of "the code is embarrassing so I haven't released it yet".

To make matters worse, `ni` doesn't just take an input file; it expects a _project_, laid out the way the IDE lays it out, even though Inform 7 programs are almost always a single file.  You see, `ni` is also responsible for generating all the fancy stuff like the phrase index, which it dumps into a specific place in the project.  Also, the IDE layout isn't even confined to a single directory; it creates _two_ sibling directories, `Your Project.inform` and `Your Project.materials`.  This drives me up the fucking wall.

So for the first time ever, I was forced to write [a Makefile](https://github.com/eevee/project-euler/blob/master/heteroglot/Makefile), _just_ for this project.  It creates a temporary directory containing the minimum structure necessary to convince the compiler to run, then runs it based on copying what the IDE reports having done.  It works on my machine!

As for running it, I've been using a terminal Z-machine implementation called `frotz`, which unfortunately has a fancy full-screen interface.  That's why it gives you a "hit any key" prompt: so you can read any final text before actually closing the program.

The heteroglot rules demand printing to stdout and immediately exiting, though.  The solution is simply...  to use `dfrotz` instead.  That's short for "dumb Frotz", and is a similar implementation but with only simple printing to the terminal.  Running `dfrotz 017.z8` does, indeed, print out the answer and then exit.  It does include two leading spaces (part of a left margin it adds by itself), but if COBOL is allowed leading zeroes, I think I can stomach leading spaces.

The final program is [017.ni][].

### Impression

I already knew this language, so I can't give an honest first impression.  It was definitely handy for this particular problem, and just like with [vimscript](https://github.com/eevee/project-euler/blob/master/heteroglot/008.vim), most of the difficulty came in figuring out how to print the answer and nothing else.  (I actually had a ton of extra junk in there trying to skip various rules that print introductory text, and only today realized none of it was necessary.)

If you have any interest in interactive fiction (or...  math problems?), you might want to give it a whirl.  The manual is very thorough and written with non-programmers in mind.  I'm writing a game in it and having a blast, even when I get stuck trying to make it do extremely fancy things.


## Next up

I am actually _not_ accepting language suggestions this time, because I already know exactly what language I want to use.  I think you'll enjoy it.

[heteroglot:cobol]: /blog/2012/09/07/heteroglot-number-15-in-cobol/
[Problem 16]: https://projecteuler.net/problem=16
[libgmp]: http://gmplib.org/
[016.pas]: https://github.com/eevee/project-euler/blob/master/heteroglot/016.pas
[Problem 17]: https://projecteuler.net/problem=17
[017.ni]: https://github.com/eevee/project-euler/blob/master/heteroglot/017.ni
