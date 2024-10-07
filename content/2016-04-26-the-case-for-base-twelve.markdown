title: The case for base twelve
date: 2016-04-26 17:43
category: blog
tags: math

Decimal sucks.

Ten is such an awkward number.  Its only divisors are two and five.  Two is nice, but five?  Who cares about five?  What about three and four?

I have a simple solution to all of these non-problems _and more_, which is: we should switch to base twelve.

<!-- more -->


## A brief recap

For ease of writing larger numbers, we use places.  The number "123" really means: three ones, two tens, one hundred.  "Hundred", of course, is just what we call ten tens.

This all assumes that ten is a magical number.  It's not.  We generally have ten fingers, which makes it convenient.  Mathematically, though, ten is not particularly special.  We could just as well use a different number, like two (which gives us binary), or seven, or twelve.  The number we pick, the number where the ones place gets full and rolls over, is called the number _base_.

We use decimal, base ten.  This post is about duodecimal, base twelve.

It turns out that there are [people who advocate for this](https://en.wikipedia.org/wiki/Duodecimal#Advocacy_and_.22dozenalism.22).  I haven't read any of their writing, instead opting to do my own research.  The one tidbit I've picked up is that they insist that base twelve be called _dozenal_, as the name "duodecimal" is still in terms of ten.

So, in dozenal, "123" means: three ones, two dozens, one gross.  You know that number as one hundred and seventy-one.

To avoid confusion, all numbers in this post that are written with _digits_ will be in dozenal.  Words are independent of base — "thirteen" always means the same thing — so I'll use those to translate.

### Extra digits

Base ten has ten digits, so base twelve needs twelve digits.  I need to pick some.

There are in fact already two dozenal digits in Unicode 8.0: ↊ U+218A TURNED DIGIT TWO and ↋ U+218B TURNED DIGIT THREE.  Unfortunately, since these are very recent, font support is lacking.

There's also the consideration of 7-segment LCD displays.  An upside-down 3 would work fine and would resemble a capital E, but an upside-down 2 would look the same as a 5.

I mulled this over for a while and came up with:

- ƌ for ten — resembles "d" for decimal, and displays in 7-segment like a mirrored 6
- ⅃ for eleven — resembles a rotated 7, which it also rhymes with

No?  Fair enough.  These are all pretty awkward to type, anyway, even for me.  I _could_ use the more self-explanatory ⑩ and ⑪...  but perhaps not.

For now, I'll go with the old standby and use A to mean ten, B to mean eleven.

The numbers from one to twenty are thus written: 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, 10, 11, 12, 13, 14, 15, 16, 17, 18.

Got it?  Super.


## Twelve in daily life

We're already surrounded by twelves.  This year is 1200 in dozenal!

There are twelve months in a year.  (Leap years are every four years, so in dozenal, a leap year would always be a year ending in 0, 4, or 8.)

There are twelve hours on the clock and sixty minutes in an hour (which is 50 — five dozen).  Dozenal would let us save an entire digit on clock faces, since the hour will never be two digits; the moment before midnight is B:4B.

There are 10 (twelve) inches in a foot, 3080 feet in a mile (easily rounded to an even 3000).  If metric were based on dozenal, the biggest part of the squabble between metric and imperial units would largely disappear.

Donuts come in dozens.  It's there in plain sight: a donut resembles a zero, and one dozen is written 10.

Teenagedom would begin at 10, and adulthood would be at 16, halfway to 20.  No one would ever have lived to 100, though.

We have unique names for numbers from one to twelve; it's only at thirteen that patterns start to emerge.  We also already have a name for twelve twelves.

I had to learn times tables up to twelve in elementary school, which makes much more sense if twelve is written as 10.

Twelve digits would fit nicely in a 3×4 grid.  Adding a fifth row for symbols (pound, star, something else?) would make the grid 3×5, which with square buttons is pleasingly close to the golden ratio.

A full circle is three hundred sixty degrees, which is a multiple of twelve.  It's also two and a half gross, i.e. 260.

Numbers would be eight percent shorter on average.  (Dozenal can express everything up to one hundred forty-three with only two digits.)

Twitter might have rounded the number of available characters up from B8 to an even 100.

"But wait!" I hear you cry.  "Twelve might be great, but how do we count to it when we only have ten fingers?"

No problem!  Check out your hands.  Each of your fingers has two knuckles, which divide it into three segments.  Three segments times four fingers makes...  twelve!  And your thumb is left over for keeping track of where you are.  You can actually count higher with one hand in dozenal than with _both_ hands in decimal!  If you use your other hand for the dozens place, you can count all the way to 100 (a gross, one hundred forty-four) just on your fingers.


## Arithmetic

Is exactly the same, but with two more digits.  Carrying and whatnot are the same regardless of base; the only difference is that 9 + 1 is the single-digit A rather than wrapping around to two digits.

You can do long subtraction:

```text
  23
  3̸4̸2
- 173
-----
  18B
```

Or long multiplication:

```text
  342
× 173
-----
  A06
1B52
342
-----
54526
```

Or long _division_...  which I will not attempt to Unicode-art here.


## Fractions

Twelve is what's called a _highly composite number_ — it's the smallest number with five divisors.  (One, two, three, four, and six.)  Ten, on the other hand, has three divisors (one, two, five), making it only as composite as six.  What a waste.

The number of divisors is important, because it allows for many more "natural" divisions.  Consider that most simple fractions in decimal repeat forever, making them ugly and cumbersome to work with.  Well, check out some fractions in dozenal.

- ½ = 0.6
- ⅓ = 0.4
- ⅔ = 0.8
- ¼ = 0.3
- ¾ = 0.9
- ⅙ = 0.2
- ⅚ = 0.A
- ⅛ = 0.16
- ⅜ = 0.46
- ⅑ = 0.16

True, one-fifth is written as the somewhat less-pleasing 0.2̅4̅9̅7̅.  But, honestly, who cares about fifths?  Fifths are usually a cheap imitation of sixths, which are the beautiful 0.2 in dozenal.

You can see how nice this scheme really is when you consider it in terms of percentages.  Decimal percentages are a little hard to reckon with, since so few of them divide evenly into one hundred — what does thirteen percent _mean_, exactly?  (About one-eighth.  You can't even express a pizza slice as a whole percentage!)  On the other hand, _all_ of the above fractions can be expressed as whole dozenal percentages: one third is 40%, one half is 60%, one twelfth is of course 10%.  Just look how many dozenal percentages ending in zero are really simple fractions.

Let's say a percentage is "satisfying" if it can be converted into a fraction where at least two primes cancel out.  For example, seventeen percent is just seventeen hundredths, which is unsatisfying; but thirty-two percent is eight twenty-fifths, which is at least partly simplified.

By this definition, only 28 whole decimal percentages are satisfying — that's 3A%.  But a whopping 48 whole dozenal percentages are satisfying, which is of course 48%!  48% is itself even satisfying; it's seven eighteenths.


## Divisibility rules

These are tricks like, "if the sum of the digits is divisible by three, the original number is divisible by three".  Dozenal has a different set of digits, so the same tricks won't work.

However, the new tricks are often much easier.  I went ahead and figured some out:

- **2**: If the last digit is divisible by two (0, 2, 4, 6, 8, or A), the number is divisible by two.

- **3**: If the last digit is divisible by three (0, 3, 6, or 9), the number is divisible by three.

- **4**: If the last digit is divisible by four (0, 4, or 8), the number is divisible by four.

- **5**: Multiply the last digit by two, and subtract from the rest of the number.  If the result is divisible by five, the original number is divisible by five.

    Here's an example, for the number B3 (one hundred thirty-five).

    Take off the 3 and double it to get 6.  The rest of the number is B (eleven).  B - 6 = 5, which is divisible by 5, so B3 is also divisible by 5.

- **6**: If the last digit is divisible by six (0 or 6), the number is divisible by six.

- **7**: Multiply the last digit by three, and add it to the rest of the number.  If the result is divisible by seven, the original number is divisible by seven.

- **8**: If the last _two_ digits are divisible by eight (0, 8, 14, 20, 28, 34, ...), the number is divisible by eight.

    Alternatively, but more of a mouthful, you can see a pattern in the numbers above.  If the last digit is 0 or 8 and the dozens digit is even, OR the last digit is 4 and the dozens digit is odd, the number is divisible by eight.

- **9**: If the last two digits are divisible by nine (0, 9, 16, 23, 30, ...), the number is divisible by nine.

    Again, there's a pattern in the numbers, though this one is more complicated.

- **A** (ten): Must be divisible by both two and five.

- **B** (eleven): Add all the digits.  If the result is divisible by eleven, the original number is divisible by eleven.

- **10** (twelve): If the last digit is 0, the number is divisible by twelve.

- **11** (thirteen): From left to right, alternate subtracting and adding the digits.  If the result is divisible by thirteen, the original number is divisible by thirteen.

    Here's an example, for 891 (one thousand two hundred sixty-one, or thirteen times ninety-seven).

    Compute 8 - 9 + 1; it's zero, which is divisible by thirteen, so the original number is too.

- **12** (fourteen): Must be divisible by both two and seven.

- **13** (fifteen): Must be divisible by both three and five.

- **14** (sixteen): If the last two digits are divisible by sixteen (0, 14, 28, 40, 54, ...), the number is divisible by sixteen.

The primes start to get trickier after that.


## Dozenal and computers

A double-precision floating point number has fifty-three binary digits.  That's only (barely) sixteen decimal digits of precision.  In dozenal, it's slightly worse at almost fifteen digits, since each dozenal digit stores more information.

A byte is 8 bits and can hold a value up to 193.  Two bytes is 14 bits and maxes out at 31B13 (a lovely palindrome!).  Four bytes is 28 bits, max 9BA461593.  Eight bytes is 54 bits, max 839365134A2A240713.  Six bytes is, pleasingly, 40 bits.

A kilobyte (kibibyte, if you must) is 714 bytes...  but of course, we wouldn't define it that way if we used dozenal.  We like one thousand twenty-four because it's a power of two that's coincidentally very close to a power of ten.  This doesn't really happen in dozenal until 2¹⁶ = 107854.  But hey, that means we'd never have had this ridiculous inconsistency in advertised hard drive space; we would've just said a kilobyte is 1000 bytes from the beginning.  If so, a two terabyte hard drive would be described as a paltry 2B6 gigabytes.

With two extra digits, ASCII would have two fewer slots available for punctuation.  I wonder which two wouldn't have made it?

Unicode would have space for 458,8A7 characters.


## Some familiar numbers

The square numbers up to 20 are 1, 4, 9, 14, 21, 30, 41, 54, 69, 84, A1, 100, 121, 133, 169, 194, 201, 230, 261, 294, 309, 344, 381, 400.

The primes up to 200 are 2, 3, 5, 7, B, 11, 15, 17, 1B, 25, 27, 31, 35, 37, 3B, 45, 4B, 51, 57, 5B, 61, 67, 6B, 75, 81, 85, 87, 8B, 91, 95, A7, AB, B5, B7, 105, 107, 111, 117, 11B, 125, 12B, 131, 13B, 141, 145, 147, 157, 167, 16B, 171, 175, 17B, 181, 18B, 195, 19B, 1A5, 1A7, 1B1, 1B5, 1B7.  Notably and pleasingly (to me, anyway), 101 is composite: it's 5 × 25.

π = 3.184809493B918664573A...

τ = 6.349416967B635108B279...

e = 2.8752360698219BA71971...

√2 = 1.4B79170A07B85737704B...

φ = 1.74BB6772802A46A6A186...

It's suspected that π is a normal number — that is, it has an even distribution of all possible digits no matter what base you write it in.


## Okay uh

This is less of a case for base twelve and more that I wanted to write a bunch of math stuff and play in a different base.  This post isn't really going anywhere in particular, so I'll arbitrarily cut it off here.  I hope you enjoyed this hazy thought experiment, if you read this far.

I like to remember sometimes that even many of the things we take for granted — like the way we write numbers — are still arbitrary conventions.

Decimal _does_ suck a bit, though.


## Appendix: convert to a base in Python

Curiously, Python can convert integers _from_ any base, but can't handle floats or convert _to_ an arbitrary base.  So here is some code that can, and that also handles negative numbers and floats.  And `fractions.Fraction`.  And `decimal.Decimal`.  And complex numbers.

```python
def tobase(n, b, precision=20, digits='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    # Split off any imaginary part to be dealt with later
    imag = n.imag
    n = real = n.real

    # Handle negation separately
    neg = False
    if n < 0:
        n *= -1
        neg = True

    # Split off any fractional part
    n, frac = divmod(n, 1)
    n = int(n)

    # Convert to base b.  Yep, that's all it takes
    out = []
    while n:
        n, r = divmod(n, b)
        out.append(digits[r])

    if neg:
        out.append('-')

    # Converting to a base moves away from the decimal point, so these digits
    # are in reverse order and need flipping before dealing with a fraction
    out = out[::-1]
    if frac:
        # Leading zero if necessary
        if not out:
            out.append(digits[0])
        out.append('.')
        for _ in range(precision):
            if not frac:
                break
            d, frac = divmod(frac * b, 1)
            out.append(digits[int(d)])

    # Add any imaginary part, keeping in mind that there might not even be a real part
    if imag:
        imagres = tobase(imag, b, precision=precision, digits=digits)
        if not real:
            return imagres + 'j'
        if imag > 0:
            out.append('+')
        out.append(imagres)
        out.append('j')

        # Python's repr wraps fully complex numbers in parentheses
        if real:
            out.insert(0, '(')
            out.append(')')

    return ''.join(out)
```


## Appendix: deriving divisibility rules

How did I figure out the rules above?  I'm glad you asked because that's actually _super interesting_.

The reason we have divisibility rules at all is that _someone has already done a bunch of division for you_, by virtue of writing the number out in digits.  That's _how_ you convert an abstract number to something you can write out: you divide repeatedly by twelve, or ten, or whatever base you're using.  A divisibility rule is a trick for taking that work and adapting it to a different divisor.


### Easy cases

The easiest cases are for divisibility by `d`, where the base itself is already divisible by `d`.  You only have to look at the last digit.  That's why picking out even numbers in both decimal and dozenal is so easy — the base is divisible by 2, so the last digit gives away whether an entire number is divisible by 2.

I think this is pretty intuitive.  Count up by twos: 2, 4, 6, 8, A, 10.  Every sixth number will roll over the ones place into the dozens place, _and_ reset the ones place to zero, which is where it started.  Counting like this will eventually find every multiple of two...  so every number ending in an even digit must be divisible by two, and no number divisible by two can ever end in an odd digit.

Symbolically, you can write any natural number as:

$$
n = 10x + y = (2 × 6x) + y
$$

where $y$ is the ones digit and $x$ is all the rest of the digits.  This is just the definition of how we write numbers; 984 is really $98 × 10 + 4$.

$x$ must be an integer, since it's just digits, so $2 × 6 x$ must be even.  Iff $y$ is also even, the original number must be even.

You can easily do the same thing for any number that's a factor of the base.  For decimal, that's two, zero, and ten; for dozenal, it's two, three, four, six, and twelve.  Consider for a moment that that means if we used an _odd_ base, you couldn't easily tell whether a number were even!  It's only trivial in decimal because ten is a multiple of two.

You can also extend this to work for any number that's a factor of a _power of_ the base.  Dozenal's divisibility rule for 9 is to look at the last two digits of the number.  That's because:

$$
n = 100 x + y = (9 × 14 x) + y
$$

This time, $y$ is the last _two_ digits, but otherwise it's the same idea.  There's a similar rule in decimal for divisibility by four (though you only need one digit to work that out in dozenal).


### Special cases

Most shenanigans that involve looking at individual digits actually work just as well in dozenal, or _any_ base, but perhaps with different results.  Of particular interest: in base $b$, the same divisibility rules for $b - 1$ and $b + 1$ will always work.

Adding all the digits works for $b - 1$.  To prove this, consider a simpler case: instead of adding all the digits together, add the last digit ($y$) to the rest of the digits ($x$) to make a new number, $s$.  Then:

$$
\begin{align}
n & = b x + y \\
s & = x + y \\
n - s & = (b x + y) - (x + y) = b x - x = (b - 1) × x
\end{align}
$$

$n - s$ is _always_ divisible by $b - 1$.  Thus, if $s$ is also divisible by $b - 1$, the original number must be — because it's just the sum of these other two numbers.

Summing all the digits is just a matter of repeating the above process.

Incidentally, the decimal rule for 3 exists specifically because 3 is a factor of 9, one less than ten.  (Eleven is prime, so this doesn't come into play with dozenal.)  You can kind of see how it works above.  Hint: $n$ and $s$ have the same remainder when dividing by $b - 1$.

$b + 1$ has several possible rules; I used the one I like the most, which is to alternate adding and subtracting.  Note that it doesn't matter whether you start out subtracting or adding; $x - y + z$ is just the negation of $-x + y - z$.

If we split off two digits _separately_ this time, we get:

$$
\begin{align}
n & = b² x + b y + z \\
s & = x - y + z \\
n - s & = (b² x + b y + z) - (x - y + z) \\
      & = (b² - 1) x + (b + 1) y \\
      & = (b + 1)(b - 1) x + (b + 1) y
\end{align}
$$

Same thing happens here: $n - s$ is always divisible by $b + 1$.


### Hard cases

Decimal doesn't have a "hard" case until seven; dozenal has one as early as five.  I basically reverse-engineered the decimal rule for seven to figure out the rest.

Let's play with my rule for five (multiply the last digit by two, and subtract from the rest of the number) and see what happens.

$$
\begin{align}
n & = 10 x + y \\
s & = x - 2 y \\
2 n + s = 2 (10 x + y) + (x - 2 y) = 21 x
\end{align}
$$

Aha.  21 is twenty-five, which is divisible by the number we're interested in, five.  So $2n + s$ is always divisible by five.  If $s$ is also divisible by five, then $2n$ must be...  and the 2 isn't contributing to divisibility here, so the original number must also be divisible by five.

I came up with this by looking for a number $c$ that would work out nicely:

$$
\begin{align}
n & = 10 x + y \\
s & = x + c y \\
c n - s & = (10 c - 1) x \\
s - c n & = (-10 c + 1) x
\end{align}
$$

For either of those expressions to be divisible by five, I need a number ending in either 1 or B that's a multiple of five.  I listed out the multiples of five until I found one: 5, A, 13, 18, 21, aha!  That gives me $c = -2$.

This works for any (prime...ish...) number, though the values of $c$ start to get a little ridiculous if the number you want to test is very large.  I did come up with a divisibility rule for nineteen, for example, by counting multiples: 17, 32, 49, 64, 7B.  $c = 7$, and you just need to multiply the last digit by _seven_ and add it to the rest of the number, then repeat until you can tell whether it's a multiple of nineteen.  Yikes.

Also, note that the expressions above don't actually do any math with $10$, which is really $b$, the base you're working in.  Exactly the same approach would get you the decimal divisibility rule for seven — seven times three is twenty-one, so $c = -2$, and the rule is...  coincidentally, exactly the same as dozenal's rule for five.
