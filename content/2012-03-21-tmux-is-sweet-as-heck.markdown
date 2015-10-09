title: tmux is sweet as heck
date: 2012-03-21 14:24
category: blog
tags: reference, tmux, tools, tech

People occasionally ask me why `tmux` is significantly better than `screen`, and I end up mumbling the first few things that come to mind.  This has yet to sway anyone.  Here, then, are some things that I enjoy about using `tmux`.

First, some terminology, so the rest of this makes any sense at all.

* `tmux` and `screen`, if you were not aware, are _multiplexers_—they let you run multiple terminals (or terminal programs) at the same time, switch between them, and disconnect or close your terminal without killing everything you were running.  If you didn't know this then you should probably stop now and poke around [tmux's site][tmux] or something.
* A _session_ is a particular group of terminals owned by `tmux` (or `screen`).  When you run `tmux` bare, you get a new session.
* A _window_ is a numbered terminal inside a session.
* A _pane_ is each compartment within a split window.  (I lied above; a window might actually have several panes and thus several terminals.  But a window is identified by one number.)
* An _xterm_ is a single GUI terminal window (or tab).  You may be using another terminal emulator, or you may be in a non-GUI virtual terminal; I'm using "xterm" as an umbrella term for all of these.

I'm also assuming that `^A` is your multiplexer trigger key, although `tmux` defaults to the more awkward `^B`.

## Works out of the box

Here's my `.screenrc`, fiddled by hand over the course of many months after I started using `screen`.

    caption always "%{= kw}%?%-Lw%?%{Kw}%n*%f %t%?(%u)%?%{kw}%?%+Lw%? %=%{= dw} %H "

    # terminfo and termcap for nice 256 color terminal
    # allow bold colors - necessary for some reason
    attrcolor b ".I"
    # tell screen how to set colors. AB = background, AF=foreground
    termcapinfo xterm 'Co#256:AB=\E[48;5;%dm:AF=\E[38;5;%dm'
    # erase background with current bg color
    defbce "on"

What the fuck is any of this?  The only real _configuration_ here is the first line, which sets a fairly simple status bar.  The rest is unreadable sludge picked off of Google to make terminals inside `screen` work the same way as terminals outside it.  I see this as a serious failing in the one core feature that defines a multiplexer: _being invisible_.

Some of this might not be necessary any more; maybe termcaps have been improved in the meantime.  Part of the very problem is that _I can't know_; the best I can do is delete bits of it and see if `screen` still behaves correctly, assuming I remember all the quirks I was trying to fix in the first place.  It's 2012.  I shouldn't ever see the word "termcap".

Contrast with `tmux`, which just worked.  The only terminal-related fudging I ever had to do was set my `$TERM` to `xterm-256color` for it to respect 256-color sequences.  Not entirely unreasonable.

`tmux` can also inherit parts of the environment when it's detected a change; by default it looks for some common X and SSH stuff.  The upshot of this is that your SSH agent continues to work across SSH connections; the new environment only applies to newly-created windows, but zero [hacks][ssh agent and gnu screen] are necessary.

By default as of `tmux` 1.6 (I think), when you create a new window, it'll get the same current working directory as the current window.

<!-- more -->

## The status bar

If you run `screen` with no `.screenrc`, you get what looks like a regular terminal—you can't even easily tell that you're in a multiplexer, save for any terminal-related weirdness.

If you run `tmux` with no `.tmux.conf`, you get a status bar listing all your windows, as well as the name of the session and a timestamp.

Sure, you can just paste a line you find on the Web (like mine above, even!) into your `.screenrc` and fix this instantly.  But look at that line: what if you want to change a color?  Can you even tell which of those escapes _is_ a color?  I wrote the damn thing and I couldn't tell you.

Here's an excerpt of the status bar configuration from [my `.tmux.conf`][tmux.conf]:

    # Status bar has a dim gray background
    set-option -g status-bg colour234
    set-option -g status-fg colour0
    # Left shows the session name, in blue
    set-option -g status-left-bg default
    set-option -g status-left-fg colour74

High xterm color names are not particularly friendly, and the actual contents of each part of the status bar are still controlled by special escapey codes.  But you can tell what's going on, and you can customize it yourself with relative ease.  You can even change these settings from within `tmux` itself and see the changes live.

## xterm window title

How do you customize the xterm title in `screen`?  According to [the FAQ][screen faq on xterm titles]:

    termcapinfo xterm*|rxvt*|kterm*|Eterm* 'hs:ts=\E]0;:fs=\007:ds=\E]0;\007'
    defhstatus "screen ^E (^Et) | $USER@^EH"
    hardstatus off

Ah! it's our old friend termcap, followed by line noise.  The FAQ entry indicates that this doesn't _really_ set the xterm title, but uses an obscure terminal feature known as a hard status line, and tells `screen` to update the hard status line by using the xterm escapes that actually change the xterm title.

Let's compare to my take on this for `tmux`:

    set-option -g set-titles on
    set-option -g set-titles-string '[#S:#I #H] #W'

