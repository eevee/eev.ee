title: Eevee gained 4,219 experience points...
seriestitle: 2025
date: 2025-01-17 20:00
category: personal
series: birthday

Eevee grew to level 38!

It's been a few years since I did one of these.  My birthday in 2022 was kind of overshadowed by the [loss of our darling cat Pearl]({filename}/2022-01-25-goodbye-pearl.markdown).  But I think I'd like to get back into it, to christen the redone website.

<!-- more -->

<audio src="{static}/media/2012-01/levelup.ogv" controls autoplay style="margin: 1em auto;">

## This year

### Untitled Trefoil game

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/trefoil-demo.gif" alt="Clip of a pixel art game where three chibi characters walk around a grassy field, encounter a sheep called a &quot;Cubaa&quot;, and attack it until it's &quot;not feeling it any more&quot;">
</div>

This was my entry for my annual horny game jam, [🔞 Strawberry Jam 8](https://itch.io/jam/strawberry-jam-8).  Tragically, we did not make it.  I think I bit off a bit more than I could chew by trying to design and also implement an RPG battle system in an engine I haven't used much.

The engine in question is [Godot](https://godotengine.org/), which I keep _desperately_ trying to get a foothold in, and then...  not...  doing.  By "foothold" I mostly mean a little bundle of common code I've written atop Godot for dealing with cases that come up a lot in games but that are too specific for the engine to include directly — a basic actor type, scene switching, that sort of thing.  Just a mini library for me that's already made all the decisions I would make, so I'm not starting completely from scratch.

I guess the other half of a "foothold" is figuring out how to make the engine do things _at all_.  Other than a [brief foray into Unity many years ago]({filename}/2017-10-13-coaxing-2d-platforming-out-of-unity.markdown) that didn't go much further than twiddling with player physics, I just haven't really tried using an integrated engine, and _boy_ — in some ways, it's harder than rolling your own everything.  If a built-in gizmo doesn't do something I take for granted that I should be able to do, then...  fuck me, I guess?

But I would still like to get away from actually having to build every feature from scratch myself (like I do in [LÖVE](https://love2d.org/)) because it just takes so much dang time, which I am then not spending on _making a video game_.  So I would really like to get something resembling a game built and released in Godot!  And this is the latest of several attempts in which I do not do that.

I think there were two big stumbling blocks here that were not conducive to wrangling a new-to-me engine in a jam setting, and I think both are partly effects of Godot's being new-in-general:

- There's often not an obvious good way to approach a problem with Godot's primitives.  Nodes are a cool idea and all, but I think it's less than obvious that you might want to use node names as an ad-hoc interface, e.g. by giving actors a collection of behavior nodes named after components or states or something.

- There's a lot of little oddball behavior and little feature gaps, most notably from GDScript, Godot's bespoke language that's "we have Python at home".  But for a non-code example: there's no way to give a UI widget a maximum size, so if a long word sneaks into your text somewhere...  don't do that, I guess?  Stuff like that that will cost you a few valuable hours chasing down only to find that it doesn't exist.

I took notes at the time about a lot of the speed bumps I ran into, and many of them were about GDScript specifically, but I never wrote them up because...  I mean, christ, I don't want to do another epic teardown XD of a language.  It's embarrassing enough being known for the first one.  Instead, let me try to summarize with a single bullet point that I hope will convey _the vibe_ to anyone who's ever thought about language design for a few minutes:

- Some builtin functions can accept an arbitrary number of arguments.  There is no way to write a function in user code that accepts an arbitrary number of arguments.

Anyway the short version here is that I picked too big of a project to do in a month _and_ I tried to do it in an engine that still has a lot of rough edges.


### Anise

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/anise2020.jpg" alt="Photo of a black sphynx cat in a wintery sweater looking somewhat solemnly at the camera, with an American flag background edited in around him and &quot;anise 2020&quot; poorly scribbled underneath">
</div>

Anise was sick for much of 2023, which kind of fucked up that whole year, but we finally cured him this past spring.  Hooray!  Here is a photo of him from his 2020 Presidential campaign.

This is worth its own post, which I have already written, but it was on Cohost, which is now gone.  Maybe I'll port it over and add a bunch of cat photos to it.

Anyway he's fine and that's great.


### vignettes

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/vignettes-walk.png" alt="Screenshot of a visual novel where two sheep-like characters are out for a walk; one, named Clover, is saying &quot;It's not too far, I think.  About half a mile past that burrito place where none of the waiters wear pants.&quot;">
</div>

So, we released [🔞 Cherry Kisses](https://eevee.itch.io/cherry-kisses) a few years ago.  (Five.  _Five_ years ago??  Oh my god)  It's a little spruced-up jam game where you walk around and talk to customers and do little sex scenes with them, accompanied by art, and also there's an overarching puzzle aspect you can completely ignore if you want.

This was _originally_, as I said, a jam game, which we didn't actually finish in time, but which took maybe a month and a half to do.  At the time, I thought: wow, great!  This porn stuff is E-Z.  We should just crank a couple of these out a year, in between other stuff we're doing!

_Five years later_, we have not yet released another porn game.  Or another game on Steam at all!  Not for lack of trying — we started several (overscoped) visual novels that never ended up finding their footing.

COVID and other world events kind of put a damper on things, creating a broader problem: it's just been _hard_ to drum up the right mood for writing extended lighthearted sex romps.

That said, we _finally_ have something that is _almost_ done.  Actually it's been asymptotically approaching "done" for a while.  It's tentatively called **vignettes**, and the idea is that we will release a _shorter_ story, then go back and update the game later with more shorter stories, and also play around with the format if I feel like it too.  Hopefully this will fix some of our scoping problems.

It's still not done.  But we did most of the work for it this past year.  Like 90%.  It's so close.  I'm getting back to it after I finish this post and another urgent thing.

I'm actually going slowly insane over this, because I've been designing characters and whatnot for VN purposes for _years_, and they have all been rolling around in my head like marbles that whole time, and _no one outside this house knows anything about them_.  I need to let them out!


### fox flux

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/fox-flux-home.png" alt="Screenshot of a pixel art platformer, showing the protagonist (an orange fox) standing in a sort of basement of an abstract home, with jelly beans and chick-shaped candies floating next to her and gift boxes and furniture on a level above">
</div>

Wow!  When I sat down to write this post I thought I'd done basically nothing on [fox flux](https://eevee.itch.io/fox-flux-deluxe) all year.  But I guess I did a lot actually.  It's not moving quite as quickly as I'd hoped, and the game is in a bit of disarray so there haven't been [Patreon](https://www.patreon.com/eevee) builds in a bit, but, it _is_ moving.

I don't want to write out a whole gritty changelog here, but suffice to say I implemented a _bunch_ of stuff that had been languishing as little stubs for a long time, so the game feels a lot closer to feature-complete.  Now I just have to make a zillion levels!  How hard could _that_ be?

(It's very hard.  It's where I got blocked, creatively!  All my level ideas turned out not fun and I didn't have any more so I went to work on other stuff for a while.  Puzzle level design is fuckin' _gnarly_ my dudes)


### Lexy's Labyrinth

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/lexys-labyrinth.png" alt="Screenshot of Lexy's Labyrinth, a tile-based browser puzzle game, showing a small fox player in a maze of ice, water, hot coals, and land mines, as well as a lot of surrounding UI">
</div>

[Lexy's Labyrinth](https://c.eev.ee/lexys-labyrinth/), my free Chip's Challenge emulator, was like 90% finished, so I sat down and 100% finished it.  Or, I dunno, 99%.

Highlights include:

- Now has [CCLP5](https://c.eev.ee/lexys-labyrinth/#pack=cclp5), the latest and greatest community level pack!  Adding this in is what got me back to working on LL, so, thanks for putting it together, everyone.

- The tileset got a lot of touching up, and it now sports a brighter palette, instead of merely a copy of an old dull (not even pastel, just, dull) fox flux palette.  The website is pink to match Lexy, too, though I fear it might be too reddish?

- You can hold <kbd>R</kbd> to restart the level!  At last!

- Undo now uses much less memory, and the undo buffer is limited by size rather than time (though it will always save at least 30 seconds).  On the most pathological built-in level I could find, 30 seconds was about 12 MB, and the limit is 10 MB, so this should be a huge improvement pretty much anywhere.  On a sokoban-like level where the player is mostly stopping and thinking while nothing else happens, undo is virtually unlimited.

- Rewind now accelerates the further back you go, too.

- There are several touchscreen control schemes now: swipe, tap relative to the player, or tap relative to the viewport.  So you can try whichever is least bad.  There's also partial gamepad support, though only within a level.

- A bit more CC2 behavior is now shown visually within the level where it wouldn't be in CC2, like dynamite always showing its full explosion radius.

- Compatibility is vastly improved, _and_ more of the built-in levels are beatable.  (Some of the built-in levels are designed for CC1, but the default rules are CC2-like and _slightly_ different.  A couple levels now have manual patches specifically to make them beatable, a tactic borrowed from ZDoom.)

- Support for Lynx mode has gone from "very bad" to "pretty solid"!  It's still not speedrun legal, largely because it doesn't fully emulate frankly insane bugs like actors being able to teleport on top of each other, but it should be sufficiently accurate for normal purposes.

The editor is also vastly, _vastly_ better; it has multiple new tools for otherwise awkward tasks, it supports arbitrary selections (including a new wand select tool), it supports CC1-style tile connections, and it can export levels in CC1 format!

I'd had code for that last thing written for ages and just never plugged it in, and I didn't even notice until I saw someone in the Bit Busters Discord comment that LL wasn't useful for CC1 level editing because it couldn't actually export as CC1.  Whoops.

There are also lots of experimental extra tiles, though they aren't all fully implemented, and I haven't made any "official" levels with them.  I _did_ start on my own level pack for Lexy's Labyrinth specifically, but I completely forgot about it until I was writing this post just now.  Wonder if I'll ever finish that.  200 levels is a lot, but it's also good practice.


### Doom stuff

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/idfkn.png" alt="Screenshot of an &quot;idgames archive&quot; website listing, showing two Doom WADs that list their maps with some stats, whether they support skill levels, whether they have music, etc.">
</div>

In August, Microsoft unveiled an entirely redone official Doom release, now with Boom support, making it compatible with more of the Doom ecosystem.

That was weird, because Boom is a third-party fork of the open source Doom release, meaning it's GPL.  And there was no release of the current Doom codebase.

Turns out that what Microsoft did was pay someone to cleanroom Boom from scratch, effectively laundering the GPL off of it, so that they could add open source extensions to Doom (an open source game) and make it proprietary again.

I found this...  _frustrating_.  But a lot of Doom people didn't really care and mostly found it neat that they can play Doom on an XBox now.  (It's notoriously difficult to put someone else's GPL code on a console.  The console APIs are all covered under NDAs — you know, to prevent anyone from finding out that the **X**Box uses Direct**X** — so you'd be in a position where the GPL requires you to release your modified code, but the NDA requires you to not do that.)

Instead of sitting around being mad forever that the very people who've benefitted so much from Doom's being open source don't really care about open source, I tried to pour it into something slightly more constructive, and so I started tinkering with an improved [idgames](https://www.doomworld.com/idgames/) frontend.  I guess the idea was that people mostly seemed to value having a WAD browser built into Microsoft Doom, but there's no reason we can't have that for the entire archive of everything ever made, right?

I ran out of steam before it got _too_ far, but I did get it doing a few interesting things, like automatically producing screenshots of the opening shot of each level (which you can see in the screenshot above).  I had some other ideas, like trying to infer qualitative descriptions of level size and difficulty, but didn't quite get around to it.  Oh well.

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/doom-text-generator.png" alt="Screenshot of my Doom text generator, with a selection of fonts and colors and text rendering sliders, currently displaying &quot;Instead, I worked on this some more&quot;">
</div>

So I went back to my [Doom text generator](https://c.eev.ee/doom-text-generator/), a former advent calendar project that I cranked out in a day and [wrote about before]({filename}/updates/2019-12-01-doom-text-generator.markdown).  I'd seen a couple people mention having actually used it, which was cool, so I went and did some stuff to it.

- It could only render its own built-in fonts, so an obvious extension was to extend it to load fonts of any format from a provided WAD or PK3, all client-side.

- It has a truckload more built-in fonts now, courtesy of [Jimmy Paddock's collection](https://forum.zdoom.org/viewtopic.php?t=33409).  So the Doom text generator can now generate Duke Nukem text, too.  Weird.

- It can, finally, combine multiple fonts in a single message, using a tiny bbcode-like markup language.

- It can generate a bunch of images in bulk, which is exceptionally handy for level authors targeting vanilla-like Doom, where you have to provide your own level name images.  It can even read the level names directly from a `MAPINFO` file that more advanced ports would use to render names themselves.

Now it's got a [Doomworld thread](https://www.doomworld.com/forum/topic/147196-doom-text-generator-%E2%80%94-last-updated-2024-11-25/) and [source code](https://github.com/eevee/doom-text-generator) (little redundant since it's all shipped to the client) and everything.  It's like a real project!  I'm glad people find it useful.

It even got a Cacowards 2024 sidebar shoutout, which is cool, making this basically the only thing of note I've ever done in the Doom ecosystem.  The Boom license laundering also got an explicit shoutout, though, so.  Cool.



### Sudoku

<div class="prose-full-illustration">
<img style="max-height: 20em;" src="https://c.eev.ee/puzzles/sudoku-20241018-1.svg" alt="A sudoku with no given digits, but several diagonal clues outside the grid and some killer cages inside">
</div>

I made some sudoku, after realizing I could just make some sudoku if I wanted to.  My first one is appropriately titled [1](https://sudokupad.app/cb5yikms2b) (killer + little killer), and the rest are on my new [puzzle index](https://c.eev.ee/puzzles/).  Speaking of which—


### You are here

<div class="prose-full-illustration">
<img src="{attach}/media/2025-01-birthday/you-are-here.png" alt="Screenshot of this post">
</div>

I [redesigned the website]({filename}/updates/2024-12-03-fresh-start.markdown) in the wake of Cohost's shutdown, and after several years of not writing much.  Time will tell if it encourages me to write more going forward, but so far, so good.

I also wrote those pages about stuff!  The list of [variant sudoku types]({filename}/pages/fyi/variant-sudoku.markdown) (which I've even used for my own reference already), and ports of my [Lights Out]({filename}/pages/toys/lights-out.markdown) and [Rush Hour]({filename}/pages/toys/rush-hour.markdown) CSS crimes from Cohost.


## This year

I basically forget about any aspirational list like this within a week, but I would _really really_ like to:

- Get **vignettes** released, _and_ get a couple more stories added to it!

- Get **fox flux** out of its level design rut and just accelerate into building the game proper.  Also more patron builds.

- Write more, I think.  I do kind of miss it.

I'd like to...  reconnect with the world, I guess.  Everything feels disconnected.  I dropped Twitter and tried to rebuild on Cohost, did not really succeed at that (there's a post in that, too), and then Cohost went down.  Now there's Bluesky, I guess, but I feel like I'm two platforms and several years in the hole.  _And_ a couple closer friendships disintegrated over the same period, so I have been adrift as all hell.

And the primary way I know how to connect with anyone is through my work!  So I need to make some!
