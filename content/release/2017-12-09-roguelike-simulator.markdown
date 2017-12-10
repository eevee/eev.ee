title: Roguelike Simulator
date: 2017-12-09 22:59
category: release
tags: making things

<div class="prose-full-illustration">
<img src="{filename}/media/2017-12-09-roguelike-simulator/roguelike-simulator.png" alt="Screenshot of a monochromatic pixel-art game designed to look mostly like ASCII text">
</div>

On a recent [game night](content/2017-12-05-game-night-1-lisa-lisa-moop.markdown), glip and I stumbled upon [bitsy](https://ledoux.itch.io/bitsy) — a tiny game maker for "games where you can walk around and talk to people and be somewhere."  It's enough of a genre to have become a [top tag](https://itch.io/games/tag-bitsy) on itch, so we flicked through a couple games.

What we found were tiny windows into numerous little worlds, ill-defined yet crisply rendered in chunky two-colored pixels.  Indeed, _all_ you can do is walk around and talk to people and be somewhere, but the _somewheres_ are strangely captivating.  My favorite was [the last days of our castle](https://candle.itch.io/castle), with [a day on the town](https://seansleblanc.itch.io/a-day-on-the-town) in a close second (though it cheated and extended the engine a bit), but there are several hundred of these tiny windows available.  Just single, short, minimal, interactive glimpses of an idea.

I've been wanting to do more of that, so I gave it a shot today.  The result is [**Roguelike Simulator**](https://eevee.itch.io/roguelike-simulator), a game that condenses the NetHack experience into about ninety seconds.

<!-- more -->

----

Constraints breed creativity, and bitsy is practically _made of_ constraints — the only place you can even make any decisions at all is within dialogue trees.  There are only three ways to alter the world: the player can step on an _ending_ tile to end the game, step on an _exit_ tile to instantly teleport to a tile on another map (or not), or pick up an item.  That's it.  You can't even implement keys; the best you can do is make an annoying maze of identical rooms, then have an NPC tell you the solution.

In retrospect, a roguelike — a genre practically defined by its randomness — _may_ have been a poor choice.

I had a lot of fun faking it, though, and it worked well enough to fool at least one person for a few minutes!  Some choice hacks follow.  Probably play the game a couple times before reading them?

- Each floor reveals itself, of course, by teleporting you between maps with different chunks of the floor visible.  I originally intended for this to be much more elaborate, but it turns out to be a huge pain to juggle multiple copies of the same floor layout.

- Endings can't be changed or randomized; even the text is static.  I still managed to implement multiple variants on the "ascend" ending!  See if you can guess how.  (It's not that hard.)

- There are no Boolean operators, but there _are_ arithmetic operators, so in one place I check whether you have both of two items by multiplying together how many of each you have.

- Monsters you "defeat" are actually just items you pick up.  They're both drawn in the same color, and you can't see your inventory, so you can't tell the difference.

Probably the best part was writing the text, which is all completely ridiculous.  I really enjoy writing a lot of quips — which I guess is why I like Twitter — and I'm happy to see they've made people laugh!

----

I think this has been a success!  It's definitely made me more confident about making smaller things — and about taking the first idea I have and just running with it.  I'm going to keep an eye out for other micro game engines to play with, too.
