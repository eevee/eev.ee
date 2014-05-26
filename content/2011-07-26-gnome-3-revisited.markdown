title: GNOME 3 revisited
date: 2011-07-26 14:39:00
tags: linux, interfaces
category: 90% of everything

How did I write this?  I don't know what happened.  I was just jotting down notes and prose came out.

I wrote a whole thing about Shell and Unity before, but it was kinda knee-jerk ranting.  With my newfound blog fame, here's a lame attempt at a more constructive list of specific criticisms of GNOME 3, now that I've actually used it for a while on my laptop.

<!-- more -->

I know that GNOME 3.2 is in progress, so maybe some of this is addressed.  I had a look and I can't find anything that conclusively tells me; there's a roadmap on the GNOME wiki, with a handful of papercuts listed, but no hints at substantial behavior changes.  There's a Planet GNOME, but not a lot on it about GNOME itself.

This has also given me some ideas for what I _would_ like to see in a window manager, but it's a little harder to explain without cobbling together a mockup.  I'll try to do that.  Someday.

* The Super key cannot be rebound for anything else.  I use it frequently for global operations: changing input method, running common programs, activating a launcher, WM shenanigans, and so forth.  It was fantastically useful, as virtually nothing but WMs have Super bound to anything, so I have a whole keyboard for personal custom shortcut use.  Now I'm bound to the bland shortcuts GNOME gives me.

    I also don't much like that Super brings up the Activities dashboard on its own—it's a _modifier_, and I frequently tap it when I may not mean to and have to dismiss a whole context change.  (I did this with Alt on Windows all the time.  It drove me batty.)

* I unintentionally hit the hot corner in the top left with the mouse _all the time_, because I'm used to tossing the cursor away when I'm done with it.  It feels like Paul Fitts has come back from the grave to haunt me.  The Activities dashboard comes up on accident about twenty times more often than I actually want it.

* I know I actually asked for this before, but it seems I was sorely mistaken: I can't stand the Alt-Tab and Alt-backtick behavior.  Consider the following.

    * I use a lot of terminals.  Like, a _lot_.  Most of them are used for radically different tasks: one is IRC, one is toodling around the filesystem, one is playing NetHack, and a dozen are writing code.  When I want to switch between "email" and "IRC", okay, those are different tasks, so I press Alt-Tab.  When I want to switch between "main email window" and "currently-open email", okay, those are different windows of the same task, so I press Alt-backtick.  When I want to switch between "IRC" and "code", those are different tasks, so I—whoops, no they aren't, they're the same program so they must be the same thing.  I keep hitting this horrible context wall where I have to stop and think about which key to press just to toggle between a couple windows.

        I saw a response to a similar complaint some time ago: "have you tried workspaces?"  What am I to do, have a separate workspace just for my NetHack game?  That won't work very well either, since:

    * Say I have two virtual desktops open.  On desktop A, I have a Firefox windows.  On desktop B, I have a Firefox window and a terminal.  I'm on desktop A, and I press Alt-Tab.  What happens?

        Well, the last focused application was a terminal, so GNOME wants to give me a terminal.  But the only recent terminal is on desktop B, so it _switches to desktop B_ and focuses the terminal.  My immediately reaction is "that's not what I meant, let me try again"; so I press Alt-Tab again, and now I see the Firefox window on desktop B.  I'm even further from where I started and briefly confused about what happened.

        Now multiply this by a dozen applications and half a dozen desktops.  Maddening.

    I have discovered that Alt-Esc tabs between all individuals windows on the current workspace, but it seems glitchy (leaves a lot of rendering junk behind), it's hard to press, and I don't even get a window or any other indication that it's doing anything.
    
    There's an extension to change Alt-Tab to do the Right Thing, but I'm still baffled as to why the new behavior would be so broken in the first place.

* Virtual desktops come and go automatically, which is good.  But they are in a single vertical column, which is awful.  If I have more than a few (which seems to be the intent?) then it's very easy to lose my place and forget which desktop is for what, especially when they're all the same at a glance: some terminals and a browser window.  At least with my main machine's 2×2 layout, each desktop has a unique position in space, and I can always get there by holding Ctrl-Alt and mashing the right pair of arrow keys.

* I had gvim open.  I wanted to open another gvim window.  No problem; invoke GNOME Do and run gvim.  Oops: GNOME helpfully focused the gvim window I already had open on some other desktop.  Also, gvim itself doesn't have a menu item for opening a new GUI window.

    It took me a few minutes and some Googling to actually figure this out; I had to find gvim within the Activities window, and I can either right-click it for a menu or do something like shift-clicking.

    I emphasize that I had to _look for help_ on how to _run a program_ because the _window manager was in my way_.  This is precisely why I avoid docks.

The running theme so far is that, despite the push for task-oriented desktops, GNOME 3 is doing the same naïve guessing as to what "task" means that we had with Windows XP a decade ago.  Multiple windows for the same application do not mean the same "task"; there are fundamentally different kinds of applications, and the ones that spawn the most windows (editors and viewers) are the ones that do so precisely _because_ each window is a separate task.

