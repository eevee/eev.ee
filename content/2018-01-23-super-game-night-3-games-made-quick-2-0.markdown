title: SUPER game night 3: GAMES MADE QUICK??? 2.0
date: 2018-01-23 23:03
category: blog
tags: game night

[Game night](/everything/tags/game-night/) continues with a smorgasbord of games from my recent game jam, [GAMES MADE QUICK??? 2.0](https://itch.io/jam/games-made-quick-2)!

The idea was to make a game in only a week while watching AGDQ, as an alternative to doing absolutely nothing for a week while watching AGDQ.  (I didn't submit a game myself; I was chugging along on my Anise game, which isn't finished yet.)

I can't very well run a game jam and not play any of the games, so here's some of them in no particular order!  Enjoy!

*These are impressions, not reviews.  I try to avoid major/ending spoilers, but big plot points do tend to leave impressions.*

<!-- more -->

## Weather Quest, by timlmul

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/weather-quest.png" alt="">
</div>

<center>*short · rpg · jan 2017 · (lin)/mac/win · free on [itch](https://timlmul.itch.io/weather-quest) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/214063)*</center>

Weather Quest is its author's first shipped game, written completely from scratch (the only vendored code is a micro OO base).  It's very short, but as someone who has also written LÖVE games completely from scratch, I can attest that producing something this game-like in a week is a _fucking miracle_.  Bravo!

For reference, a week into my first foray, I think I was probably still writing my own Tiled importer like an idiot.

Only Mac and Windows builds are on itch, but it's a LÖVE game, so Linux folks can just grab a zip from [GitHub](https://github.com/timothymullen/weatherquest) and throw that at `love`.

**FINAL SCORE:** ⛅☔☀


## Pancake Numbers Simulator, by AnorakThePrimordial

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/pancake-numbers-simulator.png" alt="">
</div>

<center>*short · sim · jan 2017 · lin/mac/win · free on [itch](https://anoraktheprimordial.itch.io/pancake-numbers-simulator) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/213239)*</center>

Given a stack of N pancakes (of all different sizes and in no particular order), the Nth pancake number is the _most_ flips you could possibly need to sort the pancakes in order with the smallest on top.  A "flip" is sticking a spatula under one of the pancakes and flipping the whole sub-stack over.  There's, ah, [a video](https://www.youtube.com/watch?v=m3drS_8BpU0) embedded on the game page with some visuals.

Anyway, this game lets you simulate sorting a stack via pancake flipping, which is surprisingly satisfying!  I enjoy cleaning up little simulated messes, such as…  incorrectly-sorted pancakes, I guess?

This probably doesn't work too well as a simulator for solving the _general_ problem — you'd have to find an optimal solution for _every_ permutation of N pancakes to be sure you were right.  But it's a nice interactive illustration of the problem, and if you know the pancake number for your stack size of choice (which I wish the game told you — for seven pancakes, it's 8), then trying to restore a stack in that many moves makes for a nice quick puzzle.

**FINAL SCORE:** $\frac{18}{11}$


## Framed Animals, by chridd

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/framed-animals.png" alt="">
</div>

<center>*short · metroidvania · jan 2017 · web/win · free on [itch](https://chridd.itch.io/framed-animals) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/214158)*</center>

The concept here was to _kill the frames, save the animals_, which is a delightfully literal riff on a long-running AGDQ/SGDQ donation incentive — people vote with their dollars to decide whether Super Metroid speedrunners go out of their way to free the critters who show you how to walljump and shinespark.  Super Metroid didn't have a showing at this year's AGDQ, and so we have this game instead.

It's rough, but clever, and I got really into it pretty quickly — each animal you save gives you a new ability (in true Metroid style), and you get to test that ability out by playing _as the animal_, with only that ability and no others, to get yourself back to the most recent save point.

I did, tragically, manage to get myself stuck near what I think was about to be the end of the game, so some of the animals will remain framed forever.  What an unsatisfying conclusion.

Gravity feels a little high given the size of the screen, and like most tile-less platformers, there's not really any way to gauge how high or long your jump is before you leap.  But I'm only even nitpicking because I think this is a great idea and I hope the author really _does_ keep working on it.

**FINAL SCORE:** $136,596.69


## Battle 4 Glory, by Storyteller Games

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/battle-4-glory.png" alt="">
</div>

<center>*short · fighter · jan 2017 · win · free on [itch](https://storytellergames.itch.io/battle-4-glory) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/214091)*</center>

This is a Smash Bros-style brawler, complete with the four players, the 2D play area in a 3D world, and the random stage obstacles showing up.  I do like the Smash style, despite not otherwise being a fan of fighting games, so it's nice to see another game chase that aesthetic.

Alas, that's about as far as it got — which is pretty far for a week of work!  I don't know what more to say, though.  The environments are neat, but unless I'm missing something, the only actions at your disposal are jumping and very weak melee attacks.  I did have a good few minutes of fun fruitlessly mashing myself against the bumbling bots, as you can see.

**FINAL SCORE:** 300%


## Icnaluferu Guild, Year Sixteen, by CHz

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/icnaluferu-guild-year-sixteen.png" alt="">
</div>

<center>*short · adventure · jan 2017 · web · free on [itch](https://chz.itch.io/icnaluferu-guild-year-sixteen) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/213873)*</center>

Here we have the first of several games made with [bitsy](https://ledoux.itch.io/bitsy), a micro game making tool that basically only supports walking around, talking to people, and picking up items.

I tell you this because I think half of my appreciation for this game is in the ways it wriggled against those limits to emulate a Zelda-like dungeon crawler.  _Everything_ in here is totally fake, and you can't really understand just how fake unless you've tried to make something complicated with bitsy.

It's pretty good.  The dialogue is entertaining (the rest of your party develops distinct personalities solely through oneliners, somehow), the riffs on standard dungeon fare are charming, and the Link's Awakening-esque perspective walls around the edges of each room are fucking _glorious_.

**FINAL SCORE:** 2 bits


## The Lonely Tapes, by JTHomeslice

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/the-lonely-tapes.png" alt="">
</div>

<center>*short · rpg · jan 2017 · web · free on [itch](https://jthomeslice.itch.io/the-lonely-tapes) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/212755)*</center>

Another bitsy entry, this one sees you play as a Wal— sorry, a _JogDawg_, which has lost its cassette tapes and needs to go recover them!

(A _cassette tape_ is like a VHS, but for music.)

(A _VHS_ is—)

I have the sneaking suspicion that I missed out on some musical in-jokes, due to being uncultured swine.  I still enjoyed the game — it's always clear when someone is passionate about the thing they're writing about, and I could tell I was awash in that aura even if some of it went over my head.  You know you've done good if someone from way outside your sphere shows up and still has a good time.

**FINAL SCORE:** Nine…  Inch Nails?  They're a band, right?  God I don't know write your own damn joke


## Pirate Kitty-Quest, by TheKoolestKid

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/pirate-kitty-quest.png" alt="">
</div>

<center>*short · adventure · jan 2017 · win · free on [itch](https://finnrocket5.itch.io/pirate-kitty-quest) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/213885)*</center>

I completely forgot I'd even given "my birthday" and "my cat" as mostly-joking jam themes until I stumbled upon this incredible gem.  I don't think — let me just check here and — yeah no this person doesn't even follow me on Twitter.  I have no idea who they are?

BUT THEY MADE A GAME ABOUT ANISE AS A PIRATE, LOOKING FOR TREASURE

PIRATE.  ANISE

PIRATE ANISE!!!

This game wins the jam, hands down.  🏆

**FINAL SCORE:** Yarr, eight pieces o' eight


## CHIPS Mario, by NovaSquirrel

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/chips-mario.png" alt="">
</div>

<center>*short · platformer · jan 2017 · (lin/mac)/win · free on [itch](https://novasquirrel.itch.io/chips-mario) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/214130)*</center>

You see this?  This is _fucking witchcraft_.

This game is made with MegaZeux.  MegaZeux games look like [THIS](http://vault.digitalmzx.net/show.php?id=182).  Text-mode, bound to a grid, with two colors per cell.  That's all you get.

Until now, apparently??  The game is a tech demo of "unbound" sprites, which can be drawn on top of the character grid without being aligned to it.  And apparently have looser color restrictions.

The collision is a _little_ glitchy, which isn't surprising for a MegaZeux platformer; I had some fun interactions with platforms a couple times.  But hey, goddamn, it's free-moving Mario, in MegaZeux, what the hell.

(I'm looking at the most recently added games on [DigitalMZX](http://vault.digitalmzx.net/) now, and I notice that not only is this game in the first slot, but NovaSquirrel's MegaZeux entry for Strawberry Jam _last February_ is still in the seventh slot.  RIP, MegaZeux.  I'm surprised a major feature like this was even added if the community has largely evaporated?)

**FINAL SCORE:** n/a, disqualified for being probably summoned from the depths of Hell


## d!¢&lt; pic, by 573 Games

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/dick-pic.png" alt="">
</div>

<center>*short · story · jan 2017 · web · free on [itch](https://studio573games.itch.io/d-pic) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/212800)*</center>

This is a short story about not sending dick pics.  It's _very_ short, so I can't say much without spoiling it, but: you are generally prompted to either text something reasonable, or send a dick pic.  You should not send a dick pic.

It's a fascinating artifact, not because of the work itself, but because it's so terse that I genuinely can't tell what the author was even _going_ for.  And this is the kind of subject where the author was, surely, going for _something_.  Right?  But was it genuinely intended to be educational, or was it tongue-in-cheek about how some dudes still don't get it?  Or is it side-eying the player who clicks the obviously wrong option just for kicks, which is the same reason people do it for real?  Or is it commentary on how "send a dick pic" is a literal option for every response in a real conversation, too, and it's not that hard to just not do it — unless you are one of the kinds of people who just feels a _compulsion_ to try everything, anything, just because you can?  Or is it just a quick Twine and I am way too deep in this?  God, just play the thing, it's shorter than this paragraph.

I'm also left wondering when it _is_ appropriate to send a dick pic.  Presumably there is a correct time?  Hopefully the author will enter Strawberry Jam 2 to expound upon this.

**FINAL SCORE:** 3½”  ;)


## Marble maze, by Shtille

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/marble-maze.jpg" alt="">
</div>

<center>*short · arcade · jan 2017 · win · free on [itch](https://shtille.itch.io/marble-maze) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/214039)*</center>

Ah, hm.  So this is a maze navigated by rolling a marble around.  You use WASD to move the marble, and you can also turn the camera with the arrow keys.

The trouble is…  the marble's movement is always relative to _the world_, **not the camera**.  That means if you turn the camera 30° and then try to move the marble, it'll move at a 30° angle from your point of view.

That makes navigating a maze, er, difficult.

Camera-relative movement is the kind of thing I take so much for granted that I wouldn't even think to do otherwise, and I think it's valuable to look at surprising choices that violate fundamental conventions, so I'm trying to take this as a nudge out of my comfort zone.  What _could_ you design in an interesting way that used world-relative movement?  Probably not the player, but maybe something else in the world, as long as you had strong landmarks?  Hmm.

**FINAL SCORE:** ᘔ


## Refactor: flight, by fluffy

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/refactor-flight.png" alt="">
</div>

<center>*short · arcade · jan 2017 · lin/mac/win · free on [itch](https://fluffy.itch.io/refactor) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/155962)*</center>

Refactor is a game album, which is rather a lot what it sounds like, and Flight is one of the tracks.  Which makes this a single, I suppose.

It's one of those games where you move down an oddly-shaped tunnel trying not to hit the walls, but with some cute twists.  Coins and gems hop up from the bottom of the screen in time with the music, and collecting them gives you points.  Hitting a wall costs you some points and kills  your momentum, but I don't think outright _losing_ is possible, which is great for me!

Also, the monk cycles through several animal faces.  I don't know why, and it's very good.  One of those odd but memorable details that sits squarely on the intersection of abstract, mysterious, and a bit weird, and refuses to budge from that spot.

The music is great too?  Really chill all around.

**FINAL SCORE:** 🎵🎵🎵🎵


## The Adventures of Klyde

<div class="prose-full-illustration">
<img src="{static}/media/game-night/games-made-quick-2/the-adventures-of-klyde.png" alt="">
</div>

<center>*short · adventure · jan 2017 · web · free on [itch](https://jazdaredbone.itch.io/the-adventures-of-klyde) · [jam entry](https://itch.io/jam/games-made-quick-2/rate/214132)*</center>

Another bitsy game, this one starring a pig (humorously symbolized by a giant pig nose with ears) who must collect fruit and solve some puzzles.

This is charmingly nostalgic for me — it reminds me of some standard fare in engines like MegaZeux, where the obvious things to do when presented with tiles and pickups were to make mazes.  I don't mean that in a _bad_ way; the maze is the fundamental environmental obstacle.

A couple places in here felt like invisible teleport mazes I had to brute-force, but I might have been missing a hint somewhere.  I did make it through with only a little trouble, but alas — I stepped in a bad warp somewhere and got sent to the upper left corner of the starting screen, which is surrounded by walls.  So Klyde's new life is being trapped eternally in a nowhere space.

**FINAL SCORE:** 19/20 apples


## And more

That was only a _third_ of the games, and I don't think even half of the ones I've played.  I'll have to do a second post covering the rest of them?  Maybe a third?

Or maybe this is a ludicrous format for commenting on several dozen games and I should try to narrow it down to the ones that resonated the most for Strawberry Jam 2?  _Maybe??_
