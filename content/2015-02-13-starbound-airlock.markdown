title: Starbound airlock
date: 2015-02-13 18:42
category: process
tags: starbound, puzzles

Starbound is a 2D exploration and building game currently in development.  Yes, yes, it's like Minecraft, except 2D, and with actual art, and fun.

A recent update added wiring (or perhaps upgraded it into being useful?), which lets you wire anything into anything.  A notable feature of Starbound's wiring over Terraria's or Minecraft's is that logic gates are _actual objects_, not emergent behavior.  So you don't have to build everything out of goddamn NANDs.  Also, the wires aren't physical objects; they're just straight lines connecting an input to an output, they take up no space in the world, they don't participate in any form of collision detection, and they appear on a separate layer that you only see when you're using the wiring tool.

There's not a _whole_ lot you can do with the wiring in Starbound yet.  The devices you can control are, for the most part, lights and doors.  Other players can just destroy anything you build, anyway.  So it's really only useful for visual effect right now, much like everything else you can build.

Still, there are a couple mechanisms of interest.  Last night I built an airlock, and while it's not an astounding feat of electrical engineering, I thought it was an interesting enough problem that someone else might enjoy reading about it.  So here I am, blogging for once.  I hope you're happy.

<!-- more -->


## The problem

I've got a friend who's started building into an asteroid.  She asked if I could wire the entrance to vaguely resemble an airlock.

It's worth note here that there won't actually be any air.  Either an entire environment has a breathable atmosphere, or none of it does.  So this is just for show.

The entrance looks like this:

{% photo /media/2015-02/airlock-start.png What we start with.%}

Astute readers may notice that this is not, in fact, an asteroid.  I forgot to take any screenshots while building this, so I'm having to do it again.

If I switch to the wiring tool, you see this:

{% photo /media/2015-02/airlock-startwires.png Wiring tool.  No wires yet. %}

Purple nodes are inputs; red nodes are outputs.  By convention, inputs appear on the left side of an object, and outputs appear on the right.  You can see here that I can wire something into the doors or the torches; if I do, the door will be open (or torch will be lit) only while the input signal is active (or on, or true, or whatever you want to call it).  If they're not wired, I can open/close doors and light/extinguish torches with the `E` key.

I also have, at my disposal, an unlimited supply of the following:

