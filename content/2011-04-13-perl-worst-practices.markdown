title: Perl Worst Practices
date: 2011-04-13 20:15:00
tags: perl
category: reference

I hate to rank my own skill at anything, but if you forced me to, I'd say I'm pretty good at Perl.  I get paid for it, at the very least.  I've been around it a long time, and I know it well enough to tell you in intricate detail why I now use Python, instead.

But this is not that post.  This post is about a particular wart of Perl: that it has a lot of warts.  Large chunks of Perl are antequated, bug-prone, or outright obsolete.  The trouble is that there are no warnings in the interpreter or documentation for many of these things, so a newcomer—or even an old-timer—won't know to avoid such pitfalls until told by someone else.

Such secret knowledge has been documented in bits and pieces in many places, but none of them are complete, and some of them are similarly antequated.  So, here's my list.

<!-- more -->

## Things you absolutely must avoid

Don't do these because "it's quicker" (it's not).  Don't do these because "nobody else will use this code" (your future self will).  Don't do these because "it's a one-time script" (almost all production software started as one-time scripts).  Just do not do them.  At all.  Ever.  Unless you are mst there is no reason to do any of this.  The language has moved on.  There is a better way.

### Forgetting `use strict` or `use warnings`

`strict` disables a lot of PHP-style abuses, like inventing variables out of thin air or soft references.

Perl is an _extremely_ lax language without these pragmas turned on.  Without them, you're virtually guaranteed to run across a mysterious bug within your first dozen lines of code.  I've seen it happen!

You might want to be extra-strict and `use warnings 'FATAL'`, which will make warnings bomb your program.  Or see [common::sense][] for a (slightly insane) example of a custom `warnings` setup.

### `-w`

This is a command-line switch to `perl` for enabling warnings.  It's been deprecated for approximately forever.  It doesn't let you control warnings within your program, it inflicts warnings on libraries you're using that may not have been designed for it (shame on them, but you don't need to hear about their warnings), and it requires specifying outside of your code.  Just use the pragma.

### Two-argument `open()`

**DO NOT** do this:

    open FILEHANDLE, ">filename";  # DO NOT DO THIS I MEAN IT

There are several problems here:

1. `FILEHANDLE` isn't a useful object.  It's not scoped; it's always global.  And you can't pass it around or store it anywhere.  (Okay, you CAN, but you have to do `\*FILEHANDLE` which is just stupid.)
2. You will inevitably at some point try to `open FILEHANDLE, $user_provided_filename;` and then you are in for a world of pain.  The user could stick any of `open()`'s magical squiggles on his filename, possibly opening a pipe or reading `/etc/passwd`.
3. You can't specify the encoding for the file.
4. You can't open filenames that begin with, say, `>`.  Yeah, yeah, I know.

Instead, do this:

    open my $fh, '>', "filename" or die "Couldn't open file: $!";

`$fh` is a regular old scalar now, and will go away (thus closing the file) at the end of the block.  You can pass it around, store it, or whatever you want.  And the filename isn't parsed for any magic squiggles, so it's safe from injection.

There is zero reason to use two-argument `open()`.  (There's even less reason to use one-argument `open()`, but I hope you're not even aware that exists.)  Just don't.  Consider writing a wrapper for it that explodes if it only gets two arguments.

You might think the `or die` is pretty noisy.  You are correct!  That's why you should either `use Fatal`, `use autodie`, or `use warnings qw(FATAL closed)`.

### `goto LABEL`

Spaghetti code ahoy, especially since Perl's `goto` is even more lax than C's.  You almost certainly just want to be breaking out of an outer loop with `next LABEL` or `last LABEL`, which are more sane and well-defined.

Don't confuse this with `goto &sub`, which can be used for tail-call optimization and delegation.

### `eval ""`

Really?  Knock that off.

### `eval {}`

This is Perl's `try` block.  Trouble is, it's almost completely useless.  The magical exception variable `$@` is overwritten too easily, and you can potentially lose your exception in all but the most trivial error handlers.  You can read all about these problems in [Try::Tiny][]'s documentation, while you're learning to use Try::Tiny instead of `eval`.

### Backtics/`qx` or `system()` with one argument

These have a similar problem as two-argument `open()`: you _will_ try to put a variable in them and you _will_ be exploited when that variable contains shell metacharacters.

