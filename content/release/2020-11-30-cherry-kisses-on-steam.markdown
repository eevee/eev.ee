title: Cherry Kisses, on Steam
date: 2020-11-30 16:44
category: release
tags: tech

<div class="prose-full-illustration">
<img src="{static}/media/release/cherry-kisses.png" alt="Cherry Kisses title screen, showing Cerise at a counter">
</div>

🔗 [**Steam release**](https://store.steampowered.com/app/1259530/)  
🔗 [**itch release**](https://eevee.itch.io/cherry-kisses)

Whoops!  I meant to write about this when it originally came out, _in April_, but never quite got around to collecting my thoughts.  Here is a very rushed subset of them.

**The game is extremely NSFW**, but the commentary below is not.

<!-- more -->

----

## The game itself

I like the game.  It's essentially a visual novel, but _disguised_.

I've played a decent number of visual novels, and I've thought a lot about them and their role as kind-of-games, and I've noticed the thorny bits that I don't like.  And my thoughts have circled around the notion of _player agency_.

Agency is what makes a game feel like a game.  You have _input_, in a broad sense.  You can do something to the game, and it will react appropriately (fingers crossed).

This theory explains the awkward position of visual novels.  The bulk of the experience is reading a passage, pressing spacebar, and GOTO 10.  You don't have meaningful input; pressing spacebar isn't a decision, it's scrolling.

When you _do_ have input, it generally comes in the form of a menu.  But this doesn't feel like you're _making_ a choice; it feels like one is being _extracted_ from you in the middle of an otherwise passive reading experience.  The base form of the game is reading, and that has been interrupted at a predetermined point to demand something of you.  You often don't have enough information to make a _meaningful_ choice, either, so this becomes a game of saving at each branch and performing an exhaustive depth-first search of the story.  As time goes on, you end up skipping through more and more of the early parts, and may hit a point where you go down a decision branch not even remembering what form the story took before you got there.

This is a weird experience.

I wanted to try to improve the feeling of a VN without altering the substance, so this one is disguised as an RPG.  I mean, not really an RPG, but that brand of top-down "walk around and interact with stuff" framing.

You play as Cerise, and the entire game takes place in her shop.  At any given time, zero or more customers are present, and you can either twiddle your thumbs at the counter or talk to one of them.  Whatever you do will generally advance time by an hour, which may change the set of customers; some folks left or arrived while you were busy doing something else.  And different folks have different reactions to being ignored, so the whole game becomes one large meta scheduling puzzle.

The thing is, this could've been done just as well with a menu at the start of each hour, asking who you want to talk to.  The gameplay would've been functionally identical.  But this scheme feels completely different (at least to me) for several reasons:

1. Instead of choices being "on top of" the prose, the prose is on top of the choices.  It feels like the choices you make _cause_ the prose to happen, rather than being forks in the middle of a river you can't escape.  You can wander around the shop as long as you like, taking breathers, and time will not pass until _you_, the human at the controls, cause something to happen.  (You could say the same about a menu in a VN, but there you can't do anything _else_ either; the entire game is frozen until you interact with this modal dialog.)

2. You can do other things.  Not _many_, granted, but you can examine every single object in the shop, and they all have different descriptions (even if they look identical).  A typical visual novel doesn't give you the opportunity to go on frivolous tangents, but I think a big part of games is being able to forget about the progression for a minute and fuck around with something that looks interesting.  Stop and smell the roses, in this case literally.

3. A menu spells out all possible options with equal priority.  They're just items in a list, after all.  A physical world, on the other hand, can add subtle differences — choices may be more or less obvious, more or less compelling, or be presented in some way that adds to the narrative.  For example, while customers tend to show up at arbitrary spots throughout the shop, your girlfriend Lexy will wait for you right behind the counter, suggesting a more personal relationship even if you don't yet know who she is.  Or consider the ubiquitous option of ignoring _everyone_ in the shop and passing time at the counter instead.  That would usually be pointless, so it would be obnoxious to list in every single menu, but having it as an option in-world makes it less obvious...  which is perfect puzzle fodder.  Just saying.

As an added bonus, every character in the game has a "happiness" rating from -3 to 3.  If you can help them with their problems, their happiness will increase.  The numbers are largely arbitrary, but you do get a final score tally at the end, and that gives some sense of measured accomplishment that's more nuanced than a mere good/bad ending.  You can ignore it altogether and be happy with the story you got, _or_ you can go down the rabbit hole and try to find the unique path through the game that will make everyone happy and get you a perfect score.

These feel like really subtle design decisions that have an equally subtle impact on the experience.  I don't know what impact it had on anyone else, but _I_ really liked the results.  I didn't mind playing through the game a gazillion times while I was developing it, because it's just nice to play.  The story isn't especially deep, but it has a lot of little lighthearted interactions with a variety of characters, and sometimes different threads impact each other in really subtle ways.  Sometimes I ran across an interaction I'd forgotten I'd written!  It feels like the kind of story game that you _can't_ merely grind every ending out of, one that always has a chance to surprise you a little.

I still have other ideas for making narrative games that feel more player-controlled, so fingers crossed that I can pull them off.

## Steam, numbers, business

This is the first game I've put on Steam, a platform I've long had mixed feelings about.  On the one hand, it's cool that video games have something like a package repository.  On the other hand, that package repository is owned and controlled by a single company that sits back and rakes in billions (30% off of every sale!) from a glorified FTP server, something that Linux distributions do for free.  And it's normalized casual DRM, which I do not enjoy.  (If I did it right, then manually running Cherry Kisses while Steam is closed should simply _run the game_ without interacting with Steam at all.)

On the other hand, I can't deny the impact.  The Steam release earned more in its first two weeks than the itch release did in more than a year.

...okay, that isn't an entirely fair comparison.  The itch release also had a free "demo" version that was exactly like the "real" version, only with lower-resolution artwork.  _Loads_ of people played that (almost 20k downloads as of now), and in retrospect we may have shot ourselves in the foot a bit by offering a free version.  But I do _like_ when people can play my games, and releasing anything only in a paid form feels like extorting people out of their money.

I am not good at business.  It mostly feels bad.

Despite that, the game has somehow grossed a bit over $10k in the last eight months (which shrinks to $6k net after the Steam tax, VAT, and refunds).  That's not a _windfall_, but it's far more than I ever expected to earn on the back of a month-long jam game, and it all went to paying our 2019 taxes so it's like nothing ever happened.  It certainly makes me optimistic about selling something meatier.

## Creating the Steam release

We did update the game somewhat for Steam, a process that ended up consuming almost _a month_ somehow and still didn't cover everything we wanted.  The most obvious in-game things were the addition of character profiles, an image gallery, and an options menu — which is to say, all UI things, which I had to build in LÖVE, by hand, which was an incredible pain in the ass.  But it works, somehow.

Of course I also added a bunch of Steam achievements, which were kinda fun to decide upon.  It's a story game, so they're mostly of the form “encounter this bit of the story”, but that's fine?

But oh boy, the thing that really took the longest time was linking to Steam at all.  You get a DLL/SO, some header files, and some hit-or-miss [documentation](https://partner.steamgames.com/doc/sdk), and the rest is up to you.

The library is, of course, designed for C++.

I am not using C++.  I am using _Lua_.

This posed something of a problem.

I prefer not to touch C++ with a ten-foot pole, so writing some glue on the C++ side did not sound appetizing.  (That would've also left me with the difficult problem of _compiling_ that code for platforms I do not own or develop on.)  That left me with binding to the Steam API from the Lua side.

After several days of Googling, finding years-old projects that promised to do this, and completely failing to get anywhere at all with them, I resigned myself to writing something from scratch.  LÖVE uses LuaJIT, which comes with the excellent FFI library, meaning I could bind to C with nothing more than a header file.

The Steam API _does_ have a C compatibility layer, but it is basically not documented, so I had to do some guesswork to get from the documentation to the parts I actually needed.  Also, the core of the Steam API is this hokey async messaging system built out of macros and C++ metaprogramming, so I had to do a clumsier polling thing using disparate parts of the C API instead.  I finally discovered that there's example code in a big honking comment in the headers themselves, except ***the example code is wrong***, so I had to fix that as well.  Plus all the obtuse bugs like with padding on different platforms which for some reason is baked into the messages that Steam sends because C programmers don't know how to actually fucking serialize anything.  It was an adventure!!

But after all that, I managed to get achievements working, and also leaderboards.  Neat, cool, etc.

The game _does_ leak coroutines indefinitely if it's run through Steam but can't connect, though.  Sorry.

Man.  The Steam website has so many features, and the documentation explains them all in one succinct list, but fuck me if I can actually _find_ any of them.  So many things are not linked from obvious places; there have been many times I knew a particular page existed but _could not_ figure out how to get there, and ultimately I started relying on address bar history instead of trying to navigate this website.

And so many features are awkwardly built on top of older features that are actually something completely different.  Like we have a ["developer" page on Steam](https://store.steampowered.com/developer/floraverse), but the only part of it we can really control is a single line of plain text at the top.  If you go to the "about" tab, it just shows you that line again!  That's all we can put there!  You have to click "visit group page" (why would you do that??) in the sidebar of _that_ page to actually get to something we can control.

In stark contrast to itch, Steam _really_ wants your store page to look like a Steam store page and not like a your-game store page.  Your artwork (and there is so much artwork) has to be manually approved by a human, and along the way I discovered some extremely unintuitive rules, like that the library header has to be SFW even though it's only visible to people who already own the game.  Store pages also have a "legal" section, but I couldn't list open source libraries I used (and their licenses) in that section, because I'm not allowed to have links.  Like, at all.  They _really_ don't want you to have links.  Games exist independently of the humans that made them in the world of Steam; they are isolated jewels floating in a vast space that is linked directly to gaben's bank account.

I cannot comprehend how weirdly low-key hostile the whole experience felt.  All so they could take a third of my money.

Oh, and there's no Mac release, because I do not have a Mac on which to sign Mac software and do not wish to pay Apple for the privilege, and Mac software does not run any more if it's not signed.  Sorry.  Yes, I fucking know about fucking right-click open, please stop fucking telling me about that, that is not useful for software that is run from _someone else's launcher_.

## Reception

People seem to like it??  I mean, I've had a dozen or so people tell me to my face that they had an _especially_ good experience with it, that it was cozy and upbeat and just _nice_.  For a few of them, it apparently helped ease some aversion they'd had to sex, simply by showing it playing out well.

It's funny that I thought so hard about the general design and how agency worked and all that, but 99% of the feedback has been about the feeling of the prose itself — something that just kinda fell out of my fingers.  I guess I'm not _surprised_ — after all, if these players thought as hard about game design as I do, they'd probably be designing games.

As of this writing, there have been 19.5k downloads on itch and 1750 sales on Steam.  Of the Steam sales, a hair under 80% of the people who own the game have actually played it, so if I extrapolate wildly, maybe 17,000 people have played it.

But I don't see anyone _talk_ about it outside of my immediate circles, which feels a bit weird.  Maybe?  I'm not sure what the "normal" amount of conversation about an admittedly niche game is.  I don't know how things really spread by word of mouth, and I thought this might be an opportunity to gleam some insight about that, but it has not visibly materialized even though the game is being bought by people I don't personally know.

On the one hand, it's a sex game, so many folks are less likely to talk about it.  (A couple people even specifically asked if Steam has a way to hide what game you're playing from your friends — and, alas, it does not.)  On the other hand, it's a _furry_ sex game, and furries are traditionally not so tight-lipped.

Maybe there's not that much to say; the impact it's had on people I know has been fairly personal, and if it didn't have that kind of impact then it's just a cute little story game.

## Lessons learned

I have no idea.  There are so many confounding factors here that I don't know how to conclude anything.

I guess I'm pleasantly surprised by how many people bought a fairly short game for $7.  As it turns out, people will give you money for a thing if you ask for it?  That's nice to know.

Releasing on Steam is such a huge pain in the ass lol.

Sales spiked right at the beginning and then flattened fairly quickly, but it still sells a few copies a week, so it looks like it'll be a little trickle of income for a while.  It'd be cool to get a few medium-sized games on Steam as an extra source of income.  I suspect porn games have a bit more staying power, too.

Writing UI by hand sucks ass.  I gotta switch to Godot asap.
