title: fox flux, three years later
date: 2020-08-04 13:50
category: dev
tags: tech, gamedev

I'm working on a video game!  Like, a serious one.

## The past

I wrote [the original game](https://eevee.itch.io/fox-flux) (very slightly NSFW) for my own "horny" game jam, [Strawberry Jam](https://itch.io/jam/strawberry-jam) (more likely to be NSFW), way back in February 2017.

You play as Lexy, my shameless Floraverse self-insert, who owns an enchanted collar that (among other things) makes her basically indestructible and allows her to easy to transform into...  whatever, given some kind of sensible trigger.  And then you do some puzzle-platforming to collect "strawberry hearts" and gain access to new areas, much of which (surprise!) involves getting turned into things.

For example, this chain-link fence blocks you:

<div class="prose-full-illustration">
<img src="{static}/dev/media/fox-flux/jam-example-fence.png" alt="Screenshot of the player being stuck on one side of a fence">
</div>

But if you let that green blob in the grass turn you into slime, you can walk right through it.

<div class="prose-full-illustration">
<img src="{static}/dev/media/fox-flux/jam-example-fence-slime.png" alt="Screenshot of the same area, but the player is now green slime and free to pass through the fence">
</div>

There are also spikes, which you get stuck on if you land on them...  but slime can walk right through them, glass can stand on top of them, and stone outright destroys them.  And so on.  As a jam game, it's not very expansive, but many of the puzzle elements interact differently with many of the handful of Lexy variants, which provided enough potential to make eight levels.


### Post-jam

The jam game was rough, but I really liked the concept and wanted to expand on it.  I spent a good chunk of the summer of 2017 on it, but it was a struggle.  I was still fairly new to pretty much every aspect of actually creating a game — I'd only been drawing for two years, I'd sometimes hit big gaps in the design with no idea how to fill them, and I wasn't yet entirely comfortable with complex physics or shaders.  The art in particular was a huge problem; it took me a long time to produce sprites that I was only passably happy with.  My spouse Ash is an artist, and we've made several games together where they produced all the art, but this was _my_ idea and I was determined to draw it myself.

Then 2018 hit, which was a whole entire mess, and I didn't really touch fox flux at all for over a year.  I made a couple of other games with Ash, some finished, some not, and kept drawing intermittently.

I returned to fox flux for the middle of 2019, and decided...  I'm not sure what I decided, exactly.  I guess I'd gotten better at all the things that had been difficult for me before, so I set about trying to improve every aspect of the game at once.

- I realized the (many, _many_) improved sprites I'd drawn in 2017 were not actually very good, and drew a new Lexy design from scratch that absolutely blew me away...  which meant throwing away all the existing art.

- I'd come up with a few new things for Lexy to turn into, each of which altered her behavior pretty significantly, and her code was becoming a spaghetti disaster.  So I spent some time completely refactoring actors into bags of components, which I was unsure about until very recently and which ended up breaking pretty much every single object in the game, sometimes in subtle ways.

- I decided to add water, which unraveled into a whole pile of decisions and problems.

- I tried to make consistent or interesting physics for pushing things (e.g. wooden crates), and that became a _nightmare_.  I easily spent weeks on this, trapped in a cycle of finding some edge case that couldn't be fixed without considerably expanding what I was simulating, struggling to do that expansion while keeping all the basic stuff working, and then finding a new and different edge case.

Did I mention that I tried to do all of these things at the same time, while _also_ trying to nail down the design of a game that's naturally prone to a combinatoric explosion of interactions?

At a certain point it just felt hopeless.  I'd poured easily over a year into this game, and all I had to show for it was a jumbled pile of stuff that didn't work, strewn about a couple test maps that didn't even contain any puzzles.


## The present

I don't know what happened, exactly.  I'd given up on the heavily-simulated push physics last year, at least, so that wasn't so much of a concern any more.  But I still had a mess.  I'd long since written `git status` off as unusable.

Until this past month, when I sat down and just started powering through the mess.  One by one, I fixed the serious breakages that the component refactor had caused.  I dedicated a day or two just to figuring out water physics, put a little more thought into it, and ended up with something that looks and plays quite nicely.  I finished redrawing basic Lexy, and even added frames I hadn't had before.

I think the difference was...  fear.  I'd previously hesitated _so much_, both in the art and the gnarlier code.  It was such a struggle to get something working _at all_ that changing it in any way was terrifying — what if I broke it and couldn't even get it back to how it'd been?

I don't know how to describe exactly how this felt, and I also don't know how to explain what changed.  It was like a switch flipped.  I think it started when I drew new dirt tiles, and it didn't even take that long, and I _loved_ them.  I've always had a hard time drawing terrain, and for once I just sat down and did it and it came out well and it looked like _mine_, like my style, which was a thing I hadn't even really grasped I have before.  After that I just cranked out a mountain of new sprite art, faster and better than anything I'd done before.  Like I'd been accumulating XP over the past few years and just now decided to spend it all on levelling up.

Over the past six weeks, I have:

- Redesigned the terrain
- Vastly improved the palette
- Completely finished redrawing Lexy
- Redesigned the HUD
- Mocked up a new dialogue layout
- Drawn a new font
- Drawn and implemented new consistent level entrances
- Animated a treasure chest opening cutscene
- Animated getting a key
- Added a completely new tally at the end of a level
- Added transitions for entering and leaving levels
- Added swimming behavior
- Redrawn the old gecko as a much more visible bananalizard
- Animated the hearts and several other pickups
- Ported the original forest levels to use all the new stuff
- I don't even know there has been just so much

Just look at the style evolution!  God damn.

<div class="prose-full-illustration">
<img src="{static}/dev/media/fox-flux/style-evolution.png" alt="Three versions of Lexy in dirt tiles; over time, the style becomes more colorful and relies on stronger shapes and silhouettes">
</div>

Here's that same level from above:

<div class="prose-full-illustration">
<img src="{static}/dev/media/fox-flux/deluxe-example-fence.png" alt="Slime Lexy once again passing freely through the fence, but using newer assets">
</div>

A lot of the last few weeks went towards level transitions, which previously...  kind of worked.  They were always a hasty jam hack that I never liked; there was a quick screen fade when going through a door, there was barely any notion of being "in a level" vs not, and the game even counted the fucking hearts in a level on the fly the first time you entered it.  It was all very silly.

_But now_ (please pardon the occasional frame drops from my screen recorder):

<div class="prose-full-illustration">
<img src="{static}/dev/media/fox-flux/level-loop.gif" alt="GIF of Lexy entering a level with a transition, collecting candy, exiting with another transition, and seeing the level tally">
</div>

I finally feel like I'm making some real progress.  I finally feel like this could be something I take seriously, that it could be a _real game_, something more than half an hour long.  At some point it just became an absolute joy to look at and run around in.

### The idea

The basic concept is the same, but I want to add some structure to it.  The jam game was four single-room levels you could tackle in any order without much guidance, then another set of the same.  Which is fine, but doesn't give me much wiggle room in the design.

In the full game, levels will contain not just hearts, but also a treasure (a la Wario Land 3), some amount of candy (usable at the _shop_ to buy [_things_ of _some description_](https://twitter.com/foxfluxDELUXE/status/1289626941637550083)), and an explicit exit.  The overworld will function a bit more like a world map, and though you'll still need to collect N hearts to get to the next zone, there may sometimes be obstacles that can only be overcome by finding the right treasure in a level.

I also intend to give Lexy some active abilities, for example this blown kiss (recorded with older art) that can toggle pink objects between two states:

<div class="prose-full-illustration">
<img src="{static}/dev/media/fox-flux/kiss.gif" alt="Lexy blows a kiss towards a pink brick wall, which changes it into a pink grating">
</div>

I even have a plot in mind!  The jam game had only a teeny tiny one.


## The future

Ash is currently busy with their own game, so I think this is gonna be The Thing I Do for a while.  To that end, I'm in the middle of setting up some infrastructure:

- A dedicated [Twitter account](https://twitter.com/foxfluxDELUXE)
- An [itch.io page](https://eevee.itch.io/fox-flux-deluxe)
- A [Discord channel](https://discord.gg/8aBpBQW)

Also, I recently created a _secret_ Discord channel on the same server, where I intend to do planning and design work that I'm not ready to make public yet!  Spoilers will abound, but if you're interested and okay with that, you can get in by pledging at least $4 on [Patreon](https://www.patreon.com/eevee) and letting me know to give you the role.  (I don't use Patreon's native Discord integration because it does rude things like forcibly rejoin you to the server even if you manually leave.)

### Specific priorities

I'd like to finish porting the old levels over to new artwork, the new level infrastructure, etc.  It'd make for a nice little Patreon demo or something, it gives me a milestone with pretty clear goals, and it'll leave me with at least a small palette of puzzle elements that I _know_ work correctly.

I'd like to write about what I'm doing sometimes on this dang blog.  I've found that structured writing is really, really, _really_ hard when my head is a mess, and it has been extremely a mess for the last two and a half years (sorry), but jotting down what I'm already doing should be much easier than the more elaborate posts I've written, which need research and tooling and whatnot.

I have a good handful of puzzle elements — some of which even work — and a bunch of ideas for more, but I haven't actually tried _building levels_ since I made the original game!  That's kind of the important part, so I'd love to do some of it now that the dust is finally settling.

I still have some design decisions to make, though they're getting trickier since I've already decided all the easy stuff.  But I'll save that for the generous folks who give me four dollars, I guess.

### The elephant in the room

So.  As I mentioned at the beginning, this game was originally made for a "horny" game jam.  Given that it's mostly platforming, you might be wondering why that is.  I already feel like I'm crossing the streams somehow by even mentioning this on this blog, so I'll try very hard not to get TMI here.

I have a foot in "TF" (transformation) kink circles, and one thing that's always struck me about that subculture is how much of it is completely non-sexual.  You can find no end of artwork of, say, someone being turned into one of those inflatable pooltoys — where both the artist and the audience are obviously having a good time with it — yet with no hint of sexual elements whatsoever.  It's a form of sexuality that doesn't need to be sexual at all.

I started Strawberry Jam because I wanted to see some adult games that were more creative with their gameplay.  Much of the genre consists of otherwise regular games that occasionally show you some explicit artwork, and while that's a perfectly fine way to design a game, I felt that the medium surely had more potential.  It turns out that a non-sexual fantasy kink works wonders as a gameplay element; rather than just giving you a picture, the game takes a concept and has you _experience it yourself_, even figure out by experimentation how it's altered the way you interact with the world.

This puts me in a slightly awkward position.  I do, genuinely _and platonically_, love these kinds of gameplay themes!  I adore changes in how you perceive or interact with a world — the dark world in Metroid Prime 2, the time reversal in Braid, the "dimension" swapping in Quantum Conundrum, etc.  I think this is a great concept that anyone can have a good time with, and I feel like this game is a love letter to the Wario Land series.

At the same time, I do _also_ appreciate the kink inspiration.  Even Lexy's collar was originally conceived as a gimmick I could use for drawing adult artwork.  The jam game contains a lot of suggestive dialogue, since Lexy herself also appreciates the kink aspect.  And that was a lot of fun to write, and I'm sure it enhanced the experience for other folks with similar leanings.

But this is such a good concept that I want it to be playable as _just_ a regular puzzle-platformer as well.  I think it would have fairly broad appeal, and I don't want to hamstring myself by totally fucking weirding people out when it dawns on them that "oh the dev is kinda Into This huh".  And yet I don't want to completely sterilize the game, either, because...  well, ultimately, it's my game and I _like_ the suggestive parts.

This is a tough line to draw, and I'm not yet sure how to do it.  I've considered just making alternative dialogue that you can opt into when you start the game, but given that Lexy already speaks differently depending on what form she's in, I have no idea how feasible that is.

I don't know how to gauge this.  I've always been up to my armpits in the side of the internet that just posts porn and talks about sexuality casually, whereas I'm dimly aware that most people see sexuality as this completely distinct part of life that you hide in a small box, far away from the eyes of polite society.  But maybe I'm overestimating that?  Does anyone actually care if the protagonist of a game comments "hey this is hot" about something weird but innocuous?

Or maybe that's exactly where the line is.  I remember Nier: Automata, a game that is all too happy to show off the protagonist's immaculately-rendered ass, which is clearly meant for the enjoyment of both the creator and the players.  But nobody comments on it _within the game_, which makes it seem incidental, somehow.  I can't explain why that is, and it feels slightly dishonest to me.

Am I overthinking this?  If you're _not_ involved in any kind of kink circles and played the original jam game, I'm curious to hear how it read to you.  Was it at all uncomfortable, like perhaps the game was expecting you to heavily empathize with a feeling you don't share at all?  Or does putting that feeling on a _character_, rather than aiming it at the human player, make it something you can easily shrug off?  The full game will have more stuff going on, so there should be lots more dialogue that _isn't_ solely about Lexy's feelings, if that helps.

----

Hm, I thought I would have more to say here!  I have a lot of ideas, but only a handful of them are implemented yet, and I guess it's hard to show what a game will be like before most of it works.

I hope this is enough to whet some appetites, at least!  I haven't been excited like this about _anything_ in far too long.
