title: Dark corners of Unicode
date: 2015-09-12 20:39
category: blog
tags: web, unicode, typography, tech, popular

I'm assuming, if you are on the Internet and reading kind of a nerdy blog, that you know what Unicode is.  At the very least, you have a very general understanding of it — maybe "it's what gives us emoji".

That's about as far as _most_ people's understanding extends, in my experience, even among programmers.  And that's a tragedy, because Unicode has a lot of...  ah, _depth_ to it.  Not to say that Unicode is a terrible disaster — more that human language is a terrible disaster, and anything with the lofty goals of representing _all of it_ is going to have some wrinkles.

So here is a collection of curiosities I've encountered in dealing with Unicode that you generally only find out about through experience.  Enjoy.

Also, I **strongly** recommend you install the [Symbola](https://archive.org/download/Symbola/Symbola613.ttf) font, which contains basic glyphs for a vast number of characters.  They may not be pretty, but they're better than seeing the infamous Unicode lego.

<!-- more -->


## Some definitions

There are already plenty of introductions to Unicode floating around ([wikipedia](https://en.wikipedia.org/wiki/Unicode), [nedbat](http://nedbatchelder.com/text/unipain.html), [joel](http://www.joelonsoftware.com/articles/Unicode.html)), and this is not going to be one.  But here's a quick refresher.

_Unicode_ is a big table that assigns numbers (_codepoints_) to a wide variety of characters you might want to use to write text.  We often say "Unicode" when we mean "not ASCII", but that's silly since of course all of ASCII is also included in Unicode.

_UTF-8_ is an encoding, a way of turning a sequence of codepoints into bytes.  All Unicode codepoints can be encoded in UTF-8.  ASCII is also an encoding, but only supports 128 characters, mostly English letters and punctuation.

A _character_ is a fairly fuzzy concept.  Letters and numbers and punctuation are characters.  But so are Braille and frogs and halves of flags.  Basically a thing in the Unicode table somewhere.

A _glyph_ is a visual representation of some symbol, provided by a font.  It might represent a single character, or it might represent several.  Or both!

Unicode is divided into seventeen _planes_, numbered zero through sixteen.  Plane 0 is also called the Basic Multilingual Plane, or just _BMP_, so called because it contains the alphabets of most modern languages.  The other planes are much less common and are sometimes informally referred to as the _astral planes_.


## Everything you know about text is wrong

If the only written languge you're familiar with is English, that goes doubly so.

Perhaps you want to sort text.  A common enough problem.  Let's give this a try in Python.  To simplify things, we'll even stick to English text.

    :::python-console
    >>> words = ['cafeteria', 'caffeine', 'café']
    >>> words.sort()
    >>> words
    ['cafeteria', 'caffeine', 'café']

Oops.  Turns out Python's sorting just compares by Unicode codepoint, so the English letter "é" (U+00E9) is greater than the English letter "f" (U+0066).

Did you know the German letter "ß" is supposed to sort equivalently to "ss"?  Where do you sort the Icelandic letter "æ"?  What about the English ligature "æ", which is the same character?

What about case?  The Turkish dotless "ı" capitalizes to the familiar capital "I", but in Turkish, the lowercase of that is "ı" and the uppercase of "i" is "İ".  Is uppercase "ß" the more traditional "SS", or maybe "Ss", or the somewhat recent addition "ẞ"?

Or, how do you compare equality?  Is "ß" equal to "ss"?  Is "æ" equal to "ae"?  Is "é" equal to "é"?

Ah, you say!  I've heard about this problem and know how to solve it.  I can just throw _Unicode normalization_ at it, which will take care of combining characters and all that other nonsense.  I can even strip out all combining characters and have nice normal English text left, because for some reason I am under the impression that English text is "normal" and all else is "abnormal".

Sure, let's give that a try.

    :::python-console
    >>> import unicodedata
    >>> normalize = lambda s: ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    >>> 
    >>> normalize('Pokémon')
    'Pokemon'

Great, problem solved.

    :::python-console
    >>> normalize('ı')
    'ı'
    >>> normalize('æ')
    'æ'
    >>> normalize('ß')
    'ß'

Hmm.

    :::python-console
    >>> normalize('한글')
    '한글'
    >>> normalize('イーブイ')
    'イーフイ'

Uh oh.

Yes, it turns out that Unicode decomposition _also_ decomposes Hangul (the alphabet used to write Korean) into its sub-components, which then may or may not still even render correctly, as well as splitting the diacritics off of Japanese kana, which significantly alters the pronunciation and meaning.  Almost as if Unicode decomposition was never meant to help programmers forcibly cram the entire world back into ASCII.

_Even_ if you only care about English text, there's more than one Latin alphabet in Unicode!  Is "x" equivalent to "𝗑" or "𝘅" or "𝘹" or "𝙭" or "𝚡" or "ｘ" or "𝐱"?  What about "×" or "х" or "⨯" or "ⅹ"?  Ah, sorry, those last four are actually the multiplication sign, a Cyrillic letter, the symbol for cross product, and the Roman numberal for ten.

This is a particularly aggravating problem because most programming languages have facilities for comparing and changing the case of text built in, and most of them are extremely naïve about it.  You can't even correctly change the case of English-looking text without knowing what locale it came from — the title-case of "istanbul" may actually be "İstanbul" depending on language, because of Turkish's dotted "i".

The only library I'm aware of off the top of my head for correctly dealing with any of these problems is [ICU](http://site.icu-project.org/), which is a hulking monstrosity hardly suited for shipping as part of a programming language.  And while their homepage does list a lot of impressive users, I've only encountered it in code I've worked on _once_.


## Combining characters and character width

Typically we think of combining characters as being the floating diacritical marks that can latch onto the preceding letter, such as using U+0301 COMBINING ACUTE ACCENT to make "q́", in case we are direly in need of it for some reason.  There are a few other combining "diacriticals" that aren't so related to language; for example, U+20E0 COMBINING ENCLOSING CIRCLE BACKSLASH can produce "é⃠", the universal symbol for "my software only supports English, and also I am not aware that English has diacritics too".  Or perhaps you'd use U+20E3 COMBINING ENCLOSING KEYCAP to make "é⃣" and indicate that the user should press their é key.

All of these have an impact on the "length" of a string.  You could write either of those "é" sequences with _three_ codepoints: the letter "e", the combining accent, and the combining border.  But clearly they each only contribute one _symbol_ to the final text.  This isn't a particularly difficult problem; just ignore combining characters when counting, right?

More interesting are the Unicode characters that are _not_ combining characters, but compose in some way in practice anyway.  The flag emoji, for example, don't actually exist in Unicode.  The Unicode Consortium didn't want to be constantly amending a list of national flags as countries popped in and out of existence, so instead they cheated.  They added a set of 26 [regional indicator symbols](https://en.wikipedia.org/wiki/Regional_Indicator_Symbol), one for each letter of the English alphabet, and to encode a country's flag you write its two-letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1) with those symbols.  So the Canadian flag, 🇨🇦, is actually the two characters U+1F1E8 REGIONAL INDICATOR SYMBOL LETTER C and U+1F1E6 REGIONAL INDICATOR SYMBOL LETTER A.  But if you put a bogus combination together, you _probably_ won't get a flag glyph; you'll get stand-ins for the characters instead.  (For example, 🇿🇿.)  So the "length" of a pair of these characters depends both on the display font (which may not support all flags), _and_ on the current geopolitical state of the world.  How's that for depending on global mutable state?

But _it gets better!_  There's a character called U+200D ZERO WIDTH JOINER, which is used to combine otherwise distinct characters in some languages (but has fairly general semantics).  Apple has made creative use of this character to compose _emoji_ together.  The report on emoji [has some examples](http://www.unicode.org/reports/tr51/index.html#ZWJ_Sequences).  So now the length of some text is completely arbitrary, based on whatever arbitrary ligatures the font includes.

To be fair, [that was already true anyway](http://www.sansbullshitsans.com/).  You might argue that the length of text in human terms is not actually all that interesting a quantity, and you'd be right, but that's why this section is about character _width_.  Because I'm typing in a terminal right now, and terminals fit all their text in a grid.

Let's return to the simpler world of _letters_ and revisit that Hangul example:

    :::python-console
    >>> normalize('한글')
    '한글'

Hangul characters are actually blocks composed of exactly three parts called Jamo.  (Here's [gritty detail on Hangul, Jamo, and Unicode](http://gernot-katzers-spice-pages.com/var/korean_hangul_unicode.html).  It's a really cool alphabet.)  Applying Unicode decomposition actually breaks each character down into its component Jamo, which are then _supposed_ to render exactly the same as the original.  They aren't marked as combining characters in the Unicode database, but if you have three of them in a row (arranged sensibly), you should only see one character.  The actual decomposition for the text above is "ㅎㅏㄴ ㄱㅡㄹ", written with separate characters that don't combine.  There are a good few languages that work this way — [Devanagari](https://en.wikipedia.org/wiki/Devanagari#Unicode) (the script used for Hindi et al.) and [Bengali](https://en.wikipedia.org/wiki/Bengali_alphabet#Unicode) rely heavily on character composition, and [Hebrew](https://en.wikipedia.org/wiki/Unicode_and_HTML_for_the_Hebrew_alphabet) uses it for rendering vowels.

And yet I ended up with four very different renderings.  In this blog post, with my default monospace font, I see the full sequence of six Jamo.  If I paste the same text somewhere with a proportional font, I see something very nearly identical to the original characters, albeit slightly fuzzier from being generated on the fly.  In Konsole, I see only the first Jamo for each character: `'ㅎㄱ'`.  (This has been [fixed](https://quickgit.kde.org/?p=konsole.git&a=commit&h=437440978bca1bd84e70ee61ba7974f63fe0630a) as of July 6, 2016, though I don't know what Konsole release contains the fix.)  And in my usual libvte-based terminal, the combining behavior falls apart, and I see a nonsensical mess that I can't even reproduce with Unicode:

![Screenshot of mangled Hangul in a terminal; several characters overlap](/media/2015-09/bad-hangul.png)

I can only guess at what happened here.  Clearly both terminals decided that each set of three Jamo was only one character wide, but for some reason they didn't combine.  Konsole adamantly refuses to render any Jamo beyond the first, even if I enter them independently; VTE dutifully renders them all but tries to constrain them to the grid, leading to overlap.

This is not the first width-related problem I've encountered with Unicode and terminals.  Consider emoji, which tend to be square in shape.  I might reasonably want to say to someone on IRC: "happy birthday! 🎁 hope it's a good one."  (That's U+1F380 WRAPPED PRESENT, if you didn't take my advice and install Symbola.)  But I use a terminal IRC client, and here's how that displays, in VTE and Konsole:

![Screenshot of the sentence in VTE; the birthday gift overlaps the following space](/media/2015-09/emoji-vte.png)

![Screenshot of the sentence in Konsole; the spacing is correct but the cursor position is wrong](/media/2015-09/emoji-konsole.png)

You can see how VTE has done the same thing as with Hangul: it thinks the emoji should only take up one character cell, but dutifully renders the entire thing, allowing the contents to spill out and overlap the following space.  You might think Konsole has gotten this one right, but look carefully — the final quote is slightly overlapping the cursor.  Turns out that Konsole will print each line of text as regular text, so any character that doesn't fit the terminal grid will misalign every single character after it.  The cursor (and selection) is always fit to the grid, so if you have several emoji in the same row, the cursor might appear to be many characters away from its correct position.  There are [several bugs open on Konsole](https://bugs.kde.org/show_bug.cgi?id=297390) about this, dating back many years, with no response from developers.  I actually had to stop using Konsole because of this sole issue, because I use ⚘ U+2698 FLOWER as my shell prompt, which misaligned the cursor every time.

All of these problems can be traced back to the same source: a POSIX function called `wcwidth`, which is intended to return the number of terminal columns needed to display a given character.  It exists in glibc, which sent me on a bit of a wild goose chase.  I originally thought that `wcwidth` must be reporting that the second and third Jamo characters are zero width, but this proved not to be the case:

    :::python-console
    >>> libc.wcwidth(c_wchar('\u1100'))  # initial Jamo
    2
    >>> libc.wcwidth(c_wchar('\u1161'))  # second Jamo
    1

Well, it seems Konsole actually [implements its own `wcwidth`](https://projects.kde.org/projects/kde/applications/konsole/repository/revisions/master/entry/src/konsole_wcwidth.cpp) which appears to be based on [this original implementation](http://www.cl.cam.ac.uk/~mgk25/ucs/wcwidth.c).  Both versions preserve an innocuous comment that explains quite a lot:

> Hangul Jamo medial vowels and final consonants (U+1160-U+11FF) have a column width of 0.

Aha.  So Konsole saw that the second and third Jamo took zero space, so it didn't bother trying to print them at all.

Then what the hell is VTE doing?  It [defers to some utility functions](https://github.com/GNOME/vte/blob/ecaf60ddab5e2c7c84e245fdce987fea7a51e24e/src/vte.cc#L201) in `glib` (GNOME's library of...  stuff), such as [`g_unichar_iszerowidth`](https://github.com/GNOME/glib/blob/9acd0ddbf3c0f14e6ae7cb3f7faf4c24767f13b8/glib/guniprop.c#L406), which...  explicitly says yes for everything between U+1160 and U+1200.  Wouldn't you know it, those are the secondary and tertiary Jamo characters.  So VTE saw that they took zero space, so it didn't make any extra room for them, but still tried to print them.  I expect they didn't combine in VTE because VTE has no idea they're _supposed_ to combine, so it printed each one individually.

Oh, but this madness gets even better.  WeeChat, another terminal IRC client, [outright strips emoji](https://github.com/weechat/weechat/issues/79), everywhere.  This is apparently the fault of...  [glibc's implementation of `wcwidth`, which defaults to 1 for printable characters and 0 otherwise](http://stackoverflow.com/a/23533623/17875), which requires knowing what the characters _are_, which oops doesn't work so well when glibc was using a vendored copy of the (pre-emoji) Unicode 5.0 database until glibc 2.22, which was [released _less than a month ago_](https://www.sourceware.org/ml/libc-alpha/2015-08/msg00609.html).

Beloved SSH replacement mosh has a [similar problem](https://github.com/mobile-shell/mosh/issues/234), in this case blamed on the `wcwidth` implementation shipped with _OS X_.  Gosh, I thought Apple was on the ball with Unicode.

We're now up to at least four mutually incompatible and differently broken versions of this same function.  Lovely.

I might be on the fringe here, but I'm pretty adamant that having a communication program silently and invisibly eat parts of your text is a **bad thing**.

While I'm at it: why are emoji left with a width of 1?  They tend to be drawn to fit a square, just like CJK characters (which are why we need double-width character support in the first place), and they're even of Japanese origin.  My rendering problems would go away in _both_ terminals if they used widths of 2.  Hell, I'm going to go file bugs on both of them right now.


## You will not go to space today

Sometimes you care about whitespace.  Perhaps you're using it to separate words.  In, say, a programming language.  [Like JavaScript](http://stackoverflow.com/questions/31507143/why-does-2-40-equal-42).

    :::javascript
    alert(2+ 40);

JavaScript's syntax defers the decision of what counts as whitespace to the Unicode database, which assigns a `WSpace` property to a handful of codepoints.  Seems like a good approach, except for this one unusual exception: " " is a space character, U+1680 OGHAM SPACE MARK.  [Ogham](https://en.wikipedia.org/wiki/Ogham) is an alphabet used in older forms of Irish, and its space character generally renders as a line.  Surprise!

Complicating this somewhat further, there are actually _two_ definitions of whitespace in Unicode.  Unicode assigns every codepoint a category, and has three categories for what sounds like whitespace: "Separator, space"; "Separator, line"; and "Separator, paragraph".

If you're familiar with Unicode categories, you might be tempted to use these to determine what characters are whitespace.  Except that CR, LF, tab, and even vertical tab are all categorized as "Other, control" and not as separators.  You might think that at least LF should count as a line separator, but no; the only character in the "Separator, line" category is U+2028 LINE SEPARATOR, and the only character in "Separator, paragraph" is U+2029 PARAGRAPH SEPARATOR.  I have never seen either of them used, ever.  Thankfully, all of these have the `WSpace` property.

As an added wrinkle, the lone oddball character "⠀" renders like a space in most fonts.  But it's not whitespace, it's not categorized as a separator, and it doesn't have `WSpace`.  It's actually U+2800 BRAILLE PATTERN BLANK, the Braille character with none of the dots raised.  (I say "most fonts" because I've occasionally seen it rendered as a 2×4 grid of open circles.)  Everything is a lie.


## JavaScript has no string type

JavaScript's "String" type ([or "string" type?](http://stackoverflow.com/questions/2051833/difference-between-the-javascript-string-type-and-string-object)) is not actually a string type.  Observe:

    :::javascript
    var bomb = "💣";
    console.log(bomb.length);  // 2

That's a string containing a single character, U+1F4A3 BOMB.  Yet JavaScript thinks it contains two!  What on earth is going on here?  Let's see what JavaScript thinks those two characters are, using `charCodeAt`.

    :::javascript
    console.log(bomb.charCodeAt(0).toString(16));  // d83d
    console.log(bomb.charCodeAt(1).toString(16));  // dca3

These aren't actually characters.  Everything from U+D800 through U+DFFF is permanently reserved as a non-character for the sake of encoding astral plane characters in UTF-16.  The short version is that all BMP characters are two bytes in UTF-16, and all astral plane characters are two of these non-characters (called a surrogate pair) for a total of four bytes.

JavaScript's string type is backed by a sequence of unsigned 16-bit integers, so it can't hold any codepoint higher than U+FFFF and instead splits them into surrogate pairs.  I argue that a string isn't a string if it can't hold a sequence of arbitrary characters, and JavaScript strings can't directly contain astral plane characters, so they don't qualify.

I rag on JavaScript, but this is an old problem.  C strings (well, `char*`) are just sequences of bytes, so you can't fit more than Latin-1.  Some libraries have historically tried to address this with "wide strings", `wchar_t*`, but the size of `wchar_t` is implementation-defined and 16 bits on Windows, where the entire OS API has the same problem as JavaScript.

Arguably, 16-bit faux strings are _worse_ than 8-bit faux strings.  It becomes pretty obvious pretty quickly that 8 bits is not enough to fit more than some European alphabets, and anyone but the most sheltered programmer is forced to deal with it the first time they encounter an em dash.  But 16 bits covers the entire BMP, which contains all current languages, some ancient languages, dingbats, mathematical symbols, and tons of punctuation.  So if you have 16-bit faux strings, it's very easy to _think_ you have all of Unicode automatically handled and then be sorely mistaken.  Thankfully, the increasing availability and popularity of emoji, which are mostly not in the BMP (but see below), makes astral plane support a more practical matter.

This probably all dates back to the original design of Unicode, which assumed that we'd never possibly need any more than 65,536 different characters and promised that two bytes would be enough for everyone.  Oops.

(This is the same reason that Chinese hanzi and Japanese kanji are merged into a single set of codepoints: they're both _huge_ alphabets and it was the only way to fit them both into two bytes.  This is called Han unification, and I have seen it _end friendships_, so I prefer not to discuss it further.)

One more trivium: MySQL has a `utf8` encoding, and it's generally regarded as best practice to use that for all your text columns so you can store Unicode.  But, oops, MySQL arbitrarily limits it to three bytes per character, which isn't enough to encode most astral plane characters!  What a great technical decision and not at all yet another thorn in the unusable sinkhole that is MySQL.  Version 5.5 introduced a `utf8mb4` encoding that fixes this, so have fun `ALTER`ing some multi-gigabyte tables in production.


## There's no such thing as emoji

I exaggerate _slightly_.

The word "emoji" is generally used to mean "any character that shows as a colored picture on my screen", much like the word "Unicode" is generally used to mean "any character not on my US QWERTY keyboard".  So what characters qualify as emoji?

There's actually no Unicode block called "emoji".  The set of smiley faces is in a block called [Emoticons](https://codepoints.net/emoticons), and most of the rest are in [Miscellaneous Symbols and Pictographs](https://codepoints.net/miscellaneous_symbols_and_pictographs) and [Transport and Map Symbols](https://codepoints.net/transport_and_map_symbols).

The Unicode Consortium has a [technical report about emoji](http://www.unicode.org/reports/tr51/index.html), which should be an immediate hint that this is not a trivial matter.  In fact the report defines [two levels of emoji](http://www.unicode.org/reports/tr51/index.html#Emoji_Levels), and look at how arbitrary these definitions are:

> emoji character — A character that is recommended for use as emoji.
>
> level 1 emoji character — An emoji character that is among those most commonly supported as emoji by vendors at present.
>
> level 2 emoji character — An emoji character that is not a level 1 emoji character.

So emoji are defined somewhat arbitrarily, and even based on what's treated as an emoji in the wild.

It's tempting to just say that those few astral plane blocks are emoji, but you might be surprised at what else qualifies sometimes.  There's also a [data table listing emoji levels](http://www.unicode.org/Public/emoji/latest/emoji-data.txt), and it classifies as emoji a good handful of arrows and dingbats and punctuation, even though they've been in Unicode for many years.  🃏 U+1F0CF PLAYING CARD BLACK JOKER is a level 1 emoji, but nothing else in the entire [Playing Cards](https://codepoints.net/playing_cards) block qualifies.  Similarly, 🀄 U+1F004 MAHJONG TILE RED DRAGON is the only representative of [Mahjong Tiles](https://codepoints.net/mahjong_tiles), and [Domino Tiles](https://codepoints.net/domino_tiles) aren't represented at all.

I stress, also, that a colored graphic _is not_ the only way emoji (however you define them) may be rendered.  Here's a screenshot of part of that table on my desktop:

![Screenshot of emoji rendered as simple outlines](/media/2015-09/monochrome-emoji.png)

That font is Symbola, which only has monochrome vector glyphs.  So they're no different than any other character.

I've been seeing an increasing trend lately of treating emoji as somehow completely unique.  The IM programs WhatsApp and Telegram both use Apple's emoji font _on every platform_, and I've seen even technically-inclined people passionately argue that this is a good state of affairs, because it means both parties will see exactly the same pixels.  Wouldn't want to confuse anyone by having them see a slightly different image of a steak!  (You'd think that's what sending images is for, but what do I know.)

This is somewhat troubling to me.  The _entire point_ of having these symbols exist in Unicode is so they can be transferred between different systems and treated just like any other text, _because now they're just text_.  They aren't special in any way (besides being in an astral plane, I suppose), and there's no reason you couldn't construct an emoji font that displayed regular English characters as graphics.  Hell, if you're using Firefox, [here's a demo of SVG embedded in an OpenType font](https://people.mozilla.org/~jkew/opentype-svg/soccer.html) that displays the letter "o" as an animated soccer ball.


## Interesting characters

To wrap this up, here are some obscure characters I've had reason to use at times and think are interesting.

[Control Pictures](https://codepoints.net/control_pictures) is an entire block of _visual representations_ of control characters.  So if you want to indicate there's a NUL byte, instead of writing out "NUL" or "\x00", you can use ␀ U+2400 SYMBOL FOR NULL.  I've actually found it fairly useful once or twice to use ␤ U+2424 SYMBOL FOR NEWLINE to display multi-line text in a way that fits in a single line!  I like it so much that I added a compose key shortcut for it: compose, n, l.

Ruby characters are annotations used with Chinese and Japanese text to explain pronuncuation, like the tiny characters here: <ruby><rb>日本語</rb><rp>（</rp><rt>にほんご</rt><rp>）</rp></ruby>.  Usually they're expressed with HTML's `<ruby>` tag, but outside of HTML, what are you to do?  Turns out Unicode actually supports this in the form of three "interlinear annotation" characters, and you could write the above as "`[U+FFF9]`日本語`[U+FFFA]`にほんご`[U+FFFB]`".  They tend not to have any rendering in fonts, since they're control characters, and Unicode actually recommends they not be exposed directly to users at all, so there are no rules for how to actually display them.  But if you want to _store_ annotated Chinese or Japanese text without pretending all text is HTML, there you go.

More well-known are U+200E LEFT-TO-RIGHT MARK and U+200F RIGHT-TO-LEFT MARK, which are part of the [byzantine Unicode bi-directional text system](https://en.wikipedia.org/wiki/Bi-directional_text#Unicode_bidi_support), but among English speakers are mainly known for being able to reverse text in unsuspecting websites.

All the way back in humble ASCII, U+000C FORM FEED can be used to encode a page break in plain text.  veekun's database uses form feeds to mark where the Pokédex flavor text in Gold, Silver, and Crystal breaks across two pages.

Finally, here are some of my favorite Unicode blocks, good places to look for interesting squiggles.  Especially if, say, you're making a [text-based game](https://github.com/eevee/flax).

* [Arrows](https://codepoints.net/arrows): ↹ ⇝ ↻ ↯
* [Mathematical Operators](https://codepoints.net/mathematical_operators): ≈ ∞ ∀ ⊕ ⊠
* [Miscellaneous Technical](https://codepoints.net/miscellaneous_technical): ⌘ ⌚ ⌛ ⌨ ⏣ ⏏
* [Box Drawing](https://codepoints.net/box_drawing) and [Block Elements](https://codepoints.net/block_elements): ╟─╢ ░ ▒ ▓
* [Geometric Shapes](https://codepoints.net/geometric_shapes) and [Geometric Shapes Extended](https://codepoints.net/geometric_shapes): ◎ 🞋 ◭ ▸ ▢ 🞠 🞴
* [Miscellaneous Symbols](https://codepoints.net/miscellaneous_symbols), containing:
    - weather symbols: ☀ ☁ ☂ ☃ ☄
    - playing card suits: ♡ ♢ ♤ ♧ ♥ ♦ ♠ ♣
    - planetary and astrological symbols: ☿ ♀ ♁ ♂ ♃ ♄ ♅ ♆ ♇ ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♒ ♓
    - chess pieces: ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟
    - dice: ⚀ ⚁ ⚂ ⚃ ⚄ ⚅
    - musical symbols: ♩ ♪ ♫ ♬ ♭ ♮ ♯
    - and other goodness: ⚢ ⚠ ☠ ☢ ☮ ☭ ⚰ ⚘ ⚙ ♲ ⛤ ⛓ ⛏
* [Dingbats](https://codepoints.net/dingbats): ✭ ❁ ❄ ➤ ➠ ✎
* [Mahjong Tiles](https://codepoints.net/mahjong_tiles): 🀀 🀟 🀩
* [Domino Tiles](https://codepoints.net/domino_tiles): 🀳🁃🂃🁐
* [Playing Cards](https://codepoints.net/playing_cards): 🂪 🂫 🂭 🂮 🂡
* [Alchemical Symbols](https://codepoints.net/alchemical_symbols): 🜱 🜲 🜻

Creating this list has made me realize that codepoints.net is not actually a very nice way to browse by block or copy-paste a lot of characters.  There's [fileformat.info](http://www.fileformat.info/info/unicode/), if you weren't aware, but it's kind of barebones and clumsy.  And most Unicode blocks have Wikipedia articles.  But overall, everything is uniquely terrible; welcome to computers.
