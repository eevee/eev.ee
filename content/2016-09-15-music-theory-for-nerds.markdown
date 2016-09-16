title: Music theory for nerds
date: 2016-09-15 19:29
category: blog
tags: music, math

Not _music_ nerds, obviously.

I don't know anything about music.  I know there are letters but sometimes the letters have squiggles; I know an octave doubles in pitch; I know you can write a pop song with only [four chords](https://www.youtube.com/watch?v=oOlDewpCfZQ).  That's about it.

The rest has always seemed completely, utterly arbitrary.  Why do we have twelve notes, but represent them with only seven letters?  Where did the key signatures come from?  Why is every Wikipedia article on this impossible to read without first having read all the others?

A few days ago, some of it finally clicked.  I feel like an idiot for not getting it earlier, but I suppose it doesn't help that everyone explains music using, well, _musical notation_, which doesn't make any sense if you don't know why it's like that in the first place.

Here is what I gathered, from the perspective of someone whose only music class was learning to play four notes on a recorder in second grade.  I stress that I don't know anything about music and this post is terrible.  If you you so much as know how to whistle, please don't read this you will laugh at me.


<!-- more -->

## Sound and waves

Music is a kind of sound.  Sound is a pressure wave.

Imagine what happens when you beat a drum.  The drumhead is elastic, so when you hit it, it deforms inwards, then rebounds outwards, then back inwards, and so on until it runs out of energy.  If you watched a point in the center of the drumhead, its movement would look a lot like what you get when you hold a slinky by the top and let the bottom go.

When the drumhead rebounds outwards, it pushes air out of the way.  That air pushes more air out of the way, which pushes more air out of the way, creating a 3D ripple leading away from the drum.  Meanwhile, the drumhead has rebounded back inwards, leaving a vacuum which nearby air rushes to fill...  which leaves another vacuum, and so on.  The result is that any given air molecule is (roughly) drifting back and forth from its original position, just like the drumhead or the slinky.

Eventually this pressure wave reaches your eardrum, which vibrates in exactly the same way as the drumhead, and you interpret this as music.  Or perhaps as noise, depending on your taste.

I would love to provide an illustration of this, but the trouble is that it would look like ripples on a pond, where the wave goes _upwards_.  Sound happens in _three_ dimensions, the movement is directed towards/away from the source, and I think that's a pretty important distinction.

Instead, let's jump straight to the graphs.  Here's a sine wave.

<div class="prose-full-illustration" markdown="1">
![Graph of a sine wave.  Frequency is labeled as the horizontal distance between waves; amplitude is labeled as the vertical distance between the highest and lowest points.]({filename}/media/2016-09-15-music/sine-wave.png)
</div>

It doesn't matter what a sine wave _is_; it just happens to be a common wave that's easy to make a graph of.

In graphs like this, time starts at zero and increases to the right, and the wave shows how much the air (or your eardrum, or whatever medium) has moved from its original position.  Complete silence would be a straight line at zero, all the way across.

All sound you ever hear is a graph like this; nothing more.  If you open up a song in Audacity and zoom in enough, you'll see a wave.  It'll probably be a bit more complicated, but it's still a wave.

Waves are defined by a couple of things: frequency, amplitude, and shape.  The particular sound you hear — the thing that distinguishes a guitar from a violin — is the shape of the wave, which musicians call _timbre_.

A sine wave sounds something like this: <audio src="{filename}/media/2016-09-15-music/sine-wave.ogg" type="audio/ogg" controls><a href="{filename}/media/2016-09-15-music/sine-wave.ogg">(sine-wave.ogg, 11.7KiB)</a></audio>

Amplitude is the distance between the lowest and highest points of the wave.  Or, depending on who you ask, it might be half that — the distance between the highest point and zero.  For sound, amplitude determines the _volume_ of the sound you hear.  This seems pretty reasonable, since in physical terms, amplitude is the furthest distance the medium moves.  If you tap a drum lightly, it only moves very slightly, and the sound is quiet.  If you wail on a drum, it moves quite a bit, and the sound is much louder.

Frequency is, quite literally, how frequent the wave is.  If each wave is very skinny, then waves are more frequent, i.e. they have a higher frequency.  If each wave is fairly wide, then waves are less frequent, and they have a lower frequency.  Musicians refer to frequency as _pitch_.  Non-musicians would probably just call it a _note_ or _tone_, which musicians would scoff at, but what do they know anyway.