Split your call into words instead, and you avoid the shell entirely.  Instead of backtics, use `open my $pipe, '-|', 'command', 'arg1', 'arg2';`.  Instead of passing a string to `system()`, use `system 'command', 'arg1', 'arg2';`.  If you need something more complex, read up on the options in `perldoc -f open`.

### `foreach`

`for` works just as well.  Seeing `foreach` in code is a very good indicator that someone either learned Perl ten years ago or ten minutes ago.

### C-style `for`

Perl has a ridiculous number of shortcuts for looping over lists of things.  Any loop that's too complex for a Perl-style `for` is too complex for a C-style `for`.  Just write a `while`.

### `chop()`

You almost certainly meant `chomp()`.  If you didn't, use a regex; you can be more specific about what you're chopping, and your intention will be clearer.

### `$_` outside microblocks

That's a term I just invented to refer to the little blocks used by `map`, `grep`, much of `List::Util`, etc.  Using `$_` is virtually required for these, and any alternative would be far harder to read.  But they localize `$_` correctly, and they're short (or _should be_), so nothing else is likely to clobber `$_`.  But for the love of god don't do this:

    for (@things) {
        tr/abc/xyz/;
        s/def/ghi/;
        print;
    }

This looks like complete nonsense at a glance, until you remember, _oh yeah that default variable thing_.

### `map` and `grep` without a microblock

I cannot stand seeing this:

    map $_ * 2, @numbers;

The way this works for _any other function_ is to pass it twice the value of `$_`, followed by the contents of `@numbers`.  The way this works _only for `map` and `grep`_ is to apply the expression `$_ * 2` to the contents of `@numbers`.

The distinction is subtle and buried somewhere in the interpreter's guts.  Don't do this.  It makes no sense at all to write code in a procedural language with no delimiters at all but have it act as an anonymous function.  Just use the damn block syntax:

    map { $_ * 2 } @numbers;

There's a slight disadvantage in that Perl's parser will get confused if you accidentally include a comma after the block, but I think the clarity is worth the risk.  If nothing else, this syntax isn't special to Perl builtins; you can write your own functions that do it.

### `$|`

That's the "buffered I/O" variable, if you weren't aware.  Setting it to a true value disables buffering for the currently-selected filehandle.  Don't do this:

    $| = 1;

And if you do this then you should probably be stopping to wonder if there's any easier way:

    select((select($fh), $| = 1)[0]);

What you really want is:

    use IO::Handle;
    $fh->autoflush(1);

Similar advice goes for all of the other filehandle-oriented magic variables, though they're far less frequently used.

And while I'm at it...

### `select`

This is a global operation that affects the entire program.  You will forget to reset it, or something will die and it won't get reset, or whatever.  That's bad.  I have seen it happen.  Instead of this:

    my $orig_stdout = select $fh;
    print "this goes to my file";
    do_something_that_prints_to_stdout();
    select $orig_stdout;

Try this:

    {
        local *STDOUT;
        open STDOUT, '>&', $fh;
        print "this goes to my file";
        do_something_that_prints_to_stdout();
    }

