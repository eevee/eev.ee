title: Embedding Lua in ZDoom
date: 2016-11-26 17:16
category: blog
tags: tech, doom, gamedev, lua


I've spent a little time trying to embed a Lua interpreter in ZDoom.  I didn't get too far yet; it's just an experimental thing I poke at every once and a while.  The existing pile of constraints makes it an interesting problem, though.

<!-- more -->


## Background

ZDoom is a "source port" (read: fork) of the Doom engine, with all the changes from the commercial forks merged in (mostly Heretic, Hexen, Strife), and a lot of internal twiddles exposed.  It has a variety of mechanisms for customizing game behavior; two are major standouts.

One is ACS, a vaguely C-ish language inherited from Hexen.  It's mostly used to automate level behavior — at the simplest, by having a single switch perform multiple actions.  It supports the usual loops and conditionals, it can store data persistently, and ZDoom exposes a number of functions to it for inspecting and altering the state of the world, so it can do some neat tricks.  Here's an arbitrary script from [my DUMP2 map]({filename}/release/2016-03-31-i-made-a-doom-level.markdown).

```c
script "open_church_door" (int tag)
{
    // Open the door more quickly on easier skill levels, so running from the
    // arch-vile is a more viable option
    int skill = GameSkill();
    int speed;
    if (skill < SKILL_NORMAL)
        speed = 64;  // blazing door speed
    else if (skill == SKILL_NORMAL)
        speed = 16;  // normal door speed
    else
        speed = 8;  // very dramatic door speed

    Door_Raise(tag, speed, 68);  // double usual delay
}
```