Please focus on fixing the problem, whatever that may mean; shaving a few seconds off of grandpa's email-checking experience is just not that important a goal.  Your target audience should surely be people who _make things_—everyone else would barely notice if the window manager vanished entirely.  Get applications to describe the _semantics_ of their windows—it's all open source, so you have the best possible environment for this kind of experiment already.  Let me actually define what my tasks are; I know better than you!  Make virtual desktops something more than a viewport onto a big space; give them their own working directory, their own wallpaper, their own names, some way to flip between them beyond spacially.  Try something new!  Think about how I use my machine, not about windows and processes and how many more levels of hierarchy you can stick them in.

Anyway.

* The number of customizations has dropped radically.  I needed to turn font hinting on slightly to fix the moiréd appearance of some characters in my terminals, and I had to resort to GNOME Tweak Tool.  Is this an obscure thing to want to do?

* NetworkManager has had its balls chopped off.  I don't have any specific complaints, as I've not done anything besides connect to the house wifi; I just have the eerie feeling that if auto-configuration doesn't work, I have no knobs to twiddle in a vain attempt to fix it.  Do I still have saved wifi connections, or are they just automatic, or what is even going on there?

    Also, deleting a VPN entry neither prompted for confirmation nor offered an undo.  Would've sucked if that were a mistake.

* Dialog windows are attached to the title bars of their parents.  They are also **unmovable**.  Several times now I've opened a dialog expecting to refer to the parent window while I use it, and I find that I can't do that because the dialog is fixed to the top center and covers what I wanted to see.

    I've also had a few such dialogs be too big to fit on my not-that-tiny laptop screen.  Because the dialog is immobile and modal, I have to close the dialog, try to move the parent window up more, and then open the dialog again.

* The menu styling is woefully inconsistent.  Most of the built-in GNOME stuff spawns huge space-wasting bubble that looks like a notification rather than something I should click on, whereas regular application menus are still...  regular application menus.  It's a bit jarring, and even now I still find myself suspicious of the GNOME-style menus.

* I frequently miss Pidgin notifications and find out that someone has been trying to talk to me for the better part of an hour (or day), to the point that I've stopped even running Pidgin on my laptop.  (Or have I?  With the tray always hidden, and my rare use of the dash, it's hard to tell.)

    This is at least in [GNOME Bugzilla][gnome bug on notifications].

* Similarly, it's become a bit awkward to use UIM, since its state is shown in the tray.  I have to remember what kind of characters I'm entering, which is worse than it sounds, because I can't use my usual shortcuts of Super-period and Super-comma.  The only alternative is a little floating window that shows all the time, even when I'm entering English text directly.

* I noticed this on our media center running Unity, so it's not really fair, but it also happened with Synapse which I think uses Zeitgeist so I'm going to complain about it anyway...

    "Most recently used" files don't really work.  They never have in the history of computing.  We have a main "media" directory, but rather than grok that we want _that_, the platform picks up on a variety of videos that we just watched and continually suggests those.  Which doesn't make any sense, because videos I just watched are the ones I'm _least likely_ to want to see right now.  I just saw them, after all.

    Are common files that big a deal?  I mean, it's convenient if I close something inadvertently and forget where it was, but I thought the demise of My Recent Documents taught us something.  Has anyone tried detecting just commonly-used _directories_, taking ancestors into account, and offering me a list (or tree!) of those?  Okay now I'm thinking about the failings of filesystems and that's really another post.

* If I want to run an application, I don't use the Activities > Applications thing; I use a launcher, perhaps even the one built in.  If I _don't_ remember what it's called, the flat Applications list is far too much to glance through quickly.  So this screen is useless for me either way; who is it benefiting?

    One of the cool things about package management was that new applications automatically added themselves to the right submenu.  Now I just have icon soup.

---

I am trying super hard to not unreasonably dislike GNOME 3, really!  But I either don't notice it's there, or it gets in my way.  Does anyone _like_ this thing?  Can you please tell me why?

I haven't gleamed a great impression of the GNOME inner circle from all this, either; I can't find plans, I can't find rationales, I can't find changes since 3.0.  (I guess this is the same problem I had with Perl.  Maybe I'm just stupid.)  I _have_ found multiple instances of devs giving resounding exasperated "NO"s to feedback similar to mine, often citing that GNOME 3 was "designed that way" (by someone other than the speaker, no less), but I can't figure out _why_ it was designed how it was.  Or sometimes it turns out _not_ to be designed that way, but it's impossible to tell the difference between bugs and misfeatures in this thing.

Who was all this designed for, exactly?  What applications besides the GIMP spawn multiple windows that always want to be grouped together?  Why is so much of the default behavior hostile to power users, when they're the ones who need the most support from the WM?

> And as I said, arguing about design in bugzilla is not useful. The designers don't read bugzilla, and so arguments here will have no effect on what they think. (As seen by the past year of inactivity on this bug.)

I guess we'll never know.

[gnome bug on notifications]: https://bugzilla.gnome.org/show_bug.cgi?id=641723
