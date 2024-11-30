title: I entered Ludum Dare 36
date: 2016-08-29 18:01
category: updates
tags: tech, gamedev, making things

Short story: I made a video game again!  This time it was for [Ludum Dare](http://ludumdare.com/compo/about-ludum-dare/), a game jam with some tight [rules](http://ludumdare.com/compo/rules/): solo only, 48 hours to make the game and all its (non-code) assets.

(This is called the "Compo"; there's also a 72-hour "Jam" which is much more chill, but I did _hard mode_.  Usually there's a ratings round, but not this time, for reasons.)

I used the [PICO-8](http://www.lexaloffle.com/pico-8.php) again, so you can [play it on the web](https://c.eev.ee/isaacs-descent/) as long as you have a keyboard.  It's also on [Ludum Dare](http://ludumdare.com/compo/ludum-dare-36/?action=preview&uid=111773), and in [splore](http://www.lexaloffle.com/bbs/?tid=27559), and here's the cartridge too.

[![Isaac's Descent](https://c.eev.ee/isaacs-descent/isaac.p8.png)](https://c.eev.ee/isaacs-descent/)

But wait!  Read on a bit first.

<!-- more -->

## Foreword

I've never entered a game jam before, and I slightly regretted that I missed a PICO-8 jam that was happening while I was making [Under Construction]({filename}/release/2016-05-25-under-construction-our-pico-8-game.markdown).  I've _certainly_ never made a game in 48 hours, so that seemed exciting.

More specifically, I have some trouble with shaking ideas loose.  I don't know a more specific word than "idea" for this, but I mean creative, narrative ideas: worldbuilding, characters, events, gameplay mechanics, and the like.  They have a different texture from "how could I solve this technical problem" ideas or "what should I work on today" ideas.

I'll often have an idea or two, maybe a theme I want to move towards, and then hit a wall.  I can't think of any more concepts; I can't find any way to connect the handful I have.  I end up shelving the idea, sometimes indefinitely.  This has been particularly haunting with my interactive fiction game in progress, Runed Awakening, which by its very nature is nothing _but_ narrative ideas.

My true goal for entering Ludum Dare was to jiggle the idea faucet and maybe loosen it a bit.  Nothing's quite as motivating as an extreme time limit.  I went in without anything in mind; I didn't even know it was coming up until two days beforehand.  (The start time is softly enforced by the announcement of a theme, anyway.)  I knew it would probably resemble a platformer, since I already had the code available to make that work, but that was about it.

----

I already wrote about the approach to making our last game, so I can't very well just do that again.  Instead, here's something a little different: I took regular notes on the state of the game (and myself), all weekend.  You can see exactly how it came together, almost hour by hour.  Is that interesting?  _I_ think it's interesting.

I don't know if this is a better read if you play the game first or last.  Maybe both?

There's also a surprise at the very end, as a reward for reading through it all!  No, wait, stop, you can't just scroll down, that's cheating—


## Timeline

### Thursday

**09:00** — Already nervous.  Registered for the site yesterday; voted on the themes today; jam actually starts tomorrow.  I have no idea if I can do this.  What a great start.

### Friday

**09:00** — Even more nervous.  Last night I started getting drowsy around 5pm, I guess because my sleep is still a bit weird.  So not only do I only have 48 hours, but by the looks of things, I'll be spending half that time asleep.

**17:00** — I can't even sit still and do anything for the next hour; I'm too antsy about getting started.

**START!! 18:00** — Theme revealed: "Ancient Technology".  I have _no_ ideas.

Well, no, hang on.  Shortly before the theme was announced, I had a brief Twitter conversation that shook something loose.  I'd mentioned that I rarely seem to have enough ideas to fill a game.  Someone accidentally teased out of me that it's more specific than that: I have trouble coming up with ideas that _appeal_ to me, that satisfy me in the way I really like in games and stories.  In retrospect, I probably have a bad habit of rejecting ideas by reflex before I even have a chance to think about them and turn them into something more inspiring.

The same person also asked how I want games to _feel_, and of course, that's what I should be keeping front and center, before even worrying about genre or mechanics or anything.  How does this feel, and how does it make _me_ feel?  I _know_ that's important, but I'm not in the habit of thinking about it.

With that in mind, how does "ancient technology" make me feel?

It reminds me immediately of two things: Indiana Jones-esque temples, full of centuries-old mechanisms and unseen triggers that somehow still work perfectly; and also Stargate, where a race literally called "Ancients" made preposterously advanced devices with such a sleek and minimalist design that they might as well have been magic.

The common thread is a sense of, hm, "soft wonder"?  You're never quite sure what's around the next corner, but it won't be a huge surprise, just a new curiosity.  There's the impression of a coherent set of rules somewhere behind the scenes, but you never get to see it, and it doesn't matter that much anyway.  You catch a glimpse of what's left behind, and half your astonishment is that it's still here at all.

Also, I bet I can make a puzzle-platformer out of this.

**18:20** — Okay, well!  I have a character Isaac (stolen from Glip, ahem) who exists in Runed Awakening but otherwise has never seen any real use.  I might as well use them now, which means this game is also set somewhere in Flora.

I've drawn a two-frame walking animation and saved it as `isaac.p8` for now.  It's enough to get started.  I'm gonna copy/paste all the engine gunk from my unfinished game, rainblob — it's based on what was in Under Construction, with some minor cleanups and enhancements.

**19:00** — I'm struggling a little bit here, because Isaac is two tiles tall, and I never got around to writing real support for actors that are bigger than a single tile.  Most of the sprite drawing is now wrapped in a little `sprite` type, so I don't think this will be _too_ bad — I almost have it working, except that it doesn't run yet.

**19:07** — Success!  Apparently I was closer than I thought.  The solution is a bit of a hack: instead of a list of tiles (as animation frames), Isaac has a list _of lists_ of tiles, where each outer list is the animation for one grid space.  It required some type-checking to keep the common case working (boo), and it blindly assumes any multi-tile actor is a 1×n rectangle.  It's fine.  Whatever.  I'll fix it if I really need to.

**19:16** — I drew and placed some cave floor tiles.  Isaac can no longer walk left or jump.  I am not sure why.  I really, really hope it's not another collision bug.  The collision function has been such a nightmare.  Is it choking on a moving object that's more than a tile tall?

**19:20** — I have been asked to put a new bag in the trash can.  This is wildly unjust.  I do not have time for such trivialities.  But I have to pee anyway, so it's okay — I'll batch these two standing-up activities together to save time.  Speed strats.

**19:28** — The left/jump thing seems to be a bug with the PICO-8; the button presses don't register at all.  Restarting the "console" fixed it.  This is ominous; I hope a mysterious heisenbug doesn't plague me for the next 46½ hours.

**19:51** — Isaac is a wizard.  Surely, they should be able to cast spells or whatever.  Teeny problem: the PICO-8 only has two buttons, and I need one of them for jumping.  (Under Construction uses up for jump, but I've seen several impassioned pleas against doing that because it makes using a real d-pad very awkward, and after using the pocketCHIP I'm inclined to agree.)

New plan, then: you have an inventory.  Up and down scroll through it, and the spare button means "use the selected item".  Accordingly, I've put a little "selected item" indicator in the top left of the screen.

Isaac hasn't seen too much real character development; it's hard to develop a character without actually putting them _in_ something.  Their backstory thusfar isn't really important for this game, but I did have the idea that they travel with a staff that can create a reflective bubble.  That's interesting, because it suggests that Isaac prefers to operate defensively.  I made a staff sprite and put it in the starting inventory, but I'm not quite sure what to do with it yet; I don't know how the bubble idea would work in a tiny game.

**20:01** — As a proof of concept, I made the staff shoot out particles when you use it.  The particle system is from rainblob, and is pretty neat — they're just dumb actors that draw themselves as a single pixel.

I bound the X button to "use".  Should jumping be X or O?  I'm not sure, hm.  My Nintendo instincts tell me the right button is for jumping, but on a keyboard, the "d-pad" and buttons are reversed.

**20:04** — I realize I added a sound effect for jumping, then accientally overwrote the code that plays it.  Oops; fixing that.  Good thing I didn't overwrite the sound!  This is what I get for trying to edit the assets in the PICO-8 and the code in vim, when it's all stored in a single file.

**20:37** — I have a `printat` function (from Under Construction) which prints text to the screen with a given horizontal and vertical alignment.  It needs to know the width of text to do this, which is easy enough: the PICO-8 font is fixed-width.  Alas!  The latest PICO-8 release added characters to represent the controller buttons, and I'd really like to use them, but they're double-wide.  Hacking around this is proving a bit awkward, especially since there's no `ord()` function available oh my god.

**20:50** — Okay, done.  The point of that was: I rigged a little hint that tells you what button to press to jump.  When you approach the first ledge, Isaac sprouts a tiny thought bubble with the O button symbol in it.  PICO-8 games tend not to explain themselves (something that has frustrated me more than once), so I think that's nice.  It's the kind of tiny detail I love including in my work.


**21:04** — I wrote a tiny fragment of music, but I really don't know what I'm doing here, so...  I don't know.

I had the idea that there'd be runes carved in the back wall of this cave, so I made a sprite for that, though it's basically unrecognizable at this size.  I don't know what reading them will do, yet.

I also made the staff draw a bubble (in the form of a circle around you) while you're holding the "use" button down, via a cheap hack.  Kinda just throwing stuff at the wall in the hopes that something will stick.

**21:07** — I've decided to eat these chips while I ponder where to go from here.

**21:22** — So, argh.  Isaac's staff is supposed to create a bubble that reflects magical attacks.  The immediate problem there is that my collision assumes everything is a rectangle.  I _really_ don't want to be rewriting collision with only a weekend to spend on this.  I could make the bubble rectangular, but who's ever heard of a rectangular magic bubble?

Maybe I could make this work, but it raises more questions: _what_ magical attacks?  What attacks you?  Are there monsters?  Do I have to write monster AI?  Can Isaac die?  I need to translate these scraps of thematics into game mechanics, somehow.

I try to remember to think about the _feel_.  I want you to feel like you're exploring an old cavern/temple/something, laden with traps meant to keep you out.  I think that means death, and death means save points, and save points mean saving the game state, which I don't have extant code for.  Oof.

**22:00** — Not much has changed; I started doodling sprites as a distraction.  Still getting this thing where left and up stop working, what the hell.

**22:05** — Actually, I'm getting tired; I should deal with the cat litter before it gets too late.  Please hold.

**22:59** — I wrote some saving, which doesn't work yet.  Almost, maybe.  I do have a pretty cool death animation, though it looks a bit wonky in-game, because animations are on a global timer.  Whoops!  All of them have been really simple so far, so it hasn't mattered, but this is something that really needs to start at the beginning and play through exactly once.

**23:15** — Okay!  I have a save, and I have death, and I even have some sound effects for them.  The animation is still off, alas (and loops forever), and there's no way to _load_ after you die, but the basic cycle of this kind of game is coming together.  If I can get a little more engine stuff working tomorrow, I should be able to build a little game.  Goodnight for now.

## Saturday

**07:48** — I'm.  I'm up.

**08:28** — Made the animation start when the player dies and stop after it's played once.  Also made the music stop immediately on death and touched up the sprites a bit.  Still no loading, so death pretty much ends the game forever; that's up next and should be easy enough.  First, breakfast.

**09:09** — The world is now restored after you die, and I fixed a few bugs as well.  Cool beans.

**09:14** — So, ah.  That's a decent start mechanically, but I need a little more _concept_, especially as it relates to the theme.  I don't expect this game to be particularly deep, what with its non-plot of "explore these caverns", but I do want to explore the theme a bit.  I want something that's interesting to play, too, even if for only five minutes.

Isaac is a clever wizard.  Canonically, he might be the cleverest wizard.  What does his staff do?

What kind of traps would be in a place like this?  Spikes, falling floors, puzzles?  Monsters?  Pressure plates?

_What does Isaac's staff do?_

Hang on, let me approach this a much more sensible way: if _I_ were going to explore a cavern like this, what would I _want_ my staff to do?

**09:59** — I'm still struggling with this question.  I thought perhaps the cavern would only be the introductory part, and then you'd find a cool teleporter to a dusty sleek place that looked a lot more techy.  I tried drawing some sleek bricks, but I can't figure out how to get the aesthetic I want with the PICO-8's palette.  So I distracted myself by drawing some foreground tiles again.  Whoops?

**10:01** — I'd tweeted two GIFs of Isaac's death while working on it, complete with joking melodramatic captions like "death has no power here".  I also lamented that I didn't know yet what the game was _about_, to which someone jokingly replied that so far it seemed to be "about death".

Aha.  Maybe the power of Isaac's staff is to _create_ savepoints, and maybe some puzzles or items or whatever transcend death, sticking around after you respawn.  I'll work with that for a bit and see what falls out of it.

**11:12** — Wow, I've been busy!  The staff now creates savepoints, complete with a post-death menu, a sound effect, a flash (bless you, UC's `scenefader`), a thought-bubble hint, and everything.  It's pretty great?  And it fits perfectly: if you're exploring a trap-laden cavern then you'd want some flavor of safety equipment with you, right?  What's safer than outright resurrection?

I can see some interesting puzzles coming out of this: you have to pick your savepoint carefully to interact with mechanisms in the right way, or you have to make sure you can kill yourself if you need to, since that's the only way to hop back to a savepoint.  And it's a purely defensive ability, just as I wanted.  And something impossibly cool and powerful but _hilariously_ impractical seems extremely up Isaac's alley, from what I know about them so far.

**11:59** — Still busy, which is a good sign!  I've been working on making some objects for Isaac to interact with in the world; so far I've focused on the runes on the wall, though I'm not quite sold on them yet.  The entire game so far is that you have to make a save point, jump down a pit to use a thing that extends a bridge over the pit, then kill yourself to get back to the save point and cross the bridge.  It's very rough, but it's finally _looking_ like a game, which is really great to see.

**12:28** — I finally got sick enough of left/up breaking that I sat down and tried every distinct action I could think of, one at a time, to figure out the cause.  Turns out it was my _drawing tablet_, which I'd used a couple times to draw sprites?  If the pen is close enough to even register as a pointer, left and up break.  I know I've seen the tablet listed as a "joypad" in other SDL applications, so my best guess is that it's somehow acting as an axis and confusing PICO-8?  I can't imagine why or how.  Super, super weird, but at least now I know what the problem is.

**14:28** — Uh, whoops.  Somehow I spent two hours yelling on Twitter.  I don't know how that happened.

**16:42** — Hey, what's up.  I've been working on music (with very mixed results) and fixing bugs.  I'm still missing a lot of minor functionality — for example, resetting the room doesn't actually clear the platforms, because resetting the map only asks actors to reset themselves, and the platforms are _new_ actors who don't know they should vanish.  Oops.

Oh, I also have them appearing on a timer, which is cool.  I want their appearance to be animated, too, but that's tricky with the current approach of just drawing tiles directly on the map.  I guess I could turn them into real actors that are always present but can appear and vanish, which would also fix the reset thing.

For now, it's time to eat and swim, so I'll get back to this later.

**18:22** — I'm so fucked.  Everything is a mess.  The room still doesn't reset correctly.  The time is half up and I have _almost_ one room so far.

I need to shift gears here: fix the bugs as quickly as I can, then focus on rooms.

**20:05** — I fixed a bunch of reset bugs, but I'm getting increasingly agitated by how half-assed this engine is.  It's alright for what it is, I guess, but it clearly wasn't designed for anything in particular, and I feel like I have to bolt features on haphazardly as I need them.

Anyway, I made progression work, kinda: when you touch the right side of the room, you move on to the next one.  When you touch the right side of the final room, you win, and the game celebrates by crashing.

I made a little moving laser eye thing that kills you on contact, creating a cute puzzle where you just resurrect yourself as soon as it's gone past you.  Changed death so time keeps passing while the prompt is up, of course.

Now I have a whopping, what, _three_ world objects?  And one item you can use, the one you start with?  And I'm not sure how to put these together into any more puzzles.

I made Isaac's cloak flutter a bit while they walk.  Cool.

**20:31** — For lack of any better ideas, I added something I'd wanted since the beginning: Isaac's color scheme is now chosen randomly at startup.  They _are_ a newt, you see.

**21:07** — Did some cleanup and minor polishing, but still feeling blocked.  Going to brainstorm with myself a bit.

What are some "ancient" mechanisms?  Pressure plates; blowdarts; secret doors; hidden buttons; ...?

Does Isaac get an improved resurrection ability later?  Resurrect where you died?  I don't know how that would be especially useful unless you died on a moving platform, and I don't have anything like that.

Other magical objects you find...?

Puzzle ideas?  Set up a way to kill yourself so you can use it later?  Currently there's no way to interact with the world other than to add those platforms, so I don't see how this would work.  I also like "conflict" puzzles where two goals seem to depend on each other, but offhand I can't think of anything along those lines besides the first room.

**21:55** — I've built a _third puzzle_, which is just some slightly aggravating platforming, made a little less so by the ability to save your progress.

**22:19** — I started on a large room marking the end of the cave sequence and the entrance to the sleek brick area.  I made a few tiles and a sound effect for it, but I'm not quite sure how the puzzle will work.  I want a bigger and more elaborate setup with some slight backtracking, and I want to give the player a new toy to play with, but I'm not sure what.

I'll have to figure it out tomorrow.

## Sunday

**08:49** — Uggh, I'm awake.  Barely.  I keep sleeping for only six hours or so, which sucks.

I think I want to start out by making a title screen and some sort of ending.  Even if I only have three puzzles, a front and back cover will make it look much more like an actual game.

**09:57** — I made a little title screen and wrote a simple ditty for it, which I might even almost like?

**11:09** — Made a credits screen as well, which implies that there's an actual ending.  And there is!  You get the Flurry, an enchanted rapier I thought of a little while ago.  It's not described in the game or even mentioned outside of the "credits", in true 8-bit fashion.

Now I have a complete game no matter what, so I can focus on hammering out some levels without worrying too much about time.

I also fixed up the ingame music; it used to have some high notes come in on a separate track, in my clumsy attempts at corralling multiple instruments, but I think they destroyed the mood.  Now it's mostly those low notes and some light "bass".  It works as a loop now, too.  Much better in every way.

The awkward-platforming room had a particularly tricky jump that turned out to be trickier than I thought — I suddenly couldn't do it at all when trying to demo the game for Mel.  At their suggestion, I made it a bit less terrible, though hopefully still tricky enough that it might need a second try.

**13:05** — Hi!  Wow!  I've been super busy!  I came up with a new puzzle involving leaving a save point in midair while dropping down a pit.  Then I finally added a new item, mostly inspired by how easy it was to implement: a spellbook that makes you float but doesn't let you jump, so you can only move back and forth horizontally until you turn it off.  I also added a thought bubble for how to cycle through the inventory, some really cute sound effects for when you use the book, and an introductory puzzle for it.  It's coming along pretty nicely!

**14:13** — Trying to design a good puzzle for the next area.  I made a stone door object which can open and close, though the way it does so is pretty gross, and a wooden wheel that opens it.  I really like the wheel; my first thought was to use a different color lever, but I wanted the doors to be reusable whereas the platform lever isn't, and using the same type of mechanism seemed misleading.

I might be trying to cram too much into the same room at the moment?  It introduces the spellbook _and_ the doors/wheel, then makes you solve a puzzle using both.  I might split this up and try to introduce both ideas separately.

I think around 16:00, I'm gonna stop making puzzle rooms (unless I still have an amazing idea) and focus on cleaning stuff up, fixing weird bugs, and maybe un-hacking some of these hacks.

**15:19** — Someone asked if I streamed my dev process, and I realized that this would've been a perfect opportunity to do that, since everything happens within a single small box.  Oops.  I guess I'll stream the last few hours, though now no one can watch without getting all he puzzle spoiled.

I made a separate room for getting the spellbook, plus another for introducing the stone doors.  The pacing is much _much_ better, and now there are more puzzles overall, which is nice.

**15:54** — My puzzles seem to be pretty solid, and I've only got space for one more on the map, so I'm thinking about what I'd like it to be.

I want something else that combines mechanics, like, using the platforms to block a door from closing all the way.  But a door and a platform can't coexist on the same tile, so the door has to start out partially open.  And...  what happens if you summon the platform after closing the door all the way?  Hm.  I wish my physics were more thorough, but right now none of these objects interact with each other terribly well; the stone door in particular just kinda ignores anything in its way until it hits solid wall.

**16:04** — Instead of all that, I fixed the animation on the wheel (it wasn't playing at all?), gave it a sound effect that I _love_, and finally added an explicit way to control draw order.  The savepoint rune had been drawing _over_ the player since the very beginning, which had been bugging me all weekend.  Now the player is always on top.  Very glad I had `sort` lying around.

**16::57** — I guess I'm done?  I filled that last puzzle room with an interesting timing thing that uses the lever, wheel, runes, _and_ floating, but there are a couple different ways to go about it, and one way is 1-cycle.  It bugs me a _little_ that the original setup I wanted (repeat the platforming, then discover it won't get you all the way to the exit and have to rethink it) doesn't work, but, there's no reason you'd _think_ to do it the fastest way the first time, and I think being able to notice that adds an extra "aha".  Gotta resist the urge to railroad!

_(Editor's note: I later fixed a bug that removed the 1-cycle solution.)_

I'll call this done and let people playtest it, once I make it fit within the compressed size limit.

**17:08** — God, fuck the compressed size limit.  I started at 20538; I deleted all the debug and unused stuff inherited from rainblob and UC, and now I'm at 18491.  The limit is 15360.  God dammit.  I don't want to have to strip all the comments again.

**17:39** — I ended up deleting all the comments again.  Oh, well.  I ran through it from start to finish once, and all seems good!  The game is done and online, and all that's left is figuring out how to put it on the LD website.

**18:46** — Time is up, but this is "submission hour" and the rules allow fixing minor bugs, so I fixed a few things people have pointed out:

- Two obvious places you could get stuck now have spikes.  You can reset the room from the menu, but I'm pretty sure nobody noticed the "enter = menu" on the title screen, and a few people have thought they had to reset the entire game.

- The last spike pit in the spellbook room required you to walk through spikes, which wasn't what I intended and _looks_ fatal, even though it's not.  The intention was for it to be an exact replica of the previous pit, except that you have to float across it from a tile higher; this solution now works.

- One of those half-rock-brick tiles somehow ended up in the first room?  Not sure how.  It's gone now.

- Mel expressed annoyance at having to align a float across the wide penultimate room with no kind of hint, so I added a half-rock-brick tile to the place where you need to stand to use the high-up wheel.


## Parting thoughts

I enjoyed making this!  It definitely accomplished its ultimate goal of giving me more experience shaking ideas loose.  Looking back over those notes, the progression is fascinating: I didn't even know the core mechanic of resurrecting until 16 hours in (a third of the time), and it was inspired by a joke reply on Twitter.  At the 41-hour mark, I still only had three and a half puzzle rooms; the final game has ten.  The spellbook seriously only exists because "don't apply gravity" was so trivial to implement, and the floating effect is something I'd already added for making the Flurry dramatically float above its platform.  _Half the game_ only exists because I decided a puzzle was too complicated and tried to split it up.

I almost can't believe I actually churned all this out in 48 hours.  I've pretty much never made music before, but I ended up really liking the main theme, and I _adore_ the sound effects.  The sprites are great, considering the limitations.  I'd never drawn a serious sprite animation before, either, but I love Isaac's death sequence.  The cave texture is _great_, and a last-minute improvement over my original sprite, which looked more like scratched-up wood.  I also drew a scroll sprite that I adored, but I never found an excuse to use it in the game, alas.

Almost everyone who's played it has made it all the way through without too much trouble, but also seemed to enjoy the puzzles.  I take that to mean the game has a good learning curve, which I'm really happy about.

I'm glad I already had a little engine, or I would've gotten _nowhere_.

I have some more ideas that I discarded as impractical due to time or size constraints, so I may port the game to LÖVE and try to expand on it.  When I say "may", I mean I started working on this about two hours after finishing the game.


## Oh, and I'm writing a book

Right, yes, about that.  I've been mumbling about this for ages, but I didn't want to go on about the idea so much that actually _doing it_ lost its appeal.  I think I've made enough of a dent now that I'm likely to stick with it.

I'm writing a book about game development — the literal act of game development.  I made a list of about a dozen free (well, except PICO-8) and cross-platform game engines spanning a wide range of ease-of-use, creative freedom, and age.  I'm going to make a little game in each of them and explain what I'm doing as I do it, give background on totally new things, preserve poor choices and show how I recovered from them, say what inspired an idea or how I got past a creative roadblock, etc.  The goal is to write something that someone with no experience in programming or art or storytelling can follow from beginning to end, getting at least an impression of what it looks like to create a game from scratch.

It's kind of a response to the web's mountains of tutorials and beginner docs that take you from "here's what a variable is" all the way to "here's what a function is", then abandon you.  I hate trying to get into a new thing and only finding slow, dull introductions that don't tell me how to do anything _interesting_, or even show what kinds of things are possible.  I hope that for anyone who learns the way I do, "here's how I made a whole game" will be more than enough to hit the ground running.

I have part of an early chapter on MegaZeux written; I wanted to finish it by the end of August, but that's clearly not happening, oops.  I also started on a Godot chapter, which will be a little different since it's for a game that will hopefully have multiple people working on it.

Isaac's Descent will be the subject of a PICO-8 chapter — that's why I took the notes!  It'll expand _considerably_ on what I wrote above, starting with going through all the code I inherited from Under Construction (and recreating how I wrote it in the first place).  I also have about 20 snapshots of the game as it developed, which I'm holding onto myself for now.

I want to put rough drafts of each chapter on the $4 [Patreon](https://www.patreon.com/eevee) tier as I finish them, so keep an eye out for that, though I don't have any ETA just yet.  I imagine MegaZeux or PICO-8 will be ready within the next couple months.