Looks slightly more arcane, but all it does is localize `STDOUT` (so it'll be dynamically-scoped to a new value, and automatically restored at the end of the block) and re-open it to your filehandle.  Even if the function you call dies, `STDOUT` will be restored.

### Non-trivial, implicit return

In Perl, the last statement executed in a function is the return value, if `return` isn't used.  Some programmers rely on this to do their returning for them.  Those programmers are insane.

You might say that this is perfectly understandable:

    sub foo {
        1;
    }

And you are correct!  I do this for constant functions all the time.  But this is not so understandable:

    sub foo {
        my $a = do_something();
        my $b = do_something_else();
        $b;
    }

Wait, what?  Is this function supposed to return or not?  Is that a typo?  What's the documentation say?  Good grief.  And then there's this:

    sub foo {
        if ($bar) {
            1;
        }
        else {
            2;
        }
    }

Great, now I have to trawl your dumb function for any statement that might be last instead of just scanning for `return`.

By the way, don't `return undef` if that's not _exactly_ what you mean.  When called in list context, your function will return a one-element list (containing only `undef`), which will evaluate to true.

### `new Object`

This is called "indirect method syntax".  It's not because `new` is a magical operator in Perl, like in C++.  Oh, no, this is much more insidious.  You see, someone had the harebrained idea that these two call styles should be equivalent:

    foo $bar @args;
    $bar->foo(@args);

I hope it's immediately obvious why this is confusing at best.  Just use `->new()`.

## Things you should not do without an extremely good reason

No, whatever you just thought is **not** a good enough reason.  If you don't know Perl intimately enough that you're already aware of all of the below and their pitfalls, you are probably going to spend a lot of time flailing around re-inventing someone else's solutions.  

### Rolling your own classes

The guts of Perl's OO are messy, bug-prone, and not much like any other language.  Unless you know _why_ you might want to bless a coderef, don't even touch `bless`.  Use [Moose][] instead.  It's not hard, there's not much overhead, and you will not regret it.

### `wantarray`

I can't count the number of times I've seen this at the end of a function:

    return wantarray ? @things : \@things;

Why are you doing this?  Just return the damn list.  If I want an arrayref, I'll make one.  The worst part is seeing such a function used in scalar context a lot, then trying to use it yourself in the wrong context:

    my $var_a = list_of_things();
    my $var_b = list_of_things();

    # Well cool I'll just refactor this:
    my %vars = (
        a => list_of_things(),
        b => list_of_things(),
    );

Whoops!  Now your entire list of return values has been interpolated into my hash.  This is kind of obscure, too, and will probably be less than fun to debug.  Just don't make assumptions about what your caller wants.

One example where this is kind of okay is DBIx::Class; a lot of methods return a list of result rows in list context, but an expression object in scalar context that will let you keep chaining methods.  (But even this is extremely dubious; I still can't use an expression object in another list easily, and it's not exactly difficult to just call `all` on the result.)

A note on returning lists: return values are _copied_.  So if your function can return a very big list, you might want to return an arrayref instead, or Perl will spend a lot of time copying all those values from the function to the caller.  (I prefer to just return a list whenever possible, but 5.14's better treatment of refs might make this perspective obsolete.)

### Disabling `strict refs`

I see this done sometimes to make walking the symbol table easier.  Ignoring for the moment that you rarely need to walk the symbol table, you're even more unlikely to need `strict refs` off to do it:

    my $method = "whatever";
    *{"Foo::Bar::$method"} = sub { 1 };  # Violates 'strict refs'

    # Read up on perldoc perlsym, and maybe do this:
    $Foo::Bar::{$method} = sub { 1 };

If you have no idea what's going on here, don't ask.

### Assigning to `@_`

    sub foo {
        $_[0] = 3;
    }

    my $x = 5;
    print $x;  # 5
    foo($x);
    print $x;  # 3

I suspect this is another case of seeing something C++ can do and wanting very badly to emulate it.

This is one of very few cases in Perl where variables are _aliased_.  It's not a very nice thing to do to your caller; just return the new value.  If you're changing something really complex, you probably ought to be using a class with a method anyway.

I was tempted to put this in the "never ever" list, but I have seen one single time when this feature was genuinely useful.  And I will take it to the grave.

## Beginner mistakes

These aren't really dangerous or particularly hard to understand, but they're definitely not the nicest way to do things.  You shouldn't ever need to do them, but they aren't horrifying enough to go in the first set.

### `&foo()`

This is ancient syntax that hasn't been necessary since the dawn of time.  Just use `foo()`.  You only need the `&` when taking a reference or using the LISPy form of `goto`.

### `for my $line (<$fh>)`

This will read the entire file into a list, then iterate over it.  You probably wanted `while (my $line = <$fh>)`.

### `my $entire_file = join '', <$fh>;`

Woefully inefficient.  Use File::Slurp.

### `@array[$i]`

This takes a slice and returns a list containing one element.  It'll still work in most cases, but you'll be very surprised when it doesn't.  Use `$array[$i]`.

### `print $fh $data`

This is difficult to tell apart from `print $fh, $data` at a glance, and the two are very different.  The idiomatic way to clarify this is `print {$fh} $data`.

---

I could easily double the size of this list, but this is a good start.  Perl has so many potholes and so much cruft that you might as well assume anything built in is to be avoided.

I might update this in the future, or I might compile a similar document for Python instead.  Depends on the reaction.

[common::sense]: http://search.cpan.org/perldoc?common::sense
[Moose]: http://search.cpan.org/perldoc?Moose
[Try::Tiny]: http://search.cpan.org/perldoc?Try::Tiny
