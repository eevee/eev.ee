title: Cheezball Rising: Main loop, input, and a game
date: 2018-07-05 09:41
category: blog
tags: tech, gamedev, cheezball rising

This is a series about [**Star Anise Chronicles: Cheezball Rising**](https://github.com/eevee/anise-cheezball-rising), an expansive adventure game about my cat for the Game Boy Color.  Follow along as I struggle to make something with this bleeding-edge console!
 
GitHub has [intermittent prebuilt ROMs](https://github.com/eevee/anise-cheezball-rising/releases), or you can get them a week early [on Patreon](https://www.patreon.com/eevee/posts?tag=cheezball%20rising) if you pledge $4.  More details in the [README](https://github.com/eevee/anise-cheezball-rising)!

----

In this issue, I fill in the remaining bits necessary to have something that _looks_ like a game.

Previously: [drawing a sprite]({filename}/2018-06-21-cheezball-rising-drawing-a-sprite.markdown).

<!-- more -->


## Recap

So far, I have this.

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/102-first-object.png" alt="A very gaudy striped background with half a cat on top">
</div>

It took unfathomable amounts of effort, but it's something!  Now to improve this from a static image to something a bit more game-like.

**Quick note**: I've been advised to use the de facto standard [`hardware.inc`](https://github.com/tobiasvl/hardware.inc) file, which gives symbolic names to all the registers and some of the flags they use.  I hadn't introduced it yet while doing the work described in this post, but for the sake of readability, I'm going to _pretend_ I did and use that file's constants in the code snippets here.


## Interrupts

To get much further, I need to deal with _interrupts_.  And to explain interrupts, I need to briefly explain _calls_.

Assembly doesn't really have functions, only addresses and jumps.  That said, the Game Boy does have `call` and `ret` instructions.  A `call` will push the PC register (_program counter_, the address of the current instruction) onto the stack and perform a jump; a `ret` will pop into the PC register, effectively jumping back to the source of the `call`.

There are no arguments, return values, or scoping; input and output must be mediated by each function, usually via registers.  Of course, since registers are global, a "function" might trample over their values in the course of whatever work it does.  A function can manually `push` and `pop` 16-bit register pairs to preserve their values, or leave it up to the caller for speed/space reasons.  All the conventions are free for me to invent or ignore.  A "function" can even jump directly to another function and piggyback on the second function's `ret`, kind of like Perl's `goto &sub`…  which I realize is probably less common knowledge than how call/return work in assembly.

Interrupts, then, are calls that can happen at any time.  When one of a handful of conditions occurs, the CPU can immediately (or, rather, just before the next instruction) call an interrupt _handler_, regardless of what it was already doing.  When the handler returns, execution resumes in the interrupted code.

Of course, since they might be called _anywhere_, interrupt handlers need to be very careful about preserving the CPU state.  Pushing `af` is especially important (and this is the one place where `af` is used as a pair), because `a` is necessary for getting almost anything done, and `f` holds the flags which most instructions will invisibly trample.

Naturally, I completely forgot about this the first time around.

The Game Boy has five interrupts, each with a handler at a fixed address very low in ROM.  Each handler only has room for eight bytes' worth of instructions, which is enough to do a very tiny amount of work — or to just jump elsewhere.

A good start is to populate each one with only the `reti` instruction, which returns as usual _and_ re-enables interrupts.  The CPU disables interrupts when it calls an interrupt handler (so they thankfully can't interrupt themselves), and returning with only `ret` will leave them disabled.

Naturally, I completely forgot about this the first time around.

```rgbasm
; Interrupt handlers
SECTION "Vblank interrupt", ROM0[$0040]
    ; Fires when the screen finishes drawing the last physical
    ; row of pixels
    reti

SECTION "LCD controller status interrupt", ROM0[$0048]
    ; Fires on a handful of selectable LCD conditions, e.g.
    ; after repainting a specific row on the screen
    reti

SECTION "Timer overflow interrupt", ROM0[$0050]
    ; Fires at a configurable fixed interval
    reti

SECTION "Serial transfer completion interrupt", ROM0[$0058]
    ; Fires when the serial cable is done?
    reti

SECTION "P10-P13 signal low edge interrupt", ROM0[$0060]
    ; Fires when a button is released?
    reti
```

These will do nothing.  I mean, obviously, but they'll do even _less_ than nothing until I enable them.  Interrupts are enabled by the dedicated `ei` instruction, which enables any interrupts whose corresponding bit is set in the IE register ($ffff).

So…  which one do I want?


## Game loop

To have a game, I need a game loop.  The basic structure of pretty much any loop looks like:

1. Load stuff.
2. Check for input.
3. Update the game state.
4. Draw the game state.
5. GOTO 2

(If you've never seen a real game loop written out before, [LÖVE's default loop](https://love2d.org/wiki/love.run) is a good example, though even a huge system like Unity follows [the same basic structure](https://docs.unity3d.com/Manual/ExecutionOrder.html).)

The Game Boy seems to introduce a wrinkle here.  I don't actually draw anything myself; rather, the hardware does the drawing, and I tell it _what_ to draw by using the palette registers, OAM, and VRAM.

But in fact, this isn't too far off from how LÖVE (or Unity) works!  All the drawing I do is applied to a buffer, not the screen; once the drawing is complete, the main loop calls `present()`, which _waits until vblank_ and then draws the buffer to the screen.  So what you see on the screen is delayed by up to a frame, and the loop really has an extra "wait for vsync" step at 3½.  Or, with a little rearrangement:

1. Load stuff.
2. Wait for vblank.
3. Draw the game state.
4. Check for input.
5. Update the game state.
6. GOTO 2

This is approaching something I can implement!  It works out especially well because it does all the drawing as early as possible during vblank.  That's good, because the LCD operation looks something like this:

```
LCD redrawing...
LCD redrawing...
LCD redrawing...
LCD redrawing...
VBLANK
LCD idle
LCD idle
```

While the LCD is refreshing, I can't (easily) update anything it might read from.  I only have free control over VRAM et al. during a short interval after vblank, so I need to do all my drawing work _right then_ to ensure it happens before the LCD starts refreshing again.  Then I'm free to update the world while the LCD is busy.

First, right at the entry point, I enable the vblank interrupt.  It's bit 0 of the IE register, but `hardware.inc` has me covered.

```rgbasm
main:
    ; Enable interrupts
    ld a, IEF_VBLANK
    ldh [rIE], a
    ei
```

Next I need to make the handler actually do something.  The obvious approach is for the handler to call one iteration of the game loop, but there are a couple problems with that.  For one, interrupts are disabled when a handler is called, so I would never get any _other_ interrupts.  I could explicitly re-enable interrupts, but that raises a bigger question: what happens if the game lags, and updating the world takes longer than a frame?  With this approach, the game loop would _interrupt itself_ and then either return back into itself somewhere and cause untold chaos, or take too long again and eventually overflow the stack.  Neither is appealing.

An alternative approach, which I found in [gb-template](https://github.com/exezin/gb-template) but only truly appreciated after some thought, is for the vblank handler to set a flag and immediately return.  The game loop can then _wait_ until the flag is set before each iteration, just like LÖVE does.  If an update takes longer than a frame, no problem: the loop will always wait until the _next_ vblank, and the game will simply run more slowly.

```rgbasm
SECTION "Vblank interrupt", ROM0[$0040]
    push hl
    ld hl, vblank_flag
    ld [hl], 1
    pop hl
    reti

...

SECTION "Important twiddles", WRAM0[$C000]
; Reserve a byte in working RAM to use as the vblank flag
vblank_flag:
    db
```

The handler fits in eight bytes — the linker would yell at me if it didn't, since another section starts at $0048! — and leaves all the registers in their previous states.  As I mentioned before, I originally neglected to preserve registers, and some _zany things_ started to happen as `a` and `f` were abruptly altered in the middle of other code.  Whoops!

Now the main loop can look like this:

```rgbasm
main:
    ; ... bunch of setup code ...

vblank_loop:
    ; Main loop: halt, wait for a vblank, then do stuff

    ; The halt instruction stops all CPU activity until the
    ; next interrupt, which saves on battery, or at least on
    ; CPU cycles on an emulator's host system.
    halt
    ; The Game Boy has some obscure hardware bug where the
    ; instruction after a halt is occasionally skipped over,
    ; so every halt should be followed by a nop.  This is so
    ; ubiquitous that rgbasm automatically adds a nop after
    ; every halt, so I don't even really need this here!
    nop

    ; Check to see whether that was a vblank interrupt (since
    ; I might later use one of the other interrupts, all of
    ; which would also cancel the halt).
    ld a, [vblank_flag]
    ; This sets the zero flag iff a is zero
    and a
    jr z, vblank_loop
    ; This always sets a to zero, and is shorter (and thus
    ; faster) than ld a, 0
    xor a, a
    ld [vblank_flag], a

    ; Use DMA to update object attribute memory.
    ; Do this FIRST to ensure that it happens before the screen starts to update again.
    call $FF80

    ; ... update everything ...

    jp vblank_loop
```

It's looking all the more convenient that I have my own copy of OAM — I can update it whenever I want during this loop!  I might need similar facilities later on for editing VRAM or changing palettes.


## Doing something and reading input

I have a loop, but since nothing's _happening_, that's not especially obvious.  Input would take a little effort, so I'll try something simpler first: making Anise move around.

I don't actually track Anise's _position_ anywhere right now, except for in the OAM buffer.  Good enough.  In my main loop, I add:

```rgbasm
    ld hl, oam_buffer + 1
    ld a, [hl]
    inc a
    ld [hl], a
```

The second byte in each OAM entry is the x-coordinate, and indeed, this causes Anise's torso to glide rightwards across the screen at 60ish pixels per second.  Eventually the x-coordinate overflows, but that's fine; it wraps back to zero and moves the sprite back on-screen from the left.

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/02a-anise-slide.gif" alt="The half-cat is now sliding across the screen">
</div>

Excellent.  I mean, sorry, this is _extremely_ hard to look at, but bear with me a second.

This would be a _bit_ more game-like if I could control it with the buttons, so let's read from them.

There are eight buttons: up, down, left, right, A, B, start, select.  There are also eight bits in a byte.  You might suspect that I can simply read an I/O register to get the current state of all eight buttons at once.

Ha, ha!  You naïve fool.  Of _course_ it's more convoluted than that.  That single byte thing is a pretty good idea, though, so what I'll do is read the input at the start of the frame and coax it into a byte that I can consult more easily later.

Turns out I pretty much _have_ to do that, because button access is slightly flaky.  Even the official manual advises reading the buttons several times to get a reliable result.  Yikes.

Here's how to do it.  The buttons are wired in two groups of four: the dpad and everything else.  Reading them is thus also done in two groups of four.  I need to use the P1 register, which I assume is short for "player 1" and is so named because the people who designed this hardware had also designed the two-player NES?

Bits 5 and 6 of P1 determine which set of four buttons I want to read, and then the lower nybble contains the state of those buttons.  Note that each bit is set to 1 if the button is _released_; I think this is a quirk of how they're wired, and what I'm doing is extremely direct hardware access.  Exciting!  (Also very confusing on my first try, where Anise's movement was inverted.)

The code, which is very similar to an example in the official manual, thus looks like this:

```rgbasm
    ; Poll input
    ; The direct hardware access is nonsense and unreliable, so
    ; just read once per frame and stick all the button states
    ; in a byte

    ; Bit 6 means to read the dpad
    ld a, $20
    ldh [rP1], a
    ; But it's unreliable, so do it twice
    ld a, [rP1]
    ld a, [rP1]
    ; This is 'complement', and flips all the bits in a, so now
    ; set bits will mean a button is held down
    cpl
    ; Store the lower four bits in b
    and a, $0f
    ld b, a

    ; Bit 5 means to read the buttons
    ld a, $10
    ldh [rP1], a
    ; Apparently this is even more unreliable??  No, really, the
    ; manual does this: two reads, then six reads
    ld a, [rP1]
    ld a, [rP1]
    ld a, [rP1]
    ld a, [rP1]
    ld a, [rP1]
    ld a, [rP1]
    ; Again, complement and mask off the lower four bits
    cpl
    and a, $0f
    ; b already contains four bits, so I need to shift something
    ; left by four...  but the shift instructions only go one
    ; bit at a time, ugh!  Luckily there's swap, which swaps the
    ; high and low nybbles in any register
    swap a
    ; Combine b's lower nybble with a's high nybble
    or a, b
    ; And finally store it in RAM
    ld [buttons], a

...

SECTION "Important twiddles", WRAM0[$C000]
vblank_flag:
    db
buttons:
    db
```

Phew.  That was a bit of a journey, but now I have the button state as a single byte.  To help with reading the buttons, I'll also define a few constants labeling the individual bits.  (There are instructions for reading a particular bit by number, so I don't need to mask a single bit out.)

```rgbasm
; Constants
BUTTON_RIGHT  EQU 0
BUTTON_LEFT   EQU 1
BUTTON_UP     EQU 2
BUTTON_DOWN   EQU 3
BUTTON_A      EQU 4
BUTTON_B      EQU 5
BUTTON_START  EQU 6
BUTTON_SELECT EQU 7
```

Now to adjust the sprite position based on what directions are held down.  Delete the old code and replace it with:

```rgbasm
    ; Set b/c to the y/x coordinates
    ld hl, oam_buffer
    ld b, [hl]
    inc hl
    ld c, [hl]

    ; This sets the z flag to match a particular bit in a
    bit BUTTON_LEFT, a
    ; If z, the bit is zero, so left isn't held down
    jr z, .skip_left
    ; Otherwise, left is held down, so decrement x
    dec c
.skip_left:

    ; The other three directions work the same way
    bit BUTTON_RIGHT, a
    jr z, .skip_right
    inc c
.skip_right:
    bit BUTTON_UP, a
    jr z, .skip_up
    dec b
.skip_up:
    bit BUTTON_DOWN, a
    jr z, .skip_down
    inc b
.skip_down:

    ; Finally, write the new coordinates back to the OAM
    ; buffer, which hl is still pointing into
    ld [hl], c
    dec hl
    ld [hl], b
```

Miraculously, Anise's torso now moves around on command!

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/02b-anise-slide-dpad.gif" alt="The half-cat is now moving according to button presses">
</div>

Neat!  But this still looks really, really, incredibly bad.


## Aesthetics

It's time to do something about this artwork.

First things first: I'm really tired of writing out colors _by hand_, _in binary_, so let's fix that.  In reality, I did this bit _after_ adding better art, but doing it first is better for everyone.

I think I've mentioned before that rgbasm has (very, very rudimentary) support for macros, and this seems like a perfect use case for one.  I'd like to be able to write colors out in typical `rrggbb` hex fashion, so I need to convert a 24-bit color to a 16-bit one.

```rgbasm
dcolor: MACRO  ; $rrggbb -> gbc representation
_r = ((\1) & $ff0000) >> 16 >> 3
_g = ((\1) & $00ff00) >> 8  >> 3
_b = ((\1) & $0000ff) >> 0  >> 3
    dw (_r << 0) | (_g << 5) | (_b << 10)
    ENDM
```

This is going to need a whole _paragraph_ of caveats.

A macro is contained between `MACRO` and `ENDM`.  The assembler has a curious sort of universal assignment syntax, where even ephemeral constructs like macros are introduced by labels.  Macros can take arguments, but they aren't declared; they're passed more like arguments to shell scripts, where the first argument is `\1` and so forth.  (There's even a `SHIFT` command for accessing arguments beyond the ninth.)  Also, passing strings to a macro is some kind of byzantine nightmare where you have to slap backslashes in just the right places and I will probably avoid doing it altogether if I can at all help it.

Oh, one other caveat: compile-time assignments like I have above _must start in the first column_.  I believe this is because assignments are _also_ labels, and labels have to start in the first column.  It's a bit weird and apparently rgbasm's lexer is horrifying, but I'll take it over writing my own assembler and stretching this project out any further.

Anyway, all of that lets me write `dcolor $ff0044` somewhere and have it translated at compile time to the appropriate 16-bit value.  (I used `dcolor` to parallel `db` and friends, but I'm strongly considering using CamelCase exclusively for macros?  Guess it depends how heavily I use them.)

With that on hand, I can now doodle some little sprites in [Aseprite](https://www.aseprite.org/) and copy them in.  This part is not especially interesting and involves a lot of squinting at zoomed-in sprites.

```rgbasm
SECTION "Sprites", ROM0
PALETTE_BG0:
    dcolor $80c870  ; light green
    dcolor $48b038  ; darker green
    dcolor $000000  ; unused
    dcolor $000000  ; unused
PALETTE_ANISE:
    dcolor $000000  ; TODO
    dcolor $204048
    dcolor $20b0b0
    dcolor $f8f8f8
GRASS_SPRITE:
    dw `00000000
    dw `00000000
    dw `01000100
    dw `01010100
    dw `00010000
    dw `00000000
    dw `00000000
    dw `00000000
EMPTY_SPRITE:
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
ANISE_SPRITE:
    ; ... I'll revisit this momentarily
```

Gorgeous.  You may notice that I put the colors as _data_ instead of inlining them in code, which incidentally makes the code for setting the palette vastly shorter as well:

```rgbasm
    ; Start setting the first color, and advance the internal
    ; pointer on every write
    ld a, %10000000
    ; BCPS = Background Color Palette Specification
    ldh [rBCPS], a

    ld hl, PALETTE_BG0
    REPT 8
    ld a, [hl+]
    ; Same, but Data
    ld [rBCPD], a
    ENDR
```

Loading sprites into VRAM also becomes a bit less of a mess:

```rgbasm
    ; Load some basic tiles
    ld hl, $8000

    ; Read the 16-byte empty sprite into tile 0
    ld bc, EMPTY_SPRITE
    REPT 16
    ld a, [bc]
    inc bc
    ld [hl+], a
    ENDR

    ; Read the grass sprite into tile 1, which immediately
    ; follows tile 0, so hl is already in the right place
    ld bc, GRASS_SPRITE
    REPT 16
    ld a, [bc]
    inc bc
    ld [hl+], a
    ENDR
```

Someday I should write an actual copy function, since at the moment, I'm using an alarming amount of space for pointlessly unrolled loops.  Maybe later.

You may notice I now have _two_ tiles, whereas before I was relying on filling the entire screen with _one_ tile, tile 0.  I want to dot the landscape with tile 1, which means writing a bit more to the actual background grid, which begins at $9800 and has one byte per tile.

```rgbasm
    ; Fill the screen buffer with a pattern of grass tiles,
    ; where every 2x2 block has a single grass at the top left.
    ; Note that the buffer is 32x32 tiles, and it ends at $9c00
    ld hl, $9800
.screen_fill_loop:
    ; Use tile 1 for every other tile in this row.  Note that
    ; REPTed part increments hl /twice/, thus skipping a tile
    ld a, $01
    REPT 16
    ld [hl+], a
    inc hl
    ENDR
    ; Skip an entire row of 32 tiles, which will remain empty.
    ; There is almost certainly a better way to do this, but I
    ; didn't do it.  (Hint: it's ld bc, $20; add hl, bc)
    REPT 32
    inc hl
    ENDR
    ; If we haven't reached $9c00 yet, continue looping
    ld a, h
    cp a, $9C
    jr c, .screen_fill_loop
```

Sorry for all these big blocks of code, but _check out this payoff_!

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/02c-grass-background.png" alt="A very simple grassy background">
</div>

POW!  Gorgeous.

And hey, why stop there?  With a little more pixel arting against a very reduced palette...

```rgbasm
SPRITE_ANISE_FRONT_1:
    dw `00000111
    dw `00001222
    dw `00012222
    dw `00121222
    dw `00121122
    dw `00121111
    dw `00121122
    dw `00121312
    dw `00121313
    dw `00012132
    dw `00001211
    dw `00000123
    dw `00100123
    dw `00011133
    dw `00000131
    dw `00000010
SPRITE_ANISE_FRONT_2:
    dw `11100000
    dw `22210000
    dw `22221000
    dw `22212100
    dw `22112100
    dw `11112100
    dw `22112100
    dw `21312100
    dw `31312100
    dw `23121000
    dw `11210000
    dw `32100000
    dw `32100000
    dw `33100000
    dw `13100000
    dw `01000000
```

Yes, I am having trouble deciding on a naming convention.

This is now a 16×16 sprite, made out of two 8×16 parts.  This post has enough code blocks as it is, and the changes to make this work are relatively minor copy/paste work, so the quick version is:

1. Set the LCDC flag (bit 2, or `LCDCF_OBJ16`) that makes objects be 8×16.  This mode uses pairs of tiles, so an object that uses either tile 0 or 1 will draw both of them, with tile 0 on top of tile 1.
2. Extend the code that loads object tiles to load _four_ instead.
3. Define a second sprite that's 8 pixels to the right of the first one.
4. Remove the hard-coded object palette, and instead load the `PALETTE_ANISE` that I sneakily included above.  This time the registers are called `rOCPS` and `rOCPD`.

Finally, extend the code that moves the sprite to also move the second half:

```rgbasm
    ; Finally, write the new coordinates back to the OAM
    ; buffer, which hl is still pointing into
    ld [hl], c
    dec hl
    ld [hl], b
    ; This bit is new: copy the x-coord into a so I can add 8
    ; to it, then store both coords into the second sprite's
    ; OAM data
    ld a, c
    add a, 8
    ; I could've written this the other way around, but I did
    ; not, I guess because this structure mirrors the above?
    ld hl, oam_buffer + 5
    ld [hl], a
    dec hl
    ld [hl], b
```

Cross my fingers, and…

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/02d-anise-move-grass.gif" alt="A little cat sprite atop the grassy background">
</div>

Hey hey hey!  That finally looks like something!


## To be continued

It was a surprisingly long journey, but this brings us more or less up to [commit `313a3e`](https://github.com/eevee/anise-cheezball-rising/commit/313a3e1aee596270530cc1bf40db3df2a1e69535), which happens to be the first commit I made a release of!  It's been more than a week, so you can grab it on [Patreon](https://www.patreon.com/posts/cheezball-rising-19556867) or [GitHub](https://github.com/eevee/anise-cheezball-rising/releases/tag/v20180619pre).  I strongly recommend playing it with a release of mGBA prior to 0.7, for…  reasons that will become clear next time.

Next time: I'll take a breather and clean up a few things.
