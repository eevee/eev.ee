title: Making Mario
date: 2015-09-20 23:45
category: essay
tags: game dev

I bought [Super Mario Maker](https://en.wikipedia.org/wiki/Super_Mario_Maker) a few days ago.  I was a little iffy on blowing $60 on a level editor, but I really like level editors, so here we are.

<!-- more -->

I've always liked level editors.  They appeal the same way programming does: here's a blank slate; here's a bunch of individual components that may interact in interesting ways; see what you can come up with.  In many cases level editors express logic via special invisible node objects, which really _is_ programming.

I didn't do much with it at first.  I played a few demo levels, but the need to spam blocks (or make a lot of very bland levels) to unlock all the tools was a bit of a turn-off.

My mind was really on Doom mapping, for whatever reason.  I've been distantly orbiting the [ZDoom](http://zdoom.org/) world on and off for over a decade, making the occasional wiki edit or giving the odd mapping tip here and there.  But in all that time I've never made a _completed_ map.  I'm pretty sure that's true even for the loosest possible definition of "completed", which is "has an exit".

I made some tweets reflecting on my attempts to build worlds, and realized I have much the same problem as I do in other spheres.  I run out of obvious ideas for the big picture, which I hate, because it's a problem with no fixed solution and no reliable approach for finding one.  So I naturally drift towards fiddling with small details, which I _do_ still have ideas for.

This is particularly bad with Doom because it has actual maps, not just tiles.  If I put a crate in the corner of a room flush with the walls, I can't easily move it later once I've figured out more about the general map layout — the walls of the room and the edges of the crate are the _same line_ as far as the map format is concerned.

Someone suggested that I use Mario Maker to practice overall world design.  I thought that was a pretty good idea.


## I built some levels

I started a [gist](https://gist.github.com/eevee/45e08c55e1d4ea89665c) for keeping track of them, though this strikes me as the kind of thing that _this, my personal website_ ought to be able to handle, and I'm gonna beat on Pelican a bit sometime to see if I can make that work.

The first one was inspired by the realization that the two parts of a level (joined by pipes) can use _any_ themes, and I thought it would be interesting to start with a fairly simple-looking grassy level that then transitions to something entirely unexpected.  I ended up building an airship and filling it with, well, very airshipesque traps.

Rather than make it linear — go down pipe A, traverse airship, return through pipe B — I decided to make the player _circle_ the airship and return the way they came.  This meant that something on the airship had to make it possible to reach the goal when it wasn't before, and there are only so many ways to do that with what's available, so I went with giving the player a feather and making them high-jump up to the goal.

I somewhat regret this decision, since it's kind of mean to make a level unbeatable if the player loses a particular powerup.  I mean, part of the point of _having_ a powerup is that you can survive another hit.  (Maybe I should've given the player a helmet or shoe as well.)  It was extra mean since I'd originally intended for the player to _backtrack_ all the way back through the airship, but I discovered that you could skip all that with a single fairly easy jump, so I let that be.

I've played 100 Mario Challenge a few times, which subjects you to a random selection of uploaded levels, and I've gotten the faint impression that many level authors deliberately try to _stop_ players from using creative alternate routes.  I think that's really against the spirit of Mario, and certainly against the spirit of many of the original levels — how many entire _games_ can you skip with a feather?  Or, christ, a P-Wing?  Forcing players through your single blessed path does not a grand level make.

Also, being forced to beat my own course before I could upload it was _fantastic_ — I went back and edited it so many times after I'd initially intended to publish it.  Some of the pain points I discovered I never would've thought of just by looking at the map (or even playtesting from the middle) — for example, thrown wrenches blend into a _lot_ of backgrounds really well, and I removed a few moles entirely because they were causing problems.

The only other thing I regret is that the level is kind of cramped in places, which makes for some jumps that are more awkward than they need to be.  There's not really any good reason for this, and it's a shame when the intro part is very open.  Not leaving enough breathing room (whitespace?) seems to be a fairly common mistake: I see it in a lot of uploaded Mario levels, and I know I have to try hard to resist making every hallway 64 units wide (about the width of the player) in Doom maps.

---

The second one was a Boo house, because I like Boo houses.  They're generally twisty and confusing and weird.  I also put it in SMB style, which was kind of interesting since that game never had Boo houses of its own; all the music and most of the graphics were created specifically for this game.

The first part ends with the classic "ha ha this isn't the real exit", along with a light hint that may have been a bit too light.  The second part has multiple different areas that look identical, along with a subtle hint as to how to escape.

It's always tricky leaving hints for players.  I can't very well tell what other people will catch on to, and the whole point of a puzzle is for everyone else to actually solve it.  In the end I added an alternate route that I thought players would likely discover if they missed the hint and flailed around wildly.

The main problem with this level, I think, is the Boo circles.  I just had a hell of a time placing them well, and I think in a couple places they force trickier jumps than I'd intended.  I still like it, but I think the unintended difficulty detracts from the theme too much.

Incidentally, I don't think difficulty is fun.  _Challenge_ is fun, and that implies something that you can learn to overcome.  Expert mode of 100 Mario Challenge (which I believe picks levels with very low completion rates) produces utterly _nasty_ levels, requiring numerous pixel-perfect jumps in sequence, or incredible reflexes for dodging a dozen things on the screen at once, or wall-jumping through an entire level.  Most of the levels don't feel like something I could do if I were slightly better at platforming, but something designed to make me fail so the level designer can pat themselves on the back and chuckle about how "hard" they made their level.  Well, congratulations, but if all you wanted was to stop me from winning, you could've just built a wall in front of the flag and called it a day.  (I ran across a level that literally did this.  I beat it anyway and left a comment spoiling it.  Fuck that noise.)

---

My third level is the first one I feel was actually successful.  It's fairly straightforward platforming, except that there are several pipes that take you to an identical area where all the enemies are double-size.  There are several puzzles throughout that are most easily solved by switching back and forth between the big and little worlds.

I had to pay a _lot_ of attention to decorations here, though it was less tedious than you might expect.  The background decorations (bushes, small trees, flowers, etc.) aren't actually objects in their own right; they sprout from ground tiles when you place them, _at random_.  Thankfully, you can copy decorated ground tiles around.  So after I'd finished the level, I had to create a little "palette" of the decorations in both areas, and toggle back and forth making sure the same decorations were in the same places.  (You can't copy between areas, alas.)

Though I'd intended that the player _has_ to switch back and forth several times, _every single puzzle_ can actually be completed in either area.  I really didn't want to end up with an arduously difficult level again, so I'm going to say this is a good thing.

Overall I think this was a pretty successful exercise, and I'm going to keep playing around to see what I can come up with.  I haven't run into many uploaded levels that _feel_ like Mario levels, just fun platforming and exploring, so I'd like to try improving on that.

I did go back to Doom mapping along the way, and I managed to get a map's general layout from 20% to 70% done, after it had haunted me for ages.  I don't know if I can ascribe that to Mario Maker, but I'd like to think working with simpler constraints shook a few cobwebs loose.


## I miss some tools

Super Mario Maker is a great tool, don't get me wrong.  It has a good spread of objects that interact in neat ways, a pretty friendly editor, and some clever touches (like requiring you to beat your own level before you can upload it).

_But..._

I find myself left a little wanting.  The most blindingly obvious problem is that you can't actually recreate World 1–1 from any of the four games it emulates:

* Super Mario Bros. has one-way pipes and variable powerups (fire flower if you're super or better, otherwise a mushroom).
* Super Mario Bros. has a split pipe, black pipes, and four colors of semisolid platform.
* Super Mario World has a checkpoint, slopes, Yoshi coins, Rexes (the dragons), Banzai Bill (the screen-filling bullet), hint blocks, and a Chargin' Chuck (the football guys).
* New Super Mario Bros. U has a ridiculous title.  But it also sports a checkpoint, flying squirrels, acorn mushrooms, star coins, fake foreground, moving semisolid platforms, colored pipes, red coins, moving coins, a coin heaven theme, and more complex pipe connections.

The various Worlds 1-2 are missing yet more objects: infinite platform elevators from SMB, pink note blocks from SMB3, berries from SMW, tilted pipes and rotating platforms from NSMBU.

I'm not just nitpicking, or lamenting that no one can be super creative and recreate all the old levels.  I have _actual design concerns here_:

* There are very few **mechanisms** in the game right now, things the player can interact with to change the state of the level.  We've got P switches and vines, and that's really about all.  I miss the _track switches_ from SMW, which gave the player something to actually do while riding a track.  The _blue warp doors_ from SMW only appeared when a P switch was active, and that helped a few Boo houses feel all the more bizarre.  _Control coins_ and _silver coins_ interacted with P switches in interesting ways too.  _Looping levels_ from several of the castles in SMB were mean, but made for cute simple puzzles.  SMW's _switch houses_ spanned levels, granted, but they could be emulated here to alter a level.

* It's hard to **reward** players at the moment.  There are no _Coin Heavens_ — there's no _coin heaven theme_, _vines_ can't be climbed off the top of the screen as in SMB, and the _pink note blocks_ are just for playing music.  There are no _Yoshi coins_ from SMW nor _star coins_ from NSMBU, so nothing to collect.  You can give the player coins and 1-Ups, of course, but those don't feel very rewarding when they rarely persist and when bunches of levels drown you in 1-Ups anyway.

    This is proving to be a little frustrating for me, since I absolutely love designing secrets but have very little to offer the player as a reward.  I've been using 1-Ups just because they're an obvious indicator, but jeez.  Hurrah, here's yet another 1-Up.  You did it.  There are no real _secret exits_, no _warp zones_, no _key and keyhole_, no _3-Up Moon_, no _bonus block_.

    You can't even reward the player for clearing a difficult part by giving them a _checkpoint_, since those aren't in either.  As a designer this is actually fairly limiting, since if you have more than a couple of tricky spots, chances are you're just going to make the player sick of your level.

* **Movement** is largely restricted to jumping, flying, and standing on platforms.  Which is a shame, because Mario is all _about_ movement, and new Mario series tend to revolve around giving the player new ways to move around.  SMB3 added _slopes_ and sliding, _water_ outside of water levels.  SMW had the _triangle block_ that let you run up walls, the _fences_ in castles that you could climb on and punch Koopas through, _ropes_ and _buzzsaws_ for traversing tracks, the _Power Balloon_, and _Yoshi's wings_.  NSMBU has a lot of various _rotating blocks_ and _moving semisolid platforms_.  Even the _platforms_ and _skull rafts_ have limited range you can't change, and you can't make _rotating platforms_ or  _multi-block winged platforms_, which has led to a lot of clumsily overlapping objects in a lot of levels I've seen.

* **Decorations** are hard to wrangle!  All we really have to work with are three kinds of decorations on ground tiles, which show up whenever they want.  You can use semisolid platforms to kind of fake a background, but they are _really_ cumbersome to work with: you can't directly place objects on top of a semisolid platform, because that's interpreted as moving the platform.  And that's it.  Anything else requires some really creative use of objects intended for other purposes.

    Surprising omissions include the _castle background_ from World 8 of SMB, and of course the large bushes from SMW.

* There are a lot of **enemies**, and yet rather a lot of them just walk back and forth along the ground.  I'd like a little more variety, like the _angry sun_, _Roto-disc_, _Pile Driver Micro-Goomba_ (the tiny monsters that hide in blocks), _Chargin' Chuck_, _Pokey_, _Eerie_, _Blargg_, and _Big Bertha_.

    Also, it's pretty tricky to make a boss battle that actually requires defeating a boss, rather than just going around it.  Would be nice if a monster could drop...  something...  when defeated?

* Some miscellaneous **mechanics** are altered or conspicuously missing.  Yoshi has no color-related powers — no fireballs, no flight, no earthquake.  No baby Yoshi, either.  You can jump over the goalposts in SMW levels.  Using Lakitu without trivially breaking a level is actually kind of hard, because there's no way to make Lakitu _not_ leave a cloud behind.  You can't spin jump on grinders.  The more I think about how all the games (save for SMB) actually worked, the more shallow Mario Maker seems in comparison.

* The **world itself** has some frustrating limitations.  The start and goal are completely fixed, and in fact you can't avoid having a seam between the starting point and the ground after it.  The vertical size constraints (two screens high) mean you can't make vertical cave levels, or paths that diverge too widely.  If you want to have separate underground areas, doing it _right_ means filling in at least 12 columns of solid blocks — which seriously eats into your limit of 2000 "environment" blocks.  You can only have water as a full area style, not as a small pond or running across the bottom to make a Big Bertha level.  Similarly, you can't mix styles in the same level, so you can't have a water/ground level like exist in SML2, and you can't have a ground/underground level like SMB3 World 1–5.  Doors can't go to the other area, pipes can't lead to the same area, and both doors and pipes must be symmetric two-way connections.

* And **browsing levels** could use a teeny bit of work — you can't easily offer a set of your own levels intended to be played as a single world, and I hear it's actually surprisingly difficult to find levels made by your friends?

So I really hope they update the game to add some more of these classic mechanics and lift a few of the restrictions.

And while they're at it, I wouldn't mind seeing the game list expanded to Super Mario Land 2: Six Golden Coins, which was my first Mario and has some unique touches like the bunny suit and blocks that can only be destroyed by fireballs.  Super Mario 3D World has a nice aesthetic, too, and a few interesting touches of its own (_cat suit_).

If you'd made or found any interesting levels, I would love to see them!  Gimme gimme.
