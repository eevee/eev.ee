title: Random with care
date: 2018-01-02 17:34
category: articles
tags: tech, patreon, math

Hi!  Here are a few loose thoughts about picking random numbers.

<!-- more -->


## A word about crypto

**DON'T ROLL YOUR OWN CRYPTO**

This is all aimed at frivolous pursuits like video games.  Hell, even video games where money is at stake should be deferring to someone who knows way more than I do.  Otherwise you might find out that your deck shuffles in  your poker game are woefully inadequate and some smartass is cheating you out of millions.  (If your random number generator has fewer than 226 bits of state, it can't even generate every possible shuffling of a deck of cards!)


## Use the right distribution

Most languages have a random number primitive that spits out a number uniformly in the range `[0, 1)`, and you can go pretty far with just that.  But beware a few traps!

### Random pitches

Say you want to pitch up a sound by a random amount, perhaps up to an octave.  Your audio API probably has a way to do this that takes a pitch multiplier, where I say "probably" because that's how the [only audio API I've used](https://love2d.org/wiki/Source:setPitch) works.

Easy peasy.  If 1 is unchanged and 2 is pitched up by an octave, then all you need is `rand() + 1`.  Right?

No!  Pitch is _exponential_ — within the same octave, the "gap" between C and C♯ is about half as big as the gap between B and the following C.  If you pick a pitch multiplier uniformly, you'll have a noticeable bias towards the higher pitches.

One octave corresponds to a doubling of pitch, so if you want to pick a random _note_, you want `2 ** rand()`.

### Random directions

For two dimensions, you can just pick a random angle with `rand() * TAU`.

If you want a vector rather than an angle, or if you want a random direction in _three_ dimensions, it's a little trickier.  You might be tempted to just pick a random point where each component is `rand() * 2 - 1` (ranging from −1 to 1), but that's not quite right.  A direction is a point on the surface (or, equivalently, within the volume) of a _sphere_, and picking each component independently produces a point within the _volume of a cube_; the result will be a bias towards the corners of the cube, where there's much more extra volume beyond the sphere.

No?  Well, just trust me.  I don't know how to make a diagram for this.

Anyway, you could use the Pythagorean theorem a few times and make a huge mess of things, _or_ it turns out there's a [really easy way](http://mathworld.wolfram.com/HyperspherePointPicking.html) that even works for two or four or any number of dimensions.  You pick each coordinate from a _Gaussian_ (normal) distribution, then normalize the resulting vector.  In other words, using Python's [`random` module](https://docs.python.org/3/library/random.html):

```python
def random_direction():
    x = random.gauss(0, 1)
    y = random.gauss(0, 1)
    z = random.gauss(0, 1)
    r = math.sqrt(x*x + y*y + z*z)
    return x/r, y/r, z/r
```

Why does this work?  I have no idea!

Note that it _is_ possible to get zero (or close to it) for every component, in which case the result is nonsense.  You can re-roll all the components if necessary; just check that the _magnitude_ (or its square) is less than some epsilon, which is equivalent to throwing away a tiny sphere at the center and shouldn't affect the distribution.

### Beware Gauss

Since I brought it up: the Gaussian distribution is a pretty nice one for choosing things in some range, where the middle is the common case and should appear more frequently.

That said, I never use it, because it has one annoying drawback: the Gaussian distribution has no minimum or maximum value, so you can't _really_ scale it down to the range you want.  In theory, you might get _any_ value out of it, with no limit on scale.

In _practice_, it's astronomically rare to actually get such a value out.  I did a hundred million trials just to see what would happen, and the largest value produced was 5.8.

But, still, I'd rather not knowingly put extremely rare corner cases in my code if I can at all avoid it.  I could clamp the ends, but that would cause unnatural bunching at the endpoints.  I could reroll if I got a value outside some desired range, but I prefer to avoid rerolling when I can, too; after all, it's still (astronomically) possible to have to reroll for an indefinite amount of time.  (Okay, it's really not, since you'll eventually hit the period of your PRNG.  Still, though.)  I don't bend over backwards here — I _did_ just say to reroll when picking a random direction, after all — but when there's a nicer alternative I'll gladly use it.

And lo, there _is_ a nicer alternative!  Enter the [beta distribution](https://en.wikipedia.org/wiki/Beta_distribution).  It always spits out a number in `[0, 1]`, so you can easily swap it in for the standard normal function, but it takes two "shape" parameters α and β that alter its behavior fairly dramatically.

With α = β = 1, the beta distribution is uniform, i.e. no different from `rand()`.  As α increases, the distribution skews towards the _right_, and as β increases, the distribution skews towards the _left_.  If α = β, the whole thing is symmetric with a hump in the middle.  The higher either one gets, the more extreme the hump (meaning that value is far more common than any other).  With a little fiddling, you can get a number of interesting curves.

Screenshots don't really do it justice, so here's a little Wolfram widget that lets you play with α and β live:

<iframe src="https://www.open.wolframcloud.com/objects/b6ae9330-d387-42d5-90ca-e41b738f3c78" width="600" height="400" style="margin: 0 auto; border: none;"></iframe>

Note that if α = 1, then 1 is a possible value; if β = 1, then 0 is a possible value.  You probably want them both greater than 1, which clamps the endpoints to zero.

Also, it's possible to have either α or β or both be _less_ than 1, but this creates very different behavior: the corresponding endpoints become _poles_.

Anyway, something like α = β = 3 is probably close enough to normal for most purposes but already clamped for you.  And you could easily replicate something like, say, NetHack's incredibly bizarre [`rnz` function](https://nethackwiki.com/wiki/Rnz).

### Random frequency

Say you want some event to have an 80% chance to happen every second.  You (who am I kidding, _I_) might be tempted to do something like this:

```python
if random() < 0.8 * dt:
    do_thing()
```

In an ideal world, `dt` is always the same and is equal to `1 / f`, where `f` is the framerate.  Replace that 80% with a variable, say `P`, and every tic you have a `P / f` chance to do the… whatever it is.

Each second, `f` tics pass, so you'll make this check `f` times.  The chance that _any_ check succeeds is the inverse of the chance that every check fails, which is $1 - \left(1 - \frac{P}{f}\right)^f$.

For `P` of 80% and a framerate of 60, that's a total probability of 55.3%.  Wait, what?

Consider what happens if the framerate is 2.  On the first tic, you roll `0.4` twice — but probabilities are combined by _multiplying_, and splitting work up by `dt` only works for _additive_ quantities.  You lose some accuracy along the way.  If you're dealing with something that multiplies, you need an exponent somewhere.

But in this case, maybe you don't want that at all.  Each separate roll you make _might independently succeed_, so it's possible (but very unlikely) that the event will happen 60 times within a single second!  Or 200 times, if that's someone's framerate.

If you explicitly want something to have a chance to happen on a specific interval, you have to check on that interval.  If you don't have a gizmo handy to run code on an interval, it's easy to do yourself with a time buffer:

```python
timer += dt
# here, 1 is the "every 1 seconds"
while timer > 1:
    timer -= 1
    if random() < 0.8:
        do_thing()
```

Using `while` means rolls still happen even if you somehow skipped over an entire second.

(For the curious, and the nerds who already noticed: the expression $1 - \left(1 - \frac{P}{f}\right)^f$ converges to a specific value!  As the framerate increases, it becomes a better and better approximation for $1 - e^{-P}$, which for the example above is 0.551.  Hey, 60 fps is pretty accurate — it's just accurately representing something nowhere near what I wanted.  Er, you wanted.)


### Rolling your own

Of course, you can fuss with the classic `[0, 1]` uniform value however you want.  If I want a bias towards zero, I'll often just square it, or multiply two of them together.  If I want a bias towards one, I'll take a square root.  If I want something _like_ a Gaussian/normal distribution, but with clearly-defined endpoints, I might add together _n_ rolls and divide by _n_.  (The normal distribution is just what you get if you roll infinite dice and divide by infinity!)

It'd be nice to be able to understand _exactly_ what this will do to the distribution.  Unfortunately, that requires some calculus, which this post is too small to contain, and which I didn't even know much about myself until I went down a deep rabbit hole while writing, and which in many cases is straight up impossible to express directly.

Here's the non-calculus bit.  A source of randomness is often graphed as a PDF — a [_probability density function_](https://en.wikipedia.org/wiki/Probability_density_function).  You've almost certainly seen a [bell curve](https://en.wikipedia.org/wiki/Normal_distribution) graphed, and that's a PDF.  They're pretty nice, since they do exactly what they look like: they show the relative chance that any given value will pop out.  On a bog standard bell curve, there's a peak at zero, and of course zero is the most common result from a normal distribution.

(Okay, actually, since the results are continuous, it's vanishingly unlikely that you'll get _exactly_ zero — but you're much more likely to get a value _near_ zero than _near_ any other number.)

For the uniform distribution, which is what a classic `rand()` gives you, the PDF is just a straight horizontal line — every result is equally likely.

----

If there were a calculus bit, it would go here!  Instead, we can cheat.  Sometimes.  Mathematica knows how to work with probability distributions in the abstract, and there's a [free web version](https://sandbox.open.wolframcloud.com/app/) you can use.  For the example of squaring a uniform variable, try this out:

```mathematica
PDF[TransformedDistribution[u^2, u \[Distributed] UniformDistribution[{0, 1}]], u]
```

(The `\[Distributed]` is a funny tilde that doesn't exist in Unicode, but which Mathematica uses as a first-class operator.  Also, press <kbd>shift</kbd><kbd>Enter</kbd> to evaluate the line.)

This will tell you that the distribution is…  $\frac{1}{2\sqrt{u}}$.  Weird!  You can plot it:

```mathematica
Plot[%, {u, 0, 1}]
```

(The `%` refers to the result of the last thing you did, so if you want to try several of these, you can just do `Plot[PDF[…], u]` directly.)

The resulting graph shows that numbers around zero are, in fact, vastly — _infinitely_ — more likely than anything else.

What about multiplying two together?  I can't figure out how to get Mathematica to understand this, but a great amount of digging revealed that the answer is `-ln x`, and from there you can [plot them both](http://www.wolframalpha.com/input/?i=1%2F%282sqrt%28x%29%29,+-ln+x+from+0+to+1) on Wolfram Alpha.  They're _similar_, though squaring has a much better chance of giving you high numbers than multiplying two separate rolls — which makes some sense, since if _either_ of two rolls is a low number, the product will be even lower.

What if you know the graph you want, and you want to figure out how to play with a uniform roll to get it?  Good news!  That's a whole thing called [inverse transform sampling](https://en.wikipedia.org/wiki/Inverse_transform_sampling).  All you have to do is take an integral.  Good luck!

----

This is all extremely ridiculous.  New tactic: **Just Simulate The Damn Thing**.  You already _have_ the code; run it a million times, make a histogram, and tada, there's your PDF.  That's one of the great things about computers!  Brute-force numerical answers are easy to come by, so there's no excuse for producing something like [rnz](https://nethackwiki.com/wiki/Rnz).  (Though, be sure your histogram has sufficiently narrow buckets — I tried plotting one for rnz once and the weird stuff on the left side didn't show up at all!)

By the way, I learned something from futzing with Mathematica here!  Taking the square root (to bias towards 1) gives a PDF that's a straight diagonal line, nothing like the hyperbola you get from squaring (to bias towards 0).  How do you get a straight line the other way?  Surprise: $1 - \sqrt{1 - u}$.

### Okay, okay, here's the actual math

I don't claim to have a very firm grasp on this, but I had a hell of a time finding it written out clearly, so I might as well write it down as best I can.  This was a great excuse to finally set up MathJax, too.

Say $u(x)$ is the PDF of the original distribution and $u$ is a representative number you plucked from that distribution.  For the uniform distribution, $u(x) = 1$.  Or, more accurately,

$$
u(x) = \begin{cases}
1 & \text{ if } 0 \le x \lt 1 \\
0 & \text{ otherwise }
\end{cases}
$$

Remember that $x$ here is a possible outcome you want to know about, and the PDF tells you the relative probability that a roll will be _near_ it.  This PDF spits out 1 for every $x$, meaning every number between 0 and 1 is equally likely to appear.

We want to _do something_ to that PDF, which creates a new distribution, whose PDF we want to know.  I'll use my original example of $f(u) = u^2$, which creates a new PDF $v(x)$.

The trick is that we need to work in terms of the _cumulative_ distribution function for $u$.  Where the PDF gives the relative chance that a roll will be ("near") a specific value, the CDF gives the relative chance that a roll will be _less than_ a specific value.

The conventions for this seem to be a bit fuzzy, and nobody bothers to explain which ones they're using, which makes this all the more confusing to read about…  but let's write the CDF with a capital letter, so we have $U(x)$.  In this case, $U(x) = x$, a straight 45° line (at least between 0 and 1).  With the definition I gave, this should make sense.  At some arbitrary point like 0.4, the value of the PDF is 1 (0.4 is just as likely as anything else), and the value of the CDF is 0.4 (you have a 40% chance of getting a number from 0 to 0.4).

Calculus ahoy: the PDF is the _derivative_ of the CDF, which means it measures the _slope_ of the CDF at any point.  For $U(x) = x$, the slope is always 1, and indeed $u(x) = 1$.  See, calculus is easy.

Okay, so, now we're getting somewhere.  What we want is the _CDF_ of our new distribution, $V(x)$.  The CDF is defined as the probability that a roll $v$ will be less than $x$, so we can literally write:

$$V(x) = P(v \le x)$$

(This is why we have to work with CDFs, rather than PDFs — a PDF gives the chance that a roll will be "nearby," whatever that means.  A CDF is much more concrete.)

What is $v$, exactly?  We defined it ourselves; it's the _do something_ applied to a roll from the original distribution, or $f(u)$.

$$V(x) = P\!\left(f(u) \le x\right)$$

Now the first tricky part: we have to solve that inequality for $u$, which means we have to _do something, backwards_ to $x$.

$$V(x) = P\!\left(u \le f^{-1}(x)\right)$$

Almost there!  We now have a probability that $u$ is less than some value, and that's the definition of a CDF!

$$V(x) = U\!\left(f^{-1}(x)\right)$$

Hooray!  Now to turn these CDFs back into PDFs, all we need to do is differentiate both sides and use the chain rule.  If you never took calculus, don't worry too much about what that means!

$$v(x) = u\!\left(f^{-1}(x)\right)\left|\frac{d}{dx}f^{-1}(x)\right|$$

Wait!  Where did that absolute value come from?  It takes care of whether $f(x)$ increases or decreases.  It's the least interesting part here by far, so, whatever.

There's one more magical part here when using the uniform distribution — $u(\dots)$ is always equal to 1, so that entire term disappears!  (Note that this only works for a uniform distribution with a width of 1; PDFs are scaled so the entire area under them sums to 1, so if you had a `rand()` that could spit out a number between 0 and 2, the PDF would be $u(x) = \frac{1}{2}$.)

$$v(x) = \left|\frac{d}{dx}f^{-1}(x)\right|$$

So for the specific case of modifying the output of `rand()`, all we have to do is invert, then differentiate.  The inverse of $f(u) = u^2$ is $f^{-1}(x) = \sqrt{x}$ (no need for a ± since we're only dealing with positive numbers), and differentiating that gives $v(x) = \frac{1}{2\sqrt{x}}$.  Done!  This is also why square root comes out nicer; inverting it gives $x^2$, and differentiating that gives $2x$, a straight line.

Incidentally, that method for turning a uniform distribution into _any_ distribution — [inverse transform sampling](https://en.wikipedia.org/wiki/Inverse_transform_sampling) — is pretty much the same thing in reverse: integrate, then invert.  For example, when I saw that taking the square root gave $v(x) = 2x$, I naturally wondered how to get a straight line going the other way, $v(x) = 2 - 2x$.  Integrating that gives $2x - x^2$, and then you can use the quadratic formula (or just ask Wolfram Alpha) to solve $2x - x^2 = u$ for $x$ and get $f(u) = 1 - \sqrt{1 - u}$.

Multiply _two_ rolls is a bit more complicated; you have to write out the CDF as an integral and you end up doing a double integral and wow it's a mess.  The only thing I've retained is that you do a division somewhere, which then gets integrated, and that's why it ends up as $-\ln x$.

And that's quite enough of that!  (Okay but having math in my blog is pretty cool and I will definitely be doing more of this, sorry, not sorry.)


## Random vs varied

Sometimes, _random_ isn't actually what you want.  We tend to use the word "random" casually to mean something more like _chaotic_, i.e., with no discernible pattern.  But that's not really random.  In fact, given how good humans can be at finding incidental patterns, they aren't all that unlikely!  Consider that when you roll two dice, they'll come up either the same or only one apart almost half the time.  _Coincidence?_  Well, yes.

If you ask for randomness, you're saying that _any_ outcome — or series of outcomes — is acceptable, including five heads in a row or five tails in a row.  Most of the time, that's fine.  Some of the time, it's less fine, and what you really want is _variety_.  Here are a couple examples and some fairly easy workarounds.

### NPC quips

The nature of games is such that NPCs will eventually run out of things to say, at which point further conversation will give the player a short brush-off quip — a slight nod from the designer to the player that, hey, you hit the end of the script.

Some NPCs have multiple possible quips and will give one at random.  The trouble with this is that it's very possible for an NPC to repeat the _same_ quip several times in a row before abruptly switching to another one.  With only a few options to choose from, getting the same option twice or thrice (especially across an entire game, which may have numerous NPCs) isn't all that unlikely.  The notion of an NPC quip isn't very realistic to start with, but having someone repeat themselves and then abruptly switch to something else is especially jarring.

The easy fix is to show the quips in order!  Paradoxically, this is more consistently varied than choosing at random — the original "order" is likely to be meaningless anyway, and it already has the property that the same quip can never appear twice in a row.

If you like, you can shuffle the list of quips every time you reach the end, but take care here — it's possible that the last quip in the old order will be the same as the first quip in the new order, so you may still get a repeat.  (Of course, you can just check for this case and swap the first quip somewhere else if it bothers you.)

That last behavior is, in fact, the canonical way that [Tetris chooses pieces](https://harddrop.com/wiki/Random_Generator) — the game simply shuffles a list of all 7 pieces, gives those to you in shuffled order, then shuffles them again to make a new list once it's exhausted.  There's no avoidance of duplicates, though, so you can still get two S blocks in a row, or even two S and two Z all clumped together, but no more than that.  Some Tetris variants take other approaches, such as [actively avoiding repeats even several pieces apart](https://harddrop.com/wiki/TGM_randomizer) or [deliberately giving you the worst piece possible](http://blahg.res0l.net/2009/01/bastet-bastard-tetris/).

### Random drops

Random drops are often implemented as a flat chance each time.  Maybe enemies have a 5% chance to drop health when they die.  [Legally speaking](https://en.wikipedia.org/wiki/Law_of_large_numbers), over the long term, a player will see health drops for about 5% of enemy kills.

Over the _short_ term, they may be desperate for health and not survive to see the long term.  So you may want to put a thumb on the scale sometimes.  Games in the Metroid series, for example, have a somewhat infamous bias towards whatever kind of drop they think you need — health if your health is low, missiles if your missiles are low.

I can't give you an exact approach to use, since it depends on the game and the feeling you're going for and the variables at your disposal.  In extreme cases, you might want to _guarantee_ a health drop from a tough enemy when the player is critically low on health.  (Or if you're feeling particularly evil, you could go the other way and deny the player health when they most need it…)

The problem becomes a little different, and worse, when the event that triggers the drop is relatively rare.  The pathological case here would be something like a raid boss in World of Warcraft, which requires hours of effort from a coordinated group of people to defeat, and which has some tiny chance of dropping a good item that will go to only one of those people.  This is why I stopped playing World of Warcraft at 60.

Dialing it back a little bit gives us Enter the Gungeon, a roguelike where each room is a set of encounters and each floor only has a dozen or so rooms.  Initially, you have a 1% chance of getting a reward after completing a room — but every time you complete a room and _don't_ get a reward, the chance increases by 9%, up to a cap of 80%.  Once you get a reward, the chance resets to 1%.

The natural question is: how frequently, exactly, can a player expect to get a reward?  We could do math, or we could Just Simulate The Damn Thing.

```python
from collections import Counter
import random

histogram = Counter()

TRIALS = 1000000
chance = 1
rooms_cleared = 0
rewards_found = 0
while rewards_found < TRIALS:
    rooms_cleared += 1
    if random.random() * 100 < chance:
        # Reward!
        rewards_found += 1
        histogram[rooms_cleared] += 1
        rooms_cleared = 0
        chance = 1
    else:
        chance = min(80, chance + 9)

for gaps, count in sorted(histogram.items()):
    print(f"{gaps:3d} | {count / TRIALS * 100:6.2f}%", '#' * (count // (TRIALS // 100)))
```

```text
  1 |   0.98%
  2 |   9.91% #########
  3 |  17.00% ################
  4 |  20.23% ####################
  5 |  19.21% ###################
  6 |  15.05% ###############
  7 |   9.69% #########
  8 |   5.07% #####
  9 |   2.09% ##
 10 |   0.63%
 11 |   0.12%
 12 |   0.03%
 13 |   0.00%
 14 |   0.00%
 15 |   0.00%
```

We've got kind of a hilly distribution, skewed to the left, which is up in this histogram.  Most of the time, a player should see a reward every three to six rooms, which is maybe twice per floor.  It's vanishingly unlikely to go through a dozen rooms without ever seeing a reward, so a player _should_ see at least one per floor.

Of course, this simulated a single continuous playthrough; when starting the game from scratch, your chance at a reward always starts fresh at 1%, the worst it can be.  If you want to know about how many rewards a player will get on the first floor, hey, Just Simulate The Damn Thing.

```text
  0 |   0.01%
  1 |  13.01% #############
  2 |  56.28% ########################################################
  3 |  27.49% ###########################
  4 |   3.10% ###
  5 |   0.11%
  6 |   0.00%
```

Cool.  Though, that's assuming exactly 12 rooms; it might be worth changing that to pick at random in a way that matches the level generator.

(Enter the Gungeon does some other things to skew probability, which is very nice in a roguelike where blind luck can make or break you.  For example, if you kill a boss without having gotten a new gun anywhere else on the floor, the boss is guaranteed to drop a gun.)


### Critical hits

I suppose this is the same problem as random drops, but backwards.

Say you have a battle sim where every attack has a 6% chance to land a devastating critical hit.  Presumably the same rules apply to both the player and the AI opponents.

Consider, then, that the AI opponents have exactly the same 6% chance to ruin the player's day.  Consider also that this gives them an 0.4% chance to critical hit _twice in a row_.  0.4% doesn't sound like much, but across an entire playthrough, it's not unlikely that a player might see it happen and find it incredibly annoying.

Perhaps it would be worthwhile to explicitly forbid AI opponents from getting consecutive critical hits.


## In conclusion

An emerging theme here has been to Just Simulate The Damn Thing.  So consider Just Simulating The Damn Thing.  Even a simple change to a random value can do surprising things to the resulting distribution, so unless you feel like differentiating the inverse function of _your code_, maybe test out any non-trivial behavior and make sure it's what you wanted.  Probability is [hard to reason about](https://en.wikipedia.org/wiki/Monty_Hall_problem).
