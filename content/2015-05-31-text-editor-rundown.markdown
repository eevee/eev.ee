title: Text editor rundown
date: 2015-05-31 19:27
category: essay
tags: linux, tools, tech, patreon

As part of my experiment to [monetize my personal brand](https://www.patreon.com/eevee), or however we're describing this now, I have a milestone that lets a patron impose a blog topic of their choosing on me.  What could _possibly_ go wrong?

And so, this month, [Russ](https://www.patreon.com/cmrx64) brings us:

> You should totally write about text editors.

I totally should.  I mean, wait, no I shouldn't.  I haven't seriously used a text editor other than Vim for _years_.

Thankfully this was a moderately vague request, so here's what I've done: I've subjected myself to all these hip shiny text editors that I haven't been bothering with and taken notes of my initial impressions.  I only had a few hours to devote to each, so this won't really be a fair comparison...  but you know, life isn't fair, so eat your peas and do your homework.

<!-- more -->


## Sublime Text 3

Here is a list of all of the things I know about Sublime Text.

1. It's shareware.
2. It does a neat file-opening thing when you press `Ctrl-P`, which is why we have [ctrlp.vim][].
3. Something about multiple selections???

So, this should be fun.

Because this isn't an open source project (gotta protect all those trade secrets buried in our _text editor_), it's not in my package manager.  So I went to their website to find a download link, an arcane ritual I have not had to partake in since time immemorial.  My very first observation is that none of the [download links](http://www.sublimetext.com/3) use https, nor is there a checksum offered anywhere.  This is a great start for an arbitrary binary that they want me to run and also hopefully give them money for.  I ran it anyway because I follow 0xabad1dea on Twitter and I'm pretty sure that makes me a security expert.

I ran it, and it ran.  It looked like a text editor, the empty canvas at once inviting yet paralyzing.

(This post contains no screenshots, because these things all _look_ pretty much the same; imagine a lot of letters in a box, and you're pretty much there.)

I vaguely recalled that Sublime has a file browser sidebar or something, so I hunted through the File menu.  I tried "Open Folder" which sounded like it might do useful things related to editing multiple files in the same directory tree, so I tried that.  And I got a file browser sidebar!  Magic.  Then I tried it a second time (because this project involves several subprojects), and it opened a new window, and that is an unforgiveable sin.

Then I noticed there's a Project menu, but it sounded potentially invasive and IDE-like which put me right off.  I have a deep aversion to editors that seek to manage "projects" for me — it reminds me of using C and C++ IDEs many years ago, where "project" meant "dozens and dozens of useless opaque junk files, vastly outnumbering your actual source files, which squirrel away all the important metadata so you have no hope of ever building your project from anything but our IDE, which by the way you will want to purchase an upgrade for next year."  I'm working on a Python thing, so much of that doesn't apply, but the general aversion remains.

So we're sticking with the open-folder thing.  The sidebar is your classic drill-down file browser, and I'm immediately confused by its contents.  I realize that I have a bunch of junk (`.*.swp`, `*.pyc`, and the like) ignored in both zsh's and Vim's tab completion, so it's very rare that I actually see half of the files I'm now presented with.  Seems odd that it doesn't know out of the box to ignore some common junk files.  Or, since I'm opening a _folder_, respect `.gitignore` or something?  That'd be pretty slick.  (And not without precedent — it's half the allure of [ag](https://github.com/ggreer/the_silver_searcher/).)

This minor problem is compounded by my workaround for opening two subprojects: I open the parent directory instead, which is a virtualenv, so it contains a bunch of junk like `lib` and `bin` that I will almost certainly not want to edit.

Anyway, let's try editing a file.  There's no built-in Sass syntax, which is a little surprising.  There's also no built-in Mako syntax, which is less surprising but still annoying.  I also discover that the list of known syntaxes includes a submenu "Python", under which is a single choice, "Python".  Curious.

I'd intended to use each editor vanilla (especially since I don't have time to try out dozens of packages for each), but understanding syntax is kind of a big deal in text editors, so I went off to hunt for some.

I found a Mako syntax package, but its install instructions were very terse, appeared to be for TextMate, and also didn't actually work.  I ended up finding a third-party package manager, Package Control, that seemed to be well-respected.  That had a oneliner to paste into Sublime (which is, I suppose, one level above piping `curl` into `bash`), but it did get itself installed.  The UI was almost entirely built out of the command palette, Sublime's version of ex mode, so I still felt like I had no idea what I was doing.  I went to browse packages, which just sent me to their website, which nowhere mentioned how to actually _install_ anything.  Turns out that once you've found the package you want, you go back to Sublime and there's a separate "install packages" command in the Package Control menu which (again using the command palette) lets you just type the name of a package.

None of this is really important and none of it has anything to do with Sublime itself, but I was in a hurry and largely felt lost the whole time, for whatever that's worth.

Anyway, I got the Mako package installed, and then discovered that installing it manually had worked in the first place, but I had to reopen the file or restart Sublime or something, so Package Control was a completely irrelevant detour.  Whoops.  I also learn along the way that Sublime reopens my previous files when I start it, which seems nice on the surface, but would surely be less nice if I were working on more than one thing at a time?  Not sure how it works.

I go to edit some Mako and immediately discover that the syntax doesn't recognize `<%! ... %>` blocks.  Mako only has maybe four kinds of syntax, so it's surprising that one of them would be missed.  I'm also under the impression that Sublime is at least partly powered by Python — there are Python files in the Sublime tarball, and the Package Control oneliner was Python — so it's extra surprising that it doesn't correctly support one of Python's most popular template languages.

I observe while using Sublime that it is, indeed, quite fast — the Ctrl-P "open a file by mashing parts of its name" launcher thing never slows for even an instant, and even shows the currently-selected file, syntax highlighted and all, in the background as I type.  A lot of Vim plugins are distinctly not-fast, which is weird since they ought to have strictly _less_ work to do.  I wish more Vim plugins were more fast.

I'm _extremely_ used to the hierarchy in Vim: tabs are at the absolute top level, and you can (arbitrarily) split each tab into panes however you want.  Sublime seems to be the opposite: you can pick one of a few fixed "layouts" which give you multiple panes, but each pane gets its own distinct tab row.  I can't figure out how to switch panes with the keyboard, and there's no menu item to give me a hint, so I'm stuck clicking between files which is super annoying.  I also come to realize very quickly that I rely heavily on using `:sp` to split a pane and browse around it "temporarily" in one half while my old cursor position remains visible in the other.  I can't do that now without using this heavy-handed "layout" thing, so I have to just resist the urge.  Between that and not having `Ctrl-O` (jump to the cursor position before the last major jump) I feel lost in my own files.

If you type a paired symbol, like `[` or `"`, Sublime will fill in the other one for you, ahead of the cursor.  That's fine, since if you aren't used to the feature or don't like it, you can just type the closing symbol and Sublime is smart enough not to insert a second one.  That's fine.

But in HTML files, typing `</` fills in the _entire_ most recently opened tag.  The double-typing prevention no longer applies, I guess because it's more than one character, and this immediately drives me up the wall.  If I type `</`, Sublime fills in `</section>`, and if I keep typing the rest of the tag name because _that's what I want to put in the file_, I end up with `</section>section>`.  It means _typing_ is no longer _typing_.  I have to learn (or just guess) when to stop typing the actual characters I want to see on the screen, or else I'll be typing extra garbage.

Even better: Mako-in-HTML files still do this, and the suggested tag _is often wrong!_  Mako's `<%foo>` tags aren't recognized, and of course embedded logic might completely change the nesting of tags, so on multiple occasions I have to go out of my way to _delete_ the wrong thing that Sublime injected into my file without asking.  _And_, after this happens, there's a completion popup for HTML attributes (even though this is a _closing tag_ and my cursor is beyond the `>` anyway), so the down arrow and enter keys don't work correctly.

I really really don't like when a text editor interferes with _writing text_.  It interrupts me when I'm trying to get a thought onto the screen, and forces me to waste time cleaning up its errant suggestions.

Thankfully, once I'm used to this, the rest of my editing passes without major incident.

I discover that when I select a whole word, Sublime helpfully outlines other occurrences of that word, and...  I don't know.  I'm dimly aware that there's a multiple-cursor thing that lets me overwrite every instance at once, but there's no indication as to how I actually use it.  Nothing in the Selection menu, nothing in the right-click menu.  Why is it showing me this if I can't do anything with it?  The answer eventually reveals itself: "Quick find all" creates a true multiple selection.  This is a little bizarre to me — clearly Sublime has _already found_ every occurrence, so why would I think to ask it to search again?

I do get a little frustrated that I can't easily delete a single line.  `Shift-Home`, `Delete` leaves a blank line, so I need to type `Ctrl-L`, `Delete` (`Ctrl-L` is select line) which is a little awkward.  In Vim this is a quick tap, `dd`.

### vintage

At some point I mention to Twitter that I'm trying out Sublime, and a few people mention they've heard it has a vi(m?) mode, or something.  Indeed it does, called "vintage", and it's the only built-in package.

I do not have high hopes for this.  I've tried things with a "vi mode" before, and it usually comes down to a handful of the most basic keybindings and nothing more.

I spent fifteen minutes with Sublime's Vintage.  Things that didn't work:

* `Ctrl-W` doesn't switch panes; it closes the current file.
* There is no ex mode.  `:` opens the command palette, but only `:w` and `:e` with no arguments are implemented.  So no `:%s///`.
* Visual line sort of exists, but is broken; the selection is lost if you go up one line, then down.  At this point you're back in command mode, but the modeline claims you're still in visual line mode.
* There is no visual block mode.
* `gq` followed by a direction works, but `gqq` does not.
* `d↓` deletes the current line plus the part of the following line _up to the cursor position_, which is wrong — it's supposed to delete two entire lines.

I'm pleased to discover that `zz`/`zb`/`zt`, marks, (automatic) folds, and `%` all seem to work, but this is basically useless to me if even _deleting lines_ is buggy.


## Atom

With a new day comes a new editor, so it was time to try Atom, the text editor GitHub created for some reason.

A disclaimer: I've always thought Atom sounded ridiculous, so I might have a teeny bias towards making fun of it.  Sorry in advance!

Atom has a welcome screen, which is something of an improvement over Sublime.  It calls itself a "hackable text editor for the 21st century", where I suppose "hackable" means "we have never used Vim", and "21st century" means "JavaScript".  (If you're not familiar: Atom is built atop WebKit.)

It also mentions that they anonymously collect metrics, which I seem to recall means Google Analytics is baked into my text editor.  Perhaps "21st century" actually means "needs an Internet connection".

The welcome screen offers me a list of things I can do, and the first one is "open a project", so it looks like I have no choice this time.  Thankfully, "project" here seems to just mean "directory".  I get a familiar sidebar, with a familiar unnerving problem — it lists junk files as well.  What's extra confusing here is that there's a preference for "ignored files", and the default value lists `.git` amongst other things, yet `.git` still appears in the sidebar.  To what, then, does this setting actually apply?

The welcome screen also starts out vertically split, with each pane having its own tab strip, so this is looking a whole lot like Sublime so far.

I open a file and it becomes glaringly obvious, after my [recent font adventures](/blog/2015/05/20/i-stared-into-the-fontconfig-and-the-fontconfig-stared-back-at-me/), that Atom is not using my default monospace font!  [Apparently](https://discuss.atom.io/t/what-is-the-default-font-in-atom/374) (warning: page is totally blank with noscript, because it's the 21st century, which means JavaScript) the default is "Inconsolata, Monaco, Consolas, 'Courier New', Courier".  I have Inconsolata installed, so that's what I get.

This is kind of annoying, and I interpret it as the first sign of the Web platform leaking through.  A website can't reasonably be expected to serve different default fonts per client OS, but _local software_ generally can, and on Linux you should be using fontconfig's generic "monospace".  Atom, though, is styled with CSS, so all it has is a `font-family` somewhere.  Which doesn't even include "monospace" as a _fallback_.

I briefly consider fixing this.  After all, the welcome screen (still open in the right pane) says I can customize _anything_ in this _hackable text editor_, and encourages me to "uncomment some of the examples or try your own".  So I click the button and get a completely empty stylesheet, along with zero indication of what _elements_ are actually available to me, which is a fairly important feature when writing CSS.

I don't really feel like wasting time researching the DOM of my text editor when I'm only going to use for a few hours, so i give up and will just live with Inconsolata for now.

Relatedly, I notice that Atom tries, and largely fails, to use my native theme — active menus have the wrong color and an inappropriate border, and menu items use the wrong background color on hover.  It's wrong in the same way Chromium is wrong, but it's a bit more obvious when there's a menu bar.

I finally start doing some actual work.  I find that Atom has the same selection keybindings as Sublime.  This is starting to feel a lot like a clone of Sublime.  I guess to delete two lines I need `Ctrl-L`, `Shift-Down`, `Delete`?  This is so awkward.  I think Sublime was the same.  I also discover that `Ctrl-L` selects the current line; `Ctrl-L`, `Shift-Down` selects the current line plus the following line; `Ctrl-L`, `Shift-Up` selects absolutely nothing.  What?

I type a _capital_ `C` in a Python file, and Atom automatically suggests a single completion: the `class` keyword.  What?  Capital `I` similarly suggests `if`, yet typing `Tru` fails to suggest `True`!  Later on I start to get completion suggestions of English words from within docstrings and comments, so I don't really understand how this is supposed to work at all.  Sometimes Atom only manages to come up with a completion by the time I've finished typing a word, at which point...  I've already typed it, so what use is it to show me a menu containing only the word I just typed?

Admittedly I'm pretty harsh on magical automatic features like tabless completion, because they have a high upfront cost in the form of distraction — they flash crap on the screen, and often they take over important movement keys like up/down arrow too.  (Even worse here: Atom only directs up/down arrow to the completion popup if there's more than one suggestion, so I have to actually stop and examine the popup if I want to know if my keys will work!)  So when these features just plain _don't work_, even if it's only 10% of the time, I'm paying this cost for _nothing_.

Sometimes, the cursor disappears.  I don't know why.  It comes back if I type some more.

Again, of course, there's no Mako syntax built in.  There _is_ syntax for Rails HTML, Mustache HTML, and Go HTML, which I suppose speaks volumes about the people who built Atom.  I wonder why this Internet-enabled text editor from the 21st century doesn't offer to download syntax _for_ me when it doesn't recognize a filetype.

There's no keyboard shortcut for "save all".

I can't scroll beyond the end of the document, which got really annoying when Thunderbird new-email alerts popped up while I was trying to add to the end of a file.  I don't like typing on the last visible line anyway; I can't tell whether I'm actually at the bottom or there's something more that I might care about.  I tried to work around this by mashing `Enter` a lot, which preserved my current indentation level for every single new line, so I had ten lines in a row that consisted of nothing but eight spaces.  Suddenly I understand why so many projects are full of trailing whitespace.

The rest of my adventure passes without incident.  It is, after all, a text editor, and it successfully edited some text.

But I walk away enlightened.  Finally, I understand why Atom exists: so a bunch of nerds making six-digit salaries can weasel out of paying seventy bucks to register Sublime Text.

Yes, I'm making fun of Sublime for being closed-source and of Atom for being a clone of it.  Life's not fair.  Go mow the lawn.


## Emacs

Despite what you might think, I bear no ill will towards Emacs.  I may think Atom is silly for technical reasons, but I don't actually care what text editor you use.  Just as long as it's not, like, Wordpad.

I saved this for last because I knew it would be like trying to learn Vim from scratch again, and I'm only spending a few hours with it so I can't possibly do it justice.

Right off the bat I'm lost in the weeds.  This whole time I'd thought XEmacs was just the name of Emacs's GUI (you know, X for X11) mode, like how GVim is graphical Vim.  Much to my surprise, XEmacs turns out to be a _fork_ dating back to the _80s_, which has not had a stable release in over six years.  XEmacs's website has [a page explaining the differences](http://www.xemacs.org/About/XEmacsVsGNUemacs.html), which was written in 2001 and half-heartedly updated in 2008.

I guess I'll use Emacs, then.

Sorry, I mean GNU Emacs.  GNU/Emacs?

On first start, it looks rather a lot like GVim.  Except it has GRAPHICS (for some reason), and a proportional font, and hyperlinks.  I briefly fear Emacs is actually a Dreamweaver clone.

Emacs is even worse at obeying my theme than Atom was, and this time I have no explanation.  GVim gets it right.

There's a tutorial, which I guess I should probably follow.  I'm relieved to find that the tutorial is in monospace.

These keybindings are baffling.  `Ctrl-G` to abort a partial command?  Why not `Ctrl-C`?  I don't even know what `Ctrl-G` does in a terminal.

Apparently `Ctrl-V` means "**v**iew next page", which is a bit of a stretch.  (Why not `PgDn`?  I try it.  It works.)  The mneumonic falls apart entirely on Page 2, wherein I'm told that `Alt-V` means "**v**iew previous page".  (`PgUp` works.)

Oh, here we go.

> You can also use the PageUp and PageDn keys to move by screenfuls, if your
> terminal has them, but you can edit more efficiently if you use C-v and M-v.

I don't know what kind of Stretch Armstrong fingers the author of this document has, but touchtyping `Alt-V` is not what I'd call "efficient".

> You can use the arrow keys, but it's more efficient to keep your hands in the
> standard position and use the commands C-p, C-b, C-f, and C-n.

Yes, it's much more efficient to use four letters that are all over the place.

To be fair, I don't home-row touchtype.  But also, I don't tend to rapidly switch back and forth between moving around and typing.  Moving is _reading_, typing is _writing_.  They feel fairly different to me.  I even position my hands differently when I'm reading, with my right hand floating between the navigation keys and occasionally the mouse.  You might say they are totally different, uh...  modes.

Hmm.  Moving the cursor off the bottom of the screen causes the next line to jump to the _middle_ of the screen, and I find myself having to hunt for where the cursor ended up.  To be fair, I use `zz` all the time in Vim; this is only frustrating in Emacs because I didn't expect it, and there's no highlight for the current line.  It sucks for reading, though, where I want to scroll more text onto the screen _before_ I've read all the way to the bottom, so my eye can stay locked on the same position in the text and I can keep reading without interruption.  Later I learn that to do that I need something like `Ctrl-U`, `4`, `Ctrl-V`.

`Alt-F` and `Alt-B` move between words, but again, `Ctrl-<Arrow>` works fine.

> Very often Meta characters are used for operations related to the units
> defined by language (words, sentences, paragraphs), while Control characters
> operate on basic units that are independent of what you are editing
> (characters, lines, etc).

I literally only know two things so far, and one of them uses `Ctrl` to mean "down" and `Alt` to mean "up".

> You can also move the cursor with the arrow keys, if your terminal has arrow
> keys.  We recommend learning C-b, C-f, C-n and C-p for three reasons.  First,
> they work on all kinds of terminals.

If you are transported back to 1972, you will be all set to use Emacs.

> To insert a Newline character, type `<Return>` (this is the key on the
> keyboard which is sometimes labeled "Enter").

This documentation is targeted at people who know what "newline" means, but are not familiar with the enter key.

> Reinsertion of killed text is called "yanking".

No wonder Emacs and Vim are bitter rivals.  They use the same word to mean opposite things!

Okay, enough of that.  I'll finally edit a file.

First I have to look up how to open a file, because I already forgot.  Luckily the tutorial is still open.

Emacs supports Git out of the box and automatically tells me my current branch in the modeline, which is pretty nice.

I make some minor changes.  I already forgot how to save a file.  I consult the help for the help and muddle through several attempts at searching by command name, until I finally come up with `Ctrl-X`, `Ctrl-S`, which I probably should've guessed.

Honestly, this is a harrowing experience.  I edit as conservatively as possible, much like when I was learning Vim, so I don't have to worry about being stalled in the middle of a thought by wondering how to accomplish some trivial task.  I don't know if there are vertical splits, and don't bother to look.  There's a menu bar here, but it seems more concerned with checking my email and playing Tetris than actually making the power of Emacs more accessible.

None of my readline knowledge is helpful here.  Even `Ctrl-W` doesn't do what I expect: it deletes to the last mark, or something, rather than deleting the previous word.

There is no built-in Mako mode, of course.  I don't even know where to look for one.  I don't try.

I feel oppressed, suffocated.  It knows what I am, and what I am is a Vim user.  I am not welcome here.  I turn back, confounded and saddened.  Emacs demands patience be sacrificed upon its altar, and I have none to give.  I am defeated.

As I leave, Emacs delivers a parting shot:

> Unprinted PostScript waiting; exit anyway? (yes or no)

I have no idea what I pressed to make this happen.

But there is a glimmer of hope.  I know of one other terminal editor that shares Emacs's aspirations of modelessness.  I have used it before.  Perhaps I can use it once again.


## Nano

I've heard, apocryphally, that some actual human beings have used Nano to edit actual source code.  I haven't needed to use Nano myself for well over a decade, but I'm curious to see how it holds up.  Let's give it a whirl.

We're going all out here.  First, does Nano do syntax highlighting?  (Does Nano do _color_?)  I find that [yes, it totally does](http://askubuntu.com/a/90026/127106), but you have to explicitly include them in your `.nanorc`.  Weird!  I'm also alarmed by this warning:

> Note: Sometimes you might get a `segmentation fault` after you have edited your ~/.nanorc file.

Thankfully, this doesn't happen.  I create a `.nanorc` (with Nano!) that loads Python syntax.

Time to open a file.  Thankfully, Nano has all its important keys listed at the bottom of the screen.  `Ctrl-O` actually means "write **o**ut", so `Ctrl-R` is "**r**ead", even though in terminals `Ctrl-R` means search through history.  I think this is because `Ctrl-S` is the terminal sequence for freezing output, maybe?  But Emacs uses `Ctrl-S` just fine.  I don't know.  Also, `Ctrl-G` means "**g**et help", probably because `Ctrl-H` is the backspace key.

Nano even has tab completion, though it's the crappy kind where it only fills in a unique prefix and then shows you all the possibilities, and you have to mash Tab like three times to get that much.  I successfully load a Python file.

It is not syntax-highlighted.

The top of the screen still says "New Buffer".  I feel a dawning dread.  I press `Ctrl-O` experimentally, and Nano asks me for a filename.  It seems Nano literally read in the contents of a file, but did not consider itself to be editing that file.  I begin to fear I don't understand Nano, either.

I exit and instead start Nano with the file as an argument.  This seems to work, and I have glorious 4-bit color.  Decorators aren't colored, but I can't tell if that's deliberate or not.  Comments are _bold red_, an interesting choice for something that I often want to gloss over.

I pause.

It's been so long since I've actually edited any text that I don't remember what I wanted to do in the first place.

While I mull that over, it seems Nano defaults to hard tabs, and that won't do.  [Another `.nanorc` edit](http://stackoverflow.com/a/15364505/17875) saves the day.  Unfortunately, Nano isn't clever enough to delete an entire indentation level at once when I press `Backspace`.

I make some minor edits.  Nano doesn't automatically preserve the indentation level on `Enter`.  I perspire slightly.

Nano has the same scroll behavior as Emacs — moving off-screen recenters the cursor.  I wonder who copied who, here.

I wonder if Nano has tab completion.

No.

Nano _does_ highlight trailing spaces, though (in green...?), which gives it a point over Atom.

I browse around this file a bit.  I might have wanted a different file, but it seems impossible to open a file in Nano.

I'm cold and tired of this experiment.  I want to go home.  Color is a cute novelty, but Nano is still terrible.


## Vim

Vim is my usual editor, really my _only_ editor, so I would be remiss to mention text editors and not discuss Vim.

I can't tell you what it's like to use Vim for the first time.  Well, hm, I suppose I can, since I still remember — it's pretty much like my experience with Emacs, except with Vim you have to learn "press `i` to type words" first.  After that, they're pretty much the same: ancient relics of immeasurable power that you must learn one agonizing keystroke at a time.

### The good

Almost universally, I run Vim in a terminal inside tmux.  I can then pick up whatever I was doing from my laptop, without having to even _touch_ my desktop or plan in advance in any way.  I can edit files on remote machines with exactly the same editor, and without having to dink around with something like sshfs.  This is _fantastic_.

It's fairly Unixy, in the good way — there are a lot of little composable parts.  There's the motion adjectives (which I still struggle to remember to use), sure, but it's also got regexes and pipes and whatnot.  I can make a lot of one-off edits to files right from a text editor, which I vastly prefer to `awk`.

Undo persists, if you set it up!  That's awesome and has saved my ass a couple times.  I didn't think to check any of the editors above for persistent undo; oops.

The plugin ecosystem is massive.  I don't use too many of them ([here's what I've got](https://github.com/eevee/rc/tree/master/.vim/bundle)), but there's a good selection of stuff that's unintrusive and quietly useful.

I could go on.  (Maybe.  Christ, it's just a text editor.)  But you don't want to hear why I _like_ something.  No, no, dear audience, I know why you came here.  I know what you want.

Here you go.


### The bad

Vim is fairly hostile to beginners, and not even for any good reason.  (zsh has a similar problem.)  There's the problem of backwards compatibility, sure, but consider: if a default changed, all the existing users with massive `.vimrc`s are exactly the people most capable of dealing with it.  But instead of putting the biggest burden on the _experts_, Vim puts it on _beginners_, who not only have to figure out how to use it, but also have to hunt down the dozen or so knobs they need to turn to make Vim actually worth using.

Some defaults don't even make sense.  Why is _mouse support_ disabled (in Unix terminals) by default?  What possible harm is there in supporting mouse input?  That's about as unobtrusive as it gets.

I don't actually use a lot of Vim's functionality; it's easier for me to use visual block mode and mash down-arrow a couple times than to count lines.  (I have relnumber on, in the hopes that it might encourage me, but it hasn't yet helped.)  I suppose that's not necessarily bad.  Vim has a big enough surface area that everyone will naturally find the bits they want to use, and that's fine.

But I never learned to use netrw, and I went ages without realizing how much you could customize Vim's filename input.  I always forget to use ctrlp, too — because it choked on Vim's massive source tree and I trained myself not to try it because it'd freeze Vim.

Vim has _massive_ surface area, and not much discoverability.  The only way to find a new way to do something is to get tired of it and go hunt down a better way to do it.  (At which point you discover you could've been doing it with two keystrokes.)  I don't know if there's anything to be done here, but it seems a shame that there is so much overwhelming depth that after a decade I still haven't gotten around to learning all (or even most) of it.

The encoding story is kind of weird.  If you want to edit something that's not in your default encoding, you have to do something wacky like `:e filename ++encoding`, maybe, and then I'm actually not sure what happens when you save.  There are a surprising number of settings related to this, one of which (iirc) controls Vim's _internal_ charset, which I don't understand why you'd really want to change.  I've basically resigned myself to only editing UTF-8, and the occasional binary file.

The regex language is pretty weird.  `\v` makes it _mostly_ like you'd expect, but there are still oddities like `<` and `>` for matching word boundaries or `{-}` for non-greedy repetition.

I had some hopes that NeoVim might be trying to solve some of this—

> Arrow key support in all modes enabled by default (new users will need this is you wish to keep as many as possible, but I believe they will naturally transition to the home row when they learn how convenient it is, and veteran users will feel right at home without even touching the arrow keys anyways).

...[right then](https://github.com/neovim/neovim/issues/276).  I actually forgot that `hjkl` control movement in Vim.  I really, truly forgot.  I guess I'm not a "veteran user".


### The ugly

There is a vast ecosystem of plugins, but actually finding them is a nightmare; you basically have to rely on finding a blog post written by someone who's already found them (presumably from someone else's blog post).  There's a [directory on the Vim website](http://www.vim.org/scripts/), but in my experience most of the interesting development nowadays just happens on GitHub.  I've never found browsing the official plugin registry to be a joyous occasion, really.

Vim does ship with a _ton_ of language support, but all those syntax files risk getting crufty.  And if you want newer ones...  where do you look?  I've seen at least five different Python syntax definitions floating around, all seemingly forked from each other.

Vim's syntax definitions are based on regexes and keywords, so you're not going to get any semantic highlighting (like coloring variable names based on scope) without some very heavy lifting.  After numerous upgrades to "fixed" Python syntax, I still get the "id" in `row.id` highlighted like it's a built-in function name.

Vim has a lot of built-in programming functionality, but it tends to be very barebones without third-party support.  For example, there are motions for operating on a paragraph (of plain text), or a braced block (in C)...  but not an _indented_ block, like you might have in Python or Haskell or Inform.  Or, um, vimscript.  There's a [plugin](https://github.com/michaeljsmith/vim-indent-object) to add this...  _and_ a page on the disastrously messy Vim Tips wiki that has no fewer than [four slightly different versions of the same thing](http://vim.wikia.com/wiki/Indent_text_object).

(This is gonna be a recurring theme here: the Vim ecosystem just never feels _polished_.  It may not be entirely fair to blame Vim for the problems of its third-party contributions, but Vim _needs_ its third party contributions in order to not rot.  I know package management is a Hard Problem, but somehow Vim seems to be the worst off of the ecosystems I've seen, even though it should surely have the people from all the other ecosystems working on it.)

Speaking of C: Vim has a set of built-in highlighting groups ("identifier", "constant", etc.), but they are pretty obviously aimed at C.  So languages that are insufficiently similar to C have to make creative use of the groups, which often means that two languages will end up not even using the same color for keywords, because they both had a different idea of how to map those keywords to highlight groups.

Even the color schemes contain fun surprises — the one I use seemed great, until I tried using vimdiff, and discovered it had chosen to use blue and purple backgrounds that clash horribly with almost every other color in the theme.

Different languages even configure your indentation differently; for me, HTML is _very_ insistent about keeping the cursor in what it thinks is the "right" place.  Not nearly so much for Python.

Also, my comments auto-wrap at column 80 while I'm typing in Python, but not in Mako.  `gq` doesn't work correctly on Mako comments, either.  But they're still colored as comments.  I don't know why any of this is.

For the longest time, it seemed that the only tab-completion thing anyone used in Vim was ctags, which was designed for C (because of course it was) and involves running some command outside of Vim _first_ to index all your code.  Recently there have appeared some plugins that try to do actual smart tab completion, like [python-mode](https://github.com/klen/python-mode).  But python-mode has a teeny tiny bug where sometimes it will think your "project" is actually your **entire home directory**, so the moment you press `Tab`, Vim freezes for _minutes_ while python-mode recursively scans every file in your home directory looking for things to index.

I used python-mode for a while and I have, by and large, trained myself not to press `Tab` so much any more, unless I really mean it.  Now I use some other thing, which half the time works and the rest of the time just sorta gives up and tries to suggest keywords and builtins.  Either way, sometimes it takes longer to produce results than I would've taken to just type the word myself.  I assume there's some way to make this all work, but I've yet to find it.

Vim itself is pretty sleek, but I'm frustrated with this recurring problem of plugins freezing it with mountains of blocking work.  It happened with python-mode, it happened with ctrlp, I'm sure it happens with others.  This is Unix, right?  Can you not run a child process or something?

I'm reminded of yet another plugin quirk.  There's a neat thing, [gitgutter](https://github.com/airblade/vim-gitgutter), which shows which lines you've added or modified.  It creates a temporary directory to do its work.  The thing is, on my (Arch) system, temporary files are nuked after ten days.  So if I leave a Vim session open, then come back to it later, I get a bunch of error messages complaining that the temporary directory no longer exists.  But just creating the directory makes it stop complaining, so clearly the plugin still _works_ even without that data.  The maintainer [blamed this on Vim](https://github.com/airblade/vim-gitgutter/issues/190), so it's still a silly problem with a silly workaround, which never happens with any other plugin.  Swell.

Oh, and Vim inserts garbage if I click beyond the ~256th column of my terminal.  There's a reason for this, and I forget what it was, and I could swear it was fixed, but it isn't.


## Yeah so

Everything is bad and computers are terrible.

I don't have the time to learn Emacs — hell, I barely have the time to learn Vim.  I don't see the appeal of Atom.  Sublime Text seems kinda slick, but I'm pretty attached to being able to edit things in a terminal, so I don't think they'll be getting seventy bucks from me anytime soon.

My only hope is that someday [tpope](https://github.com/tpope/) will descend from the heavens and solve all of my problems for me.

And after all this, I haven't made much progress at all on the thing I was actually trying to work on.  Damn.


[ctrlp.vim]: https://github.com/kien/ctrlp.vim
