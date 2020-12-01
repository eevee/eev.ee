title: Conundrum
date: 2018-03-20 12:31
category: blog
tags: tech, doom

Here's a problem I'm having.  Or, rather, a problem I'm _solving_, but so slowly that I wonder if I'm going about it very inefficiently.

I intended to just make a huge image out of this and tweet it, but it takes so much text to explain that I might as well put it on my internet website.

<!-- more -->

## The setup

I want to do pathfinding through a Doom map.  The ultimate goal is to be able to automatically determine the path the player needs to take to reach the exit — what switches to hit in what order, what keys to get, etc.

Doom maps are 2D planes cut into arbitrary shapes.  Everything outside a shape is ｔｈｅ　ｖｏｉｄ, which we don't care about.  Here are some shapes.

<div class="prose-full-illustration">
<object type="image/svg+xml" data="{static}/media/2018-03-20-conundrum/map-01-original.svg"></object>
</div>

The shapes are defined implicitly by their edges.  All of the edges touching the red area, for example, say that they're red on one side.

That's very nice, because it means I don't have to do any geometry to detect which areas touch each other.  I can tell at a glance that the red and blue areas touch, because the line between them _says_ it's red on one side and blue on the other.

Unfortunately, this doesn't seem to be all that useful.  The player can't necessarily move from the red area to the blue area, because there's a skinny bottleneck.  If the yellow area were a raised platform, the player couldn't fit through the gap.  Worse, if there's a switch somewhere that lowers that platform, then the gap is _conditionally_ passable.

I thought this would be uncommon enough that I could get started only looking at neighbors and do actual geometry later, but that "conditionally passable" pattern shows up _all the time_ in the form of locked "bars" that let you peek between or around them.  So I might as well just do the dang geometry.

----

