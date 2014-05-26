title: Unity vs. GNOME Shell
date: 2011-05-10 22:22:00
tags: interfaces, linux
category: 90% of everything

For those not aware, the [GNOME][] world is getting shaken up lately.  GNOME 3.0 was released last month, with a completely redesigned interface called [GNOME Shell][].  Meanwhile [Ubuntu][], the biggest GNOME-based distribution by a gigantic margin, decided that they are super special snowflakes and do not want to use GNOME Shell, so they [repurposed][nih] their [netbook interface, Unity][unity], and scrambled to make it tolerable on desktops for the [11.04 Ubuntu release][natty] next week.

Our media center is running some ass-old release of Ubuntu and its main partition is too tiny to even upgrade any more, so a few days ago I bought a new drive, slapped it in, cleaned out an inch-thick layer of dust, and installed the 11.04 beta for the hell of it.  After using Unity for "long enough", I installed GNOME Shell and gave that a spin too.  Here is my impression.

Quick version: They are both terrible and I am sad.

<!-- more -->

## In common

### Docks

The biggest feature in both environments is the switch from a taskbar/menu setup to a dock, because hey that's what everyone else is doing now.

I _hate_ docks.  **Hate.**  Please understand the severity of this statement.  I try very hard not to say I "hate" much technology, so I can reserve the power of the word exclusively for docks.  I have never used AvantDock or RocketDok or Gnome Do's dock or BobsFirstSuperCoolDock.  The dock is one of the biggest reasons I cannot bear to use Mac OS X.

Docks are the embodiment of a major cardinal sin: they conflate "what I'm doing" with "what I might want to do".

I can see the logic here, and sometimes it might make sense.  I probably only need one copy of Thunderbird or a music player running, and if I just want to check my email, I don't care whether I'm running it for the first time or focusing an existing window.  Sure, I get that.

But that's just not how all—even _most_—applications work.  If I'm trying to run my file browser, I probably want a new window, because each window represents a _new task_.  Same goes for terminal windows, text editors, office software, web browsers, and so on; anything I create with, or otherwise use actively, rather than something that spins quietly in the background most of the time.  The little abstraction has been broken, because launching the program for the first time gives me a new window/document, but focusing a running window gives me something old I was already working on.  I now have to switch to the application and _then_ ask it directly to do a new task.  So my window manager now does less window-managing for me?  Great?

To add insult to injury, docks always give the slightest disdainful nod to this problem by putting a laughably subtle indicator on dock icons that happen to be running.  GNOME Shell has a slight white glow that I didn't even notice until I read about it.  Unity has two-pixel...  chevrons?  Dots?  They're too small on our giant TV for me to tell from the couch a few feet away.  Throw in several virtual desktops and these are utterly worthless.

There is but a single platform that almost kinda gets this right.  It is, of all things, Windows 7.

Rather than taking a launcher bar and kind of jamming task management into it, the Windows 7 taskbar is a _taskbar_ that can also quick launch.  If it's not a running application, it's not a button, and thus doesn't look "like a taskbar".  If it has several running windows, there are extra buttons peeking out from the right edge.  The only dock I can stand is the one that isn't a dock.

### Search

Both Unity and Shell get a lot of praise for having a cool integrated search bar whatsit so you can launch stuff just by typing a few letters.  Cool.  Except I've been using [Launchy][] or [GNOME Do][] or [Synapse][] for many years now, and they are all orders of magnitude better than the search in Unity or Shell (or Windows 7 or OS X's Spotlight), and oh by the way both environments broke them:

### Super