Frequency is measured in Hz (Hertz), which is a funny way of spelling "per second".  If it takes half a second to get from one point on a wave back to the same point on the next wave, that's 2 Hz, because there are two waves per second.  The sound above has a frequency of 440 Hz.  (The graph, of course, does not; it's a completely unchanged sine wave generated by wxMaxima, so its frequency is 1/τ = 1/(2π).)

A critical property of the human ear, which informs all the rest of this, is that if you _double_ or _halve_ the frequency of a sound, we consider it to be "the same" in some way.  Obviously, the result will sound higher- or lower-pitched, but they "feel" very similar.  I can take a few guesses at the physical reasons for this, but we can treat it as an arbitrary rule.

Compare these three sine waves, if you like.  The first is the same as the sine wave from earlier; the second has 1.5× the frequency of the first; the third has 2× the frequency of the first.  The first and third sound much more related than the second sounds to either.

- 440 Hz: <audio src="{filename}/media/2016-09-15-music/sine-wave.ogg" type="audio/ogg" controls><a href="{filename}/media/2016-09-15-music/sine-wave.ogg">(sine-wave.ogg, 11.7KiB)</a></audio>
- 660 Hz: <audio src="{filename}/media/2016-09-15-music/sine-wave-1.5.ogg" type="audio/ogg" controls><a href="{filename}/media/2016-09-15-music/sine-wave-1.5.ogg">(sine-wave-1.5.ogg, 13.1KiB)</a></audio>
- 880 Hz: <audio src="{filename}/media/2016-09-15-music/sine-wave-2.ogg" type="audio/ogg" controls><a href="{filename}/media/2016-09-15-music/sine-wave-2.ogg">(sine-wave-2.ogg, 13.7KiB)</a></audio>


## Notes and octaves

The difficulty with music is that half of it is arbitrary and half of it is actually based on something, but you can't tell the difference just by looking at it.