However, ZDoom doesn't actually understand the language itself; ACS is compiled to bytecode.  There's even at least one [alternative language](https://forum.zdoom.org/viewtopic.php?f=19&t=32078) that compiles to the same bytecode, which is interesting.

The other big feature is `DECORATE`, a mostly-declarative mostly-interpreted language for defining new kinds of objects.  It's a fairly direct reflection of how Doom actors are implemented, which is in terms of states.  In Doom and the other commercial games, actor behavior was built into the engine, but this language has allowed almost all actors to be extracted as text files instead.  For example, [the imp is implemented](http://zdoom.org/wiki/Classes:DoomImp) partly as follows:

```text
  States
  {
  Spawn:
    TROO AB 10 A_Look
    Loop
  See:
    TROO AABBCCDD 3 A_Chase
    Loop
  Melee:
  Missile:
    TROO EF 8 A_FaceTarget
    TROO G 6 A_TroopAttack
    Goto See
  ...
  }
```

`TROO` is the name of the imp's sprite "family".  `A`, `B`, and so on are individual frames.  The numbers are durations in tics (35 per second).  All of the `A_*` things (which are optional) are _action functions_, behavioral functions (built into the engine) that run when the actor switches to that frame.  An actor starts out at its `Spawn` state, so an imp behaves as follows:

- Spawn.  Render as `TROO` frame `A`.  (By default, action functions don't run on the very first frame they're spawned.)
- Wait 10 tics.
- Change to `TROO` frame `B`.  Run `A_Look`, which checks to see if a player is within line of sight, and if so jumps to the `See` state.
- Wait 10 tics.
- Repeat.  (This time, frame `A` will also run `A_Look`, since the imp was no longer just spawned.)

All monster and item behavior is one big state table.  Even the player's own weapons work this way, which becomes very confusing — at some points a weapon can be running two states _simultaneously_.  Oh, and there's `A_CustomMissile` for monster attacks but `A_FireCustomMissile` for weapon attacks, and the arguments are different, and if you mix them up you'll get extremely confusing _parse_ errors.

It's a little bit of a mess.  It's fairly flexible for what it is, and has come a long way — for example, even original Doom couldn't pass arguments to action functions (since they were just function pointers), so it had separate functions like `A_TroopAttack` for every monster; now that same function can be [written generically](http://zdoom.org/wiki/A_TroopAttack).  People have done some very clever things with zero-delay frames (to run multiple action functions in a row) and storing state with dummy inventory items, too.  Still, it's not quite a programming language, and it's easy to run into walls and bizarre quirks.

When `DECORATE` lets you down, you have one interesting recourse: to call an ACS script!

Unfortunately, ACS also has some old limitations.  The only type it truly understands is `int`, so you can't manipulate an actor directly or even store one in a variable.  Instead, you have to work with TIDs ("thing IDs").  Every actor has a TID (zero is special-cased to mean "no TID"), and most ACS actor-related functions are expressed in terms of TIDs.  For _level automation_, this is fine, and probably even what you want — you can dump a group of monsters in a map, give them all a TID, and then control them as a group fairly easily.

But if you want to use ACS to enhance `DECORATE`, you have a bit of a problem.  `DECORATE` defines _individual_ actor behavior.  Also, many `DECORATE` actors are designed independently of a map and intended to be reusable anywhere.  `DECORATE` should thus not touch TIDs at all, because they're really the _map_'s concern, and mucking with TIDs might break map behavior...  but ACS can't refer to actors any other way.  A number of action functions can, but you can't call action functions from ACS, only `DECORATE`.  The workarounds for this are not pretty, especially for beginners, and they're very easy to silently get wrong.

Also, ultimately, some parts of the engine are just not accessible to _either_ ACS or `DECORATE`, and neither language is particularly amenable to having them exposed.  Adding more native types to ACS is rather difficult without making significant changes to both the language and bytecode, and `DECORATE` is barely a language at all.

Some long-awaited work is finally being done on a "ZScript", which purports to solve all of these problems by expanding `DECORATE` into an entire interpreted-C++-ish scripting language with access to tons of internals.  I don't know what I think of it, and it only seems to half-solve the problem, since it doesn't replace ACS.


## Trying out Lua

Lua is supposed to be easy to embed, right?  That's the one thing it's famous for.  Before ZScript actually started to materialize, I thought I'd take a little crack at embedding a Lua interpreter and exposing some API stuff to it.

It's not very far along yet, but it can do one thing that's always been completely impossible in both ACS and `DECORATE`: print out the player's entire inventory.  You can check how many of a _given_ item the player has in either language, but neither has a way to iterate over a collection.  In Lua, it's pretty easy.

```lua
function lua_test_script(activator, ...)
    for item, amount in pairs(activator.inventory) do
        -- This is Lua's builtin print(), so it goes to stdout
        print(item.class.name, amount)
    end
end
```

I made a tiny test map with a switch that tries to run the ACS script named `lua_test_script`.  I hacked the name lookup to first look for the name in Lua's global scope; if the function exists, it's called immediately, and ACS isn't consulted at all.  The code above is just a regular (global) function in a regular Lua file, embedded as a lump in the map.  So that was a good start, and was pretty neat to see work.


## Writing the bindings

I used the bare Lua API at first.  While its API is definitely very simple, actually using it to define and expose a large API in practice is kind of repetitive and error-prone, and I was never confident I was doing it quite right.  It's plain C _and_ it works entirely through stack manipulation _and_ it relies on a lot of casting to/from `void*`, so virtually anything might go wrong at any time.

I was on the cusp of writing a bunch of gross macros to automate the boring parts, and then I found [sol2](https://github.com/ThePhD/sol2), which is _pretty great_.  It makes heavy use of basically every single C++11 feature, so it's a nightmare when it breaks (and I've had to track down a few bugs), but it's expressive as hell when it works:

```cpp
lua.new_usertype<AActor>("zdoom.AActor",
    "__tostring", [](AActor& actor) { return "<actor>"; },
    // Pointer to an unbound method.  Sol automatically makes this an attribute
    // rather than a method because it takes no arguments, then wraps its
    // return value to pass it back to Lua, no manual wrapper code required.
    "class", &AActor::GetClass,
    "inventory", sol::property([](AActor& actor) -> ZLuaInventory { return ZLuaInventory(actor); }),
    // Pointers to unbound attributes.  Sol turns these into writable
    // attributes on the Lua side.
    "health", &AActor::health,
    "floorclip", &AActor::Floorclip,
    "weave_index_xy", &AActor::WeaveIndexXY,
    "weave_index_z", &AActor::WeaveIndexZ);
```

This is the type of the `activator` argument from the script above.  It works via template shenanigans, so most of the work is done at compile time.  `AActor` has a _lot_ of properties of various types; wrapping them with the bare Lua API would've been awful, but wrapping them with Sol is fairly straightforward.


## Lifetime

`activator.inventory` is a wrapper around a `ZLuaInventory` object, which I made up.  It's just a tiny proxy struct that tries to represent the inventory of a particular actor, because the engine itself doesn't quite have such a concept — an actor's "inventory" is a single item (itself an actor), and each item has a pointer to the next item in the inventory.  Creating an intermediate type lets me hide that detail from Lua and pretend the inventory is a real container.

The inventory is thus not a real table; `pairs()` works on it because it provides the `__pairs` metamethod.  It calls an `iter` method returning a closure, per Lua's [iteration]({filename}/2016-11-18-iteration-in-one-language-then-all-the-others.markdown) API, which Sol makes _just work_:

```cpp
struct ZLuaInventory {
    ...
    std::function<AInventory* ()> iter()
    {
        TObjPtr<AInventory> item = this->actor->Inventory;
        return [item]() mutable {
            AInventory* ret = item;
            if (ret)
                item = ret->NextInv();
            return ret;
        };
    }
}
```

C++'s closures are slightly goofy and it took me a few tries to land on this, but it works.

Well, sort of.

I don't know how I got this idea in my head, but I was pretty sure that ZDoom's `TObjPtr` did reference counting and would automatically handle the lifetime problems in the above code.  Eventually Lua reaps the closure, then C++ reaps the closure, then the wrapped `AInventory`'s refcount drops, and all is well.

Turns out `TObjPtr` _doesn't_ do reference counting.  Rather, all the game objects participate in tracing garbage collection.  The basic idea is to start from some root object and recursively traverse all the objects reachable from that root; whatever isn't reached is garbage and can be deleted.

Unfortunately, the Lua interpreter is not reachable from ZDoom's own object tree.  If an object ends up only being held by Lua, ZDoom will think it's garbage and delete it prematurely, leaving a dangling reference.  Those are bad.

I _think_ I can fix without too much trouble.  Sol allows customizing how it injects particular types, so I can use that for the type tree that participates in this GC scheme and keep an `unordered_set` of all objects that are alive in Lua.  The Lua interpreter itself is already wrapped in an object that participates in the GC, so when the GC descends to the wrapper, it's easy to tell it that that set of objects is alive.  I'll probably need to figure out read/write barriers, too, but I haven't looked too closely at how ZDoom uses those yet.  I don't know whether it's possible for an object to be "dead" (as in no longer usable, not just 0 health) before being reaped, but if so, I'll need to figure out something there too.

It's a little ironic that I have to do this weird workaround when ZDoom's tracing garbage collector is based on...  Lua's.

ZDoom does have types I want to expose that _aren't_ garbage collected, but those are all map structures like sectors, which are never created or destroyed at runtime.  I _will_ have to be careful with the Lua interpreter itself to make sure those can't live beyond the current map, but I haven't really dealt with map changes at all yet.  The ACS approach is that everything is map-local, and there's some limited storage for preserving values across maps; I could do something similar, perhaps only allowing primitive scalars.


## Asynchronicity

Another _critical_ property of ACS scripts is that they can pause themselves.  They can either wait for a set number of tics with `delay()`, or wait for map geometry to stop being busy with something like `tagwait()`.  So you can raise up some stairs, wait for the stairs to finish appearing, and then open the door they lead to.  Or you can simulate game rules by running a script in an infinite loop that waits for a few tics between iterations.  It's pretty handy.  It's incredibly handy.  It's non-negotiable.

Luckily, Lua can emulate this using coroutines.  I implemented the `delay` case yesterday:

```lua
function lua_test_script(activator, ...)
    zprint("hey it's me what's up", ...)
    coroutine.yield("delay", 70)
    zprint("i'm back again")
end
```

When I press the switch, I see the first message, then there's a two-second pause (Doom is 35fps), then I see the second message.

A lot more details need to be hammered out before this is really equivalent to what ACS can do, but the basic functionality is there.  And since these are full-stack coroutines, I can trivially wrap that yield gunk in a `delay(70)` function, so you never have to know the difference.


## Determinism

ZDoom has demos and peer-to-peer multiplayer.  Both features rely critically on the game state's unfolding exactly the same way, given the same seed and sequence of inputs.

ACS goes to great lengths to preserve this.  It executes deterministically.  It has very, _very_ few ways to make decisions based on anything but the current state of the game.  Netplay and demos _just work_; modders and map authors never have to think about it.

I don't know if I can guarantee the same about Lua.  I'd _think_ so, but I don't _know_ so.  Will the order of keys in a table be exactly the same on every system, for example?  That's important!  Even the ACS random-number generator is deterministic.

I _hope_ this is the case.  I know some games, like Starbound, implicitly assume for multiplayer purposes that scripts will execute the same way on every system.  So it's probably fine.  I do wish Lua made some sort of guarantee here, though, especially since it's such an obvious and popular candidate for game scripting.


## Savegames

ZDoom allows you to quicksave at any time.

_Any_ time.

Not while a script is running, mind you.  Script execution blocks the gameplay thread, so only one thing can actually be happening at a time.  But what happens if you save while a script is in the middle of a `tagwait`?

The coroutine needs to be persisted, somehow.  More importantly, when the game is _loaded_, the coroutine needs to be restored to the same state: paused in the same place, with locals set to the same values.  Even if those locals were wrapped pointers to C++ objects, which now have different addresses.

Vanilla Lua has no way to do this.  Vanilla Lua has a pretty poor serialization story overall — _nothing_ is built in — which is honestly kind of shocking.  People use Lua for games, right?  Like, a lot?  How is this not an extremely common problem?

A potential solution exists in the form of [Eris](https://github.com/fnuecke/eris), a _modified_ Lua that does all kinds of invasive things to allow absolutely anything to be serialized.  Including coroutines!

So Eris makes this at least possible.  I haven't made even the slightest attempt at using it yet, but a few gotchas already stand out to me.

For one, Eris serializes _everything_.  Even regular ol' functions are serialized as Lua bytecode.  A naïve approach would thus end up storing a copy of the _entire_ game script in the save file.

Eris has a thing called the "permanent object table", which allows giving names to specific Lua values.  Those values are then serialized by name instead, and the names are looked up in the same table to deserialize.  So I could walk the Lua namespace _myself_ after the initial script load and stick all reachable functions in this table to avoid having them persisted.  (That won't catch if someone loads new code during play, but that sounds like a really bad idea anyway, and I'd like to prevent it if possible.)  I have to do this to some extent anyway, since Eris can't persist the wrapped C++ functions I'm exposing to Lua.  Even if a script does some incredibly fancy dynamic stuff to replace global functions with closures at runtime, that's okay; they'll be different functions, so Eris will fall back to serializing them.

Then when the save is reloaded, Eris will replace any captured references to a global function with the copy that already exists in the map script.  ZDoom doesn't let you load saves across different mods, so the functions should be the same.  I think.  Hmm, maybe I should check on exactly what the load rules are.  If you _can_ load a save against a more recent copy of a map, you'll want to get its updated scripts, but stored closures and coroutines might be old versions, and that is probably bad.  I don't know if there's much I can do about that, though, unless Eris can somehow save the underlying code from closures/coros as named references too.

Eris also has a mechanism for storing wrapped native objects, so all I have to worry about is translating pointers, and that's a problem Doom has already solved (somehow).  Alas, that mechanism is also accessible to pure Lua code, and the docs warn that it's possible to get into an infinite loop when loading.  I'd rather not give modders the power to fuck up a save file, so I'll have to disable that somehow.

Finally, since Eris loads bytecode, it's possible to do nefarious things with a specially-crafted save file.  But since the save file is full of a web of pointers anyway, I suspect it's not too hard to segfault the game with a specially-crafted save file anyway.  I'll need to look into this.  Or maybe I won't, since I don't seriously expect this to be merged in.


## Runaway scripts

Speaking of which, ACS currently has detection for "runaway scripts", i.e. those that look like they _might_ be stuck in an infinite loop (or are just doing a ludicrous amount of work).  Since scripts are blocking, the game does not actually progress while a script is running, and a very long script would appear to freeze the game.

I think ACS does this by counting instructions.  I see Lua has its own [mechanism](http://stackoverflow.com/a/3400896/17875) for doing that, so limiting script execution "time" shouldn't be too hard.


## Defining new actors

I want to be able to use Lua with (or instead of) `DECORATE`, too, but I'm a little hung up on syntax.

I do have something _slightly_ working — I was able to create a variant imp class with a bunch more health from Lua, then spawn it and fight it.  Also, I did it at runtime, which is probably bad — I don't know that there's any way to _destroy_ an actor class, so having them be map-scoped makes no sense.

That could actually pose a bit of a problem.  The Lua interpreter _should_ be scoped to a single map, but actor classes are game-global.  Do they live in separate interpreters?  That seems inconvenient.  I could load the game-global stuff, take an internal-only snapshot of the interpreter with Lua (bytecode and all), and then restore it at the beginning of each level?  Hm, then what happens if you capture a reference to an actor method in a save file...?  Christ.

I could consider making the interpreter global and doing black magic to replace all map objects with `nil` when changing maps, but I don't think that can possibly work either.  ZDoom has _hubs_ — levels that can be left and later revisited, preserving their state just like with a save — and that seems at odds with having a single global interpreter whose state persists throughout the game.

Er, anyway.  So, the problem with _syntax_ is that `DECORATE`'s own syntax is extremely compact and designed for its very specific goal of state tables.  Even ZScript appears to preserve the state table syntax, though it lets you write your own action functions or just provide a block of arbitrary code.  Here's a short chunk of the imp implementation again, for reference.

```text
  States
  {
  Spawn:
    TROO AB 10 A_Look
    Loop
  See:
    TROO AABBCCDD 3 A_Chase
    Loop
  ...
  }
```

Some tricky parts that stand out to me:

- Labels are important, since these are state tables, and jumping to a particular state is very common.  It's tempting to use Lua coroutines here somehow, but short of using a lot of `goto` in Lua code (yikes!), jumping around arbitrarily doesn't work.  Also, it needs to be possible to tell an actor to jump to a particular state from _outside_ — that's how `A_Look` works, and there's even an ACS function to do it manually.

- Aside from being shorthand, frames are fine.  Though I do note that hacks like `AABBCCDD 3` are relatively common.  The actual animation that's wanted here is `ABCD 6`, but because animation and behavior are intertwined, the labels need to be repeated to run the action function more often.  I wonder if it's desirable to be able to separate display and behavior?

- The durations seem straightforward, but they can actually be a restricted kind of expression as well.  So just defining them as data in a table doesn't quite work.

- This example doesn't have any, but states can also have a number of flags, indicated by keywords after the duration.  (Slightly ambiguous, since there's nothing strictly distinguishing them from action functions.)  `Bright`, for example, is a common flag on projectiles, weapons, and important pickups; it causes the sprite to be drawn fullbright during that frame.

- Obviously, actor behavior is a big part of the game sim, so ideally it should require dipping into Lua-land _as little as possible_.

Ideas I've had include the following.

**Emulate state tables with arguments?**  A very straightforward way to do the above would be to just, well, cram it into one big table.

```lua
define_actor{
    ...
    states = {
        'Spawn:',
        'TROO', 'AB', 10, A_Look,
        'loop',
        'See:',
        'TROO', 'AABBCCDD', 3, A_Chase,
        'loop',
        ...
    },
}
```

It would work, technically, I guess, except for non-literal durations, but I'd basically just be exposing the `DECORATE` parser from Lua and it would be pretty ridiculous.

**Keep the syntax, but allow calling Lua from it?**  `DECORATE` is _okay_, for the most part.  For simple cases, it's great, even.  Would it be good enough to be able to write new action functions in Lua?  Maybe.  Your behavior would be awkwardly split between Lua and `DECORATE`, though, which doesn't seem ideal.  But it would be the most straightforward approach, and it would completely avoid questions of how to emulate labels and state counts.

As an added benefit, this would keep `DECORATE` almost-purely declarative — which means editor tools could still reliably parse it and show you previews of custom objects.

**Split animation from behavior?**  This could go several ways, but the most obvious to me is something like:

```lua
define_actor{
    ...
    states = {
        spawn = function(self)
            self:set_animation('AB', 10)
            while true do
                A_Look(self)
                delay(10)
            end
        end,
        see = function(self)
            self:set_animation('ABCD', 6)
            while true do
                A_Chase(self)
                delay(3)
            end
        end,
    },
}
```

This raises plenty of other API questions, like how to wait until an animation has finished or how to still do work on a specific frame, but I think those are fairly solvable.  The big problems are that it's very much _not_ declarative, and it ends up being rather wordier.  It's not all boilerplate, though; it's fairly straightforward.  I see some value in having state delays and level script delays work the same way, too.  And in some cases, you have only an animation with no code at all, so the heavier use of Lua should balance out.  I don't know.

A more practical problem is that, currently, it's possible to jump to an arbitrary number of states _past_ a given label, and that would obviously make no sense with this approach.  It's pretty rare and pretty unreadable, so maybe that's okay.  Also, labels aren't _blocks_, so it's entirely possible to have labels that don't end with a keyword like `loop` and instead carry straight on into the next label — but those are usually used for logic more naturally expressed as `for` or `while`, so again, maybe losing that ability is okay.

Or...  perhaps it makes sense to do both of these last two approaches?  Built-in classes should stay as `DECORATE` anyway, so that existing code can still inherit from them and perform jumps with offsets, but new code could go entirely Lua for very complex actors.

Alas, this is probably one of those questions that won't have an obvious answer unless I just build several approaches and port some non-trivial stuff to them to see how they feel.


## And further

An enduring desire among ZDoom nerds has been the ability to write custom "thinkers".  Thinkers are really anything that gets to act each tic, but the word also specifically refers to the logic responsible for moving floors, opening doors, changing light levels, and so on.  Exposing those more directly to Lua, and letting you write your own, would be pretty interesting.


## Anyway

I don't know if I'll do all of this.  I somewhat doubt it, in fact.  I pick it up for half a day every few weeks to see what more I can make it do, just because it's interesting.  It has virtually no chance of being upstreamed anyway (the only active maintainer hates Lua, and thinks poorly of dynamic languages in general; plus, it's redundant with ZScript) and I don't really want to maintain my own yet another Doom fork, so I don't expect it to ever be a serious project.

The source code for what I've done so far is available, but it's brittle and undocumented, so I'm not going to tell you where to find it.  If it gets far enough along to be useful as more than a toy, I'll make a slightly bigger deal about it.