Unity and Shell both use Super (aka OS X's ⌘ key or the Windows key) to activate their overlay whatsits.  Note two things: that the Super key is a modifier, and that I didn't say what it's modifying.  Because it isn't.  Unity and Shell both trigger stuff when I press Super on its own.

You'll laugh at this, but one of the things that made me happiest about first switching to Linux was that pressing Alt on its own no longer did something.  I'd frequently hold Alt thinking about alt-tabbing somewhere, then change my mind and let go of Alt, then have a bunch of menus fly around the next time I pressed a key because Alt moves the focus to the menu bar.  The lesson ingrained in my head from this experience and subsequent relief was: **it is absolutely fucking unacceptable to have modifiers do things alone**.

Because they are modifiers.  They modify.  Imagine if pressing the Shift key alone was how you toggled Caps Lock.  Or imagine if you toggled some irritating accessibility feature by tapping Shift a few times...  [wait, nevermind][StickyKeys].

So now my Super key, my favorite modifier, has become a minefield.  But the nonsense doesn't stop here, oh no.

I really like to tie global modifiers to Super.  It matches how Windows's default keybindings work, and it fits pretty well since virtually no applications use the Super key for anything.  I have Super-S to launch a new terminal window, Super-H to open my home directory, Super-Shift-S for a new interactive Python terminal, and some other crap I can't remember.  It's nice to have a whole key to use for this kind of thing.

Canonical and GNOME agree with me so strongly that they've reserved the Super key _solely_ for use by the window manager.  I always had Super-space bound to my launcher (Do or Synapse or whatever), because a program launcher seems like a pretty global thing.  These no longer work; it's simply impossible to bind a global application shortcut that uses Super.  GNOME considers this [working as intended][gnome super bug]; Ubuntu [doesn't seem to care][ubuntu super bug].

The best part is that both environments only have a handful of actual shortcut keys that use Super, so most of my keyboard is going to waste.  I've been hunting for a replacement binding I like but have yet to find one.

### Customization

Both GNOME and Ubuntu have decided to collapse the various control panel applications into a single "System Settings" thing, much like KDE and OS X have.  Okay, cool.

Problem: some two-thirds of the settings seem to have disappeared.

There are fully _three_ different gizmos to mess with the screen in GNOME ("Screen", "Displays", and "Background"—and what the fuck are you doing calling two different things "Screen" and "Displays"?).  There are _zero_ for messing with the actual appearance of anything.  I can't figure out how to change the GTK theme, how to change the window decorations, how to change colors, how to change the icon set, how to change the cursor, or how to change the _default fucking fonts_.  But thank goodness that I can change _Bluetooth_ settings; now I can sync to my six-pound Palm smartphone from 2003.

(On a side note: all of Shell's system-y menus are a completely different design from regular menus and have huge padding around them.  This is driving me nuts.)

Ubuntu has hidden a lot of its settings as plugin options in the ever-arcane Compiz Config Settings Manager, which isn't installed by default.  Is this more or less insane?  I don't know.  Oh and by the way, despite Ubuntu's endless support for Compiz and how great it is, some combination of Compiz settings has turned the top bar completely black.  I found a few tickets about this with no responses yet.  So, good job there.

## Unity

Admittedly I broke Unity a bit when installing Shell over top of it, and only recently got around to fixing it, so I've used it somewhat less.  I suppose my biggest unique complaint is the shoddy handling of the menu bar, which is now jammed into the top bar, which is also the menu bar.  What?  Some applications actually _use_ their menu bars; imposing this design decision on them, for a window manager used by only a single distribution, seems incredibly rude.  (What's with the sudden hatred of menu bars, anyway?  Can we at least introduce a new idea before we all decide to bail on the old one?)

## Shell

### Workspaces

Way back when Shell first hit public (okay, "public" for Linux users) consciousness, the dashboard overlay activity view thing was a little different.  It showed all of your workspaces in a grid, with a great honking "+" button at the bottom.  You could click it and just get a new workspace, just like that.  Or you could click "-" on an existing workspace with no windows on it, and it would just vanish.  All the rest would rearrange themselves into a nice grid to accomodate the change.

I was _ecstatic_ over this.  I've never seen a workspace implementation before that didn't force you into picking a rigid x-by-y grid in some hidden dialog somewhere.  It was looking like Shell actually matched how I want workspaces: spin up a new one for a new task, dump some junk in it, get rid of it when I'm done.  Right now I have four workspaces that accumulate several tasks each at a time, just because changing the number of workspaces and managing a varying number of them is so painful.

Somewhere along the line this approach was quietly dropped.  The _one feature_ I was looking forward to was scrapped without so much as a blog post announcing its untimely demise.

For a while Shell was back to a traditional grid approach, but now they have something different.  The current implementation just gives you a new workspace whenever there's at least one window on all your existing workspaces, and closes a workspace when it's empty.  Workspaces are apparently all in a single column.  This does some weird things; for example it's "impossible" to move a lone window down to the empty trailing workspace, because this will (a) close the now-empty workspace and (b) create a new empty workspace at the end again.  So while I get my easily spun-up workspaces, I can no longer have any "permanent" workspaces; if one becomes empty, it just vanishes.  I can't see any way to reorder them, either.  Or name them.  Or switch between them faster than ctrl-alt-arrow.  This is considerably less useful.

Oh, and by the way: Shell has dropped the Minimize and Maximize buttons.  If you want to minimize something, you should just "use a workspace", which they have kinda screwed up!  Also you can't minimize to the tray any more because the tray is gone.  I think the GNOME team is just telling me to stop running so many darned programs.  How can we be as popular as the iPad if we're multitasking?

## The less-bad

Admittedly this is not all horrendous; there are some good things.  I'm kinda leaving out Unity here because it's barely registering as being a real thing.  I'm sure I'll have more angry typing to do if I ever upgrade my desktop to 11.04.

* Trying something new is good.
* Windows that want my attention flash a little "Some Window is ready" thing at the bottom of the screen, which is kinda cool, though unfortunately not permanent.
* The system tray _does_ need to go, but I was hoping to see that happen with a better alternative to minimizing than "use our gimpy workspace implementation".
* The classic two-panel GNOME layout wastes a lot of screen space, which is why I ditch it ASAP after installing GNOME 2.
* I _do_ like the OS X-style window switching where it's possible to switch between instances of a single application.  I'm sure Compiz can do this but I was never buggered to figure out how.
* The new font is nice...

Okay, I tried.

## What I'd like to see

We need something that handles all of the following:

* Applications that have a lot of distinct but related windows, like the GIMP.
* Applications that really only run once.
* Applications that have a lot of similar and unrelated windows, like editors and terminals.
* What's not running, but that I frequently want to run.  (panel launchers)
* What's not running and isn't run very often, but is installed.  (menu)
* Minimized windows.  (taskbar noise)
* Applications that minimize or "close" themselves to the system tray, giving yet another place to look to see what's running.  (tray)
* Windows that want attention.  (flashing taskbar, popup notifications)
* System things that want attention.  (popup notifications)
* Notifications that aren't urgent, but may be interesting.  Don't need to handle them right now, just sometime.

Docks are awful; I've been treating Shell so far like I just have no taskbar at all.  Naïve taskbars, though, are no better; you get a lot of clutter very easily, and they don't leave much room for other interesting things in your panel.  Auto-collapsing like XP introduced is the worst of both worlds.

Window titles are more important than they're being treated as of late; if I have a program running twice, well, I kinda need to know which window is for what.  Even if not, for something document-oriented like an editor or browser or terminal, just seeing the icon doesn't actually tell me what the program is doing.

I had an idea a while ago for a taskbar that clustered windows from the same application together, having the buttons fused together with the icon only appearing once.  Minimized windows could _only_ show icons, so there'd be no need for minimizing to the tray at all.  Buttons could still flash to attract attention as always.  Common programs could sit on the far left when not run, and jump onto the taskbar while running.

I'm still unhappy with Ubuntu's new notification system; I wish notifications of "sufficient" importance could accumulate over time if I don't touch them and sit somewhere where I can see them later.  I think OS X has a third-party notification thing that can do this.

Basically I think there was still a lot more to be done with taskbars before giving up on them entirely.  Nobody has really tried to fix them since Windows 95 came out; there have been a few tweaks, but very few attempts at really resolving any of the problems with them.  I could doodle the sort of thing I have in mind, but it might be too late to bother now.  Short of moving to xfce, docks have won.  :(


PS: Shell's top bar has a ton of empty space yet can't manage to find room for the _date_.  Just the weekday.  Jesus.

[GNOME Do]: http://do.davebsd.com/
[GNOME Shell]: http://live.gnome.org/GnomeShell/Screenshots
[GNOME]: http://www.gnome.org/
[Launchy]: http://launchy.net/
[StickyKeys]: http://en.wikipedia.org/wiki/StickyKeys
[Synapse]: https://launchpad.net/synapse-project
[Ubuntu]: http://www.ubuntu.com/
[gnome super bug]: https://bugzilla.gnome.org/show_bug.cgi?id=576632
[natty]: http://www.ubuntu.com/testing/natty/beta
[nih]: http://en.wikipedia.org/wiki/Not_Invented_Here
[ubuntu super bug]: https://bugs.launchpad.net/unity/+bug/715760
[unity]: http://unity.ubuntu.com/
