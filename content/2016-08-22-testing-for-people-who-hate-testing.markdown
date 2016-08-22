title: Testing, for people who hate testing
date: 2016-08-22 08:49
category: blog
tags: tech

I _love_ having tests.

I _hate_ writing them.

It's tedious.  It's boring.  It's hard, sometimes harder than writing the code.  Worst of all, it doesn't feel like it accomplishes anything.

So I usually don't do it.  I know, I know.  I _should_ do it.  I should also get more exercise and eat more vegetables.

The funny thing is, the only time I see anyone really praise the benefits of testing is when someone who's _really into_ testing extols the virtues of test-driven development.  To me, that's like trying to get me to eat my veggies by telling me how great veganism is.  If I don't want to do it at all, trying to sell me on an entire lifestyle is not going to work.  I need something a little more practical, like "make smoothies" or "technically, chips are a vegetable".

Here's the best way I've found to make test smoothies.  I'll even deliberately avoid any testing jargon, since [no one can agree on what any of it means anyway]({filename}2016-07-26-the-hardest-problem-in-computer-science.markdown).

<!-- more -->


## Hating testing less

### Love your test harness

Your test harness is the framework that finds your tests, runs your tests, and (in theory) helps you write tests.

If you hate your test harness, you will never enjoy writing tests.  It'll always be a slog, and you'll avoid it whenever you can.  Shop around and see if you can find something more palatable.

For example, Python's standard solution is the stdlib [`unittest` module](https://docs.python.org/3/library/unittest.html).  It's a Java-inspired monstrosity that has you write nonsense like this:

```python
import unittest

from mymodule import whatever

class TestWhatever(unittest.TestCase):
    def test_whatever(self):
        self.assertIn(whatever(), {1, 2, 3})
```

It drives me up the wall that half of this trivial test is weird boilerplate.  The class itself is [meaningless]({filename}2013-03-03-the-controller-pattern-is-awful-and-other-oo-heresy.markdown), and the thing I really want to test is obscured behind one of several dozen `assert*` methods.

