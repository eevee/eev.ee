title: The curious case of the switch statement
date: 2016-09-18 21:25
category: blog
tags: tech, plt

Sometimes, I lie awake at night thinking about programming languages.

That's all the intro I've got here, sorry.  I felt like writing about the `switch` statement for some reason.

<!-- more -->


## Some history

### 1958: ALGOL 58

The earliest incarnation I can find is in ALGOL 58.  The [original description of ALGOL 58](http://www.softwarepreservation.org/projects/ALGOL/report/Algol58_preliminary_report_CACM.pdf) is a fascinating read — it's written like a math paper, with literal text in italics and heavy use of subscripts.  Character classes are even named by Greek letters, with λ representing letters and so on.  The example program at the end is completely incomprehensible, with almost every variable being a single letter and labels forming their own entire column on the left side.  I guess that last bit came from FORTRAN.

I'm not _surprised_ by this, what with ALGOL's being originally conceived as a universal way to express mathematical algorithms — "algebraic" is right in the name, after all — but seeing it in practice is a little surreal.  I can't imagine a programming language being described this way nowadays.

ALGOL 58's version of switch is a little different from the one we've all come to know and love.  It's not a statement at all; it's a declaration.  Switches are their own _kind of thing_, in the same way that variables and labels are different kinds of thing.  (Though, curiously, it seems you can return a label — but not a switch! — from a procedure in ALGOL 58.)

```algol
switch I := (D₁, D₂, ..., Dₙ)
```

A switch is used with the `go to` statement, along with a subscript indicating which `Dᵢ` to select.  `go to I[2]` would thus be equivalent to `go to D₂`, except that the subscript could be computed at runtime.

Each `Dᵢ` is a "designational expression", which is a funny way of saying "a thing you can use with `go to`" — either a label or another switch-plus-subscript.

This very first appearance of `switch` was a very simple form of computed goto: a list of places to jump to that you could index at runtime.

Please also enjoy the two example uses of the `go to` statement from the original report.

> _go to_ HADES
>
> _go to_ exit [(i ↑ 2 ↓ -j ↑ 2 ↓ +I)/2], where exit refers to the declaration  
> _switch_ exit :=(D₁, D₂, ~~~, Dₙ)


### 1960: ALGOL 60

ALGOL 58 was soon superseded by ALGOL 60, which has a [slightly more modern-looking description](http://www.masswerk.at/algol60/report.htm).  The basic idea behind `switch` as a declaration stayed the same, but it learned a few new tricks.

Inline `if ... then ... else ...` became a form of arithmetic expression, meaning it could be used as a subscript, even on a switch.  Along the same lines, anywhere a "designational expression" was expected — including within a `switch` declaration or as the argument to `go to` — an inline `if` could be substituted.  The above-linked report includes these examples:

> **switch** S:=S1,S2,Q[m], **if** v>-5 **then** S3 **else** S4
>
> **switch** Q:=p1,w

It also clarifies something I wasn't sure about from the ALGOL 58 report: the expressions in a switch are evaluated _when the jump is made_, not when the switch is declared!

Finally, both switches and individual labels could be passed around as arguments.  Don't see that much any more.


### 1963: CPL

CPL — originally Cambridge Programming Language, then later Combined Programming Language when London joined in — was heavily inspired by ALGOL 60, but sought to expand beyond mathematical algorithms and into more general programming.  It was described somewhat informally by [a paper in 1963](http://comjnl.oxfordjournals.org/content/6/2/134.full.pdf), but never saw much widespread use.

CPL dropped switches entirely, in favor of having labels themselves be a kind of storable variable.  The paper gives an example, where "Switch" is the name of a variable and _not_ a keyword:

> **label** _Switch_ = _x_ < 0 → _L1_, _L2_
>
> **go to** _Switch_

(Here, `→,` is effectively the ternary operator, the equivalent to C's `?:`.  `a → b, c` means `b` if `a` is true, `c` otherwise.)

Since the first statement is a regular assignment, the right-hand side is evaluated immediately.  The paper doesn't delve very deeply into this, but since labels were first-class values, you could presumably choose a label using whatever logic you wanted and then jump to it.  Arrays could contain any type, too, so I assume the direct equivalent to ALGOL 60's `switch` was merely an array of labels.  Certainly much more flexible.  If you're cringing right now, don't worry — you can do this in C, too!  Keep readin'.

CPL also allowed referring to (and thus jumping to) a label in the middle of a different scope, as long as the label was prefixed with the containing block's label, as `BLOCK at LABEL`.  How convenient!


### 1966: ALGOL W

[ALGOL W](https://web.archive.org/web/20121119115827/http://www.jampan.co.nz/~glyn/algolw.pdf) was a big step towards something recognizable as a modern language.  It brought us such revolutionary innovations as `null`, a value that crashes your program.

It also dropped the switch kind in favor of a new compound statement, `case`, which was sort of like the older `switch` without the labels.  `case` looked like this:

```algol
case X of begin
    WRITE("X is 1");
    WRITE("X is 2");
    WRITE("X is 3")
end
```

Yes, `case` was a regular block, and the expression indicated _which one of its statements to run_.  Any individual statement could of course be a bare `begin ... end` block wrapping multiple sub-statements, so a `case` wasn't limited to only executing one literal line of code.  Still, that seems like it would be impossible to read with more than two or three cases.

Similar to ALGOL 60's inline `if ... else ...`, ALGOL W had an inline `case ... of`:

```algol
case EXPR of (A, B, C, ...)
```

This evaluated to one of `A`, `B`, etc., as determined by the value of `EXPR`.  In most modern languages, you'd do this by indexing an array literal.


### 1967: BCPL

CPL was a "large" language for the time, which is a strange thing to say when the paper describing it is the shortest I've read today.  I can't very well look at it through 1963 eyes, so I'll take Wikipedia's word that it was too big to be fully implemented until a good few years later.

In the meantime, [someone else](https://en.wikipedia.org/wiki/Martin_Richards_%28computer_scientist%29) at Cambridge thought there were some good ideas in there, so he lopped off all the parts that were hard to implement and called the result "BCPL", for "Bootstrap CPL" (as the original compiler was written in BCPL) and later "Basic CPL".

BCPL was the origin of a few interesting ideas we now take for granted: it was the first language to delimit blocks with curly braces (or the `$(` and `$)` digraphs), and possibly the first to compile to an intermediate object code before compiling to machine code (which made porting much easier, and is roughly how LLVM and GCC work).  It also treated everything as integers and had no type-checking, so, make of that what you will.

As far as I can tell, BCPL was also the origin of the modern `switch` statement.  [The BCPL reference manual](https://www.bell-labs.com/usr/dmr/www/bcpl.pdf) describes the following block:

```bcpl
switchon EXPR into {
    ...
    ...
    case CONST:
    ...
    ...
    default:
    ...
    ...
}
```

Boy, doesn't _that_ look familiar!  It works exactly as you'd expect, and the manual even mentions that the exact compilation may vary depending on the number of cases.  I don't think `break` worked in `switchon`, but since the behavior is described solely as a jump and nothing else, you'd have needed _something_ to prevent fallthrough.

Curiously, BCPL _also_ had label-type variables, so it seems that `switchon` was a novel addition.  BCPL was first implemented only a year after ALGOL W arrived with the `case` statement, but I can't find any further details on what inspired this particular design.


### 1969: B

Now we're nearing the history that most computer people are familiar with.  B confused the next three generations' worth of budding programmers by changing assignment from `:=` to `=`, but made up for it by introducing compound assignment operators, but then ruined it again by inventing post/pre-increment/decrement.

The [B manual](https://www.bell-labs.com/usr/dmr/www/kbman.pdf) describes the `switch` statement as "the most complicated statement in B".  The general syntax is `switch EXPR STATEMENT` — the statement doesn't even have to be a block, but _may_ be.  I believe it would look like this:

```b
switch X {
    case 1;
    printf("X is 1*n");
    case 2;
    printf("X is 2 (or 1)*n");
    case 3;
    printf("X is 3 (or 2, or 1)*n");
}
```

Most notably, `case` seems to have become a statement all its own, rather than a funny kind of label.  At least, I think so.  The manual wasn't scanned particularly well, and the punctuation after `case` is underlined, so it might be a semicolon _or_ a colon with a bit of lint under it.

In a step _backwards_ from BCPL, I see no mention of a `default` label; if none of the cases match, the entire block is just skipped.

Again, since these are just jumps and `break` hasn't been overloaded to work here yet (in fact, it didn't seem to exist in the language at all!), there's unavoidable fallthrough.  The manual contains an example program that uses a `switch`, and every case ends with an explicit `goto` out of the block.

Oh, and B used `*` for escape characters in strings.  Imagine what might've been.


### 1972: C

And then we had C and that's the end of the story.  I don't own a copy of The C Programming Language First Edition (gasp!), but several people have confirmed to me that even the original version of C had the modern `switch` statement, complete with the `break` overload.


## The modern switch statement

As we've seen, the canonical `switch` statement has had basically the same form for 49 years.  The special `case` labels are based on syntax derived directly from fixed-layout FORTRAN on punchcards in 1957, several months before my father was born.

```c
switch (EXPR) {
    case 1:
        ...
        break;
    case 2:
        ...
        break;
    case 3:
        ...
        break;
    default:
        ...
}
```

I hate it.

Okay, "hate" is a strong word.  I'm not a huge fan.  From a language design standpoint, it sticks out like a sore thumb.  I've never seen a particularly pleasing design for it, and it baffles me that we still have dedicated syntax for this weird thing — and frequent requests to add it to languages that lack it.


### Some objections

**It's not like anything else in the language.**  Consider how almost every other kind of block works, especially in languages like C where a block and a single statement are interchangeable.

```c
stmt ... {
    ...;
    ...;
}
```

`if`, `do`, `while`, `for`, even function definitions all work pretty much the same way: the block is just _some stuff_, and the exact contents are irrelevant.  The semantics are always of the form: something happens, then the block runs, then something else happens.

`switch` changes the rules.  The block introduced by a `switch` is allowed to use special syntax that can't appear anywhere else.  A programmer sprinkles this unique syntax — which sorta-kinda-half slices the block into multiple blocks — throughout, and the `switch` header inspects the block's contents.  It's invasive in a way nothing else is.

**It splits an expression in half.**  _Semantically_, a `switch` asks: which of these values is _equal to_ this expression?  That is, for some expression `x` and a set of values `a`, `b`, `c`, ..., which of `x == a`, `x == b`, `x == c`, ... is true?

Those comparisons are lost in a `switch`, obscured by a construct designed to obscure them.  This is C, remember, the language that makes you explicitly write out all the parts of a `for`, yet it has a statement whose sole purpose is to hide some `==` from you.  That's weird!

**Overloading `break` is clumsy.**  Granted, C overloads just about every keyword it has; `static` alone has at least thirteen meanings.

Normally, `break` means to immediately jump to the end of a looping block _and ignore its loop condition_.  That distinguishes it from `continue`.  A `switch` is not a loop.

This _would_ make perfect sense if you were allowed to `break` out of any arbitrary block.  Perl 5, for example, has roughly equivalent `next` and `last` statements that you can use even inside bare blocks (though, curiously, not inside an `if`).  If Perl 5 had a `switch`, `last` should sensibly jump out of it, since that's the default behavior.  In C, this is a special case...  to fix a problem that shouldn't exist in the first place:

**Fallthrough by default is a horrible idea.**  The vast majority of the time, you don't want fallthrough.  So why is fallthrough _the default_, and the common case needs opting into?

Yes, I know `switch` is fundamentally just a jump.  But it's a jump to a thing that looks like a label yet has a non-opaque value in it...  unless such a label doesn't exist, in which case it's a jump to a label with a reserved name...  unless that doesn't exist either, in which case it's a jump past the end of the block.

Oh!  A jump past the end of the block.  `switch` can already do that!  Why not do it automatically after each case?

"It's so useful for parsers!" I hear you cry.  Hang on!  This behavior _wouldn't even affect_ 99% of cases that want fallthrough.  Consider this tiny tokenizer in a hypothetical world where `break` isn't necessary:

```c
switch (ch) {
    case ' ':
    case '\t':
    case '\n':
        tokentype = WHITESPACE;

    case '(':
        tokentype = OPENPAREN;

    ...
}
```

This would still work exactly as you want.  When `ch` be a space, control would jump to `tokentype = WHITESPACE;`.  Why?  Because labels can only mark a statement, _not other labels_ — and `case` is a label, not a statement!  Jumping to a label always means jumping to the next statement that appears after it.  Effectively, that assignment has three labels.

How would you create an empty case, then?  The same way you create any other empty case: a lone semicolon.

**It's not really all that useful.**  The C-style switch can only match one thing at a time.  If you want to match multiple literals, you can use multiple `case`s.  That's all you get.

It's handy if you're writing a parser, I suppose.  By hand.  Via recursive-descent.  In C.  In 1972.

It might also be useful for dealing with really big `enum`s that indicate a lot of different behavior.

Offhand, I can't think of anything else.  I sympathize with the frustrations of people who reflexively want to reach for it in a language that doesn't have it, but I find it hard to believe that it's the best tool for the job very often.

It's not even useful as an optimization any more; I'm pretty sure our compilers are plenty smart enough by now to recognize an `if` tree and turn it into a jump table or binary search or whatever.  It's one of those things that _feels_ like it'll make a program faster, but almost certainly won't make any difference whatsoever.

**It spread.**  A few language designers in the 90s made a point of inheriting all of C's mistakes: nulls, bitwise operators with nonsense precedence, C-style `for` loops, and of course the `switch` statement.

I'm looking at you, Java and JavaScript.

What's particularly curious is that neither language has `goto` — so why does either language need special computed-jump syntax?  I've seen a `switch` in JavaScript maybe once.

Also, just like C, both languages have had preposterous amounts of effort put into their compilation.  They also both have better "string" primitives than C and regexes built in, making `switch` not nearly as useful for writing parsers; JavaScript doesn't even _have_ `enum`s, and Java only got them fairly recently.

### Potentially fixing it

None of those are intended as huge complaints, and I'm not proposing we start a petition to remove `switch` from the next version of C or anything.  I merely object...  aesthetically.  (And if we were really going to change C to match my aesthetic preferences, we'd start with something much more important, such as ditching the braces.)

People occasionally ask for it in Python, and that gets me thinking about how it might be made to fit there.  Python doesn't have labels, so presumably this would have entire blocks.

```python
switch x:
    case 1:
        print("x is 1")
    case 2:
        print("x is 2")
    default:
        print("dunno")
```

The double indentation here is awful.  I also don't much like the nebulous scope inside `switch`.  What _is_ that?  Can anything other than a `case` block go there?  Every other kind of block in Python can contain completely arbitrary code, so this would be like nothing else in the language.

Okay, so let's try outdenting the cases, like a `try` with multiple `except` clauses.

```python
switch x:
case 1:
    print("x is 1")
case 2:
    print("x is 2")
default:
    print("dunno")
```

This is more consistent with the rest of the language, but now the block immediately following `switch` is empty, which is disallowed everywhere else.  Maybe the default case could go there?

```python
switch x:
    print("dunno")
case 1:
    print("x is 1")
case 2:
    print("x is 2")
```

I could kind of get behind this, but it's backwards from how most people think about `switch` (the default case is virtually always written last) as well as backwards from `elif` and `except`, the other two kinds of block that can be stacked this way.

A bigger problem is fallthrough — these are now distinct blocks, not labels, so my previous argument doesn't apply.  A couple languages have the convention of using `continue` to mean explicit fallthrough, which would give us:

```python
switch x:
    print("dunno")
case 1:
    print("x is 1")
case 2:
    print("x is 2")
case 3:
    continue
case 4:
    continue
case 5:
    print("x is 3, 4, or 5")
```

If the goal here was to save typing and/or vertical space, I don't think we're succeeding.

Alternatively, a completely empty `case` block could be treated as meaning fallthrough, and a no-op block could use `pass`.  That would leave us with empty blocks again, though.

Now I'm stuck.  I only had so much syntax to work with in the first place, and it doesn't fit the weird expectations of `switch`.  Which is probably why Python doesn't have a `switch` block.

Here's another question: what order is the comparison done in?  That is, given `switch s` and `case c`, do we check `s == c` or `c == s`?  You might argue the former because `s` appears first, and I wouldn't disagree, but that's not a particularly solid reason.  And what if you wanted it the other way?  It _shouldn't_ matter, but it _can_, because Python has operator overloading.


## Alternatives

A few languages have put interesting spins on `switch`, and they probably have better ideas than I do.  Here are some I happen to know about.

I note that not a single one of these alternatives has default fallthrough.

### Bourne shell

```bash
case $x in
1)
    echo 'x is 1'
    ;;
2)
    echo 'x is 2'
    ;;
3|4|5)
    echo 'x is 3, 4, or 5'
    ;;
*)
    echo 'dunno'
    ;;
esac
```

The syntax is totally weird, but perhaps no more weird than anything else in shell.

I believe each case _must_ have a terminator, so there's no risk of accidental fallthrough.  The use of `|` to separate multiple patterns takes care of the multiple-value case.

`*` isn't a special symbol meaning "default"; each case is actually a _pattern_, so the `*` is a wildcard that will match anything not matched thusfar.  I approve.


### Visual Basic

This is .NET, but I believe it's been the same since before then.

```vb
Select Case x
    Case 1
        Debug.WriteLine("x is 1")
    Case 2
        Debug.WriteLine("x is 2")
    Case 3 To 5
        Debug.WriteLine("x is 3, 4, or 5")
    Case Else
        Debug.WriteLine("dunno")
End Select
```

Leaving aside Visual Basic's insistence on Writing Everything In Title Case, wow, this is weird.

The case expressions have their own subsyntax that I don't think exists anywhere else in the language.  Each one is a comma-separated list of one or more expressions, `a To b` range expressions, or `Is <= expression` comparison thing.  That last one is extra weird, especially since the `Is` is optional, so you can just write `Case > 12`.  It's convenient, sure, but what a strange thing to implement solely for one kind of block.

`Case Else` is probably the worst way to spell that.  And it looks like the `Case` after `Select` is optional?  What is even going on here.


### Ruby

Ruby has a [`case` statement](http://ruby-doc.org/docs/keywords/1.9/Object.html#method-i-case), or maybe it's a method, who can even tell.

```ruby
case x
when 1
    puts "x is 1"
when 2
    puts "x is 2"
when 3, 4, 5
    puts "x is 3, 4, or 5"
else
    puts "dunno"
end
```

I heartily approve of the use of `else` here.

`when` has only slightly special syntax; listing multiple values separated by commas allows matching against any of them.  You can do some other tricks, though, because Ruby doesn't actually test with normal equality; it uses the terribly-named `===` operator, which is a slightly fuzzy kind of matching deemed to be helpful sometimes.

For example, the last `when` above could be written:

```ruby
when 3..5
    puts "x is 3, 4, or 5"
```

The `..` operator constructs a `Range`, and `Range` implements handwave-equality by checking for inclusion, as well.

This seems a _little_ hokey to me — what if you want to `case` on a `Range`? — but I can't find an exhaustive list of every non-equality use of `===` in core Ruby.  Maybe it works out okay in practice.


## Perl 6

Perl 5, historically, did not have a `switch` statement.  Perl 6, in its quest to include literally every single language feature ever conceived, sought to remedy this.

As [the documentation explains](https://docs.perl6.org/language/control#given),

> The `given` statement is Perl 6's topicalizing keyword in a similar way that `switch` topicalizes in languages such as C.

Yes, exactly.

Perl 6's answer to `switch` is composed of three parts.

`given EXPR { ... }` assigns `EXPR` to `$_`.  You might know `$_` from Perl 5, where it's the "default" variable in a number of cases.  In Perl 6, it acts much the same way, except that it became _much more defaultier_.  For example, you can do a method call without an invocant: `.foo` is equivalent to `$_.foo`.

`when EXPR { ... }` performs a "smart match" of `$_` against `EXPR` using the `~~` operator.  As in Ruby, the precise semantics vary, and are about what you'd expect except when they're not.  If the match succeeds, the block runs, and then control breaks out of the containing block.  If the match fails, nothing happens.

`default { ... }` runs a block and then breaks out of the containing block.

Used together, you get:

```perl6
given $x {
    when 1 { say "x is 1" }
    when 2 { say "x is 2" }
    when 3 | 4 | 5 { say "x is 3, 4, or 5" }
    default { say "dunno" }
}
```

The magical thing about this is that none of these parts are _required_ to be used together.  A `when` or `default` block can appear _anywhere_, and `when` will merrily match against whatever happens to be in `$_`.  Any arbitrary code can appear inside a `given`.  Even that `3 | 4 | 5` thing?  That's not special `when`-only syntax; that's a [junction](https://docs.perl6.org/type/Junction), a first-class type of value that is all three numbers simultaneously.  Perl 6 is truly the realization of Perl 5's mission: to be startlingly consistent, and also just plain startling.

If you need more complex conditions, Perl 6 has a kind of implicit lambda thing when you write an expression containing `*` as an atom.  I don't remember exactly how it works, but you can write `when * > 12`.

Fallthrough is possible, too: a `proceed` statement will immediately leave a `when` or `default` block and continue on after the block, rather than leaving the enclosing block.  It's only allowed inside those two blocks, alas.


## Perl 5

Not to be outdone by...  itself?, Perl 5 has _two_ switch statements.

The first is a module in the standard library, [`Switch`](http://perldoc.perl.org/5.8.8/Switch.html).  Much like Perl 6's smartmatch, it hardcodes a [number of different comparisons](http://perldoc.perl.org/5.8.8/Switch.html#BACKGROUND) depending on the shapes of the operands — including automatically calling functions and considering it a match if the function returns true.  Otherwise, it looks fairly similar to the C construct:

```perl
switch ($x) {
    case 1 { say "x is 1" }
    case 2 { say "x is 2" }
    case [3..5] { say "x is 3, 4, or 5" }
    else { say "dunno" }
}
```

The `[3..5]` is the regular Perl range operator `..`, inside a regular Perl arrayref.  One of the hardcoded comparisons is that if one side is an arrayref and the other is a scalar, `case` tests for array containment.

Since this isn't an actual language feature and is implemented in a module...  you don't want to know how it works.  Really.  Don't ask.  (It rewrites your source code when you import it.)

The native equivalent came with Perl 5.10, the first of the regular Perl 5 releases.  You have to opt into it by asking for a Perl version of 5.10 or later — `use v5.20;` or similar — and then you have pretty much the same `given`, `when`, and `default` as Perl 6.  Perl 5 even has smartmatch.

It appears that all three blocks, as well as smartmatch itself, were later marked "experimental" and produce warnings when you try to use them.  I've heard quiet grumblings about smartmatch's unpredictability since it was first added to Perl 5.10, which is why Ruby's similar thing gave me pause.  Seriously, y'all, just add an `in` operator; it'll solve most of this problem.


## Rust

Rust has a `match` block with its own sub-syntax:

```rust
match x {
    1 => println!("x is 1"),
    2 => println!("x is 2"),
    3 | 4 | 5 => println!("x is 3, 4, or 5"),
    _ => println!("dunno"),
}
```

Like most block constructs in Rust, `match` can be used as an expression as well.  Each statement can likewise be a braced block instead of a single statement.

The stuff on the left side of the `=>` is a [_pattern_](https://doc.rust-lang.org/book/patterns.html), a special syntax with a few bells and whistles.  Matching against any of several values with `|` is one, but you can also give a range with `...`, do destructuring assignment, express more complex conditions, and...  some other stuff.

A really nice thing here is that `_` isn't special-cased to mean "default"; it's only "destructuring" to a single variable, which can't possibly fail.  (The name `_` _is_ special in the language overall, in that Rust will never create a variable named `_`, but this isn't unique to patterns; you can use `_` in other forms of destructuring to mean "I don't actually need this part".)

My favorite thing about Rust's `match` is that it forces the matching to be _exhaustive_ — every possible value of the expression _must_ match one of the patterns you give.  If you try to match an `enum` but forget one of the possible values, your code will not compile.

My least favorite thing is the sprinkle of commas down the right side, which is a travesty.


### And others

A lot of languages have `switch` statements, but most of them are fairly similar and I'm not going to go through them all!  I'm sure plenty of commenters will mention their favorites.

In particular, the functional programming sphere makes very heavy use of pattern matching, often much more powerfully than Rust.  I believe Ruby's `case` came from Pascal, the Betamax to C's VHS, so it's a glimpse at what we could've had.


## Duff's device

Finally, I can't very well talk about `switch` without mentioning Duff's device, the greatest argument against C's `switch` syntax.  If you haven't seen it before, have fun unraveling this.

```c
send(to, from, count)
register short *to, *from;
register count;
{
    register n = (count + 7) / 8;
    switch (count % 8) {
    case 0: do { *to = *from++;
    case 7:      *to = *from++;
    case 6:      *to = *from++;
    case 5:      *to = *from++;
    case 4:      *to = *from++;
    case 3:      *to = *from++;
    case 2:      *to = *from++;
    case 1:      *to = *from++;
            } while (--n > 0);
    }
}
```
