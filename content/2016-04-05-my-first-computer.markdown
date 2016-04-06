title: My first computer
date: 2016-04-05 14:59
category: blog
tags: tech, patreon

This month — March, okay, today is March 36th — Vladimir Costescu is [sponsoring](https://www.patreon.com/eevee) an exciting post about:

> How about this: write about your very first computer (e.g. when you were a kid or whatever) and some notable things you did with it / enjoyed about it. If you've ever built your own computer from parts, feel free to talk about that too.

<!-- more -->

## My first computer

I could swear I've written about this before, but I can't find it, so it must've never escaped Twitter.

My _very very first_ computer was this bad boy, which I had when I was...  geez, I'm not even sure.  7, maybe?

{% photo /media/2016-04-05-precomputer/precomputer-1000.jpg %}

The VTech PreComputer 1000, from back in the days when "1000" still sounded futuristic.  It had a screen with one entire row of pixellated LCD characters, a qwerty keyboard complete with Caps Lock (?!), and a wide variety of trivia games.  Ran on _six_ C batteries.

I seem to recall that the behavior of Caps Lock was to _reverse_ the usual capitalization, by which I mean holding Shift while Caps Lock was on would produce lowercase characters.  Wild.  (**edit**: A _great many_ people have informed me that this is in fact how Windows always worked, which surprises me a lot, because I very distinctly remember being surprised by a real computer's behavior!  It seems that at least some combination of MS-DOS 6.22 and a particular keyboard model would ignore Shift when Caps Lock is on, so maybe that's what I remember.)

In a kind of precursor to DLC, there were also several extra cartridges you could buy.  They were about the size of a thick wallet and came with different sets of...  more trivia games.

Then there was the part that changed my life forever: a built-in BASIC interpreter.

It was a huge, huge pain in the ass.  I could only see or edit one line at a time, of course.  There was also no writable internal storage — this machine was released in 1988, when the idea of a video game that could save your progress was still novel! — so any program I wrote was lost as soon as I turned the thing off.

It did come with a book full of documentation and sample programs.  The documentation was helpful enough to get me to make some things, but perhaps not particularly well aimed at the target audience of 9-year-olds, as I remember there being several constructs I didn't understand in the slightest.  The sample programs weren't described particularly well, had no comments at all, and at the longest ran beyond 30 lines.  30 lines doesn't sound like a lot to me _now_, but it was the biggest program I'd ever seen at the time, and typing it all in on a one-line display was daunting.  (There were nine "canonical" sample programs baked into the ROM, but the programming tutorial had several lengthy examples that had to be typed in.)

I really wish I could find a copy of the book online, but it predates the web, alas!  This was all so long ago that I can't really remember any of the sample programs.  I want to say there was the usual "guess a number" game, a temperature converter, and maybe hangman?  Haven't the foggiest idea what kind of little programs I wrote from scratch, unfortunately.

I'm tempted to go find and buy one of these, partly for the nostalgia and partly to see how much I can convince a baby BASIC to do.  Mine might even still be in my parents' attic, if they haven't thrown it out by now.

While I resist the urge to scour ebay, let's move on a year or two.

### Addended interlude: the manual

Aha, a commenter has found [a post with a scan of the BASIC part of the manual](http://www.vintagecomputing.com/index.php/archives/324) (at the bottom)!  There are a lot of gems in here I'd forgotten about, like how switching to BASIC mode would _automatically_ turn Caps Lock on (something I remember hating, even as a kid).  I also fondly remember the goofy proportional font they used, even for code, that used a ∅-like glyph for zero.  I even spotted a missing semicolon in some example code that I could swear I'd noticed before.

I'm surprised to learn that there is some semblance of debugging available, though I doubt I understood it at the time — you could add a `STOP` statement to a program and it will halt there, returning you to the default REPL, where you could presumably print out variables or change lines of the running program.

Something that particularly fascinates me now is the error reporting.  A syntax error would be reported as `?SN ERROR`, and you would have to look at the list of error codes in the manual to find out that `SN` meant `SYNTAX ERROR`.  Why not just say `SYNTAX ERROR`, then?  This had me thinking that they adapted an existing BASIC interpreter rather than writing their own, and indeed, the errors have the same names as [MSX-BASIC's errors](https://www.msx.org/wiki/Category:MSX-BASIC_ERRORS).  Not sure where the two-letter codes came from, though.

I've copied [all the example programs into a gist](https://gist.github.com/eevee/3aee241c401314cc7fad9afd3a0efb29) for easier perusal.  Looking at them with a more seasoned programmer's eye, a few things stand out to me.

- There were clearly several different authors here!  Programs 6 and 9 are the only ones to start numbering from 100, to have `999 END` as their last line, to ask if the player wants to play again, and to only accept `YES` as an affirmative answer.  3 and 4 are the only two to use the `SOUND` statement, and both omit the space between the word `SOUND` and its first argument.  1 and 8 are the only programs to finish with an `END` that _doesn't_ use 999 as its line number.

- The `PRINT` statement accepted multiple arguments, separated by either semicolons _or_ commas, though the manual doesn't explain the difference (if any).  Program 1 stands out as the only program to manually insert a space at the end of a literal string followed by a variable.  The tutorial part of the manual implies that `PRINT` inserted spaces between its arguments automatically, which makes me wonder why this one program felt the need to add its own.  Program 8, seemingly by the same author, never prints two things on the same line.

- Program 4 appears to simulate a one-second delay with a 630-iteration empty loop.  There is, of course, nothing explaining why this is the case.  630 might have been my very first magic number.

- Program 8 is an implementation of [selection sort](https://en.wikipedia.org/wiki/Selection_sort)!  This is the only use of `DIM` — the statement for declaring an array — in the example programs.  I remember being very confused as to what `DIM` even did, let alone realizing the point of the program.  None of them have any kind of explanation or comments, except for a couple comments dividing up the rather long program 9.

- The only built-in functions used in any of these programs are `INT()` in program 9 and `RND()` in program 5.  None of the example programs demonstrate use of `FOR ... STEP`, `ABS()`, `SGN()`, `SQR()`, `LOG()`, `EXP()`, `SIN()`, `COS()`, `TAN()`, `ATN()`, `LEN()`, `STR$()`, `VAL()`, `LEFT$()`, `RIGHT$()`, `MID$()`, `ASC()`, `CHR$()`, `GOSUB ... RETURN`, `AND`, `NOT`, `READ`, `DATA`, or `RESTORE`.

- Program 9 implements the perfect single-pile Nim strategy.  If the player doesn't correctly decide whether to go first or second, or doesn't play perfectly, the computer will always win.


## My first actual computer

We got it in the mid-90s — a 486 DX running MS-DOS 6.22 and Windows 3.11 for Workgroups.  It screamed along at <s>25 MHz</s> 33 MHz, and if that wasn't enough for you, it had a _turbo button_ that would boost it all the way to 100 MHz!  I had to turn turbo off when I won at sol.exe, or else the card waterfall animation would play nearly instantly, but otherwise turning turbo off resulted in a hard lock and a loud angry endless beep.  Thanks to an upgrade, it also had 40MB of RAM.  _Nice._

It came with a huge CRT monitor with an incredible high-def resolution of 1280x1024.  (The full-size photo of the PreComputer above is 1024×801.)  It had a keyboard lock, too, which I eventually learned how to pick using a paperclip.  For reasons.

I distinctly remember its price tag of <s>$1999</s> $1995.  I didn't know what many things cost yet, nor did I have any sense of how much money people with jobs actually made, so that might as well have been "infinity dollars".  Twenty years later, you can buy a _phone_ that's orders of magnitude better than that computer for a third of the price.

Thanks to the power of the Internet, I actually managed to track down one of the original ads!  This is from [page 331 of the May 30, 1995 issue of PC Mag](https://books.google.com/books?id=elneMPYGaagC&pg=RA1-PA331&hl=en&sa=X&ved=0ahUKEwie1Oysz_rLAhVB_GMKHQo_BmsQ6AEIMTAF), courtesy of Google Books, which incredibly has a searchable index of quite a few old PC Mag issues.  That pins down the date we bought this to the summer of 1995, when I was 8 years old.  Damn, I remember those little speakers and that joystick too.

{% photo /media/2016-04-05-precomputer/fushigidane-ad.jpg %}

I graduated naturally from toy-computer-BASIC to a _real_ programming language: QBasic.  I first encountered it on school computers, and mostly enjoyed it for the fascinating sample programs, `nibbles.bas` ([Snake](https://en.wikipedia.org/wiki/Snake_%28video_game%29)) and `gorillas.bas` (a game where two large gorillas standing on skyscrapers try to throw exploding bananas at each other).  I remember scrolling through their source code numerous times, having absolutely no idea how any of it worked.  I didn't really understand the feeling at the time, but I'm sure I was amazed and confused at how the same tools I'd used to make guess-a-number could also make these graphical, uh, masterpieces.

Lurking in there is a critical stop along the way to several flavors of enlightenment: realizing and internalizing that the amazing creative things you see and admire were just made by regular people, using regular tools.  You can do it too.

I only remember one notable thing I made in QBasic in those days.  I must've still been in middle school, which would mean I was 9 or 10?  I got regular homework that involved taking a set of vocabulary words and making "word pyramids" out of them, like this:

    c    d
    ca   do
    cat  dog

...except that the words were more like ten letters long.  I guess the point was to learn their spelling, but as someone who was just fine at spelling thank you very much, I thought this was agonizingly boring and a waste of time.  So I decided to write a program to do it.  I spent well over a week on it, but I did it, and it worked!  I managed to get pyramids (effectively squares, really) of different sizes arranged on a page automatically and to print out (directly to the _printer_) one line at a time.  I felt like a fucking wizard for what may have been the first time.

Alas, the teacher wouldn't accept a printout for some reason.

----

The 486 was the family computer for a while, what with its being our only one, but after a few years my parents bought a better one (a _Pentium!_) and I inherited the 486.  The glorious beast.  I must've been 11 or 12.

Somewhere along the way it also got an upgrade to Windows 95, which I _hated_ initially.  It was just a blank screen!  Where was Program Manager?!  Where was Cardfile?

This was just before the turn of the millenium, right when digital music was getting popular.  By "digital music", of course, I mean "Napster", as the music industry was still a few years away from hearing that the Internet exists.  You could download a massive 4 MB MP3 of your favorite song in only ten minutes!

_You_ could, anyway.  _I_ could not.  My 486 couldn't decode MP3s in real time, even with the turbo button.  In other words, it took more than one second to understand one second of music.  I think I had a single WAV, but 40MB was a huge chunk of my 851MB hard drive (later improved to 1.2GB thanks to [DoubleSpace](https://en.wikipedia.org/wiki/DriveSpace), and partly mitigated by a 100MB Zip drive), so I mostly listened to MIDIs.

The timeline is a bit fuzzy, but at some point I graduated from QBasic to a few different things.  I think the earliest was some proprietary shareware scripting language I'd read about in PC Magazine or whatever; it was clumsy, but it could be triggered by hotkeys and manipulate existing programs, which let me do more interesting tinkering than the confines of a command prompt would allow.  I want to say it was "Wilson WindowWare" or something similarly alliterative; that finds me a extant company with a product called "[WinBatch](http://www.winbatch.com/winbatch.html)".  The name doesn't ring a bell, but it fits the description, so maybe that was it.

I ended up with a copy of Visual Basic 6 at some point (free copy on a CD with a magazine, maybe?) and built a few little toy programs with it, like a color picker and a really bad "encryption" program.  I also got into JavaScript (!) for a little while, back before anyone was even saying "DHTML", back when XSS was unheard of and I was free to embed rainbow-text JS into a forum post.  That largely fell by the wayside when I discovered server-side Perl, which was _magical_.  [veekun](http://veekun.com/) was probably the first _big_ thing I tried to build (and stuck with for more than a month or two).


## My first built computer

I was still using a 486 in 2000 or 2001, at which point it was comically obsolete.  Again, the timeline is fuzzy here, because I could swear that I got a new machine by 2001, but I distinctly remember building it in a place I thought I only lived in 2003.  I don't think I had an extra machine in the middle there, either.

I couldn't tell you much about the process of building it, but I imagine it went much the same as my experience with building computers now: get a bunch of parts, wiggle them together because everything only fits one way, spend all day trying to figure out why it doesn't boot only to find that a stick of RAM is sticking out one millimeter too far.

It was a Pentium something in a tower case, which was quite a change.  I named it `kabigon`, the Japanese name for Snorlax, beginning a theme that I've continued ever since.

I also put Gentoo on it for reasons I cannot fathom.  This was back in the day when the "real" way to install Gentoo was from stage1, which means you don't get an installer; you just get a massive, massive list of instructions on how to manually bootstrap everything from scratch.  It took _days_ to get a working system, including a day or two to compile X and KDE, but I sure did learn a lot about Linux and how a desktop environment is put together.

I'm not sure XP was actually out at this point, so consumer Windows still had no built-in way to share an Internet connection, and ISPs weren't yet giving out routers.  The very concept of a router was still pretty alien.  Up until this point, we'd been sharing the connection via some terrible shareware garbage called WinGate (which is somehow [_still around_](http://www.wingate.com/)) that mostly worked, except when it didn't.  I, despite having no clue what the hell I was doing, offered to instead have _my_ computer act as the router, because Linux is better at being a router than Windows ME.  Which is true!  The plan almost fell apart when my parents got tired of waiting for days for me to finish creating a computer, but in the end I did manage to get `kabigon` acting as the router, by blindly pasting a bunch of `iptables` rules my boyfriend gave to me.  Hm, actually, I think my interest in Linux can all be traced back to (and squarely blamed on) him.

In 2003 I was also in a high school programming class.  The class really had two classes taught at the same time: computer science 1, where the teacher taught maybe 16 or 20 kids to do simple stuff in QBasic; and computer science 2, where four of us who vaguely knew what we were doing basically had free reign.  I'd taken the AP Computer Science AB class and exam a year or two prior (and was nearly constantly mystified by why C++ was such a pain in the ass compared to everything else I knew), so by now I was finally dipping my toes into building slightly more complex stuff.

One such thing I remember well is an implementation of [Hex](https://en.wikipedia.org/wiki/Hex_%28board_game%29), the board game on a hexagonal grid where two players try to be the first to connect their two opposite sides of the board.  I remember it so well, in fact, that I have managed to exactly reproduce the source code and [placed it in this gist just for you](https://gist.github.com/eevee/aa71799e7ec0a4981ee13ea8185b854c).  Also I made this screenshot.

{% photo /media/2016-04-05-precomputer/hex.png C++ implementation of Hex, with Allegro %}

Or maybe I just still have most of the code I wrote in that class because I'm a packrat.  I'm glad, too, because it's the oldest window I have into what the heck I was doing thirteen years ago.  I see I was also showing off.  At one point the computer science 1 class had been told to write a change-giving program, where you enter a cost and an amount paid, and the program spits out the assortment of coins and bills you should get back.  It's not too difficult a problem; read a line of input, do a little math, print out a few numbers.  I, however, decided that not only would I also write this program, but I would be a total dick about it.

{% photo /media/2016-04-05-precomputer/change.png Giving change %}

Don't worry, I've got [the source code for that, too](https://gist.github.com/eevee/21def460854e675438a0353246385885)!  And it is unreadable slop.

I also remember an assignment about drawing a picture using QBasic's drawing primitives.  So I dug up a picture an artist friend had drawn me, reduced it to 16 colors, and wrote a Perl script to generate a QBasic program that would render it one pixel at a time.  Alas, I don't have the source code for that.

But my greatest achievement was probably writing a Chip's Challenge clone, complete with a bunch of tiles that were supposed to be in the eternally-delayed Chip's Challenge 2 (incidentally, [now released at last](http://www.chipschallenge2.com/)).  I had no understanding of a game clock or an event queue or any of that nonsense, so it's entirely turn-based; the game waits for you to move, and then the entire world updates.  I never got around to making any monsters, so it would've been purely puzzle-based, except I never got around to making any levels, either.  I don't think you could even die; the game would just not let you walk onto hazards.  Also it was just DOS characters, no graphics.  I _was_ working on a level editor, but never finished it.  Tragic.

{% photo /media/2016-04-05-precomputer/chips.png Just like Chip's Challenge, except not very good at all %}

That's all of interest I can remember.  A couple years later, I was in college, playing a lot of World of Warcraft and making bad stubs of websites that never saw the light of day.


## Appendix: all my computers ever

If you're curious!  Primary, in order:

- `fushigidane` (Bulbasaur, named retroactively for being the first): the 486, running Windows 3.11 and later Windows 95 — current location unknown, possibly parents' attic?
- `kabigon` (Snorlax, named for being gigantic): the Pentium I built, running Gentoo — left behind at a friend's house many years ago and not seen since
- `rapurasu` (Lapras, named for portability): a lumbering brick of a Dell laptop I had in college, running XP and then eventually Kubuntu — still in my possession
- `myuutsuu` (Mewtwo, named for its nebulous origins): a Frankenstein('s monster) assembled from my roommate's spare parts after I left home, running XP — eventually returned to its component parts
- `tekkanin` (Ninjask, named for its impressive speed): the first machine I actually bought for myself, running Ubuntu — I believe was incorporated into a former roommate's media center
- `perushian` (Persian, named because I splurged on it): my current machine, running Arch — typing on it right now

Secondary:

- `nyarumaa` (Glameow, named for Apple aesthetic): a glossy white MacBook I bought for work in 2007, running Ubuntu — current location unknown
- `rukushio` (Luxio, named for being medium-sized, blue, and electric): a "big" netbook I bought on a whim, originally running Ubuntu, then Arch, then accidentally bricked when I tried to update it after a long time — current location unknown
- `jarooda` (Serperior, named "because it is a smug macbook for smug people"): the MacBook Pro that Yelp loaned me while I worked there, running OS X and Arch — returned to Yelp
- `zeruneasu` (Xerneas, named for being newest??): a System76 laptop I bought after getting sick of fighting to get Apple hardware to work with Linux, running Ubuntu — in my bedroom, though rarely used nowadays
- `itomaru` (Spinarak, named because...  web...): a Soekris 6501 running pfsense and acting as our router — still doing that