These are minor gripes, but minor gripes make a big difference when they apply to every single test — and when I have to force myself to write tests in the first place.  (Maybe they don't bother you, in which case, keep using `unittest`!)  So I use [`py.test`](http://docs.pytest.org/en/latest/) instead:

```python
from mymodule import whatever

def test_whatever(self):
    assert whatever() in {1, 2, 3}
```

If the test fails, you still get useful output, including diffs of strings or sequences:

```
    def test_whatever():
>       assert whatever() in {1, 2, 3}
E       assert 4 in set([1, 2, 3])
E        +  where 4 = whatever()
```

You really, really don't want to know how this works.  It _does_ work, and that's all I care about.

`py.test` also has some bells and whistles like the ability to show locals when a test fails, hooks for writing your own custom `assert`s, and bunches of other hooks and plugins.  But the most important thing to me is that it minimizes the friction involve in writing tests to as little as possible.  I can pretty much copy/paste whatever I did in the REPL and sprinkle `assert`s around.


### If writing tests is hard, that might be a bug

I've seen tests that do some impressive acrobatics just to construct core objects, and likewise heard people grumble that they don't want to write tests because creating core objects is so hard.

The thing is, _tests are just code_.  If you have a hard time constructing _your own_ objects with some particular state, it might be a sign that your API is hard to use!

"Well, we never added a way to do this because there's no possible reason anyone would ever want it."  But _you_ want it, _right now_.  You're consuming your own API, complaining that it can't do X, and then not adding the ability to do X because no one would ever need X.

One of the most underappreciated parts of writing tests is that they force you to write actual code that uses your interfaces.  If doing basic setup is a slog, fix those interfaces.


### Aggressively make your test suite fast and reliable

I've worked with test suites that took _hours_ to run, if they ran at all.

The tradeoff is obvious: these test suites were fairly thorough, and speed was the cost of that thoroughness.  For critical apps, that might be well worth it.  For very large apps, that might be unavoidable.

For codebases that are starting out with no tests at all, it's a huge source of testing pain.  Your test suite should be as fast as possible, or _you won't run it_, and then you'll (rightfully!) convince yourself that there's no point in writing even more tests that you won't run.

If your code is just slow, consider this an excellent reason to make it faster.  If you have a lot of tests, see if you can consolidate some.

Or if you have a handful of especially slow tests, I have a radical suggestion: maybe just delete them.  If they're not absolutely critical, and they're keeping you from running your test suite _constantly_, they may not be worth the cost.  Deleting a test drops your coverage by a fraction of a percent; never running your tests drops your coverage to zero.

Flaky tests are even worse.  Your tests should always, _always_, pass completely.  If you have a test that fails 10% of the time and you just can't figure out why, disable or delete it.  It's not telling you anything useful, and in the meantime it's training you to _ignore when your tests fail_.  If a failing test isn't an immediate red alert, there's no point in having tests at all.


### Run it automatically

Have you seen those GitHub projects where pull requests automatically get a thing saying whether the test suite passed or failed?  Neat, right?  It's done through [Travis](https://travis-ci.org/), and it's surprisingly painless to set up.  Once it _is_ set up, someone else's computer will run your tests all the damn time and bug you when they fail.  It's really annoying, and really great.

(There's also [Coveralls](https://coveralls.io/), which measures your test coverage.  Neat, but if you're struggling to write tests at all, a looming reminder of your shame may not be the most helpful thing.)

I recently ran into an interesting problem in the form of Pelican, the Python library that generates this blog.  It has tests for the `fr_FR` locale, and the test suite _skips them_ if you don't have that locale set up...  but the README tells you that before you submit a pull request, you should generate the locale so you can run the tests.  Naturally, I missed this, didn't have `fr_FR`, thought I passed all the tests, and submitted a pull request that instantly failed on Travis.

Skipping tests because optional dependencies are missing is a tricky affair.  When you write them, you think "no point claiming the test failed when it doesn't indicate problems with the actual codebase" — when I run them, I think "oh, these tests were skipped, so they aren't really important".


## What to test

### Test what you manually test

When you're working on a big feature or bugfix, you develop a little ritual for checking whether it's done.  You crack open the REPL and repeat the same few lines, or you run a script you hacked together, or your launch your app and repeat the same few actions.  It gets incredibly tedious.

You may have similar rituals just before a big release: run the thing, poke around a bit, try common stuff, be confident that at least the basics work.

These are the _best_ things to test, because you're already testing them!  You can save yourself a lot of anguish if you convert these rituals into code.  As an added benefit, other people can then repeat your rituals without having to understand yours or invent their own, and your test suite will serve as a rough description of what you find most important.

Sometimes, this is hard.  Give it a try anyway, even if (especially if) you don't have a test suite at all.

Sometimes, this is _really_ hard.  Write tests for the parts you can, at least.  You can always sit down and work the rest out later.


### Test what's likely to break

Some things are easy to test.  If you have a function that checks whether a number is even, oh boy!  You can write like fifty tests for that, _no problem_.  Now you have fifty more tests!  Good job!

That's great, and feel free to write them all, but...  how likely is it that anyone will ever change that function?  It does one trivial thing, it can be verified correct at a glance, it doesn't depend on anything else, and it almost certainly can't be improved upon.

The primary benefit of testing is a defense against change.  When code changes, tests help convince you that it still works correctly.  Testing code that has no reason to change doesn't add much more value to your test suite.

This isn't to say that you _shouldn't_ test trivial functions — especially since we can be _really bad_ at guessing what'll change in the future — but when you have limited willpower, they're not the most efficient places to spend it.

Knowing what to test is the same kind of artform as knowing what to comment, and I think many of the same approaches apply.  Test obscure things, surprising special cases.  Test things that were tricky to get right, things that _feel_ delicate.  Test things that are difficult to verify just by reading the code.  If you feel the need to explain yourself, it's probably worth testing.


### Test the smallest things you can possibly test

It's nice to have some tests that show your code works from a thousand miles up.  Unfortunately, these also tend to be the slowest (because they do a lot), most brittle (because any small change might break many such tests at once), least helpful (because a problem might come from anywhere), and least efficient (because two such tests will run through much of the same code).

People who are _into testing_ like to go on about unit tests versus functional tests, or maybe those are integration tests, or are they acceptance tests, or end-to-end tests, or...  christ.

Forget the categories.  You already know the shape of your own codebase: it's a hierarchy of lumps that each _feel_ like they relate to a particular concept, even if the code organization doesn't reflect that.  You're writing a disassembler, and there's some code in various places that deals with jumps and labels?  That's a lump, even if the code isn't contiguous on disk.  You, the human, know where it is.

So write your tests around those lumps, and make them as small as possible.  Maybe you still have to run your entire disassembler to actually run certain tests, but you can still minimize the extra work: disable optional features and make the test as simple as possible.  If you ever make changes to jumps or labels, you'll know exactly which tests to look for; if those tests ever break, you'll have a good idea of why.

Don't get me wrong; I know it's _reassuring_ to have a mountain of tests that run through your entire app from start to finish, just as a user would.  But in my experience, those tests break all the time without actually telling you anything you didn't already know, and having more than a handful of them can bog down the entire test suite.  Hesitate before each one you write.


## How to test

### Test output, avoid side effects

Testing code should be easy.  You make some input; you feed it to a function; you check that the output is correct.  The precise nature of "input" and "output" can easily spiral out of control, but at least the process is simple enough.

Testing code that has side effects is a huge, huge pain in the ass.  (And since tests are just code, that means _using_ code that has side effects is also a pain in the ass.)

"Side effect" here means exactly what it sounds like: you feed input into a function, you get some output, and in the meantime something elsewhere has changed.  Or in a similar vein, the behavior of the function depends on something other than what's passed into the function.  The most common case is global record-keeping, like app-wide configuration that sits at the module level somewhere.

It sucks, it's confusing, avoid avoid avoid.

So...  don't use globals, I guess?

I've heard a lot of programmers protest that there's nothing very difficult to understand about one global, and I'm going to commit heresy here by admitting: _that's probably true_!  The extra cognitive burden of using and testing code that relies on a _single_ global is not particularly high.

But one global begets another, and another.  Or perhaps your "one" global mutates into a massive sprawling object with tendrils in everything.  Soon, you realize you've written the [Doom renderer](https://github.com/rheit/zdoom/blob/master/src/r_draw.h#L28) and you have [goofy obscure bugs](https://github.com/rheit/zdoom/commit/8fa9aa26275e71b32cd92065c7ba6d80c7fd1b17) because it's so hard to keep track of what's going on at any given time.

Similar to the much-maligned C `goto`, globals _aren't_ an infectious and incurable toxin that will instantly and irreparably putrefy your codebase.  They just have a cost, and you'll only need to pay it sometime down the road, and it's usually not worth the five minutes of effort saved.  If you must introduce a global, always take a moment to feel _really bad_ about what you're doing.


### Test negative cases and edge cases

I used to work for a company.  As part of the hiring process, prospective hires would be asked to implement a particular board game, complete with tests.  Their solution would be dumped in my lap, for some reason, and I would unleash the harsh light of my judgment upon it.

I'm being intentionally vague because I don't want to help anyone cheat, any more than I already am by telling you how to write tests.  So let's say the game is the most trivial of board games: tic tac toe.

A _significant_ proportion of solutions I graded had test suites like this.

```
board = """
    X--
    -X-
    --X
"""
assert check_winner(board) == "X"

board = """
    OOO
    ---
    ---
"""
assert check_winner(board) == "O"
```

And that was it.  Two or three tests for particular winning states.  (Often not even any tests for whether placing a piece actually worked, but let's leave that aside.)

I would always mark down for this.  The above tests check that your code is _right_, but they don't check that your code **isn't wrong**.  What if there's no winner, but your code thinks there is?

That's much harder to reason about, I grant you!  A tic tac toe board only has a relatively small handful of possible winning states, but a much larger number of possible non-winning states.  But I think what really throws us is that winning is defined in the positive — "there must be three in a row" — whereas non-winning is only defined as, well, not winning.  We don't tend to think of the _lack_ of something as being concrete.

When I took this test, I paid attention to the bugs I ran into while I was writing my code, and I thought about what could go wrong with my algorithm, and I made a few tests based on those educated guesses.  So perhaps I'd check that these boards have no winner:

    OO-     -O-     -X-
    O-X     -O-     --X
    -XX     -X-     X--

The left board has three of each symbol, but not in a row.  The middle board has three in a row, but not all the same symbol.  The right board has three in a row, but only if the board is allowed to wrap.

Are these cases likely to be false positives?  I have no idea.  All I did was consider for a moment what _could_ go wrong, then make up some boards that would have that kind of error.  (One or two of the solutions I graded even had the kinds of false positives that I'd written tests for!)

The same kind of thinking — what could I have missed? — leads me swiftly to another glaring omission from this test suite: _what if there's a tie?_  And, indeed, quite a few of the submissions I graded didn't handle a tie at all.  (Ties were less likely in the actual game than they are in tic tac toe, but still possible.)  The game would ask you to make a move, you wouldn't be able to, and the game would linger there forever.

Don't just write tests to give yourself the smug satisfaction that you did something right.  Write tests to catch the ways you might conceivably have done something _wrong_.  Imagine the code you're testing as an adversary; how might you catch it making a mistake?

If that doesn't sound convincing, let me put this another way.  Consider this hypothetical test suite for a primality test.

```python
def test_is_prime():
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert is_prime(11)
    assert is_prime(17)
    assert is_prime(97)
```

Quick: write some code that passes these tests.  Call it test-driven development practice.

Here's what I came up with:

```python
def is_prime(n):
    return True
```

Whoops!

A related benefit of negative tests is that they make sure your tests actually _work_.  I've seen one or two tests that couldn't reasonably verify that the output of some program was actually correct, so instead, they ran the program and checked that there were no errors.  Later, something went wrong in the test suite, and the program silently _didn't run at all_ — which, naturally, produced no exceptions.  A single test that fed in bad input and checked for an error would've caught this problem right away.


### Refactor

Tests are code.  If you're repeating yourself a lot or there's a lot of friction for some common task, _refactor_.  Write some helpers.  See if your test harness can help you out.

Tests are code.  Don't write a bunch of magical, convoluted, brittle garbage to power your tests.  If you can't convince yourself that your tests work, how can your tests convince you that the rest of your code works?  You should be _more_ confident in your tests than in the rest of your code, yet you'll probably spend far _less_ time maintaining it.  So err on the side of explicit and boring, even if you have to stick to repeating yourself.


## Troublesome cases

### External state

Testing against something outside your program sucks.  With filesystems, you can make a temporary directory.  With time, you can (maybe) fake it.  In general, your life will be easier if you consolidate all your external state access into as few places as possible — easy to understand, easy to test, easy to swap out for some alternative implementation.

With databases, you're just fucked.  Database access _pervades_ most code that needs to touch a database at all.

The common wisdom in the Python web development community is that you should just run your test suite against a little SQLite database.  That's a great idea, except that you're suddenly restricted to the subset of SQL that works identically in SQLite and in your target database.  The next best thing is to run against an actual instance of your target database and call it a day.

And you should probably stop there; nothing I can come up with is any better.  Even for very large apps with very complex databases, that seems to be the best you can do.  You might end up spending twenty minutes per test run starting up a full replicated setup and memcached and whatever else, but I don't have any better ideas.

The problem is that database access still goes through SQL, and SQL is an entire other programming language you're sending out over the wire.  You can't easily swap in an in-process SQL implementation — that's called SQLite.  You can hide all database access in functions with extremely long names and convoluted return values that are only called in one place, then swap out a dummy implementation for testing, but that's really no fun at all.  Plus, it doesn't check that your SQL is actually correct.

If you're using an ORM, you have slightly more of a chance, but I've never seen an ORM that can natively execute queries against in-memory data structures.  (I would _love_ to, and it seems within the realm of possibility, but it would be a huge amount of work and still not cover all the little places you're using functions and syntax specific to your database.)

I don't know.  I got nothin'.


### Procedural generation and other randomness

Imagine you wrote NetHack, which generates some 2D cavern structures.  How can you possibly test that the generated caverns are correct, when they're completely random?

I haven't gotten too deep into this, but I think there's some fertile ground here.  You don't know _exactly_ what the output should be, but you certainly have some _constraints_ in mind.  For example, a cavern map should be at least 10% cave walls and at least 30% open space, right?  Otherwise it's not a cavern.  You can write a test that verifies _that_, then just run it some number of times.

You can't be absolutely sure there are no edge cases (unless you are extremely clever in how you write the terrain generation in the first place), but each run of the test suite will leave you a little more confident.  There's a real risk of flaking here, so you'll have to be extra vigilant about diagnosing and fixing any problems.

You can also write some more specific tests if you give your thing-generator as many explicit parameters as possible, rather than having it make all its decisions internally.  Maybe your cavern algorithm takes a parameter for how much open space there is, from 0.3 to 0.9.  If you dial it down to the minimum, will there still be an open path from the entrance to the exit?  You can test for that, too.


### Web output

This is kind of an interesting problem.  HTML is more readily inspected than an image; you can parse it, drill down with XPath or CSS selectors or what have you, and check that the right text is in the right places.

But!  You may also want to know that it _looks right_, and that's much more difficult.  The obvious thing is to automate a browser, take a screenshot, and compare it to a known good rendering — all of which will come crumbling down the moment someone adds makes a border one pixel wider.  I don't know if we can do any better, unless we can somehow explain to a computer what "looks right" means.

Something I'd like to see is an automated sanity check for HTML + CSS.  Lay out the page _without rendering it_ and check for any obvious screwups, like overlapping text or unwanted overflow.  I don't know how much practical use this would be (or whether it already exists), but it seems like a nice easy way to check that you didn't do something catastrophic.  You wouldn't even necessarily need it in your test suite — just plug it into a crawler and throw it at your site.


### GUIs and games

Oh my god I have no idea.  Keep your UI separated from your internals, test the internals, and hope for the best.


## But most of all

Just test _something_.  Going from zero tests to one test is an infinite improvement.

Once you have a tiny stub of a test suite, you have something to build on, and the next test will be a little easier to write.  You might even find yourself in the middle of adding a feature and suddenly thinking, hey! this is a great opportunity to write a quick test or two.