- Wire (since it doesn't cost anything)
- Logic gates: AND, OR, NOT, XOR
- D-latches
- Wall switches, levers, and other manual input devices
- Sensors and pressure plates
- Various liquid and water sensors which are unlikely to be helpful here

Now, the goal of an airlock is that no more than one door is ever open at a time.  What I want is this sequence of events:

1. One door opens
2. A player steps through into the airlock
3. The first door closes
4. The second door opens
5. The player continues through the airlock
6. The second door closes

Seems simple enough.

## First attempt

You may notice that the doors also have an output node.  This is active only when the door is open.  So the obvious thing is to just wire the second door, through a NOT gate, to the second door.

{% photo /media/2015-02/airlock-attempt1.png First attempt, wired. %}
{% photo /media/2015-02/airlock-attempt1b.png First attempt, no wires. %}

Great!  You open the outer door, and the inner door closes.  Perfect.

Except, er.  Because the inner door is now wired, it can't be opened or closed manually.  You have to open the outer door, walk through it, then _turn around and close it_ before you can continue.

Also, you can't ever actually leave.  Because you have no way of controlling the inner door.  Oops.

Well, this seems fixable.  I have some pressure plates, after all.  I'll just put some around the _inner_ door, and open it if you're standing on them.

{% photo /media/2015-02/airlock-attempt1-plates.png Pressure plates wired to the door. %}
{% photo /media/2015-02/airlock-attempt1-both.png Both doors open.  Whoops. %}

Hmm.  Okay, let's wire the pressure plates through another NOT, and then attach that to the outer door.  So the outer door will be closed if you're next to the inner door.

{% photo /media/2015-02/airlock-attempt1-morewires.png Attempting to fix this. %}

Now the outer door can't be opened manually; it just remains open as long as no one is near the inner door.

That...  _works_, but doesn't quite fit what I wanted.  I'd like _both_ doors to be closed if no one is nearby.

To do that, I'd need pressure plates around both doors.  And I'd have to wire each door so that it's only open when a pressure plate is active AND the other door is NOT open.

Okay, we can do this.  No problem.

{% photo /media/2015-02/airlock-attempt2-wired.png Mirroring to the other door. %}
{% photo /media/2015-02/airlock-attempt2-unwired.png Mirrored, without wires. %}

Great!  This does actually work.  By default, both doors are closed.  When I approach one, it opens.  When I approach the other, it opens when the other closes.

Except...

There's a slight delay after stepping off a pressure plate, before it deactivates.  It's not very long, maybe half a second or less.  It's just a bit more than the time required to run through a door, which is good, because otherwise the doors would close on top of you as soon as you tried to step through them.

Unfortunately, this means that the first door you run through stays open for a moment.  Just long enough for you to run right into the other door, and have to wait for the other pressure plates to deactivate before you can continue.

It's a minor problem, but it's annoying.  You could solve it by making the airlock wider, so the plates have deactivated by the time a player has run across to the other door.

But I started to wonder whether it were possible to really fix this, even for a small airlock.  If holding down _both_ pressure plates meant that the _most recently approached_ door opened, the airlock would work perfectly.  It would even function usefully when two people tried to cross it in opposite directions.


## The latch

The problem is, if both plates are held down, there's nothing indicating which happened more recently.  Circuits don't have a useful notion of memory; there's only inputs and outputs.

We need memory.  We need a _latch_.  And thank god that Starbound supplies one, because building one yourself is...  [awkward](http://en.wikipedia.org/wiki/Flip-flop_%28electronics%29#Gated_D_latch).

{% photo /media/2015-02/airlock-attempt3-latch.png Well, that's encouraging. %}
{% photo /media/2015-02/airlock-attempt3-latchnodes.png Latch nodes. %}

The latch in Starbound is a gated D latch, a memory cell with two inputs.  The top input node is _enable_, and the bottom input node is _data_.

As long as _enable_ is on, the latch will merely pass through _data_.  However, the moment _enable_ turns off, the latch's output will "freeze" as the current value of _data_.  Any future changes to _data_ are ignored until _enable_ turns on again.

The latch effectively remembers a single bit, and you write to it by turning _enable_ on briefly.  Perfect.


## Latching the airlock

At any given moment, there are two questions we want to answer:

1. Should the left door be open?
2. Should the right door be open?

The only information we have is whether a pressure plate for the left door is active, and similar for the right door.  We'll call these `L` and `R`.

`L` and `R` only give us four possibilities, but we actually have _five_ cases to distinguish between:

1. No plates are active.  Close both doors.
2. Only left plates are active.  Open the left door.
3. Only right plates are active.  Open the right door.
4. Both plates are active, _but the left plates were pressed more recently_.  Open the left door.
5. Both plates are active, _but the right plates were pressed more recently_.  Open the right door.

The "most recently" part is what we need to store in our latch, which we'll call `D`.  The question is, how do we actually store "most recent"?  That only makes sense the moment the second plate is pressed, at which point we've already lost that information.

Instead, let's try it the other way: we'll store the plate that was pressed _first_.  We can do this easily, by storing the pressed plate, when only _one_ plate is pressed.  Let's say a left plate is stored as 0 and a right plate is stored as 1.  Then we have:

* _enable_ = `L ⊕ R` — we only want to store a value while _one_ door is open
* _data_ = `R` — we want to store 0 for `L` and 1 for `R`, but only one is active, so that simplifies to just storing whether a right plate is pressed

With this, we can construct our latch, and demonstrate to ourselves that it remembers the last individual plate to be pressed.  To make things simpler, I've replaced the plates with small toggle switches, so I can easily simulate pressing both at the same time.  I've also introduced OR gates above each door; these are the values of `L` and `R`.  You can always connect multiple wires to one input node to simulate an OR, but this gives a visual cue for the values we're using, because the gates light up when they're on.  Plus, wires disappear when the object at either end is destroyed, so having a dummy gate as a buffer means I can move the doors around later without wrecking the guts of the circuit.

We can see that the latch is correctly 1 when I flip the right switch, then stays as 0 when I flip the left switch:

{% photo /media/2015-02/airlock-latch-right.png Right switch flipped. %}
{% photo /media/2015-02/airlock-latch-rightleft.png Right switch, then left switch. %}

And if I flip only the left switch, it's set to 0.  Then if I flip the right switch, it becomes...  1?  What?

{% photo /media/2015-02/airlock-latch-left.png Left switch flipped. %}
{% photo /media/2015-02/airlock-latch-leftright.png Left switch, then right switch. %}

There's a very subtle problem here, and it took several rounds of rapidly flicking switches to figure out what it was.

You see, circuit updates in Starbound are _not_ instantaneous.  They propagate (I believe) along only one wire per frame.

So initially, `L` = 1, `R` = 0, `L ⊕ R` = 1.  Thus the latch receives _enable_ = `L ⊕ R` = 1, _data_ = `R` = 0.

When I flip the right switch, `R` becomes 1.  `R` is wired directly into two gates: the XOR, and the latch's _data_ node.  So it updates `L ⊕ R` to be 0, and updates _data_ to be 1.

But the latch only sees the change to _data_, because the change to _enable_ is one gate further away!  For **just this one frame**, the latch sees _enable_ = 1 and _data_ = 1, because the XOR makes the _enable_ "lag" one frame behind.

The fix is to make _data_ lag as well!  If I add a useless OR gate and plug `R` into it, the problem disappears:

{% photo /media/2015-02/airlock-lagfix.png Fix for the lag. %}
{% photo /media/2015-02/airlock-lagfix-left.png Fixed lag: left switch flipped. %}
{% photo /media/2015-02/airlock-lagfix-leftright.png Fixed lag: left switch, then right. %}

Success!  We have our latch, which remembers the last switch/plate to be the _only one active_.  Now we just need to open the doors.


## The doors

Keeping in mind that our idea of what `D` means has changed, we can make a truth table:

 `L` | `R` | `D` | left door | right door
-----|-----|-----|-----------|------------
  0  |  0  |  —  | closed    | closed
  0  |  1  |  —  | closed    | open
  1  |  0  |  —  | open      | closed
  1  |  1  |  0  | closed    | open
  1  |  1  |  1  | open      | closed

From here it's not hard to see that:

* `left door = L ∧ (¬R ∨ D)`
* `right door = R ∧ (¬L ∨ ¬D)`

Intuitively, this makes sense.  For a door to be open, its plates _must_ be active.  Also, _either_ the other door's plates are inactive, _or_ (if both plates are active) the other plates were the first ones activated.

Throw in a couple AND and NOT gates, replace the switches with pressure plates, and we have our airlock!  Remember, you can attach multiple wires to a node to simulate an OR.

{% photo /media/2015-02/airlock-final-wired.png Final wiring. %}
{% photo /media/2015-02/airlock-final-notwired.png Final without wires. %}

Never said it would be pretty.

And here it is on the actual asteroid:

{% photo /media/2015-02/airlock-live-wired.png My actual airlock. %}
{% photo /media/2015-02/airlock-live-unwired.png My actual airlock, no wires. %}

And with that, I have run out of interesting mechanisms to build, which is why I need to go mod some into the game.  ♥
