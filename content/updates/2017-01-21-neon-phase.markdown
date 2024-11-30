title: NEON PHASE
date: 2017-01-21 20:02
category: updates
tags: gamedev, making things

It all started after last year's [AGDQ](https://gamesdonequick.com/), when I lamented having spent the entire week just watching speedruns instead of doing anything, and thus having lost my rhythm for days afterwards.

This year, several friends reminded me of this simultaneously, so I begrudgingly went looking for something to focus on during AGDQ.  I'd already been working on Isaac's Descent HD, so why not keep it up?  Work on a video game while watching video games.

Working on a game for a week sounded an awful lot like a game jam, so I jokingly tweeted about a game jam whose express purpose was to not _completely_ waste the week staring at a Twitch stream.  Then someone suggested I make it an actual jam on itch.io.  Then Mel asked to do a game with me.

And so, thanks to an almost comical sequence of events, we made [NEON PHASE](https://eevee.itch.io/neon-phase) — a half-hour explorey platformer.

<!-- more -->


## The game

<div class="prose-full-illustration">
<a href="https://eevee.itch.io/neon-phase"><img src="/media/2017-01-neon-phase/neon-phase.png"></a>
</div>

The game is set in the [Flora](http://floraverse.com/) universe, as is everything Mel gets their hands on.  (I say this with all the love in the world.  ♥  Anyway, my games are _also_ set in the Flora universe, so who am I to talk.)

I started out by literally copy-pasting the source code for Isaac's Descent HD, the game I've been making with [LÖVE](http://floraverse.com/) as an extension of an [earlier PICO-8 game I made](https://eevee.itch.io/isaacs-descent).  It's not terribly far yet, but it's _almost_ to the point of replicating the original game, which meant I had a passable platformer engine that could load Tiled maps and had some notion of an "actor".  We both like platformers, anyway, so a platformer it would be.

We probably didn't make the _best_ use of the week.  I think it took us a couple days to figure out how to collaborate, now that we didn't have the PICO-8's limitations and tools influencing our direction.  Isaac is tile-based, so I'd taken for granted that this game would also be tile-based, whereas Mel, being an illustrator, prefers to draw...  illustrations.  I, an idiot, decided the best way to handle this would be to start cutting the illustrations into tiles and then piecing them back together.  It took several days before I realized that oh, hey, Mel could just draw _the entire map_ as a single image, and I could make the player run around on that.

So I did that.  Previously, collision had been associated only with tiles, but it wasn't too hard to just draw polygons right on the map and use those for collision.  (_Bless_ [Tiled](http://www.mapeditor.org/), by the way.  It has some frustrating rough edges due to being a very general-purpose editor, but I can't imagine how much time it would take me to write my own map editor that can do as much.)

And speaking of collision, while I did have to dig into a few thorny bugs, I'm _thrilled_ with how well the physics came out!  The collision detection I'd written for Isaac's Descent HD was designed to support arbitrary polygons, even though so far I've only had square tiles.  I knew the whole time I was making my life a lot harder, but I _really_ didn't want to restrict myself to rectangles right out of the gate.  It paid off in NEON PHASE — the world is full of sloping, hilly terrain, and you can run across it fairly naturally!

I'd also thought at first that the game would be a kind of actiony platformer, which is why the very first thing you get greatly resembles a weapon, but you don't end up actually fighting anything.  It turns out enemy behavior takes a bit of careful design and effort, and I ended up busy enough just implementing Mel's story.  Also, dropping fighting meant I didn't have to worry about death, which meant I didn't have to worry about saving and loading map state, which was _great news_ because I still haven't done any of that yet.

It's kind of interesting how time constraints can influence game design.  The game has little buildings you can enter, but because I didn't have saving/loading implemented, I didn't want to _actually_ switch maps.  Instead, I made the insides of buildings a separate layer in Tiled.  And since I had both layers on hand, I just drew the indoor layer right on top of the outdoor layer, which made kind of a cool effect.

A side effect of this approach was that you could see the inside of all buildings (well, within the viewport) while you were inside one, since they all exist in the same space.  We ended up adding a puzzle and a couple minor flavor things that took advantage of this.

If I _had_ had saving/loading of maps ready to go, I might have opted instead for a more traditional RPG-like approach, where the inside of each building is on its own map (or appears to be) and floats in a black void.

Another thing I really liked was the glitch effect, which I wrote on a whim early on because I've had shaders on the brain lately.  We were both a little unsure about it, but in the end Mel wrote it into the plot and I used it more heavily throughout, including as a transition effect between indoors/outdoors.

Mel was responsible for art _and_ music _and_ story, so the plot unfortunately wasn't finalized until the last day of the jam.  It ended up being 30 pages of dialogue.  Sprinkled throughout were special effects that sound like standard things you'd find in any RPG dialogue system — menus, branches, screen fades, and the like — but that I just hadn't written yet.

The dialogue system was downright primitive when we started; I'd only written it as a brief proof of concept for Isaac, and it had only gotten as far as showing lines of wrapped text.  It didn't even know how to deal with text that was too long for the box.  Hell, it didn't even know how to _exit_ the dialogue and return to the game.

So when I got the final script, I went into a sort of mad panic, doing my best to tack on features in ways I wouldn't regret later and could maybe reuse.  I got pretty far, but when it became clear that we couldn't possibly have a finished product in time, I invoked my powers as jam coordinator and pushed the deadline back by 24 hours.  48 hours.  54⅓ hours.  Oh, well.

The [final product](https://eevee.itch.io/neon-phase) came out pretty well, modulo a couple release bugs, ahem.  I've been really impressed with itch.io, too — it has a _thousand_ twiddles, which makes me very happy, plus graphs of how many people have been playing our game and how they found it!  Super cool.


## Lessons learned

Ah, yes.  Here's that sweet postmortem content you computer people crave.

### Don't leave debug code in

There's a fairly long optional quest in the game that takes a good few minutes to complete, even if you teleport everywhere instantly.  (Ahem.)  Finishing the quest kicks off a unique cutscene that involves a decent bit of crappy code I wrote at the last minute.  I needed to test it a lot.  So, naturally, I added a dummy rule to the beginning of the relevant NPC's dialogue that just skips right to the end.

I forgot to delete that rule before we released.

Whoops!

The game even _has_ a debug mode, so I could've easily made the rule only work then.  I didn't, and it possibly spoiled the whole sidequest for a couple dozen people.  My bad.

### Try your game at other framerates

The other game-breaking bug we had in the beginning was that some people couldn't make jumps.  For some, it was only when indoors; for others, it was all the time.  The common thread was...  low framerates.

Why does this matter?  Well!  When you jump, your upwards velocity is changed to a specific value, calculated to make your jump height slightly more than two tiles.  The problem is, gravity is applied _after_ you get jump velocity but _before_ you actually move.  It looks like this:

```lua
self.velocity = self.velocity + gravity * dt
```

Reasonable, right?  Gravity is acceleration, so you multiply it by the amount of time that's passed to get the change to velocity.

Ah...  but if your framerate is low, then `dt` will be relatively large, and gravity will eat away a relatively large chunk of your upwards velocity.  On the frame you jump, this effectively reduces your initial jump speed.  If your framerate is low _enough_, you'll never be able to jump as high as intended.

One obvious fix would be to rearrange the order things happen, so gravity doesn't come between jumping and movement.  I was wary of doing this as an emergency fix, though, because it would've taken a bit of rearchitecturing and I wasn't sure about the side effects.  So instead, I made a fix that's worth having anyway: when the framerate is too long, I slice up `dt` and do multiple rounds of updating.  Now even if the game _draws_ slowly, it plays at the right speed.

This was really easy to discover once I knew to look; all I had to do was add a `sleep()` in the update or draw loops to artificially lower the framerate.  I even found a second bug, which was that you _move_ slowly at low framerates — much like with jumping, your walk speed is capped at a maximum, then friction lowers it, then you actually move.

I _also_ had problems with framerates that were too _high_, which took me completely by surprise.  Your little companion flips out and jitters all over the place or even gets stuck, and jumping just plain doesn't work most of the time.  The problems here were much simpler.  I was needlessly rounding Chip's position to the nearest pixel, so if `dt` was very small, Chip would only try to move a fraction of a pixel per frame and never get anywhere; I fixed that by simply not rounding.

The issue with jumping needs a little backstory.  One of the problems with sloped terrain is that when you walk up a slope and reach the _top_, your momentum is still carrying you along the path of the slope, i.e. upwards.  I had a lot of problems with launching right off the top of even a fairly shallow hill; it looked goofy and amateurish.  My terrible solution was: if you started out on the ground, then after moving, _try_ to move a short distance straight down.  If you _can't_, because something (presumably the ground) is in the way, then you probably just went over a short bump; move as far as you can downwards so you stick to the ground.  If you _can_ move downwards, you just went over a ledge, so _abort_ the movement and let gravity take its course next frame.

The problem was that I used a fixed (arbitrary) distance for this ground test.  For very short `dt`, the distance you moved upwards when jumping was _less than_ the distance I then tried dragging you back down to see if you should stay on the ground.  The easy fix was to scale the test distance with `dt`.

Of course, if you're jumping, obviously you don't _want_ to stay on the ground, so I shouldn't do this test at all.  But jumping is an active thing, and staying grounded is currently a passive thing (but shouldn't be, since it emulates _walking_ rather than _sliding_), and again I didn't want to start messing with physics guts _after_ release.  I'll be cleaning a few things up for the next game, I'm sure.

This _also_ turned out to be easy to see once I knew to look — I just turned off vsync, and my framerate shot up to 200+.


### Quadratic behavior is bad

The low framerate issue wouldn't have been _quite_ so bad, except for a teeny tiny problem with indoors.  I'd accidentally left a loop in when refactoring, so instead of merely drawing every indoor actor each frame, I was drawing every indoor actor _for every indoor actor_ each frame.  I think that worked out to 7225 draws instead of 85.  (I don't skip drawing for offscreen actors yet.)  _Our_ computers are pretty beefy, so I never noticed.  Our one playtester did comment at the eleventh hour that the framerate dipped very slightly while indoors, but I assumed this was just because indoors requires more drawing than outdoors (since it's drawn right on top of outdoors) and didn't investiage.

Of course, if you play on a less powerful machine, the difference will be rather more noticeable.  Oops.


### Just Do It

My collision detection relies on the [separating axis theorem](https://en.wikipedia.org/wiki/Hyperplane_separation_theorem), which only works for convex polygons.  (Convex polygons are ones that have no "dents" in them — you could wrap a rubber band around one and it would lie snug along each face.)  The map Mel drew has rolling terrain and caverns with ceilings, which naturally lead to a lot of concave polygons.  (Concave polygons are not convex.  They have caves!)

I must've spent a good few hours drawing collision polygons on top of the map, manually eyeballing the terrain and cutting it up into only convex polygons.

Eventually I got so tired of this that I threw up my hands and added support for concave polygons.

It took me, like, two minutes.  Not only does LÖVE have a built-in function for cutting a polygon into triangles (which are always convex), it also has a function for detecting whether a polygon is convex.  I already had support for objects consisting of multiple shapes, so all I had to do was plug these things into each other.

Collision probably would've taken much less time if I'd just done that in the first place.


### Delete that old code, or maybe not

One of the very first players reported that they'd managed to crash the game right off the bat.  It didn't take long to realize it was because they'd pressed `Q`, which isn't actually used in NEON PHASE.  It _is_ used in Isaac's Descent HD, to scroll through the inventory...  but NEON PHASE doesn't _use_ that inventory, and I'd left in the code for handling the keypress, so the game simply crashed.

(This is Lua, so when I say "crash", I mean "showed a stack trace and refused to play any more".  Slightly better, but only so much.)

So, maybe delete that old code.

Or, wait, maybe don't.  When I removed the debugging sequence break just after release, I also deleted the code for the `Q` key...  and, in a rush, _also_ deleted the code for handling the `E` key, which _is_ used in NEON PHASE.  Rather heavily.  Like, for everything.  Dammit.

Maybe just play the game before issuing emergency releases?  Nah.


### Melding styles is easier than you'd think

When I look at the whole map overall, it's hilarious to me how much the part I designed sticks out.  It's built out of tiles and consists of one large puzzle, whereas the rest of the game is as untiled as you can get and mostly revolves around talking to people.

And yet I don't think anyone has noticed.  It's just one part of the game with a thing you do.  The rest of the game may not have a bunch of wiring puzzles, but enough loose wires are lying around to make them seem fitting.  The tiles Mel gave me are good and varied enough that they don't _look_ like tiles; they just look like they were deliberately made more square for aesthetic or story reasons.

I drew a few of the tiles and edited a few others.  Most of the dialogue was written by Mel, but a couple lines that people really like were my own, completely impromptu, invention.  No one seems to have noticed.  It's all one game.  We didn't sit down and have a meeting about the style or how to keep it cohesive; I just did stuff when I felt like it, and I naturally took inspiration from what was already there.


### People will pay for things if you ask them to

itch.io does something really interesting.

Anything you download is presented as a _purchase_.  You are absolutely welcome to sell things for free, but rather than being an instant download, itch.io treats this as a case of _buying for zero dollars_.

Why do that?  Well, because you are always free to pay _more_ for something you buy on itch, and [the purchase dialog](https://itch.io/docs/creators/how-buying-works#the-purchase-dialog) has handy buttons for adding a tip.

It turns out that, when presented with a dialog that offers a way to pay money for a free thing, an awful lot of people...  paid money!  Over a hundred people chipped in a few bucks for our _free game_, just because itch offered them a button to do so.  The vast majority of them paid one of itch's preset amounts.  I'm totally blown away; I knew abstractly that this was _possible_, but I didn't really expect it to happen.  I've never actually sold anything before, either.  This is amazing.

Now, granted, we _do_ offer bonuses (concept art and the OST) if you pay $2 or more, at Mel's request.  But consider that I also put my two PICO-8 games on itch, and those have an interesting difference: they're played in-browser and load automatically right in the page.  Instead of a payment dialog, there's a "support this game" button below the game.  They're older games that most of my audience has probably played already, but they still got a few hundred views between them.  And the number of purchases?

Zero.

I'm not trying to criticize or guilt anyone here!  I release stuff for free because I want it to be free.  I'm just genuinely amazed by how effective itch's download workflow seems to be.  The buttons for chipping in are a natural part of the process of _something you're already doing_, so "I might as well" kicks in.  I've done this myself — I paid for the free [m5x7](https://managore.itch.io/m5x7) font I used in NEON PHASE.  But something played in-browser is already there, and it takes a much stronger impulse to go out of your way to _initiate_ the process of supporting the game.

Anyway, this is definitely encouraging me to make more things.  I'll probably put my book on itch when I finish it, too.


## Also, my book

Speaking of!

If you remember, I've been writing a book about game development.  Literally, a book _about_ game development — the concept was that I build some games on various free platforms, then write about what I did and how I did it.  Game development as a story, rather than a lecture.

I've hit a bit of a problem with it, and that problem is with my "real" games — i.e., the ones I didn't make for the sake of the book.  Writing about Isaac's Descent requires first explaining how the engine came about, which requires reconstructing how I wrote Under Construction, and now we're at two games' worth of stuff even before you consider the whole _writing a collision engine_ thing.

Isaac's Descent HD is posed to have exactly the same problem: it takes a detour through the development of NEON PHASE, so I should talk about that too in some detail.

Both of these games are huge and complex tales already, far too long for a single "chapter", and I'd already been worrying that the book would be too long.

So!  I'm adjusting the idea slightly.  Instead of writing about making a bunch of "artificial" games that I make solely for the sake of writing about the experience...  I'm cutting it down to just Isaac's Descent, HD, and the other games in their lineage.  That's already half a dozen games across two platforms, and I think they offer more than enough opportunity to say everything I want.

The overall idea of "talk about making something" is ultimately the same, but I like this refocusing a lot more.  It feels a little more genuine, too.

Guess I've got a bit of editing to do!


## And, finally

You should try out [the other games](https://itch.io/jam/games-made-quick/entries) people made for my jam!  I can't believe a Twitter joke somehow caused _more than forty_ games to come into existence that otherwise would not have.  I've been busy with NEON PHASE followup stuff (like writing this post) and have only barely scratched the surface so far, but I do intend to play every game that was submitted!
