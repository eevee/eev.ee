title: Coaxing 2D platforming out of Unity
date: 2017-10-13 12:28
category: blog
tags: tech, gamedev, unity

An anonymous donor asked a question that I can't even _begin_ to figure out how to answer, but they also said anything else is fine, so here's anything else.

I've been avoiding writing about game physics, since I want to save it for ✨ the book I'm writing ✨, but that book will almost certainly not touch on Unity.  Here, then, is a brief run through some of the brick walls I ran into while trying to convince Unity to do 2D platforming.

This is fairly high-level — there are no blocks of code or helpful diagrams.  I'm just getting this out of my head because it's interesting.  If you want more gritty details, I guess you'll have to wait for ✨ the book ✨.

<!-- more -->


## The setup

I hadn't used Unity before.  I hadn't even used a "real" physics engine before.  [My games](https://eevee.itch.io/) so far have mostly used [LÖVE](https://love2d.org/), a Lua-based engine.  LÖVE includes box2d bindings, but for various reasons (not all of them good), I opted to avoid them and instead write my own physics completely from scratch.  (How, you ask?  ✨ Book ✨!)

I was invited to work on a Unity project, Chaos Composer, that someone else had already started.  It had basic movement already implemented; I taught myself Unity's physics system by hacking on it.  It's entirely possible that none of this is actually the best way to do anything, since I was really trying to reproduce my own homegrown stuff in Unity, but it's the best I've managed to come up with.

Two recurring snags were that you can't ask Unity to do multiple physics updates in a row, and sometimes getting the information I wanted was difficult.  Working with my own code spoiled me a little, since I could invoke it at any time and ask it anything I wanted; Unity, on the other hand, is someone else's black box with a rigid interface on top.

Also, wow, Googling for a lot of this was not quite as helpful as expected.  A _lot_ of what's out there is just the first thing that works, and often that's pretty hacky and imposes severe limits on the game design (e.g., "this won't work with slopes").  Basic movement and collision are the _first_ thing you do, which seems to me like the _worst_ time to be locking yourself out of a lot of design options.  I tried very (very, very, very) hard to minimize those kinds of constraints.


## Problem 1: Movement

When I showed up, movement was already working.  Problem solved!

Like any good programmer, I immediately set out to un-solve it.  Given a "real" physics engine like Unity prominently features, you have two options: ⓐ treat the player as a physics object, or ⓑ don't.  The existing code went with option ⓑ, like I'd done myself with LÖVE, and like I'd seen countless people advise.  Using a physics sim makes for bad platforming.

But...  _why_?  I believed it, but I couldn't concretely defend it.  I had to know for myself.  So I started a blank project, drew some physics boxes, and wrote a dozen-line player controller.

Ah!  Immediate enlightenment.

If the player was sliding down a wall, and I tried to move them into the wall, they would simply freeze in midair until I let go of the movement key.  The trouble is that the physics sim works in terms of _forces_ — moving the player involves giving them a nudge in some direction, like a giant invisible hand pushing them around the level.  Surprise!  If you press a real object against a real wall with your real hand, you'll see the same effect — friction will cancel out gravity, and the object will stay in midair..

Platformer movement, as it turns out, doesn't make any goddamn physical sense.  What _is_ air control?  What are you pushing against?  Nothing, really; we just have it because it's nice to play with, because [not having it is a nightmare](https://en.wikipedia.org/wiki/Super_Ghouls_%27n_Ghosts).

I looked to see if there were any common solutions to this, and I only really found one: _make all your walls frictionless_.

Game development is full of hacks like this, and I...  don't like them.  I can accept that minor hacks are necessary sometimes, but this one makes an early and widespread change to a fundamental system to "fix" something that was wrong in the first place.  It also imposes an "invisible" requirement, something I try to avoid at all costs — if you _forget_ to make a particular wall frictionless, you'll never know unless you happen to try sliding down it.

And so, I swiftly returned to the existing code.  It wasn't too different from what I'd come up with for LÖVE: it applied gravity by hand, tracked the player's velocity, computed the intended movement each frame, and moved by that amount.  The interesting thing was that it used `MovePosition`, which _schedules_ a movement for the next physics update and stops the movement if the player hits something solid.

It's kind of a nice hybrid approach, actually; all the "physics" for conscious actors is done by hand, but the physics engine is still used for collision detection.  It's also used for collision _rejection_ — if the player manages to wedge themselves several pixels into a solid object, for example, the physics engine will try to gently nudge them back out of it with no extra effort required on my part.  I still haven't figured out how to get that to work with my homegrown stuff, which is built to _prevent_ overlap rather than to jiggle things out of it.


## But wait, what about...

Our player is a dynamic body with rotation lock and no gravity.  Why not just use a kinematic body?

I must be missing something, because I do not understand the point of kinematic bodies.  I ran into this with Godot, too, which documented them the same way: as intended for use as players and other manually-moved objects.  But by default, they don't even collide with other kinematic bodies _or static geometry_.  What?  There's a checkbox to turn this on, which I enabled, but then I found out that `MovePosition` doesn't stop kinematic bodies when they hit something, so I would've had to cast along the intended path of movement to figure out when to stop, thus duplicating the same work the physics engine was about to do.

But that's impossible anyway!  Static geometry generally wants to be made of edge colliders, right?  They don't care about concave/convex.  Imagine the player is standing on the ground _near_ a wall and tries to move towards the wall.  Both the ground and the wall are different edges from the same edge collider.

If you try to cast the player's hitbox horizontally, parallel to the ground, you'll only get one collision: the _existing_ collision with the ground.  Casting doesn't distinguish between touching and hitting.  And because Unity only reports one collision per collider, and because the ground will always show up _first_, you will never find out about the impending wall collision.

So you're _forced_ to either use raycasts for collision detection or decomposed polygons for world geometry, both of which are slightly worse tools for no real gain.

I ended up sticking with a dynamic body.

----

Oh, one other thing that doesn't really fit anywhere else: _keep track of units_!  If you're adding something called "velocity" directly to something called "position", something has gone very wrong.  Acceleration is distance per time squared; velocity is distance per time; position is distance.  You **must** multiply or divide by time to convert between them.

I never even, say, add a constant directly to position every frame; I always phrase it as velocity and multiply by _Δt_.  It keeps the units consistent: time is always in seconds, not in tics.


## Problem 2: Slopes

Ah, now we start to get off in the weeds.

A sort of pre-problem here was detecting whether we're _on_ a slope, which means detecting the ground.  The codebase originally used a manual physics query of the area around the player's feet to check for the ground, which seems to be somewhat common, but that can't tell me the _angle_ of the detected ground.  (It's also kind of error-prone, since "around the player's feet" has to be specified by hand and may not stay correct through animations or changes in the hitbox.)

I replaced that with what I'd eventually settled on in LÖVE: detect the ground by detecting collisions, and looking at the _normal_ of the collision.  A normal is a vector that points straight out from a surface, so if you're standing on the ground, the normal points straight up; if you're on a 10° incline, the normal points 10° away from straight up.

Not all collisions are with the ground, of course, so I assumed something is ground if the normal pointed _away from gravity_.  (I like this definition more than "points upwards", because it avoids assuming anything about the direction of gravity, which leaves some interesting doors open for later on.)  That's easily detected by taking the dot product — if it's negative, the collision was with the ground, _and_ I now have the normal of the ground.

Actually doing this in practice was slightly tricky.  With my LÖVE engine, I could cram this right into the middle of collision resolution.  With Unity, not quite so much.  I went through a couple iterations before I really grasped Unity's [execution order](https://docs.unity3d.com/Manual/ExecutionOrder.html), which I guess I will have to briefly recap for this to make sense.

Unity essentially has two update cycles.  It performs physics updates at _fixed intervals_ for consistency, and updates _everything else_ just before rendering.  Within a single frame, Unity does as many fixed physics updates as it has spare time for (which might be zero, one, or more), then does a regular update, then renders.  User code can implement _either or both_ of `Update`, which runs during a regular update, and `FixedUpdate`, which runs just before Unity does a physics pass.

So my solution was:

- At the very end of `FixedUpdate`, clear the actor's "on ground" flag and ground normal.

- During `OnCollisionEnter2D` and `OnCollisionStay2D` (which are called from within a physics pass), if there's a collision that looks like it's with the ground, set the "on ground" flag and ground normal.  (If there are multiple ground collisions, well, good luck figuring out the best way to resolve that!  At the moment I'm just taking the first and hoping for the best.)

That means there's a brief window between the end of `FixedUpdate` and Unity's physics pass during which a grounded actor might mistakenly believe it's _not_ on the ground, which is a bit of a shame, but there are very few good reasons for anything to be happening in that window.

Okay!  Now we can do slopes.

Just kidding!  First we have to do sliding.

When I first looked at this code, it didn't apply gravity while the player was on the ground.  I think I may have had some problems with detecting the ground as result, since the player was no longer _pushing_ down against it?  Either way, it seemed like a silly special case, so I made gravity always apply.

Lo!  I was a fool.  The player could no longer move.

Why?  Because `MovePosition` does exactly what it promises.  If the player collides with something, they'll stop moving.  Applying gravity means that the player is trying to move _diagonally downwards_ into the ground, and so `MovePosition` stops them _immediately_.

Hence, sliding.  I don't want the player to actually try to move into the ground.  I want them to move the _unblocked_ part of that movement.  For flat ground, that means the horizontal part, which is pretty much the same as discarding gravity.  For sloped ground, it's a bit more complicated!

Okay but actually it's less complicated than you'd think.  It can be done with some cross products fairly easily, but Unity makes it _even easier_ with a couple casts.  There's a `Vector3.ProjectOnPlane` function that projects an arbitrary vector on a plane given by its normal — exactly the thing I want!  So I apply that to the attempted movement before passing it along to `MovePosition`.  I do the same thing with the current velocity, to prevent the player from accelerating infinitely downwards while standing on flat ground.

One other thing: I don't actually use the detected ground normal for this.  The player might be touching two ground surfaces at the same time, and I'd want to project on both of them.  Instead, I use the player body's `GetContacts` method, which returns contact points (and normals!) for _everything_ the player is currently touching.  I believe those contact points are tracked by the physics engine anyway, so asking for them doesn't require any actual physics work.

(Looking at the code I have, I notice that I _still_ only perform the slide for surfaces facing upwards — but I'd want to slide against sloped ceilings, too.  Why did I do this?  Maybe I should remove that.)

(Also, I'm pretty sure projecting a vector on a plane is non-commutative, which raises the question of which _order_ the projections should happen in and what difference it makes.  I don't have a good answer.)

(I note that my LÖVE setup does something slightly different: it just tries whatever the movement ought to be, and if there's a collision, _then_ it projects — and tries again with the remaining movement.  But I can't ask Unity to do multiple moves in one physics update, alas.)

Okay!  _Now_, slopes.  But actually, with the above work done, slopes are most of the way there already.

One obvious problem is that the player tries to move _horizontally_ even when on a slope, and the easy fix is to change their movement from `speed * Vector2.right` to `speed * new Vector2(ground.y, -ground.x)` while on the ground.  That's the ground normal rotated a quarter-turn clockwise, so for flat ground it still points to the right, and in general it points rightwards along the ground.  (Note that it assumes the ground normal is a unit vector, but as far as I'm aware, that's true for all the normals Unity gives you.)

Another issue is that if the player stands motionless on a slope, gravity will cause them to slowly slide down it — because the movement from gravity will be projected onto the slope, and unlike flat ground, the result is no longer zero.  For _conscious actors only_, I counter this by adding the opposite factor to the player's velocity as part of adding in their walking speed.  This matches how the real world works, to some extent: when you're standing on a hill, you're exerting some small amount of effort just to stay in place.

(Note that slope resistance is _not_ the same as friction.  Okay, yes, in the real world, virtually all resistance to movement happens as a result of friction, but _bracing_ yourself against the ground isn't the same as being passively resisted.)

From here there are _a lot_ of things you can do, depending on how you think slopes should be handled.  You could make the player unable to walk up slopes that are too steep.  You could make walking down a slope faster than walking up it.  You could make jumping go along the ground normal, rather than straight up.  You could raise the player's max allowed speed while running downhill.  Whatever you want, really.  Armed with a normal and awareness of dot products, you can do whatever you want.

But first you might want to fix a few aggravating side effects.


## Problem 3: Ground adherence

I don't know if there's a better name for this.  I rarely even see anyone talk about it, which surprises me; it seems like it should be a very common problem.

The problem _is_: if the player runs up a slope which then abruptly changes to flat ground, their momentum will carry them into the air.  For very fast players going off the top of very steep slopes, this makes sense, but it becomes visible even for relatively gentle slopes.  It was a mild nightmare in the original release of our game [Lunar Depot 38](https://eevee.itch.io/lunar-depot-38), which has very "rough" ground made up of lots of shallow slopes — so the player is very frequently _slightly_ off the ground, which meant they couldn't jump, for seemingly no reason.  (I even had code to fix this, but I disabled it because of a silly visual side effect that I never got around to fixing.)

Anyway!  The _reason_ this is a problem is that game protagonists are generally not boxes sliding around — they have _legs_.  We don't go flying off the top of real-world hilltops because we put our foot down until it touches the ground.

Simulating this footfall is surprisingly fiddly to get right, especially with someone else's physics engine.  It's made somewhat easier by `Cast`, which casts the _entire hitbox_ — no matter what shape it is — in a particular direction, _as if_ it had moved, and tells you all the hypothetical collisions in order.

So I cast the player in the direction of gravity by some distance.  If the cast hits something solid with a ground-like collision normal, then the player must be close to the ground, and I move them down to touch it (and set that ground as the new ground normal).

There are some wrinkles.

Wrinkle 1: I only want to do this if the player is _off_ the ground now, but was _on_ the ground last frame, **and** is not _deliberately_ moving upwards.  That latter condition means I want to skip this logic if the player jumps, for example, but also if the player is thrust upwards by a spring or abducted by a UFO or whatever.  As long as external code goes through some interface and doesn't mess with the player's velocity directly, that shouldn't be too hard to track.

Wrinkle 2: When does this logic run?  It needs to happen _after_ the player moves, which means _after_ a Unity physics pass...  but there's no callback for that point in time.  I ended up running it at the beginning of `FixedUpdate` _and_ the beginning of `Update` — since I definitely want to do it before rendering happens!  That means it'll sometimes happen twice between physics updates.  (I could carefully juggle a flag to skip the second run, but I...  didn't do that.  Yet?)

Wrinkle 3: I can't move the player with `MovePosition`!  Remember, `MovePosition` _schedules_ a movement, it doesn't actually perform one; that means if it's called twice before the physics pass, the first call is effectively ignored.  I can't easily combine the drop with the player's regular movement, for various fiddly reasons.  I ended up doing it "by hand" using `transform.Translate`, which I think was the "old way" to do manual movement before `MovePosition` existed.  I'm not totally sure if it activates triggers?  For that matter, I'm not sure it even notices collisions — but since I did a full-body `Cast`, there shouldn't be any anyway.

Wrinkle 4: What, exactly, is "some distance"?  I've yet to find a satisfying answer for this.  It seems like it ought to be based on the player's current speed and the slope of the ground they're moving along, but every time I've done that math, I've gotten totally ludicrous answers that sometimes exceed the size of a tile.  But maybe that's not wrong?  Play around, I guess, and think about when the effect should "break" and the player should go flying off the top of a hill.

Wrinkle 5: It's _possible_ that the player will launch off a slope, hit something, and then be adhered to the ground where they wouldn't have hit it.  I don't much like this edge case, but I don't see a way around it either.

This problem is surprisingly awkward for how simple it sounds, and the solution isn't entirely satisfying.  Oh, well; the results are much nicer than the solution.  As an added bonus, this also fixes occasional problems with running _down_ a hill and becoming detached from the ground due to precision issues or whathaveyou.


## Problem 4: One-way platforms

Ah, what a nightmare.

It took me ages just to figure out how to _define_ one-way platforms.  Only block when the player is moving downwards?  Nope.  Only block when the player is above the platform?  Nuh-uh.

Well, okay, yes, those approaches might work for convex players and flat platforms.  But what about...  _sloped, one-way platforms_?  There's no reason you shouldn't be able to have those.  If Super Mario World can do it, surely Unity can do it almost 30 years later.

The trick is, again, to look at the collision normal.  If it faces away from gravity, the player is hitting a ground-like surface, so the platform should block them.  Otherwise (or if the player _overlaps_ the platform), it shouldn't.

Here's the catch: Unity doesn't have conditional collision.  I can't decide, _on the fly_, whether a collision should block or not.  In fact, I _think_ that by the time I get a callback like `OnCollisionEnter2D`, the physics pass is already _over_.

I could go the other way and use triggers (which are non-blocking), but then I have the opposite problem: I can't _stop_ the player on the fly.  I could move them back to where they hit the trigger, but I envision all kinds of problems as a result.  What if they were moving fast enough to activate something on the other side of the platform?  What if something else moved to where I'm trying to shove them back to in the meantime?  How does this interact with ground detection and listing contacts, which would rightly ignore a trigger as non-blocking?

I beat my head against this for a while, but the inability to respond to collision conditionally was a huge roadblock.  It's all the more infuriating a problem, because Unity _ships with_ a one-way platform modifier thing.  Unfortunately, it seems to have been implemented by someone who has never played a platformer.  It's _literally one-way_ — the player is only allowed to move straight upwards through it, not in from the sides.  It also tries to block the player if they're moving downwards while inside the platform, which invokes clumsy rejection behavior.  And this all seems to be built into the physics engine itself somehow, so I can't simply copy whatever they did.

Eventually, I settled on the following.  After calculating attempted movement (including sliding), just at the end of `FixedUpdate`, I do a `Cast` along the movement vector.  I'm not thrilled about having to duplicate the physics engine's own work, but I do filter to only things on a "one-way platform" physics layer, which should at least _help_.  For each object the cast hits, I use `Physics2D.IgnoreCollision` to either ignore or un-ignore the collision between the player and the platform, depending on whether the collision was ground-like or not.

(A lot of people suggested turning off collision between _layers_, but that can't possibly work — the player might be standing on one platform while inside another, and anyway, this should work for _all_ actors!)

Again, wrinkles!  But fewer this time.  Actually, maybe just one: handling the case where the player already _overlaps_ the platform.  I can't just check for that with e.g. `OverlapCollider`, because that doesn't distinguish between overlapping and merely _touching_.

I came up with a fairly simple fix: if I was _going_ to un-ignore the collision (i.e. make the platform block), and the cast distance is reported as zero (either already touching _or_ overlapping), I simply do nothing instead.  If I'm standing on the platform, I must have already set it blocking when I was approaching it from the top anyway; if I'm overlapping it, I must have already set it non-blocking to get here in the first place.

I can imagine a few cases where this might go wrong.  Moving platforms, especially, are going to cause some interesting issues.  But this is the best I can do with what I know, and it seems to work well enough so far.

Oh, and our player can deliberately drop down through platforms, which was easy enough to implement; I just decide the platform is always passable while some button is held down.


## Problem 5: Pushers and carriers

I haven't gotten to this yet!  Oh boy, can't wait.  I implemented it in LÖVE, but my way was hilariously invasive; I'm hoping that having a physics engine that supports a handwaved "this pushes that" will help.  Of course, you also have to worry about sticking to platforms, for which the recommended solution is apparently to _parent_ the cargo to the platform, which sounds goofy to me?  I guess I'll find out when I throw myself at it later.


## Overall result

I ended up with a fairly pleasant-feeling system that supports slopes and one-way platforms and whatnot, with all the same pieces as I came up with for LÖVE.  The code somehow ended up as _less_ of a mess, too, but it probably helps that I've been down this rabbit hole once before and kinda knew what I was aiming for this time.

<div class="prose-illustration-full">
<img src="{static}/media/2017-10-13-unity-platforming/ccboneride.gif" alt="Animation of a character running smoothly along the top of an irregular dinosaur skeleton">
</div>

Sorry that I don't have a big block of code for you to copy-paste into your project.  I don't think there are nearly enough narrative discussions of these fundamentals, though, so hopefully this is useful to someone.  If not, well, look forward to ✨ my book, that I am writing ✨!
