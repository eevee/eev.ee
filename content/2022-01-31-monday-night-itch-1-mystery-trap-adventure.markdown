title: Monday Night Itch #1: Mystery Trap Adventure
date: 2022-01-31 21:15
category: articles
series: monday night itch
tags: games

**Welcome** to Monday Night Itch, a harebrained scheme to encourage folks to play more non-AAA games by adding a touch of social gamification.  I thought I would be tweeting my adventures here, but I just had an experience so profound it can only be captured within a blog post.

<!-- more -->

## The rules

"Rules" is a strong word, but nevertheless:

- Every Monday, find a game on [itch.io](https://itch.io/), and pay at least $2 for it.

    You can buy a game with a price tag, or download a free game and leave a tip, but the point of this endeavor is to put money into more places in the ecosystem.  (Note that it _is_ possible, though uncommon, for a developer to disable payments altogether.)

- Play it.

- Leave a nice comment.

- Tell at least one person what you played, and what you thought about it.

That's it.  Buy a game, play it, tell someone about it.  You can stream it, tweet it, screenshot it, or just tell your boyfriend about it.  You don't have to like it

Your score is how many times you've done this, and your streak is how many weeks you've done it in a row.


## Some other quick tips about itch

The [itch app](https://itch.io/app) is cool.  It's a pretty thin wrapper around the website, but it adds automatic updating and big red "Launch" buttons and other stuff to make it feel a bit more like a Steam-ish thing.  Do keep in mind that devs can upload whatever they want, and sometimes the itch app gets confused.

If you're not a fan of running mystery software you downloaded from the Internet, you can just play web games and leave tips on those.

There are _a lot_ of NSFW games on itch, but they're hidden from the main browse pages by default.  You can enable them site-wide in your [user settings](https://itch.io/user/settings), or add `/nsfw` to the end of a browse page URL (for example, `https://itch.io/games` → `https://itch.io/games/nsfw`) to force a list of _only_ NSFW games.


## The main event

I decided I wanted to reward Linux releases, and also chip a few bucks towards games with a price tag that aren't necessarily getting much exposure, so I went to the full list of [recent paid Linux games](https://itch.io/games/newest/platform-linux/store).  This is how I discovered [Mystery Trap Adventure](https://rvedastudios.itch.io/mystery-trap-adventure).

I found myself _very_ much wanting to play this, but I also found myself wondering what sort of impact I should be trying for as the very first iteration of this project.  Would I torpedo it if I played a game made by a less experienced dev?  Are people looking to this expecting me to uncover unknown indie gems, like I'm wandering a beach with a metal detector?

I checked the dev's itch profile and this is their _ninth_ project.  Every single previous work of their has only a single comment: from them, announcing that comments can be left below.  That's heartbreaking to me, and what made me absolutely sure I wanted to play this.  I want to make their day.

And then, dear reader, I felt ashamed.  Because who the fuck cares.  The world already has enough people who believe that indie games are only valuable if they create the illusion of an eight-digit budget, and I am not here to enable them.  Creative work does not need to be polished, mass-appeal, least common denominator stuff handed down from heaven by a billion-dollar international corporation in order to be interesting or worthwhile.

But more importantly, it's my thing and I'm gonna do whatever the hell I want.

{% illus /media/monday-night-itch/001-mystery-trap-adventure/title.jpg The title screen for Mystery Trap Adventure: a collage of mismatched artwork on a nearly cyan background %}

And so, Mystery Trap Adventure.

The first thing to note is that the game does not, in fact, have a Linux release.  I did strongly suspect this, since a single download is flagged as all of Windows, Mac, and Linux, but the only way to be sure was to buy it.  (They're asking $4; I paid them $10.)  Even Wine had trouble with it, for some reason, so I had to play it on our Windows media center.

It's a sidescrolling platformer where you play as a dragon; you can jump about one tile high (roughly your own height) and shoot fireballs (useful for destroying bricks and defeating the boss).  The main obstacle is spikes, which kill you instantly.

Right at the beginning, there's a block you have to jump on top of, and it was very obvious that I sort of "stuck" to the side of it if I touched it.  I thought at first that this was the result of a common platforming gotcha: if you model the player as a dynamic body and implement movement (including air control) as a force on them, then they will stick to walls as long as the corresponding direction is held.  This happens because forces on dynamic bodies are external, as though a giant ghost hand were pushing them — so if a player is trying to air control into a wall, the _friction against the wall_ will hold them in place, just as if you were holding a book against a wall with your hand.

(Solving that problem is beyond the scope of this post, sorry.)

Okay, common pitfall, no big deal.  I wander ahead a bit.  I encounter a slice of watermelon, which allows me to teleport a short distance _once_.  I screw this up the first time while messing with the controls — there's a wall directly in front of it, so the teleport must be used to skip past that wall — and have to restart.

Now something interesting happens.  I'm in a pit with walls on both sides.  I can't teleport again, and even if I could, there are spikes beyond the next wall, so that would kill me immediately.

{% illus /media/monday-night-itch/001-mystery-trap-adventure/pit.jpg A screenshot of the situation just described %}

It dawns on me that this microscopic game has _walljumping_.

I'm still fairly certain that the player character is a dynamic body, but now I wonder: is the wall stickiness actually due to the friction interaction, or is it a deliberate feature to enable walljumping?

Or, perhaps more likely, is it _both_?  Did the developer trip over this pitfall, and decide to make a gameplay feature out of it?  It almost seems unbelievable.  I wouldn't consider walljumping a _basic_ platforming ability, and it's not obvious how to solve the friction problem, but it seems that this relatively new developer may have solved both problems by simply smashing them together.

And if that's the case, dearest reader: I _fucking love it_.  That is the true spirit of game development, I think — you have a big complicated simulation you want to make, and you have a big complicated engine that you want to make do it, and you have to kinda mold both of them into fitting better with the other.

I don't know.  I could be completely wrong about this came to be.  Or they could have copy/pasted from someone else who had this idea.  Either way, it made me smile to see.

The walljumping controls are, ahem, not exactly intuitive, which is why it took me nonzero time to realize it was an ability at all.  But honestly, I liked that too.  Nowadays, everyone knows exactly how every platforming ability is "supposed" to work, because devs are all copying the same ideas from each other that have been refined over a thousand different iterations.  This reminded me of playing games in the early and mid 90s, before everything had standardized as much, when part of the game itself was just working out the right muscle memory to make the right things happen.  It's surprising to find nostalgia in a game because it's _not_ like others I've played before, but there it was.  Working out the right timing without any visual cues felt like a puzzle in itself, and getting out of the pit without landing in the spikes was remarkably satisfying.  (If it helps: I used different hands for movement and jumping, and I landed on top of the right wall before trying to jump over the spikes.)

Beyond this, the tone changes somewhat to IWBTG-esque traps with no telegraphing.  Walking directly to the right will cause spikes to appear from the ground, killing you instantly.  Thankfully there aren't too many of these, and the game is very short, so simply memorizing the handful of places they appear is easy enough.

I have less to say about the rest of the game; you get another quirky powerup you only use once, dodge another couple surprise traps, and face a single boss.  The boss is a very large human warrior dude who walks straight at you and swings his sword, which kills you.  There's another fruit above you, but it seems out of reach.  He is definitely too tall to jump over.  The only solution I found is to simply spam fireballs at him before he can reach you, but I don't know if this is intended.  It seems like it can't be, since his "health bar" takes the form of a grid of his face behind him, and from where you enter the area, you can't actually see the whole grid?  So surely I'm supposed to be able to get further to the right?  But I don't know.

----

I finished the game and came back to the following reply to my original thread about this whole concept:

> most, i.e. all, small Indy games are terrible.

What a snotty, entitled, mean-spirited sentiment.  As if the very existence of a game with lower production values than Resident Evil 8 were a personal offense.  It seems to be fairly common, too, and I just do not understand it.  Small indie games aren't trying to squeeze you for more money, lure you in with gambling, exploit your friendships, make your entire life revolve around them.  They're just _there_.

This attitude is like showing up to everyone who mentions YouTube just to proclaim that everything on it sucks, because Paramount movies are better.  That's great, no one asked!  Sometimes I just want to see a seven-second clip of a kitten filmed in a dark room by a $20 phone, because dammit, kittens are still fun to watch.  No one makes a point of dunking on videos like that, so I don't know why anyone is so harsh on amateur games either.  _Especially_ when making games is so much more difficult!

Mystery Trap Adventure is that video.  Someone had an idea, worked out how to express it, and put it out into the world just because they wanted to.  I don't expect anyone else to buy it or play it; I just want you to know that _I_ did, and it made me smile for a few minutes.
