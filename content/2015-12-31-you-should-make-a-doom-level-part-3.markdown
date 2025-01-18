title: You should make a Doom level, part 3: cheating
date: 2015-12-31 23:20
modified: 2016-03-19 19:10
category: articles
series: make a doom level
tags: gamedev, tech, making things, doom

Tens of thousands of words later, you've watched me build a little world, and hopefully tried building your own.  All the way we've had to deal with Doom's limitations.  Flat surfaces.  No room over room.  The world can only move vertically.  The only tool we've found so far that can get around those restrictions is the sky hack, and even that's fairly limited.

I've saved this for last because it's more complicated than anything else, by far.  It also finally, utterly, breaks compatibility with vanilla Doom.  You could apply everything I've said so far to vanilla with some tweaking — use line types instead of specials, make a Doom-format map, skip the separate light levels and other tricks.  But, this, all of this, is very much ZDoom only.

Finally, the time has come.

It's time to annihilate all of those restrictions.

Mostly.

<!-- more -->


## 3D floors

Liquids are a tricky beast in Doom.  Historically, like I've been doing, liquids have just been floor textures.  Later, creative modders discovered the "[self-referencing sector](http://doomwiki.org/wiki/Making_a_self-referencing_sector)" trick, which creates the illusion that you're standing below the floor.  That's about as far as you can go with the vanilla engine.

One of the earliest source ports was [Boom](http://doomwiki.org/wiki/Boom). It was mainly for fixing bugs and lifting some restrictions on how big maps could get, but it also added a few new toys.  One was the `Transfer_Heights` line special, which would let you draw one sector's floor and ceiling _inside another sector_.  Remember `ExtraFloor_LightOnly`, which would copy one sector's lighting onto another sector's walls?  This is the same idea, except it would draw the control sector's entire floor and ceiling in another sector.  So you could have a fake water texture at whatever height you wanted, and the player could go entirely beneath it and see it above them.

But we're in the future now, and we can do much better.  We can make honest-to-god _3D floors_.  Let me show you.

I'm cracking open the map I already had.  There's no water here, but there's plenty of lava, and it can definitely be made to look better.  I'll start with that magma chamber.  First I'm going to lower the floor a bit, remove the lava texture, and remove the floor light level — the lava will be entirely separate, so all I need is a model of an empty chamber.

{% photo /media/2015-12/doom3/slade01-empty-chamber.png The magma chamber, without the magma %}

I need to make a _control sector_ — a dummy sector, out in the void.  The _ceiling_ will become the _top_ of the 3D floor, and the _floor_ will become the _bottom_.  I'm just going to make the floor and ceiling both lava, and put the floor height down some ways.  (If the 3D floor's bottom goes below the real sector's floor, it just won't appear.)  Finally, I'm going to make the control sector do 20% damage, and the empty magma chamber _not_.

Now for some magic.  Tag the magma chamber; I'm using `101` here, just to distinguish my 3D floors from actual mechanisms.  Pick a line of the sector and give it the `Sector_Set3dFloor` special (under "Sector").  The type should be "swimmable", and the opacity should definitely not be zero.  I'll use `160`, which is about two-thirds opaque.

{% photo /media/2015-12/doom3/zdoom01-deep-lava.png Deep lava, complete %}
{% photo /media/2015-12/doom3/zdoom02-deep-lava-gzdoom.png Deep lava, in GZDoom %}

Shazam!  Deep translucent lava, through which you can see the floor below.  If you step in it, you take the 20% damage from the control sector.

The first screenshot is in ZDoom, and the second is in GZDoom.  Remember that ZDoom still uses Doom's original palette of 256 colors, so getting a transparency effect to look nice can be tricky.  There are lots of reds, though, so this worked out pretty well.

Alas!  SLADE can't show you 3D floors in 3D mode ([_yet_](https://github.com/sirjuddington/SLADE/issues/205#issuecomment-167007882)), so you'll have to hop into the game to get a feel for how it looks.