The player is a 32×32 square and always axis-aligned (i.e., the hitbox doesn't actually rotate).  That's very convenient, because it means I can "_dilate the world_" — expand all the walls by 16 units in both directions, while shrinking the player to a single point.  That expansion eliminates narrow gaps and leaves a map of everywhere the player's _center_ is allowed to be.  Allegedly this is how Quake did collision detection — but in 3D!  How hard can it be in 2D?

The plan, then, is to do this:

<div class="prose-full-illustration">
<object type="image/svg+xml" data="{static}/media/2018-03-20-conundrum/map-02-dilated.svg"></object>
</div>

This creates a bit of an unholy mess.  (I could avoid some of the overlap by being clever at points where exactly two lines touch, but I have to deal with a ton of overlap anyway so I'm not sure if that buys anything.)

The gray outlines are dilations of _inner_ walls, where both sides touch a shape.  The black outlines are dilations of _outer_ walls, touching ｔｈｅ　ｖｏｉｄ on one side.  This map tells me that the player's _center_ can never go within 16 units of an outer wall, which checks out — their hitbox would get in the way!  So I can delete all that stuff completely.

<div class="prose-full-illustration">
<object type="image/svg+xml" data="{static}/media/2018-03-20-conundrum/map-03-trimmed.svg"></object>
</div>

Consider that bottom-left outline, where red and yellow touch horizontally.  If the player is in the red area, they can _only_ enter that outlined part if they're _also_ allowed to be in the yellow area.  Once they're inside it, though, they can move around freely.  I'll color that piece orange, and similarly blend colors for the other outlines.  (A small sliver at the top requires access to all three areas, so I colored it gray, because I can't be bothered to figure out how to do a stripe pattern in Inkscape.)

<div class="prose-full-illustration">
<object type="image/svg+xml" data="{static}/media/2018-03-20-conundrum/map-04-final.svg"></object>
</div>

This is the final map, and it's easy to traverse because it works like a graph!  Each contiguous region is a node, and each border is an edge.  Some of the edges are one-way (falling off a ledge) or conditional (walking through a door), but the player can move freely within a region, so I don't need to care about world geometry any more.


## The problem

I'm having a hell of a time doing this mass-intersection of a big pile of shapes.

I'm writing this in Rust, and I would very very _very_ strongly prefer **not** to wrap a C library (or, god forbid, a C++ library), because that will considerably complicate actually releasing this dang software.  Unfortunately, that also limits my options rather a lot.

I was referred to a paper (A simple algorithm for Boolean operations on polygons, Martínez et al, 2013) that describes doing a Boolean operation (union, intersection, difference, xor) on _two_ shapes, and works even with self-intersections and holes and whatnot.

I spent an inordinate amount of time porting its reference implementation from very bad C++ to moderately bad Rust, and I extended it to work with an arbitrary number of polygons and to spit out all resulting shapes.  It has been a _very_ bumpy ride, and I keep hitting walls — the latest is that it panics when intersecting everything results in two distinct but exactly coincident edges, which obviously happens a lot with this approach.

So the question is: **is there some better way to do this that I'm overlooking**, or should I just keep fiddling with this algorithm and hope I come out the other side with something that works?

----

Bear in mind, the input shapes _are not necessarily convex_, and quite frequently aren't.  Also, they can have holes, and quite frequently do.  That rules out most common algorithms.  It's probably possible to triangulate everything, but I'm a little wary of cutting the map into even more microscopic shards; feel free to convince me otherwise.

Also, the map format _technically_ allows absolutely any arbitrary combination of lines, so all of these are possible:

<div class="prose-full-illustration">
<object type="image/svg+xml" data="{static}/media/2018-03-20-conundrum/map-edge-cases.svg"></object>
</div>

It would be nice to handle these gracefully somehow, or at least not crash on them.  But they're usually total nonsense as far as the game is concerned.  But also that middle one _does_ show up in the original stock maps a couple times.

Another common trick is that lines might be part of the same shape on _both sides_:

<div class="prose-full-illustration">
<object type="image/svg+xml" data="{static}/media/2018-03-20-conundrum/map-self-references.svg"></object>
</div>

The left example suggests that such a line is redundant and can simply be ignored without changing anything.  The right example shows why this is a problem.

A common trick in vanilla Doom is the so-called _self-referencing sector_.  Here, the edges of the inner yellow square all claim to be yellow — _on both sides_.  The outer edges all claim to be blue only on the inside, as normal.  The yellow square therefore doesn't neighbor the blue square at all, because no edges that are yellow on one side and blue on the other.  The effect in-game is that the yellow area is invisible, but still solid, so it can be used as an invisible bridge or invisible pit for various effects.

This does raise the question of exactly how Doom itself handles all these edge cases.  Vanilla maps are preprocessed by a [node builder](https://doomwiki.org/wiki/Node_builder) and split into [subsectors](https://doomwiki.org/wiki/Subsector), which are all convex polygons.  So for any given weird trick or broken geometry, the answer to "how does this behave" is: however the node builder deals with it.

Subsectors are built right into vanilla maps, so I _could_ use those.  The drawback is that they're optional for maps targeting ZDoom (and maybe other ports as well?), because ZDoom has its own internal node builder.  Also, relying on built nodes in general would make this code less useful for map _editing_, or generating, or whatever.

ZDoom's node builder is open source, so I could bake it in?  Or port _it_ to Rust?  (It's only, ah, ten times bigger than the shape algorithm I ported.)  It'd be interesting to have a fairly-correct reflection of how the game sees broken geometry, which is something no map editor really tries to do.  Is it fast enough?  Running it on the largest map I know to exist (MAP14 of Sunder) takes 1.4 seconds, which seems like a long time, but also that's from scratch, and maybe it could be adapted to work incrementally...?  Christ.

I'm not sure I have the time to dedicate to flesh this out beyond a proof of concept anyway, so maybe this is all moot.  But all the more reason to avoid spending a lot of time on dead ends.
