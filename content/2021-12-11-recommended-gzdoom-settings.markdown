title: Recommended GZDoom settings
date: 2021-12-11 18:58
category: blog
tags: tech, doom

[GZDoom](https://zdoom.org/index) is the fanciest way to play Doom.  Unfortunately, it has also historically been difficult to recommend to newcomers, because its default settings are...  _questionable_.

Conspicuously, for over a decade, it defaulted to traditional Doom movement keys (no WASD) and no mouselook.  I am _overjoyed_ to discover that this is no longer the case, and it plays like a god damn FPS out of the box, but there are still a few twiddles that need twiddling.  Mostly the texture filtering.  Christ, the texture filtering.

Anyway GZDoom has a lot of options, so here is a handy list of the important ones.  There are fewer than I expected, which is good.

<!-- more -->

----

Note that the routes given to the various settings are for the _full_ options menu.  Out of the box, GZDoom shows a reduced options menu, _because it has a lot of options_.  You can get to the full menu from `Full options menu` near the bottom, and from there turn off the simple menu (if you want).  If you get lost, you can also use the option search.

Also, virtually every setting in GZDoom takes effect _instantly_, even while the menu is still visible.  (That's why there are no screenshots here!  Just try stuff out yourself.)  It remembers where your cursor was, too, so you can exit the menu to try stuff out, then bring it back up and mash Enter a few times to get back to where you were.


## Absolute necessities

I do not understand how anyone could argue with these.

- **Disable texture filtering.**

    `Display options > Texture options > Texture filter mode: None (linear mipmap)`

    By default, GZDoom uses linear upscaling on all sprites and textures, turning them into a blurry mess.  This is objectively ludicrous, since the sprites and textures are _pixel art_.

    `None` restores the crispy aesthetic that God intended — and when I say God, I of course mean John Carmack.  No, wait, maybe I mean Adrian Carmack?

    The "linear mipmap" bit means that GZDoom will still use linear _downscaling_, so that distant textures still somewhat resemble the actual texture and do not simply collapse into a pixel of arbitrary color.  If you find this objectionable, you may of course simply set it to `None`.

- **Fix the lighting.**

    `Display options > Hardware renderer > Sector light mode: Doom`

    GZDoom has half a dozen different lighting models (for...  some reason), all of which are way off from how Doom actually looked, except for this one.

- **Fix the partial invisibility effect.**

    `Display options > Hardware renderer > Fuzz style: Software`

    GZDoom defaults to rendering spectres (the harder-to-see variants of the pink demons) with a sort of translucent effect, which is _easier_ to see, which sort of defeats the purpose of making them harder to see.

    This will emulate the appearance of the original game, scaled up to big chunky pixels.  I actually prefer `Smooth fuzz`, which fits better at high resolutions and still looks like a rendering error, but pretty much anything is better than the `Shadow` default.

    For testing purposes, it may help to pop open the console with the backtick key (top left) and type `summon spectre` to...  well, summon a spectre.

And if all you want is something that looks kinda like Doom, you're done!  Feel free to stop reading here.

If you're pickier...


## My own preferences

These are also all correct.

- **Always run.**

    `Player setup > Always run: on`

    I don't know why you would walk anywhere in Doom.  We're in a fucking hurry, man.  There are _demons_.

    While you're here, you may want to set your `gender` as appropriate to fix pronouns in obituary messages.  You can also turn autoaim down, or off.

- **Show a crosshair.**

    `HUD options > Default crosshair: Cross 2`  
    `HUD options > Scale crosshair: 0.00`

    I just feel better with a little symbol in the middle of the screen.  I'm holding all my guns at chest height, for some reason, so the sights on those are useless.

    By default the crosshair is humongous, though, hence the scaling.

- Speaking of which, **fix the HUD scale.**

    `HUD options > Scaling options > User interface scale: 3`

    The automatic setting is _okay_ (and better than it used to be), but still leaves some things like pickup messages and the console as microscopic.  I play in a 1080p window on a 1440p monitor, and this seems nice for me.  Adjust as desired.

- **Use the alternative HUD.**

    `HUD options > Alternative HUD > Enable alternative HUD: On`

    You'll need to press <kbd>+</kbd> until the status bar disappears to actually see it.

    The alternative HUD shows you everything you need to know about the state of the game, while consuming minimal space and still letting you see the weapon sprites in their full glory.  It also shows you a count of kills and secrets, so you have some idea of the progress you've made.  _And_ it tells you a few things that you had to keep track of yourself in vanilla Doom, like what color of armor you have and whether you have the berserk fist.

    (This replaces a stock fullscreen-with-info HUD that didn't exist in vanilla Doom, but which only shows you health, armor, keys, and ammo for your current weapon.  Note that if you play a WAD that heavily alters the game, there's a chance it will add custom stuff to the stock HUD, and that stuff _will not appear_ on the alternative HUD.  It's explicitly not moddable.)

- **Draw shadows in corners.**

    `Display options > Hardware renderer > Postprocessing > Ambient occlusion quality: Medium`

    Doom has static lighting that affects the walls and floor equally, so the transition from wall to floor/ceiling is pretty flat.  A little AO helps that stand out, even if ambient occlusion is a fake idea.

- **Fix fake contrast.**

    `Display options > Use fake contrast: Smooth`

    "Fake contrast" refers to a clever trick in the Doom engine wherein horizontal (as seen on the automap) walls draw darker than the room, and vertical walls draw lighter.  In rectangular rooms, this helps avoid the "flat" feeling mentioned previously.

    Unfortunately, with complex geometry — as you see frequently in modern maps, but also occasionally in the original ones — this can backfire.  I've been fooled into thinking one particular wall in a curved hallway is a secret, just because it happened to be vertical and appeared lighter than its neighbors.  Meanwhile, rooms at a slant don't benefit at all.

    `Smooth` preserves the effect, but gradually transitions between the original effect for orthogonal walls and normal lighting for walls at a 45° angle.  (That is, a wall at a 22.5° angle will have half the fake contrast effect.)

- **Turn on antialiasing.**

    `Display options > Hardware renderer > Postprocessing > FXAA quality: Low`

    This smooths out lines in the geometry (or straight horizontal lines in textures) when drawn at an angle, without sacrificing those crunchy pixels.

- **Use particles.**

    `Display options > Hardware renderer > Particle style: Round`  
    `Display options > Rocket trails: Particles`  
    `Display options > Blood type: Sprites & particles`  
    `Display options > Bullet puff type: Sprites & particles`

    The default particles are linear filtered, which looks awful, but I don't think anything uses particles by default so you'd never notice.  You can also set them to `Square`, but I think having a single pixel floating in the air looks a bit silly.

    Adding particles to blood splatters and bullet puffs just looks nice.  I replace the rocket trails entirely because the original Doom rocket cloud is just kinda big and clumsy and ugly.

- **Enable dynamic lighting.**

    This is on by default...  sort of.  GZDoom needs to be able to find the `lights.pk3` and `brightmaps.pk3` files bundled with it, but if it runs at all, it probably knows where they are.

    So all you have to do is check `Load lights` and `Load brightmaps` in the little dialog you get when launching the game.

    _Probably_.  See, for some reason, those checkboxes are only there on Windows — in fact, I didn't know they existed at all until two minutes ago.  Even though they set a config setting, they aren't accessible via the options menu.  So if that doesn't work for you for whatever reason, try popping open the console and doing:

    ```
    autoloadlights true
    autoloadbrightmaps true
    ```

    Then restart the game.  Glowing objects should now cast (fairly subtle!) light on nearby walls.  You can see this immediately in Doom II's first map — there should be a green glow on the floor underneath the armor bonus in the far right corner of the room.  Or for a more dramatic demonstration, `IDKFA` and fire a rocket.

    It's just a nice touch.  And unlike many attempts to add dynamic lighting to Doom, it's not so over-the-top as to be distracting.


## For the extremely ornery

At the other end of the scale, there are those who want an experience as close as possible to vanilla Doom.  Those people might just want to use a port closer to vanilla, like a PRBoom variant or even Chocolate Doom, but GZDoom is willing to do its best:

- **Quantize light levels.**

    `Display options > Hardware renderer > Banded SW lightmode: On`

    Doom maps support light levels from 0 to 255, but in practice, Doom only understood...  16, I think?  That's because it was a paletted game, and it needed a colormap telling it how to darken each color while still sticking to the palette.  The game only shipped with 15 such mappings, probably because 255 of them would have been ludicrous, and thus there are only 16 light levels in practice.

    GZDoom's hardware renderer isn't bound by a palette, so it happily supports all 256 light levels.  If you can't stand this, well, it can simulate 16 for you.

- **Disable the hardware renderer altogether.**

    `Set video mode > Render mode: True color SW renderer`

    If the very notion of accelerated rendering offends you, the original core of Doom's renderer is still in there, just waiting for you.  All you need do is turn it on.  Note that this will severely restrict your ability to mouselook and will draw without vertical perspective, as the Doom renderer was designed around drawing vertical lines.

    What's that?  Even true color is too much?  You need the paletted glory that was the best a 386 could do?  Well, `Doom software renderer` is also an option.

- **Disable mouselook.**

    `Mouse options > Always mouselook: Off`

    Doom didn't support looking up and down.  Why should you?

    Despite the name, this still allows you to look around _horizontally_.  I guess technically that's turning, not looking.  Also, moving the mouse up and down will now move you (slowly) forwards or backwards.

- **Disable WASD.**

    `Customize controls > Preferred keyboard layout: Classic ZDoom`, then `Reset to defaults`

    Okay now you have gone too far.  This restores the very keyboard bindings I wanted to rally against — arrow keys to move, turning by default, <kbd>Alt</kbd> to strafe...

- **Disable teleporter zoom.**

    `Display options > Teleporter zoom: Off`

    GZDoom does a brief zoom-in effect on your field of view after (non-silent) teleporting.  Looks sick.  If you hate it, here's how to turn it off.

- **Restore the vanilla lite-amp goggles.**

    `Display options > Hardware renderer > Enhanced night vision mode: Off`

    In vanilla Doom, the lite-amp goggles simply make the entire world render as fullbright, which looks fucking terrible.  GZDoom defaults to a "night vision goggles" sort of effect that also highlights objects, but if you really can't stand that, this twiddle is here for you.

- **Enable randomized pitch on sound effects.**

    `Sound options > Randomize pitches: On`

    For the _very_ ornery, I believe this behavior was in the original release of Doom but (accidentally?) broken in Doom 1.2 and all later versions.  It's really weird, but it's the intended behavior, I guess!

- **Restore Doom's automap colors.**

    `Automap options > Map color set: Traditional Doom`

    This will change the automap back to its red-and-yellow-on-black glory.

    It will also remove the colors that tell you where locked doors and the exit are.  You might argue that those are cheating.  I argue that they are the entire point of a map.

    You can also turn off the automap's monster and secret counts here if you truly wish to be as lost as possible.

- **Twiddle with compatibility settings.**

    `Compatibility options > Compatibility mode: ?`

    You might want `Doom (strict)` for the closest vanilla experience that GZDoom can provide.  _Might_.  The most notable effects are:

    - Monsters will wake up when seeing a player with a blur sphere.  By default, they usually won't, a behavior inherited from Hexen.
    - Arch-viles can resurrect crushed corpses as "ghosts" that cannot be shot, only harmed by splash damage from rockets.
    - Pain elementals will be unable to spawn new lost souls if there are at least 21 already present in the level.
    - Monsters can't be knocked off of high ledges.
    - You will be unable to crowdsurf, meaning you will be blocked both by imps at the foot of a cliff below you, and by cacodemons flying above you.

    You can also toggle these on or off individually at your leisure.