Alas!  I can't find a way to change the light level of the _top_ of the lava.  The control sector's light is used for _inside_ the lava and _below_ it, to the next 3D floor, or in this case to the real floor.  The real sector's light is used for everything above the topmost 3D floor.  [I'm asking around](http://forum.zdoom.org/viewtopic.php?f=3&t=50295), but nothing seems to change the light level of only the top surface.

That looks kind of goofy in this dim room, so I'm going to hack this into working.  The chamber's light is currently `160`.  I'm going to change that to `224`...  and then set the light of the ceiling _and every single wall_ to `-64`.  Yes, each _side_ of a line can also have its own light level, just like floors and ceilings.  It's under "Lighting".

(If you're using a SLADE dev build, or if this is the future and you're using 3.1.1 final, you can just select the sector and then switch to lines mode to select all of its lines.  Of course, you can also just change the wall light levels in 3D mode by unlinking and using <kbd>;</kbd> and </kbd>'</kbd> — this doesn't work correctly in beta 2.)

{% photo /media/2015-12/doom3/zdoom03-bright-lava.png Brightening the deep lava %}

And there you go!  Had to take the scenic route, but hey, it works.  It's most obvious towards the back of the room.


### Getting fancier

Let's move on to the lava chasm.  I'll need a new control sector here, because the lava level is different.  (You can always slap the same sector tag on multiple sectors!  Pretty much every special will apply to every tagged sector simultaneously.)

I'm doing basically the same thing here.  Remove the lava texture, remove the 20% damage, lower the floor a little.  Draw a control sector, give it lava textures, set the floor at the lava level and the ceiling as some big negative number.  Now tag the chasm—  wait, uh oh.  I already have the cave sector tagged, for `ExtraFloor_LightOnly`.  I can't give a sector two tags, so what can I do?

(Okay, you _can_ give a sector two tags, but only in dev builds of ZDoom, and SLADE doesn't understand it yet.  So bear with this other hack.)

My cave is tagged `6`.  I'm going to tag the main part of the chasm as `102`.  And then I'm going to apply `Sector_Set3dFloor` to _two_ lines of my control sector — one applying to tag `6`, one applying to tag `102`.

I'm also going to do the same lighting trick again, to keep the lava bright and everything else not.

{% photo /media/2015-12/doom3/zdoom04-lava-chasm.png Deep lava in the chasm %}

I, uh, also went and changed the opacity to `192`, because `160` was really a bit too transparent for _lava_.

That also gives me an interesting idea.  The side cave is really blindingly obvious right now, but this lava is _deep_.  What if I made it a little deeper?  Deep enough to hide the cave entirely?  Seems like a nice way to make a secret.

{% photo /media/2015-12/doom3/slade02-deeper-cave.png Moving the cave further down %}
{% photo /media/2015-12/doom3/zdoom05-under-lava.png Cave under the lava...  but... %}

Ah...  hm.  That looks like complete ass.  To fix this, I'll have to take a brief detour into ZDoom's colored lighting.  There are two kinds of light color you can control.

* The [_light color_](http://zdoom.org/wiki/Colored_lighting) of a sector is a tint applied to every surface and thing inside that sector.  It is, of course, visible from the outside of a sector, so you might see several light colors on screen at once.  Just like transparency effects, this is hampered somewhat by ZDoom's use of a palette.  The default light color is white, which obviously doesn't tint anything at all.

* The [_fog color_](http://zdoom.org/wiki/Fog) is really the color of _darkness_.  Surfaces and things further away from you are already rendered darker (i.e., towards black) in the Doom engine, and setting the fog color allows you to change the color that distant things fade _to_.  With brighter colors, this looks like fog.  (Unfortunately, it doesn't apply to the sky, which somewhat hurts its usefulness as actual fog.)  The default is black, but as the wiki notes, there's more difference between no fog and `#010101` than between `#010101` and `#ffffff`.

You can set either of these per-sector.  If you set the light color in a control sector, it'll be transferred to the 3D floor.  So maybe you want to make the light in the lava red.  Sure, why not.

However, if you set the fog color in the control sector, it won't become the fog color in the 3D floor!  Instead it becomes a [_palette flash_](http://zdoom.org/wiki/Palette_flash), which is the name for effects like the glow when picking up items or the green overlay when wearing the radiation suit.  So if you set the control sector's fog color to a reddish-orange, say...

{% photo /media/2015-12/doom3/zdoom06-palette-blend.png Applying a palette blend %}

Beautiful!  The entire screen is blended with that color.  And this isn't susceptible to palette issues, even in ZDoom, because it actually _modifies the palette_ as long as the player's view is within the lava.

One thing still bugs me here.  This is lava, right?  Lava is thick.  I shouldn't be able to see through it so well.  This is like watery Kool-Aid™®.

Well, how do you limit view distance in Doom?  Ironically, after all that effort to make the _top_ of the lava brighter, I have to make the lava itself darker!  And bump up the "fog color" to compensate.

{% photo /media/2015-12/doom3/zdoom07-thick-lava.png Changing the light level to make the lava thicker %}

This took _a lot_ of fiddling, and it's still not quite right — for example, the upper part of the sector shines through the lava, because the sector's "real" light level is so much brighter.  You could bump the opacity up a bit more if you like, but I'm going to leave this how it is.

As for the cave, well, it's currently _under_ the lava, which is doing wacky things to `ExtraFloor_LightOnly`.  I'd better make this an actual cave above the lava, and give the teleporter a little dry land to sit on.  And of course, there should be a prize, and the sector should be marked secret.  (I would mark the wall secret as well, but that doesn't do much good here, since the edges of the cave show on the automap if you look down into the lava.  Consider that the hint.)

{% photo /media/2015-12/doom3/zdoom08-lava-secret.png Teleporter cave, now a secret %}

A worthy prize for braving the magma.


### Even fancier

We have a teeny tiny problem.  I made a second tag so that the 3D floor and `ExtraFloor_LightOnly` could coexist peacefully, but I neglected to make a third tag to handle the raising bridge.  So now it doesn't work.

I'll pretend that was on purpose, because we can do much better.  Currently, my bridge is jammed against the wall, because otherwise it would split the chasm in half and the player could still get trapped on one side.  I think that's pretty ugly, and would like to improve on it.

How about we use a 3D floor, so the player can walk under and over it?

This isn't really any different.  I have to draw a sector that will contain the floor; I'm going to cut out bits of it so it looks kind of like a grating.

{% photo /media/2015-12/doom3/slade03-draw-bridge.png Drawing a new bridge %}

Now I tag it as `103`, and I make a third copy of the lava special so there's still lava in this sector.

The control sector for my bridge will be 16 units tall, and initially sit at the very bottom of the lava.  It could start entirely below the regular floor if I wanted, even.  I'll give it some metal textures and slap on `Sector_Set3dfloor`, making it solid and fully opaque.  Note that the _sides_ of the bridge will be drawn with the front middle texture of the line with `Sector_Set3dFloor` on it.  This hasn't mattered so far because we've been dealing with lava in a pool, where you can't see the sides.

Okay, now what?  How do I make the switch work?

First I need to give _the control sector_ a tag — because the control sector is what I want to move!  But that's not enough.  The switch is currently using `Floor_RaiseByValueTxTy`, which will raise the _floor_ of the control sector, which is the _bottom_ of the bridge.  I need a special that will raise the entire sector — both its floor and ceiling.  Luckily, there are several of these!  They're intended for use in elevators, but work just as well here.  Change the switch to `FloorAndCeiling_RaiseByValue`, and be sure to fix the sector tag (of the _control sector_, not of the real bridge sector!) and the distance to raise.

Result:

{% photo /media/2015-12/doom3/zdoom09-bridge-bottom.png The bridge in its starting position %}
{% photo /media/2015-12/doom3/zdoom10-bridge-raising.png The bridge rising from the lava %}
{% photo /media/2015-12/doom3/zdoom11-bridge-raised.png The bridge in its final position %}

It even automatically casts its own shadow — because the light _beneath_ a 3D floor is inherited from its control sector.

----

You may have noticed something extra in the above screenshots that I'd already made!  I wanted to make a simple decoration with 3D floors.  All I did was draw and texture a crate (which is 64×64×64), draw a second crate outline, rotate them, overlay them, and fill in the second one with a 3D floor.

{% photo /media/2015-12/doom3/slade04-crate-drawing.png Drawing some crates %}
{% photo /media/2015-12/doom3/slade05-crate-stacking.png Stacking them together %}

Granted, this would be more impressive if my room were a little taller.  As it stands, I could've done this using only vanilla features, because there's no space directly above another space here.  But I _could_ raise the ceiling, and there would be space both above and below the extra crate.

This all, uh, may seem a little complicated and fraught with caveats.  And it totally is.  I get the impression that 3D floors aren't used too seriously yet, despite being a few years old.  Everywhere they interact with an existing feature needs special cases to handle them, and there have been some oversights, and no one notices until someone actually tries to use them that way.  I've found several obvious missing features in the past few months — but they're all fixed now, so it's getting better.

I wouldn't recommend building an entire map out of them, but they're pretty slick when used with a light touch.

You can always [read the docs](http://zdoom.org/wiki/Sector_Set3dFloor), but here are a couple other ideas:

- 3D floors can't block sound (because sound travels between sectors, not through 3D space), but they _do_ block monster sight.  So you can stack multiple floors and run around on one without alerting monsters above you.  Note that if you want monsters to spawn _on top_ of a 3D floor, you'll have to give them a Z height, or they'll just spawn on the real floor.

- For a simpler approach that still feels "more" 3D than vanilla Doom, you could have hallways that cross each other and are separated by a 3D floor.

- You could make a "thin" lift, like the ones in Quake.

- You could make suspended bridges of wooden planks.

- You can do some interesting special effects with specials like `Floor_LowerInstant`...

However, as with any other sector-based geometry, 3D floors cannot move sideways, only up and down.  Alas.

Ah, but I qualified that with "sector-based".  Does that mean...?


## Polyobjects

You betcha.

You know my door between the two tech rooms?  The one that opens with a switch?  That door is super boring.  Also, it looks like a regular door, which is pretty misleading.  Also, I want it to _slide open sideways_.

I need to draw a big open empty space somewhere in the void, well away from the rest of the map.  This is kind of like a dummy sector, but it's not the sector itself I care about.  I'm going to draw both sides of my sliding door in this sector, and then _delete them_, leaving a void.  My door frame is 128 tall and 16 wide, so each door half needs to be 64 tall.  I'm also going to texture them like I want them to appear.  I end up with this:

{% photo /media/2015-12/doom3/slade06-polyobj1.png Drawing polyobjs in the void %}
{% photo /media/2015-12/doom3/slade07-polyobj2.png Texturing polyobjs %}

Now I'll turn these into [_polyobjects_](http://zdoom.org/wiki/PolyObjects).  Polyobjects (or just "polyobjs") are chunks of geometry that get overlaid onto the map in a different place.  They consist only of lines, not sectors — they'll never have ceilings or floors.  These basic ones consist only of one-sided lines, so they're actually infinitely tall.

Turning a void shape into a polyobject requires three things.

1. Pick a line on each polyobject and give it `Polyobj_StartLine`.  Polyobjects have numbers, independent of sector tags or anything else, so I'll just make these door halves `1` and `2`.  Because they're parts of a door, their actions should mirror each other at all times, so I'll also give them _each others'_ numbers as the "mirrored" polyobj.

2. Place a "PolyObject Anchor" thing (in Special Effects → PolyObjects) inside each shape, _in the void_.  Pop open the properties for each and set the numeric value of the _angle_ to the corresponding polyobj number.  Yes, the angle.  You set the angle to `1` or `2`.  I don't know why, when things can take arguments; I guess polyobjs predate that.

3. Place a "PolyObject Start Spot" thing where you would like the polyobject to appear in the map.  It'll be placed relative to where the anchor is, of course.  Again, use the angle to indicate polyobj number.  (There are actually three types of start spots, and the difference is in how they handle trying to move when someone's in the way.  For a door, you probably want the "Harmless" variant.)

{% photo /media/2015-12/doom3/slade08-polyobj3.png Placing the anchors and start spots %}
{% photo /media/2015-12/doom3/zdoom12-polyobj-door.png The resulting door %}

That sure was a lot of work just to make a barrier.  Let's make it actually do something!  I'm changing my switch from `Door_Open` to `Polyobj_Move`.  (There's a `Polyobj_DoorSlide`, but that closes the door after a delay, which I don't want.)  I only have to move polyobj number `1`, because they're mirrored and will move together.  The angle is a [_byte angle_](http://zdoom.org/wiki/Definitions#Byte_Angles), which SLADE doesn't currently have UI for, but a quick look at that wiki page tells me I want `192` for south.  For the distance, I'm going to use _slightly less_ than 64, so the edge of the door peeks out from the wall.  Just like when a door opens upwards.

And that's it!  A sliding door.  Certainly more cumbersome than a regular door, but a nice change of pace.  It blocks sound and sight when closed, just like you'd expect.

{% photo /media/2015-12/doom3/zdoom13-polyobj-open1.png Opening the polyobj door %}
{% photo /media/2015-12/doom3/zdoom14-polyobj-open2.png Fully-opened polyobj door %}


### Two-sided polyobjs

This leaves us with a slight feature gap.  3D floors give us a free-floating block of geometry that can move up and down.  Polyobjects give us a free-floating shape that can move sideways.  Is there no way to get the best of both worlds?

Well...  kinda!  You can also make polyobjects out of _two-sided_ lines, and combine them with a couple other features of two-sided lines.

Let's say I want to turn my very first door into a sliding _gate_.  You can't do this the same way I did it above, because gates are transparent, and transparent textures on one-sided lines does bad things.  Instead I'll draw my gate (which here is just a single line) and use `Polyobj_ExplicitLine` to mark all of its lines as being part of the polyobj.  (

I will, of course, also have to give it some middle texture.  Doom has several grate-y textures named starting with `MID`.  Remember that middle textures on two-sided lines _do not tile_, and do not deal well with poking into the ceiling or floor!  (Unless you check "Wrap MidTex" or "Clip MidTex".)  Remember also that middle textures draw from the _top_, so if you want your gate to sit on the floor, you might want to lower unpeg the line.  It helps if the dummy sector has the same floor and ceiling height as the place you intend to put the polyobj.

Other than that, it's basically the same: plop down an anchor and a start spot.

{% photo /media/2015-12/doom3/slade09-gate-before.png The door, before changing anything %}
{% photo /media/2015-12/doom3/slade10-gate-polyobj.png Drawing a single-line polyobj %}
{% photo /media/2015-12/doom3/slade11-gate-anchor.png Placing the start spot %}
{% photo /media/2015-12/doom3/zdoom15-polyobj-gate.png Resulting two-sided polyobj %}

Beautiful.  Except you can walk right through it.  Oops.  To fix that you can give the line the "3D MidTex" flag, which makes its _texture_ blocking.  You can use this for regular railings and the like, too, and it'll only block the player where the texture appears.  You can even walk on top of it!

I'm also going to use the `midtex3dimpassible` flag.  It's only in dev builds of ZDoom, but it makes a 3D midtex obey the same rules as "Impassible" lines — that is, players and monsters can't walk through it, but projectiles and bullets can pass freely.  That will let the monsters outside attack the player through the door.  SLADE doesn't know about it yet, but I can add it manually with the button at the bottom of the prop grid.

Neat.  Only one problem left.  How do you open it?

If this were a regular polyobj, you could actually put a line special on the side of the door, and make it work just like any other switch.  But I can't do that here, because the only line I've got is already occupied with `Polyobj_ExplicitLine`!

The recommended way to fix this is to give the line a _line id_ — like a sector tag or TID, but yet another namespace — and then use the `SetLineSpecial` function from a script to change the line's special right as the map starts.  `Polyobj_ExplicitLine`, just like `Sector_Set3dFloor`, is an "init" special that's only consulted during map loading and never looked at again.  But that requires scripting, which I haven't covered yet and which requires some setup that I don't want to cram into this section.

Instead I'm going to cheat, in keeping with this theme.  I have perfectly good lines on either side of this door, so I'm just going to have them trigger on "Player Cross", and give _those_ the special.  (I have to edit them a bit because "cross" specials only activate when something's _center_ crosses the line, so they'll never fire if there's not enough room between the line and the door.)  I do want `Polyobj_DoorSlide` this time, with a byte angle of `64` for north.  And, behold:

{% photo /media/2015-12/doom3/slade12-gate-cheating.png Cheating to make the gate work without scripting %}
{% photo /media/2015-12/doom3/zdoom16-polyobj-gate-open.png The gate, opening %}

----

You can do a lot with polyobjs, especially the two-sided variety.  Just keep in mind that they _only consist of lines_; they have no top or bottom.  This leaves us with one serious restriction: you cannot move a flat (a floor or ceiling) sideways.  Here are some things you _can_ do:

- Wolfenstein 3D's secret doors, which move back when you press them, are pretty easy to make.

- You can make some nice decorations, like an overhead fan made out of short textures that actually rotates.

- You can combine polyobjs with 3D floors to some good effect — for example, you could make a sliding door out of two-sided lines, then cover the hollow top with a 3D floor beam.

- There are swinging doors, too!

- If worst comes to worst, you can make a two-sided polyobj with a thick grid of lines, to sort of fake a "floor" on top.  This was a pretty common hack before 3D floors came around, and is still used with the vanilla engine.

One last note of caution: ZDoom will exit _immediately_ if your polyobjs are bogus, and SLADE doesn't currently show the error anywhere.  Oops.  On a Unix you can run either SLADE or ZDoom from a terminal and look at the stderr, but I don't know what you can do on Windows.  Sorry!  Make sure you have both a single anchor and a single start spot per polyobj.


## Slopes

Yes, even the flatness of Doom is no longer a given.

I'd like to take a moment to stress how much effort I put into making SLADE 3.1.1 preview slopes in 3D mode, which is just so good, you have no idea.  There's no dedicated slope editing yet, unfortunately, but that's partly because there are quite a few ways to create slopes in ZDoom.  Like...  ten, maybe?  It's not all bad, because it gives us a nice spectrum of tradeoffs between flexible and convenient.

### `Plane_Align`

This is the easiest, and also my favorite, and also the most limited.  It's an init special (under "Sector") you can slap on a line, and it slopes the floor or ceiling of one side to meet the floor or ceiling of the other side.  So if you just carve out the corner of a cave, say, you can stick `Plane_Align` on its edge and get an instant nice slope.

{% photo /media/2015-12/doom3/slade13-plane-align-before.png Before Plane_Align %}
{% photo /media/2015-12/doom3/slade14-plane-align-after.png After Plane_Align %}

It takes almost no effort and it's pretty easy to understand.  The slope makes sure the floors touch on either side of the line.  Got it.  (For the curious: yes, the point in the sector furthest from the line will be the point that stays the sector's "native" height.)  And once you have `Plane_Align` on a line, you can just mousewheel the floor or ceiling height of either side in 3D mode, and the slope will update live!  That is _super cool_.

Note that the floor texture stays fixed to the 2D grid, even if the sector is sloped in 3D.  A very steep slope will get you a very distorted texture.  You can compensate for this with scaling.

`Plane_Align` works great for very common cases, like rounded(ish) archways or ramps instead of stairs.  It can even help with certain kinds of three-dimensional curve, like...  the top of a volcano.  If I carve it into triangular pieces and apply some `Plane_Align`...

{% photo /media/2015-12/doom3/slade15-plane-align-volcano.png Volcano with a smooth sloped ceiling %}
{% photo /media/2015-12/doom3/slade16-plane-align-volcano2d.png Volcano slope geometry in 2D %}

This is, uh, kind of complicated to explain, and [the wiki already has some diagrams](http://zdoom.org/wiki/Using_slopes#Cliff_and_basin_with_Plane_Align).  The key is that the sloped part is made out of alternating triangles all the way around, with both sets of triangles sloping to meet the others.  Each inside line is thus shared between two triangles: one sloping up, and one sloping down.  Since both ends of each line will end up with the same height in both triangles, either because it's part of a `Plane_Align`ed line or because it's the corner that stays at its native height, there can't possibly be any seams.  Got it?  Hm.  I'm not even sure how to draw a diagram for this.  Maybe crack my map open and look at the sectors.

Anyway, that's about the extent of tricks you can do with `Plane_Align`.  For more chaotic geometry, you need something else.


### Sector tilt things

These aren't too hard to use, but expressing what you want is definitely more tricky than with `Plane_Align`.  Plop a "Floor Tilt Slope" or "Ceiling Tilt Slope" (Special Effects → Slopes) into a sector.  Its first argument is a "tilt" measured in degrees — `90` is no tilt, less is a downwards tilt, more is an upwards tilt.  The direction the thing faces determines the direction of the tilt.  The slope will pass through the thing.

{% photo /media/2015-12/doom3/slade17-sector-tilt.png Using a sector tilt thing to make a one-off slope %}

That's a floor tilt thing, pointing to the left, with a tilt of `85`.  Not much to it.  Useful for one-off rocks like this, but if you care about avoiding seams, this is probably way too fiddly to bother with.


### Vertex heights

If you want to make very complex geometry...  you can use vertex heights.  It's pretty tedious, but it's doable.  Let's make, I dunno, a real stalagtite.  The most important thing is that this only works for triangular sectors, so I have to draw my geometry as triangles.

{% photo /media/2015-12/doom3/slade18-vertex-heights1.png Geometry for a vertex height stalagtite %}

Yeah, like that.  Switch to vertex mode, select a vertex, and make sure "Show All" is checked in the prop panel.  You may notice that there are "Floor Height" and "Ceiling Height" properties.

You can probably guess where this is going.  Three points define a plane, so you can define any plane you want for any sector with only three points by giving them explicit floor or ceiling heights.  So for my stalagtite, I just give the outer vertices a ceiling height equal to the actual ceiling height, and the inner one a ceiling height somewhat lower than that:

{% photo /media/2015-12/doom3/slade19-vertex-heights2.png Vertex height stalagtite, default texture scaling %}
{% photo /media/2015-12/doom3/slade20-vertex-heights3.png Vertex height stalagtite, fixed texture scaling %}

That's before and after applying some texture scaling, to compensate for the dramatic slope.

You can do pretty much whatever you want with this.  Just draw a bunch of triangles and play with the vertex heights, and voilà!  Any terrain you want.  And if you want to stop the slope from applying to a neighboring sector, just give it an extra vertex somewhere.

There are two caveats.

1. If a triangular sector only has _one_ vertex with an explicit height (and it's just plain missing for the others), ZDoom will still slope the sector, but it'll use the sector's "native" height for the other vertices.  SLADE, unfortunately, treats all properties as though they have their default values, so it doesn't clearly distinguish between 0 (meaning "please put this vertex at absolute height 0") or a missing value (meaning "please put this vertex at the sector's height").  For now, the safest thing is to fill in all three vertex heights.

2. If you have very small triangles, even with subtle slopes, the player will seem to slide around on them.  It's arguably a ZDoom bug, and the cause is really obscure, but just don't try to get too fine-grained with floors you intend anyone to walk on.


### Other slope notes

The others are [listed on the ZDoom wiki](http://zdoom.org/wiki/Slope).  You can copy slopes from one sector to another using the `Plane_Copy` special or the sector copy things.  Vertex height things are unnecessary in UDMF.  Vavoom slope things are just wacky and I wouldn't use them.  Line slope things, I can see being handy, in some cases?  And there is also a way to express any arbitrary plane _directly_ in UDMF, but SLADE doesn't support that yet.

All of the slope mechanisms are applied at map load time, and _cannot be changed_ afterwards.  You _can_ move sloped sectors up and down, but the actual slope won't change — one side won't stay "stuck" to a `Plane_Align` line like it does in 3D mode.

In most cases, the "native" height of the sector is irrelevant once a slope has been applied.  I'd hazard a guess that there are some obvious exceptions; moving a floor/ceiling to the "nearest" or "lowest" neighbor probably consults the native height rather than the slope, for instance.

You can only slope 3D floors in GZDoom, and only if they're fully opaque.  The software renderer in ZDoom just can't handle it.  It's a miracle it can do all this, frankly.

Conversely, you can put 3D floors in a sloped _sector_ with no problems, but be careful not to ever let the surface of the 3D floor intersect the slope.  ZDoom will probably try to draw both, and the result will look ridiculous.  If you want something like a pond with a sloped bank, you'll just have to split the slope at the water level and copy it across.  If you then want to _drain_ the pond, well, that's too bad.

You can use `ExtraFloor_LightOnly` with slopes to make a diagonal line of light on a wall, even in ZDoom!  Keep in mind that the slope is extrapolated from the control sector to the real sector, so you probably want to "align" the control sector, depending on how you do it.  Also, I once made a diagonal light in a narrow hallway, and found the player would occasionally get stuck on it at the very end of the hall.  So don't do that, I guess.


## Other shenanigans

Those are the big three ways to defeat the usual Doom limitations.  ZDoom can do _a lot_ more, but I cannot possibly cover it all in one measly blog post.  I think it's important to know what's _possible_, though, so I'll breeze through the big stuff and try to at least mention everything I can think of.

### Scripting

Yes, you can write scripts, in a vaguely C-ish language called ACS.  This feature was actually inherited all the way from Hexen, which also brought us polyobjects.  It takes a little setup, which I wish SLADE didn't require, but oh well.

Download (or...  compile...) ACC, the ACS compiler, from [zdoom.org](http://zdoom.org/Download).  Extract the contents...  somewhere.  You should have an `acc` binary and four `z*.acs` files.

Pop open SLADE's preferences and drill down to Scripting → ACS.  Set "Location of acc executable" to, ahem, the location of the `acc` executable.  Add an include path, and make it the directory containing those `z*.acs` files.

Once you've done that, the rest is pretty easy.  In the map editor, choose View → Script Editor, and you're off to the races.  You usually want the first line to be

    :::c
    #include "zcommon.acs"

which defines the names of all the specials and various useful constants.

The most common use for scripts is to have a switch that does more than one thing.  That's pretty easy:

    :::c
    #include "zcommon.acs"

    script "do some stuff" (void) {
        Door_Open(4, 16, 0);
        Floor_LowerInstant(5, 0, 512);
    }

Click "compile" to compile, and "save" to save.  ZDoom itself doesn't actually understand ACS, only the compiled bytecode.  It's entirely possible to ship a map with a compiled script and no source code.

There are a couple parts here.  Scripts are all defined in a `script` block.  After that comes the name of the script.  Yes, it has to be in quotes; yes, that means you can use spaces.  Historically scripts have been numbered, but fuck that noise; ZDoom has like twenty types of numbers already and I'm cool with not keeping track of yet another.

After the name comes the arguments.  You can have up to three, which look like C: `(int a, int b, int c)`.  If you have zero, you _must_ include the `void`.  There are also several special types of scripts, which use a keyword instead of arguments; an "open script", for example, is indicated by having `OPEN` instead of the argument list, and will run automatically when the map starts.

Within a particular script, you can do bunches of stuff.  `if`, C-style `for`, `while`, and so on work as you might expect.  Arithmetic is a thing.  You can call line specials (aka "action specials") directly, as though they were functions.  There are also bunches of ACS-specific functions that let you examine and modify the game world in much greater detail than you can with specials — you can wait until a sector finishes moving, get the player's exact location and velocity, mess with the player's inventory, spawn objects, delete objects, change textures, play sounds, and all kinds of stuff.  If you really want to customize the difficulty of your map depending on the number of players, for example, you'll need a script.

You can declare variables like C, though there are no pointers and only a couple types.  You can put variables at file level, in which case they're visible to every script.  There are a couple scopes even broader than that, too.  You can also do arrays, even multidimensional ones.

A few ACS functions deal with fixed-point numbers (Doom doesn't use floats), which are indistinguishable from regular integers as far as the type system is concerned.  Kinda sucks.  Numbers that look like floats in scripts are actually fixed-point as well.  They're 16.16, and integers are 32-bit, so you just shift by 16 to convert from one to the other.

It might help to know how to _run_ a script.  There are several specials for executing scripts; you'll mostly use [`ACS_Execute`](http://zdoom.org/wiki/ACS_Execute).  Just slap it on a line like any other special.  Since action specials typically take numeric arguments, you should leave the first argument as `0` and put the name of your script in the "Arg 0 Str" field, which is in the prop grid rather than the "Args" tab at the moment.  Oops.

By default a script can only be running once at a time.  Scripts can wait in various ways, which is always non-blocking; there are also specials for pausing a script, killing a script, or executing it even if it's already running.  I don't think I've ever made use of this.

By the way, you can [give action specials to things](http://zdoom.org/wiki/Thing_executed_specials) as well.  Monsters and other destructibles execute their specials when they die, which is a good way to break your map under `-nomonsters`.  Pickups execute their specials when they're picked up.  There are a few special effect things that execute their specials at certain times.

It's a matter of taste how much scripting to use.  I like to preserve the _feel_ of Doom, which to me means the player should never stop and think "well that's obviously scripted".  Printing custom text to the screen or freezing the player to show them a cutscene, for example, are pretty big signs.  On the other hand, plenty of automated stuff _seemed_ to exist in Doom (usually approximated with walkover triggers), so you can get away with a lot.  I've made a multi-floor elevator that took a couple screenfuls of code to get right, but I think it still feels Doom-ish, because it does something conceptually simple and does it with no fuss.  I guess that's the difference: stuff should blend into the game naturally, not stick out like a sore thumb like the author is on my screen going "guess what I diiiiiid".

As you might imagine, there is [hecka tons of stuff about scripting on the ZDoom wiki](http://zdoom.org/wiki/ACS).


### Beyond mapping

So, a wad file can contain more than just maps.  `doom2.wad` is a wad file much like the ones you've been making, and it contains virtually the entirety of Doom II.  But actually managing a wad is a pain, because there are no directories!  If you want to add a texture or a sprite you have to put it between special `SS_START` and `SS_END` markers or some such nonsense, and I never remember how it all works.

Lucky for me, ZDoom can also load [regular old zip files](http://zdoom.org/wiki/Using_ZIPs_as_WAD_replacement), which are usually given a `.pk3` extension.  These are super easy to manage (since you don't even need special tools), and you just put resources in directories by their type.  Got a texture?  Stick it in `/textures/`.  Done.  You can even nest directories as deep as you want within there.

ZDoom can even load a _directory_, using the same structure as a pk3!  You can work on a map or a mod or whatever just on your filesystem like a reasonable project, and then zip it out and release it when you're done.  Amazing.

One, uh, curiosity: each map is still in its own wad file, inside the pk3.  So if you've been following along and building a map, you can turn it into a pk3 (or directory) by moving your wad to `/maps/map01.wad`.  And that's it.  If you have more than one map in your wad, uh...  I don't know if there's an easy way to convert that.  SLADE was originally a very good wad management thing, so maybe it can convert a wad to a pk3 for you?  Maybe?

You can _also_ just drop a wad (not another pk3!) into the root of a pk3/directory, and ZDoom will load it recursively.  Some developers rave that this is a bad idea because it defeats ZDoom's ability to avoid loading resources it doesn't need, but what do developers know anyway?  This is super handy if you find some textures or sounds or weapons or monsters — from, say, the [realm667 repository](http://realm667.com/index.php/en/repository-18489) — and want to use them without figuring out how to merge them with your own mod.

----

I mention all this as a segue into something much more interesting: ZDoom supports a bunch of different text files ("lumps") that will let you customize a zillion different aspects of the game.  Even ZDoom's own understanding of the games it supports is mostly configured in these same files.  So if it's different between Doom and Hexen, chances are, you can customize it for yourself pretty easily.  _For example._

* The poorly-named [`DECORATE`](http://zdoom.org/wiki/DECORATE) lump lets you create entirely new actors.  From scratch.  Or even not from scratch; you can inherit from existing actors as well.  It was originally created to let you make static decorations, as you may have guessed, but nowadays you can make pretty much anything.  New keys, new pickups, new powerups, new projectiles, new weapons, new monsters, all kinds of new special effects.  You can even create new player classes, to customize player properties like what equipment they start with or how high they can jump.

    Or you can stick to modifying the stock objects, like having the Arachnotron drop a plasma cell when it dies, or making the radiation suit also protect against baron slimeballs.  Or you can avoid touching it altogether, grab some monsters from realm667, and just drop them into your map.

    This is a preposterously deep and complex feature, but probably one of the best parts of ZDoom, especially for people who have the patience and creativity to make good use of it.

* [`MAPINFO`](http://zdoom.org/wiki/MAPINFO) manages the list of maps, essentially.  Most notably, you can give your maps their own names, instead of inheriting the Doom II map names.  You can also group them into episodes, configure new secret levels, connect several maps into a hub that the player can move through seamlessly, create a progression map like the original Doom had, or change the intermission text.  There are some nice defaults for mapping too, like the ability to make the entire map use smooth lighting (rather than fake contrast) or disable jumping.

    This is also where you can define new skill levels, change the sky texture, modify parts of the game UI like the title screen, and...  lots of other stuff.

* [`TERRAIN`](http://zdoom.org/wiki/TERRAIN) lets you define terrain splashes — sounds and visual effects to play when something falls onto a certain texture.

    More interestingly, it lets you define a custom damage amount or friction for a certain texture.  So you can use this to say that everywhere in any of your levels, `LAVA1` always does 20% damage.  Then you never have to set it yourself, and you don't have to worry about forgetting it or being inconsistent about it.  Dev builds of ZDoom have a couple patches from me that extend this to work with 3D floors as well, which is just super duper convenient.

* [`LOCKDEFS`](http://zdoom.org/wiki/LOCKDEFS) is how you create new lock numbers.  Probably not used very often, since realm667 already has a pack of like 8 new colors of keys, which includes its own `LOCKDEFS`.

* [`ANIMDEFS`](http://zdoom.org/wiki/ANIMDEFS) lets you create new animated textures or switch textures.  You can also apply a Quake-style warp effect to a texture, which will apply anywhere it's used.

* [`MENUDEF`](http://zdoom.org/wiki/MENUDEF) lets you add to the menu!  You could, say, add some new feature with ACS and let the player turn it on or off via the menu.

* [`SBARINFO`](http://zdoom.org/wiki/SBARINFO) allows for customizing the status bar, or even adding custom information to the full-screen HUD.

* [`DIALOGUE`](http://zdoom.org/wiki/DIALOGUE) (a little different since it's per-map) lets you define conversations, as inherited from Strife.

* And somehow, [there are still more](http://zdoom.org/wiki/Category:ZDoom_special_lumps)!

### Even more mapping features

- You can change the sky in particular sectors, or create entirely custom [skyboxes](http://zdoom.org/wiki/Skybox).

- You can [link sectors together](http://zdoom.org/wiki/Sector_SetLink) so that their floors and ceilings are locked in the same relative position, which is useful for multi-part lifts and similar contraptions.

- You can [attach a 3D midtex to the floor or ceiling of a sector](http://zdoom.org/wiki/Sector_Attach3dMidtex), and then move the midtex by moving the sector.  You can use this to create a gate that opens upwards like a standard door without polyobjs.  Or perhaps you could use it _with_ polyobjs...

- There are some "[sector action things](http://zdoom.org/wiki/Thing_executed_specials)", which execute their specials when something happens within a sector, like an actor entering or leaving.

    You can use the "Eyes Go Above Fake Ceiling" thing in tandem with `Transfer_Heights` to make a lift that appears to carry the player upwards into the middle of another room, without 3D floors, by using silent teleportation.

- There are quite a few sector types for scrolling the floor/ceiling, optionally also carrying whatever's sitting on the floor.  There are also several specials for [scrolling wall textures](http://zdoom.org/wiki/Category:Scrolling_specials) (though that was partially available in vanilla Doom as well).

- Several colors of [particle fountains](http://zdoom.org/wiki/Classes:ParticleFountain) emit...  a fountain of particles.  I like them, okay?

- [`Line_Horizon`](http://zdoom.org/wiki/Line_Horizon) will extend the floor and ceiling of the line out to infinity, meeting at the horizon and giving the illusion of being in a very large empty space.

- [`Line_Mirror`](http://zdoom.org/wiki/Line_Mirror) is a mirror!

- [`Sector_SetPortal`](http://zdoom.org/wiki/Sector_SetPortal) is tricky to use, but creates the illusion that one sector is stacked on top of another, allowing for some decorative geometry that would be very difficult otherwise.

- There are several ways to use [cameras](http://zdoom.org/wiki/Cameras), such as having an image of part of the level appear as a texture elsewhere, or moving the player view elsewhere for a cutscene.

- [Patrol points](http://zdoom.org/wiki/Classes:PatrolPoint), in combination with a couple other mechanisms, can make monsters follow a predetermined path around the map.

- Monsters can be made to [chase and attack specific things](http://zdoom.org/wiki/Thing_Hate).

- [Earthquakes](http://zdoom.org/wiki/Radius_Quake).

- You can change the [gravity](http://zdoom.org/wiki/Gravity) in various ways.

- You can [change the current skill level](http://zdoom.org/wiki/ChangeSkill), for example if you'd like to make a Quake-style skill selection map.

- GZDoom has various extensions that only work in OpenGL: dynamic lights and support for model-based actors are the obvious ones.

- I'm sure there's [more I'm forgetting](http://zdoom.org/wiki/Main_Page)!


## Go build something already

There is nothing more I can teach you.  (Unless you ask for help, I guess.)  Go, and build me a world.

No, really, build a world.  I've hit Hacker News twice already and all the comments have just been "ho ho, I remember mapping for Doom 20 years ago, which is why I won't bother trying it now."  Come on.  _Something_ I've mentioned above should give you a spark of inspiration, surely.  ZDoom is a pretty fancy game engine now, ripe with possibility — there's even a recently-created [GPL fork](https://github.com/marrub--/GLOOME/) intended for use with real commercial projects.

So do it.  Put something together.  Make creative use of all these little extensions.  Let people run around in your universe.  You don't even have to have monsters if you don't want to; just create a little contraption and appreciate it for its own sake.

I'll be over here, chugging away at this little map set, which I'll release...  someday.  Until then, enjoy [the final version of this tutorial map]({static}/media/2015-12/doom3/part3.wad), which is mostly the same except for these special effects.  And send me yours!  There's still a (sloowly) growing list at the bottom of [part 1]({filename}/2015-12-19-you-should-make-a-doom-level-part-1.markdown).