That gives you something like `[blog:3 perushian] source/_posts/2012-03-21-tmux-is-sweet-as-heck.markdown`.  `#W`, meaning "window name", uses the same special xterm escape sequence `screen` invented to set the window name, so my `.vimrc` and `.zshrc` spit out custom window titles that work under either multiplexer.  (Though, strangely, `screen`'s own invention never worked for me very reliably in `screen`.)

## Splits

`screen` could only split horizontally when I used it, but it appears it recently learned to split vertically as well.  I can't speak to how well this works; I never actually used its splits.  It seems the only default keybinding for switching between panes is `^A tab`.

In `tmux`, `^A "` will split horizontally, and `^A %` will split vertically.  Your current pane is outlined in green.  `^A arrow` will move to the next pane in that direction.  `^A ctrl-arrow` will resize the current pane in that direction; `^A alt-arrow` will resize five cells at a time.

You can tell `tmux` to use a particular "layout", which is a general approach it'll use for determining sizes of panes.  `^A alt-1` through 5 will rearrange all your panes (even the split direction) to fit one of the five builtin layouts.  It's great if you don't care about the actual sizes of the panes, which I generally don't  8)

## Shuffling things around

If you attach to an existing session without detaching it, you'll just attach to it twice.  Both xterms will control the same session; it'll have the same current window and pane, and changes to a pane will be reflected in both xterms.  If a session is smaller than its containing xterm, `tmux` will draw a border and a field of dots in the unused space.

It gets better!  `tmux new-session -t <existing-session>` will create a new session _grouped with_ the one you name.  They'll share the same set of windows—close or create a window in either session, and you'll see it in the other.  But each session can have a different _current_ window, so your two xterms can work on two things in one session at the same time.

For finer-grained control, `tmux link-window -s foo:1 -t bar:2` will create a new window at position `2` in the session named `bar`.  This window will control the same set of panes, with the same terminals and processes, as window `1` in the session named `foo`.

`tmux break-pane -t <pane>` removes a pane from its window and sticks it into a new window.  `tmux join-pane -t <pane>` is the reverse operation: it splits the current window and uses an existing window as the new pane.

There are similar commands for rearranging panes and windows.  Anywhere you refer to a pane or window, you can refer to a pane or window in an arbitrary session as well, so you can move whatever you want to wherever you want.

## Miscellaneous

In `tmux`, `^A pgup` enters copy mode _and_ scrolls up a page, which is usually what I wanted anyway.  In `screen`, I always had to `^A esc` to enter copy mode, then `pgup`.  (I didn't know how to change the key combination timeout at the time, either, so sometimes I'd type too fast and that just wouldn't work.)

All `tmux` key bindings are just regular commands.  Anything you can do with a keybinding, you can do from `tmux`'s command line, or from running `tmux <command>` regularly from a terminal—either inside or outside `tmux`.  (A handful of commands only work from inside `tmux`, but these are interactive commands that rely on `tmux` having control over the terminal.)  You can script pretty much anything with ease.

One caveat to `tmux`: while every `screen` session is its own process, `tmux` invisibly runs a master server that handles every pane in every session owned by your user.  This lets the stuff in the previous session work.  The only real impact of this is that if the server crashes, _all_ your sessions go down with it.  Thankfully, this tends not to happen.

The manpage is excellent and thorough.  Most anything you may want to do can probably be accomplished with an obviously-named option or command.

Some other stuff from [my `.tmux.conf`][tmux.conf] that you may find useful:

Use `^A` as the magic keybinding:

    set-option -g prefix C-a
    unbind-key C-b
    bind-key a send-prefix

Bind `^A space` to switch to the next window to the right, `^A ctrl-space` to switch to the next window to the left, and `^A ^A` to switch to the last-used window:

    bind-key C-a last-window
    bind-key Space next-window
    bind-key C-Space previous-window

Set the esc/alt disambiguation timeout to 50ms.  The default is _half a second_, which makes vim kind of painful.

    set-option -sg escape-time 50

Start numbering windows at 1, not 0.  I like the leftmost window to be the leftmost number on my keyboard.

    set-option -g base-index 1

Set `TERM=screen-256color` in new windows.  (`tmux` doesn't have its own `$TERM`; it hijacks the `screen` family, so whatever recognizes `screen` should recognize `tmux`.)

    set-option -g default-terminal screen-256color

Tell `tmux` to use xterm sequences for, e.g., ctrl-arrow.  I don't know why this isn't on by default.  If odd key combinations aren't working for you, this is probably why.

    set-window-option -g xterm-keys on # to make ctrl-arrow, etc. work

Feel free to steal my color scheme, too.  It's simple, but a bit less glaring than the 70's black-on-green that you get by default.

Now, go forth and multiplex!  I am _hilarious_.


[screen faq on xterm titles]: http://aperiodic.net/screen/faq#how_can_screen_use_xterm_s_title_bar
[ssh agent and gnu screen]: http://screen.frogcircus.org/ssh-agent
[tmux]: http://tmux.sourceforge.net/
[tmux.conf]: https://github.com/eevee/rc/blob/master/.tmux.conf