Let's start with that fact about the human ear: doubling the pitch (= frequency) will sound "the same" in some indescribable way.  For any starting pitch _f_, you can thus generate an infinite number of other pitches that sound "the same" to us: _½f_, _2f_, _¼f_, _4f_, and so on.  (Of course, only so many of these will fit within the range of human hearing.)  All of those pitches together have some common quality, so let's refer to a group of them as a _note_.  ("Note" can also refer to an individual pitch, whereas _pitch class_ is unambiguous, but I'll stick with "note" for now.)

If we say 440 Hz produces a note called A, then 880 Hz, 220 Hz, 1760 Hz, 110 Hz, and so forth will also produce a note called A.  An important consequence of this is that _all_ distinct notes we could possibly come up with _must_ exist somewhere between 440 Hz and 880 Hz.  Any other pitch could be doubled or halved until it lies in that range, and thus would produce a note in that range.

Such a range is called an _octave_, for reasons we'll see in a moment.  Every note exists exactly once within any given octave, no matter how you define it.  As a special case, the lowest pitch _f_ is the same note as the highest pitch _2f_, so _2f_ is considered to be part of the next octave.

This is good news!  It means we can choose some pitches within a small range — _any_ small range, so long as it's of the form _f_ to _2f_ — and by doubling and halving those pitches, we'll have a standard set of notes spanning the entire range of human hearing.

How, then, do we choose those pitches?  You might say, well!  Since we're going from _f_ to _2f_ anyway, let's just choose pitches at _f_, _1.1f_, _1.2f_, _1.3f_, _1.4f_, and so on.  Space them equally, so they're as distinct as possible.

Good plan!  Unfortunately, that won't quite work — if you try it, you'll find that the difference between _f_ and _1.1f_ is almost twice the difference between _1.9f_ and _2f_.

The human ear distinguishes pitch based on _ratios_, which is why the halving/doubling effect exists.  _f_ to _1.1f_ is an increase of 10%; _1.9f_ to _2f_ is an increase of about 5%.

We need a set of pitches that have the same _ratio_ rather than the same difference.  If we want _n_ pitches, then we need a number that can be multiplied _n_ times to get from _f_ to _2f_.

_f × x × x × x × ... × x = 2f_  
_fxⁿ = 2f_
_xⁿ = 2_
_x = ⁿ√2_

Ah.  We need the _n_-th root of two.  That's a bit weird and awkward, since it's guaranteed to be irrational for any _n_ > 1.


## Intervals in Western music

Western music has twelve distinct pitches.  This is _somewhat_ arbitrary — twelve has a few nice mathematical properties, but it's not absolutely necessary.  You could create your own set of notes with eleven pitches, or seventeen, or a hundred, or five.  There are forms of music elsewhere in the world that do just that.

The ratio between successive pitches in Western music is thus the twelfth root of two, ¹²√2 ≈ 1.0594631.  Starting at 440 Hz and repeatedly multiplying by this value produces twelve pitches before hitting 880 Hz.

    0    440 Hz
    1    466.16 Hz
    2    493.88 Hz
    3    523.25 Hz
    4    554.36 Hz
    5    587.33 Hz
    6    622.25 Hz
    7    659.26 Hz
    8    698.46 Hz
    9    739.99 Hz
    10   783.99 Hz
    11   830.61 Hz
    12   880 Hz

No one wants to actually work with these numbers — and when this system was invented, no one knew what these numbers were.  Instead, music is effectively defined in terms of ratios.

The ratio between two pitches is called an _interval_, and an interval of one twelfth root of two is a _semitone_.  This way, all the horrible irrational numbers go out the window, and we can mostly talk in whole numbers.

(What we're really doing here is working on a logarithmic scale.  I know "logarithm" strikes fear into the hearts of many, but all it means is that we say "add" to mean "multiply".)

Now, remember, the human ear loves ratios.  It particularly loves ratios of small whole numbers — that's why doubling the pitch sounds "similar", because it creates a ratio of 2:1, the smallest and whole-number-est you can get.

The twelfth root of two may be irrational, but it turns out to _almost_ create several nice ratios.  (I don't know why twelve in particular has this effect, or if other roots do as well, but it's probably why Western music settled on twelve.)  Here are the pitches of all twelve notes, relative to the first.  Some of them are _very_ close to simple fractions.

    0    1.000          = 1:1   (unison)
    1    1.059                  (semitone; minor second)
    2    1.122  ≈ 1.125 = 9:8   (whole tone; major second)
    3    1.189                  (minor third)
    4    1.260  ≈ 1.250 = 5:4   (major third)
    5    1.335  ≈ 1.333 = 4:3   (perfect fourth)
    6    1.414
    7    1.498  ≈ 1.500 = 3:2   (perfect fifth)
    8    1.587                  (minor sixth)
    9    1.682  ≈ 1.667 = 5:3   (major sixth)
    10   1.782                  (minor seventh)
    11   1.888  ≈ 1.889 = 17:9  (major seventh)
    12   2              = 2:1   (octave)

Not counting the octave, there are seven fairly nice fractions here.

Hmm.  _Seven_.  What a conspicuous number.


## Scales

Surprise!  Those nice fractions make up the _major scale_.  Starting with C produces the _C major scale_ — the "natural" notes.  Using ♯ to mean "one semitone up" and ♭ to mean "one semitone down", we can name all of these notes.

    0    1.000          = 1:1   C           (unison)
    1    1.059                  C♯ or D♭    (semitone; minor second)
    2    1.122  ≈ 1.125 = 9:8   D           (whole tone; major second)
    3    1.189                  D♯ or E♭    (minor third)
    4    1.260  ≈ 1.250 = 5:4   E           (major third)
    5    1.335  ≈ 1.333 = 4:3   F           (perfect fourth)
    6    1.414                  F♯ or G♭
    7    1.498  ≈ 1.500 = 3:2   G           (perfect fifth)
    8    1.587                  G♯ or A♭    (minor sixth)
    9    1.682  ≈ 1.667 = 5:3   A           (major sixth)
    10   1.782                  A♯ or B♭    (minor seventh)
    11   1.888  ≈ 1.889 = 17:9  B           (major seventh)
    12   2              = 2:1   C           (octave)

I don't know for sure if this is where the modern naming convention came from, but I sure wouldn't be surprised.

You can now see where some of those interval names came from.  A _perfect fifth_ is the interval between the first and fifth notes of the scale.  An _octave_ spans eight notes in total.  Likewise, the smallest interval is a semitone because most of the notes are two steps apart, so that distance became a whole tone.

The intervals between successive notes can be written as _wwhwwwh_, where _w_ is a whole tone and _h_ is a semitone or half tone.  Because octaves repeat, you can rotate this sequence to produce seven different variations, depending on where you start.  The resulting scales are all called _diatonic scales_, and the choice of starting point is called a _mode_.  Here are all seven, marked by Roman numerals indicating the start point.  I've also chosen different starting notes for each column, so that the resulting notes are all "natural".

                        I  II  III  IV  V  VI  VII
    0    1.000  = 1:1  |C|  D   E   F   G  |A|  B
    1    1.059         | |      F          | |  C
    2    1.122  ≈ 9:8  |D|  E       G   A  |B|  
    3    1.189         | |  F   G          |C|  D
    4    1.260  ≈ 5:4  |E|          A   B  | |  
    5    1.335  ≈ 4:3  |F|  G   A       C  |D|  E
    6    1.414         | |          B      | |  F
    7    1.498  ≈ 3:2  |G|  A   B   C   D  |E|  
    8    1.587         | |      C          |F|  G
    9    1.682  ≈ 5:3  |A|  B       D   E  | |  
    10   1.782         | |  C   D       F  |G|  A
    11   1.888  ≈ 17:9 |B|          E      | |  
    12   2      = 2:1  |C|  D   E   F   G  |A|  B

I've, er, highlighted two columns.  Column I produces the _major scales_, and column VI produces the _natural minor scales_.  This explains the rest of the interval names: a _minor third_ is the span between the first and third notes in a minor scale, whereas a _major third_ is the span between the first and third notes in a major scale.  The fourth and fifth notes are the same.  (The second notes are the same, too, so I don't know where "minor second" came from.)

You can start anywhere you want to produce a major or minor scale, as long as you follow the same patterns of intervals.  With twelve notes, there are twenty-four major and minor scales altogether, which would make for a big boring diagram.  Here are a few of the major scales.

    A major:    A       B       C#  D       E       F#      G#  A
    A# major:   A#      C       D   D#      F       G       A   A#
    B major:    B       C#      D#  E       F#      G#      A#  B
    C major:    C       D       E   F       G       A       B   C
    C# major:   C#      D#      F   F#      G#      A#      C   C#
    D major:    D       E       F#  G       A       B       C#  D
    D# major:   D#      F       G   G#      A#      C       D   D#

If you rotate those major scales to start from C, they look like this.

    A major:        C#  D       E       F#      G#  A       B       C#
    A# major:   C       D   D#      F       G       A   A#      C
    B major:        C#      D#  E       F#      G#      A#  B       C#
    C major:    C       D       E   F       G       A       B   C
    C# major:       C#      D#      F   F#      G#      A#      C   C#
    D major:        C#  D       E       F#  G       A       B       C#
    D# major:   C       D   D#      F       G   G#      A#      C

Here are some minor scales, written the same way.

    F# minor:       C#  D       E       F#      G#  A       B       C#
    G minor:    C       D   D#      F       G       A   A#      C
    G# minor:       C#      D#  E       F#      G#      A#  B       C#
    A minor:    C       D       E   F       G       A       B   C
    A# minor:       C#      D#      F   F#      G#      A#      C   C#
    B minor:        C#  D       E       F#  G       A       B       C#
    C minor:    C       D   D#      F       G   G#      A#      C

Hmmmm.  Yes, every major scale is equivalent to the minor scale starting from its second-to-last note, due to the way octaves wrap around.  They're called each other's _relative major_ and _relative minor_.

Also, this notation has a _slight_ problem.  That problem is that sheet music is terrible.


## Sheet music and key signatures

If you know anything about sheet music, you may have noticed that there are no spaces for writing flat or sharp notes.

If you don't know anything about sheet music, well, there are no spaces for writing flat or sharp notes.

If you want to put any of the other notes in, you keep them on the _same line_, but with a ♯ or ♭ next to them.  So the notes in D major, which includes F♯ and C♯, are written as though they were F and C, but with some extra ♯s scattered around.  That's not very convenient, so instead, you can put a _key signature_ at the very beginning — it takes the form of several ♯s or ♭s written in specific places to indicate which notes are sharp or flat.  Then any such unadorned note is considered sharp or flat.

{% photo /media/2016-09-15-music/sheet-music-1-c-major.png C major %}
{% photo /media/2016-09-15-music/sheet-music-2-d-major.png D major, written without a key signature %}
{% photo /media/2016-09-15-music/sheet-music-3-d-major-key-signature.png D major, written with a key signature %}

I...  guess...  that's convenient?  If your music _mostly_ relies on the seven notes from a particular scale, then it's more compact to only have room for seven notes in your sheet music, and adjust the meaning of those notes when necessary...  right?

It completely obscures the relationship between the pitches, though.  You can't even easily tell which scale some sheet music is in, short of memorization.  In the example above, there are ♯s for C and F; what about that is supposed to tell you "D"?

Anyway, I really only brought this up to make a point about notation.  Look at C♯ major again.

    C# major:   C#      D#      F   F#      G#      A#      C   C#

Two pairs of notes are using the same letter — C and C♯, F and F♯ — so they'd occupy the same position in sheet music.  That won't work with the scheme I just described.

To fix this, several scales fudge it a bit.  C is one semitone above B, so you could also write it as B♯.  F is one semitone above E, so you could also write it as E♯.  Here's how C♯ is actually written.

    C# major:   C#      D#     (E#) F#      G#      A#     (B#) C#

Now all seven letters are used exactly once.

I don't think I entirely understand this, because it still seems so convoluted to me.  You have to mentally translate that C to a C♯, and _then_ translate the C♯ to however that particular note is actually played on your instrument.What does this accomplish?

I suppose it's possible to change the sound of an entire piece of music just by changing the key signature, but does anyone actually do that?  How would that work for music that also uses notes outside the scale?  These seem more like questions of composition, which I definitely don't know anything about.


## Something, something

I'm a bit out in the weeds from here on.  C major is identical to A minor, and I don't understand why we need both.

You can construct the major and minor chords by taking the first, third, and fifth note of the major and minor scales.  C major is thus C, E, and G.  Seems like a slightly strange naming convention.

The "circle of fifths" is a thing, showing all the major and minor scales in a circle — it turns out that if you name and arrange them the right way, each scale has a different number of sharp or flat notes in it, and no scale has both sharps and flats.  Why do some have sharps and some have flats, rather than using the same scheme consistently?  I have no idea.

Oh, something slightly interesting happens when you compare the major and minor scale based on the same note.

    C major:    C       D       E   F       G       A       B   C
    C minor:    C       D   D#      F       G   G#      A#      C

They're very nearly identical, except that three notes are a semitone higher in the major scale.  Someone linked me an example of [Für Elise being played in A major](https://www.youtube.com/watch?v=Y-rZD2AsHbI), rather than the A minor it was written in.  (But then, if you played it in C major...  it would be the same.  Right?  Christ.)

Also, note with the "same name" might not actually be the same note, depending on how the instrument is tuned; there are various schemes that make certain notes _exact_ integer ratios, not just approximate ones.  And that's the extent of my knowledge there.

Oh, incidentally, integer ratios probably appeal to the human ear because they make waves line up every so often.  Here's what a perfect fifth looks like — the top two tones are A4 and E5, using the not-quite-perfect twelfth root of two.

<div class="prose-full-illustration" markdown="1">
![Two waveforms add together to make a regular, repeating pattern]({filename}/media/2016-09-15-music/perfect-fifth.png)
</div>

(A4 is the A note within octave 4.  Octave 4 starts at middle C, and both are named based on the layout of a piano.  A common reference point for tuning is to set A4 to 440 Hz.)

These are all the things that I know.  I don't know any more things.


## In conclusion

This has got to be some of the worst jargon and notation for anything, ever.

I only looked into this because I want to compose some music, and I feel completely blocked when I just don't understand a subject at all.  I'm not sure any of this _helped_ in any way, but at least now I'm not left wondering.  Mission accomplished.  I'm going to forget all of this, throw notes around at random, and see what sounds good.  Consensus seems to be that music is largely about handling contrast, just like anything else.

If you aren't quite as ready to give up, here's some stuff people linked to me while I was figuring this out in real time on Twitter.

- ["This Week's Finds in Mathematical Physics"](https://web.archive.org/web/20160722080401/http://math.ucr.edu/home/baez/week234.html), some stuff based in group theory
- ["Music"](http://tobyfox.net/Tutorials/musicdef.html), by Toby Fox, best known for creating the soundtrack to Undertale, and also the rest of Undertale; short and mostly lists the considerations
- ["Musimathics: The Mathematical Foundations of Music"](https://www.amazon.com/Musimathics-Mathematical-Foundations-Music-Press/dp/0262516551), a $33 book that several people recommended but that I have not yet bought
- ["How Music Really Works"](http://howmusicreallyworks.com/), a book that brags from the outset that it has no music notation, and offers the first six chapters free; reviews suggest it is particularly helpful for composing, so maybe I should read it sometime
- ["Combinatorial Music Theory"](http://andrewduncan.net/cmt/), some music theory that appears to have been written by a mathematician who's forgotten how to explain anything without heavy math notation
