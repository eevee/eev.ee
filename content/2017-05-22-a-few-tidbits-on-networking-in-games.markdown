title: A few tidbits on networking in games
date: 2017-05-22 08:06
category: articles
tags: tech, gamedev, patreon

[Nova Dasterin](https://www.patreon.com/user?u=2491881) asks, [via Patreon](https://www.patreon.com/eevee):

> How about do something on networking code, for some kind of realtime game (platformer or MMORPG or something). :D

Ah, I see.  You're hoping for my usual detailed exploration of everything I know about networking code in games.

Well, joke's on you!  I don't know _anything_ about networking.

Wait...  wait...  maybe I know _one_ thing.

<!-- more -->


## Doom

Surprise!  The thing I know is, roughly, how multiplayer Doom works.

Doom is 100% deterministic.  Its [random number generator](https://doomwiki.org/wiki/Pseudorandom_number_generator) is really a list of shuffled values; each request for a random number produces the next value in the list.  There is no seed, either; a game always begins at the first value in the list.  Thus, if you play the game twice with _exactly identical_ input, you'll see exactly the same playthrough: same damage, same monster behavior, and so on.

And that's exactly what a Doom demo is: a file containing a recording of player input.  To play back a demo, Doom runs the game as normal, except that it reads input from a file rather than the keyboard.

Multiplayer works the same way.  Rather than passing around the entirety of the world state, Doom sends the player's input to all the other players.  Once a node has received input from every connected player, it advances the world by one tic.  There's no client or server; every peer talks to every other peer.

You can [read the code](https://github.com/id-Software/DOOM/blob/master/linuxdoom-1.10/d_net.c) if you want to, but at a glance, I don't think there's anything too surprising here.  Only sending input means there's not that much to send, and the receiving end just has to queue up packets from every peer and then play them back once it's heard from everyone.  The underlying transport was pluggable (this being the days before we'd even standardized on IP), which complicated things a bit, but the Unix port that's on GitHub just uses UDP.  The Doom Wiki has [some further detail](https://doomwiki.org/wiki/Doom_networking_component).

This approach is very clever and has a few significant advantages.  Bandwidth requirements are fairly low, which is important if it happens to be 1993.  Bandwidth and processing requirements are also completely unaffected by the size of the map, since map state never touches the network.  

Unfortunately, it has some drawbacks as well.  The biggest is that, well, sometimes you _want_ to get the world state back in sync.  What if a player drops and wants to reconnect?  Everyone has to quit and reconnect to one another.  What if an extra player wants to join in?  It's possible to load a saved game in multiplayer, but because the saved game won't have an actor for the new player, you can't really load it; you'd have to start fresh from the beginning of a map.

It's fairly fundamental that Doom allows you to save your game at any moment...  but there's no way to load in the middle of a network game.  Everyone has to quit and restart the game, loading the right save file from the command line.  And if some players load the wrong save file...  I'm not actually sure what happens!  I've seen ZDoom detect the inconsistency and refuse to start the game, but I suspect that in vanilla Doom, players would have mismatched world states and their movements would look like nonsense when played back in each others' worlds.

Ah, yes.  Having the entire game state be generated independently by each peer leads to another big problem.


## Cheating

Maybe this wasn't as big a deal with Doom, where you'd probably be playing with friends or acquaintances ([or coworkers](https://doomwiki.org/wiki/Broadcast_packet_meltdown)).  Modern games have matchmaking that pits you against _strangers_, and the trouble with strangers is that a nontrivial number of them are _assholes_.

Doom is a very moddable game, and it doesn't check that everyone is using exactly the same game data.  As long as you don't change anything that would alter the shape of the world or change the number of RNG rolls (since those would completely desynchronize you from other players), you can modify your own game however you like, and no one will be the wiser.  For example, you might change the light level in a dark map, so you can see more easily than the other players.  Lighting doesn't affect the game, only how its drawn, and it doesn't go over the network, so no one would be the wiser.

Or you could alter the executable itself!  It knows everything about the game state, including the health and loadout of the other players; altering it to show you this information would give you an advantage.  Also, all that's sent is input; no one said the input had to come from a human.  The game knows where all the other players are, so you could modify it to generate the right input to automatically aim at them.  Congratulations; you've invented the _aimbot_.

I don't know how you can reliably fix these issues.  There seems to be an entire underground ecosystem built around playing cat and mouse with game developers.  Perhaps the most infamous example is World of Warcraft, where people farm in-game gold as automatically as possible to sell to other players for real-world cash.

Egregious cheating in multiplayer really gets on my nerves; I couldn't bear knowing that it was rampant in a game I'd made.  So I will probably not be working on anything with random matchmaking anytime soon.


## Starbound

Let's jump to something a little more concrete and modern.

[Starbound](http://playstarbound.com/) is a procedurally generated universe exploration game — like Terraria in space.  Or, if you prefer, like Minecraft in space and also flat.  Notably, it supports multiplayer, using the more familiar client/server approach.  The server uses the same data files as single-player, but it runs as a separate process; if you want to run a server on your own machine, you run the server and then connect to `localhost` with the client.

I've run a server before, but that doesn't tell me anything about how it _works_.  Starbound is an interesting example because of the existence of [StarryPy](https://github.com/StarryPy/StarryPy3k) — a proxy server that can add some interesting extra behavior by intercepting packets going to and from the real server.

That means StarryPy necessarily knows what the protocol _looks like_, and perhaps we can glean some insights by poking around in it.  Right off the bat there's a [list of all the packet types](https://github.com/StarryPy/StarryPy3k/blob/7d939f0bb5878195bca45aa3f830254c7628239e/packets.py) and [rough shapes of their data](https://github.com/StarryPy/StarryPy3k/blob/7d939f0bb5878195bca45aa3f830254c7628239e/data_parser.py#L641).

I modded StarryPy to print out every single decoded packet it received (from either the client or the server), then connected and immediately disconnected.  (Note that these aren't necessarily TCP packets; they're just single messages in the Starbound protocol.)  Here is my quick interpretation of what happens:

1. The client and server briefly negotiate a connection.  The password, if any, is sent with a challenge and response.

2. The client sends a full description of its "ship world" — the player's ship, which they take with them to other servers.  The server sends a partial description of the planet the player is either on, or orbiting.

3. From here, the server and client mostly communicate world state in the form of small delta updates.  StarryPy doesn't delve into the exact format here, unfortunately.  The world basically freezes around you during a multiplayer lag spike, though, so it's safe to assume that the vast bulk of game simulation happens server-side, and the effects are broadcast to clients.

The protocol has specific message types for various player actions: damaging tiles, dropping items, connecting wires, collecting liquids, moving your ship, and so on.  So the basic model is that the player can attempt to do stuff with the chunk of the world they're looking at, and they'll get a reaction whenever the server gets back to them.

(I'm dimly aware that some subset of object interactions can happen client-side, but I don't know exactly which ones.  The implications for custom scripted objects are...  interesting.  Actually, those are slightly hellish in general; Starbound is very moddable, but last I checked it has no way to send mods from the server to the client or anything similar, and by default the server doesn't even enforce that everyone's using the same set of mods...  so it's possible that you'll have an object on your ship that's only provided by a mod you have but the server lacks, and then _who knows_ what happens.)


## IRC

Hang on, this isn't a video game at all.

Starbound's "fire and forget" approach reminds me a lot of IRC — a protocol I've even implemented, a little bit, kinda.  IRC doesn't have any way to match the messages you send to the responses you get back, and success is _silent_ for some kinds of messages, so it's impossible (in the general case) to know what caused an error.  The most obvious fix for this would be to attach a message id to messages sent out by the client, and include the same id on responses from the server.

It doesn't look like Starbound has message ids or any other solution to this problem — though StarryPy doesn't document the protocol well enough for me to be sure.  The server just sends a stream of stuff it thinks is important, and when it gets a request from the client, it queues up a response to that as well.  It's TCP, so the client should get all the right messages, eventually.  Some of them might be slightly out of order depending on the order the client does stuff, but that's not a big deal; anyway, the server knows the canonical state.


## Some thoughts

I bring up IRC because I'm kind of at the limit of things that I know.  But one of those things is that IRC is simultaneously very rickety and wildly successful: it's a decade older than Google and still in use.  (Some recent offerings are starting to eat its lunch, but those are really because _clients_ are inaccessible to new users and the protocol hasn't evolved much.  The problems with the fundamental design of the protocol are only obvious to server and client authors.)

Doom's cheery assumption that the game will play out the same way for every player feels similarly rickety.  Obviously it _works_ — well enough that you can go play multiplayer Doom with exactly the same approach right now, 24 years later — but for something as complex as an FPS it really doesn't feel like it should.

So while I don't have enough experience _writing_ multiplayer games to give you a run-down of how to do it, I think the lesson here is that you can get pretty far with simple ideas.  Maybe your game isn't deterministic like Doom — although there's no reason it _couldn't_ be — but you probably still have to save the game, or at least restore the state of the world on death/loss/restart, right?  There you go: you already have a fragment of a concept of entity state outside the actual entities.  Codify that, stick it on the network, and see what happens.

I don't know if I'll be doing any significant multiplayer development myself; I don't even play many multiplayer games.  But I'd always assumed it would be a nigh-impossible feat of architectural engineering, and I'm starting to think that maybe it's no more difficult than anything else in game dev.  Easy to fudge, hard to do well, impossible to truly get right so give up that train of thought right now.

Also now I am definitely thinking about how a multiplayer puzzle-platformer would work.
