title: Lexy's Labyrinth
date: 2020-09-26 19:28
category: updates
tags: gamedev

<div class="prose-full-illustration">
<img src="{static}/media/release/lexys-labyrinth/lexys-labyrinth.png" alt="Screenshot of a small tile-based puzzle with a number of different elements, taken from CCLP1">
</div>

🔗 [**Lexy's Labyrinth**](https://c.eev.ee/lexys-labyrinth/)  
🔗 [**Source code on GitHub**](https://github.com/eevee/lexys-labyrinth)  
🔗 itch.io later

Here is Lexy's Labyrinth, a web-based Chip's Challenge emulator.

It's easy to get into and mostly speaks for itself, so here is a story.

<!-- more -->

----

Once upon a time, there was a puzzle game called [Chip's Challenge](https://en.wikipedia.org/wiki/Chip%27s_Challenge).  It was created in 1989 for the Atari Lynx, an early handheld that is probably best known for...  uh...  Chip's Challenge.  It stood out as a curious blend of Sokoban head-scratching with real-time action, and it was one of the first computer puzzle games that had a whole pile of different mechanics and relied on exploiting the interesting interactions between them<sup>[citation needed]</sup>.

The game found wider recognition with its inclusion in [Microsoft Entertainment Pack 4](https://en.wikipedia.org/wiki/Microsoft_Entertainment_Pack), and later the Best of Windows Entertainment Pack (charmingly abbreviated "BOWEP").

----

That in itself is a curious story — numerous features of the Atari Lynx version were lost in translation, most notably that the Lynx version has the player and monsters slide smoothly between grid cells, whereas the Microsoft port has everything instantly snap from one cell to the next.  Also conspicuous is the presence of several typos in level passwords, which are exactly consistent with [a set of notes a player took about the Lynx game](https://wiki.bitbusters.club/Jaime_Villacorte%27s_notes), but which would be impossible in a straight port — the Lynx level passwords weren't manually set, but were generated on the fly by a PRNG.

<div class="prose-full-illustration">
<img src="{static}/media/release/lexys-labyrinth/mschips.png" alt="Screenshot of the Microsoft edition of Chip's Challenge, showing the first level, courtesy of the BBC wiki">
</div>

The most obvious explanation is that the developer responsible for the Microsoft port didn't have access to the Lynx source code, and in fact, _had never played the original game at all_.  That would explain nearly every major gameplay difference between the Lynx and Microsoft versions, which are all things you'd never notice if you only had static screenshots and maps to work from.  Given that restriction, hey, not a bad job.

----

I played the BOWEP edition of Chip's Challenge as a kid and was completely enamoured.  I suppose what got me the most was the same thing that I found so compelling about Doom: the ability to modify your environment, whether by using blocks to clear water or toggling green blocks or generating new monsters from a clone machine.  Being able to affect my environment in (more or less) free-form ways felt curiously powerful.

...

Well, let's not think about that too hard.  I'll save it for my therapist.

Some years later I discovered an incredible tool called _The Internet_, and with it I learned of the impending [Chip's Challenge 2](https://wiki.bitbusters.club/Chip%27s_Challenge_2), a sequel with _way_ more tiles and possibilities!  Fantastic!

Unfortunately, there was a complication.  Epyx, the original publisher of Chip's Challenge, had gone bankrupt (somehow!) and had sold most of its assets, including the Chip's Challenge rights, to a company called Bridgestone Media (now Alpha Omega Productions), a Christian propaganda distributor.

You read that correctly.

Bridgestone, a company that generally dealt in movies, had some very peculiar ideas about the video game industry.  Apparently they expected the assets they'd acquired to magically make them filthy rich — you know, just like Jesus would want — despite having acquired them _from_ a company that had just evaporated.  As such, they told the original developer, Chuck Somerville, that he could only release Chip's Challenge 2 if he paid them [one million dollars upfront](https://forum.bitbusters.club/thread-2127.html).

He did not have one million dollars, and so Chip's Challenge 2 languished forever.

(At this point, in hindsight, I wonder why Chuck didn't simply change the story and tileset and release the game under a different name.  Apparently he did start on something like this some years later, in the form of an open clone _from scratch_ called [Puzzle Studio](https://wiki.bitbusters.club/Puzzle_Studio), but it was eventually abandoned in favor of [Chuck's Challenge 3D](https://wiki.bitbusters.club/Chuck's_Challenge_3D).  But I still wonder: why start a brand new thing, rather than rebrand and release the existing thing?)

We did have some descriptions of new Chip's Challenge 2 mechanics, and so at the ripe old age of 15, with no idea what I was doing, I decided I would simply write my own version of Chip's Challenge 2.

In QBasic.

Also I didn't really understand how to handle the passage of time, so the game was turn-based and had no monsters.

But, given all that, it wasn't _that_ bad.  I found the source code a few years ago and [put it on GitHub](https://gist.github.com/eevee/1b371c4b2470dd82cbcf) along with a sample level and a description of all the tiles you can use in the plaintext level format.  I've got a [prebuilt binary for DOS](https://c.eev.ee/CHIPS.EXE) (usable in DosBox) too, if you like — just have a `levels.txt` in the same directory, and be sure it uses DOS line endings.  I used to have one or two actual levels, but they have tragically been lost to the sands of time.

<div class="prose-full-illustration">
<img src="{static}/media/release/lexys-labyrinth/qbchips.png" alt="Screenshot of my QBasic implementation of Chip's Challenge, using all character-based graphics">
</div>

That would've been 2002.

----

Thirteen years later, in April 2015, a miracle occurred and defeated the Christians.  Chip's Challenge 2 was released [on Steam](https://store.steampowered.com/app/348300/Chips_Challenge_2/).

It was fine.  I don't know.  Over a decade of anticipation gets your hopes up, maybe.  It's a perfectly good puzzle game, and I don't want to dunk on it, but sometimes I interact with it and I feel all life drain from my body.

<div class="prose-full-illustration">
<img src="{static}/media/release/lexys-labyrinth/cc2female1.png" alt="Screenshot of CC2, with an overlaid hint saying: &quot;This is Melinda.  Being female, she does some things differently than Chip.&quot;">
<img src="{static}/media/release/lexys-labyrinth/cc2female2.png" alt="Screenshot of CC2, with an overlaid hint saying: &quot;She doesn't slide when she steps on ice.  But she needs hiking boots to walk on dirt or gravel.&quot;">
</div>

I don't even know whether to talk about this completely unreadable way of showing hints or the utterly baffling justification of "being female" for these properties.

But it's fine.  The game was Windows-only, but it was _old_ Windows-only, so Wine handled it perfectly well.  I played through a few dozen levels.  Passwords were gone, so you were free to skip over levels you just didn't feel like playing.

And then they patched a level editor into the game, and it completely broke under Wine.  _Completely_.  Like, would not even run.  It's only in recent years that it even _tries_ to run, and now it can't draw the window and crashes if you attempt to do anything.

The funny thing is, apparently it doesn't draw for some people on Windows, either.  It doesn't for _me_ in a Windows VM.  The official sanctioned solution is to...  install...  wined3d, a Windows port of the Wine implementation of Direct3D.

I don't know.  I don't know!  I don't know what the hell anything.  This situation is utterly baffling.  What even are computers.

----

I gave up on the game until recently, when something reminded me of it and I tried it again in Wine.  No luck, obviously.  I spent half a day squabbling with bleeding-edge versions and Proton patches and all manner of other crap, then resorted to the [Bit Busters Club](https://bitbusters.club/) [Discord](https://discord.gg/Xd4dUY9), but they couldn't help me either.

And then something stirred, deep inside of me.  This game wasn't _that_ complicated, right?  I actually know how to make video games now.  I even know how to make art, sort of.  And sound.  And music.  And...

----

And here I am, a month later, having replicated Chip's Challenge in a web browser, fueled entirely by some new emotion I've discovered that lies halfway between spite and exhaustion.  My real goal was to clone Chip's Challenge 2 _so I can actually fucking play this game I bought_, but it is of course a more complex game.  Still, CC2 support is something like 60% done; most of what remains is wiring, tracks, and ghost/rover behavior.

CC1 support is more interesting, anyway — there are far more custom CC1 levels around, and Lexy's Labyrinth exposes almost 600 of them a mere click away.  Given that the original Microsoft port was 16-bit and is now difficult to run (and impossible to buy), and the official (free!) [Steam release](https://store.steampowered.com/app/346850/Chips_Challenge_1/) is fairly awkward and unmaintained (the dev mostly makes vague statements about "old code"), and even the favored emulator [Tile World](https://wiki.bitbusters.club/Tile_World) has the aesthetics and usability of a 1991 Unix application, I'm hoping this will make the Chip's Challenge experience a little more accessible.  It has a partially working level editor, too, which lets you share levels you make by simply passing around a URL, and I think that is fucking fantastic.

LL cannot currently load level _packs_ from the Steam release, but it's a high priority.  In the meantime, if you really want to play the original levels (even though CCLP1 is far better in my experience), it'll load `CHIPS.DAT` if you've got it lying around.  Also, it works on phones!

----

Probably the most time-consuming parts of this project were the assets.  I had to draw a whole tileset from scratch, _including_ all of the CC2 tiles which you don't even get to see yet (and a few of which aren't actually done).  That probably took a week, spread out over the course of the entire last month.  Sound effects took several days, though they got much easier once I decided to give up on doing them by wiring LFOs together in SunVox and just use a bunch of [BeepBox](https://www.beepbox.co/) presets.  I spent a couple days on my own music track, and half a dozen other kind souls chipped in their own music — thank you so much, everyone!

And thank you to the Bit Busters Club, whose incredibly detailed knowledge made it possible to match the behavior of a lot of obscure-but-important interactions.  The Steam version of CC1 comes with solution replays, and LL can even play a significant number of them back without ever desyncing.

I've been ignoring pretty much everything else for a month to get this in a usable state, so I'd like to take a break from it for now, but I'd really like to get all of CC2 working when I can, and of course make the level editor fully functional.  I love accessible modding tools, you don't see many of them in games any more, and with any luck maybe it'll inspire some other kid to get into game development later.

----

...okay, I haven't been ignoring _everything_ else.  I also reused the tiles I drew for a fox flux minigame in a similar style, except that you place a limited set of tiles in empty spaces and then let the game run _by itself_.  Kind of like...  Chip's Challenge meets The Incredible Machine.

<div class="prose-full-illustration">
<img src="{static}/media/release/lexys-labyrinth/fox-flux-minigame-demo.gif" alt="Recording of a minigame, showing a drone character interacting with moving floors and following instructions on the ground">
</div>

(That arrow tile has since been updated to be more clear, but it means "when you hit something, turn around instead of stopping and ending the game.")

I guess two little puzzle game engines isn't too bad for not quite a month of work!
