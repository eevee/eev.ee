title: Cheezball Rising: Drawing a sprite
date: 2018-06-21 12:50
category: blog
tags: tech, gamedev, cheezball rising

This is a series about **Star Anise Chronicles: Cheezball Rising**, an expansive adventure game about my cat for the Game Boy Color.  Follow along as I struggle to make something with this bleeding-edge console!

<center markdown="1">[source code](https://github.com/eevee/anise-cheezball-rising) • [prebuilt ROMs](https://www.patreon.com/eevee/posts?tag=cheezball%20rising) (a week early for $4) • works best with [mGBA](https://mgba.io/)</center>

In this issue, I figure out how to draw a sprite.  _This part was hard._

Previously: [figuring out how to put literally anything on the goddamn screen]({filename}/2018-06-19-cheezball-rising-a-new-game-boy-color-game.markdown).

<!-- more -->


## Recap

Welcome back!  I've started cobbling together a Pygments lexer for RGBDS's assembly flavor, so hopefully the code blocks are more readable, and will become moreso over time.

When I left off last time, I had...  um...  this.

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/003-color-gradient.png" alt="Vertical stripes of red, green, blue, and white">
</div>

This is all on the _background_ layer, which I mentioned before is a fixed grid of 8×8 tiles.

For anything that moves around freely, like the player, I need to use the _object_ layer.  So that's an obvious place to go next.

Now, if you remember, I can define _tiles_ by just writing to video RAM, and I define _palettes_ with a goofy system involving writing them one byte at a time to the same magic address.  You might expect defining _objects_ to do some third completely different thing, and you'd be right!


## Defining an object

Objects are defined in their own little chunk of RAM called OAM, for _object attribute memory_.  They're also made up of tiles, but each tile can be positioned at an arbitrary point on the screen.

OAM starts at $fe00 and each object takes four bytes — the y-coordinate, the x-coordinate, the tile number, and some flags — for a total of 160 bytes.  The coordinates are offset such that (8, 16) is the top-left of the screen, which both allows all zeroes to mean "no object" and allows for objects to be drawn partially offscreen.

Here's the fun part: I can't write directly to OAM?  I guess???  Come to think of it, I don't think the manual explicitly says I can't, but it's _strongly implied_.  Hmm.  I'll look into that.  But I didn't at the time, so I'll continue under the assumption that the following nonsense is necessary.

Because I "can't" write directly, I need to use some _shenanigans_.  First, I need something to write!  This is an Anise game, so let's go for Anise.

I'm on my laptop at this point without access to the source code for the LÖVE Anise game I started, so I have to rustle up a screenshot I took.

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/hi-def-star-anise.png" alt="Cropped screenshot of Star Anise and some critters, all pixel art">
</div>

Wait a second.

Even on the Game Boy Color, tiles are defined with two bits per pixel.  That means an 8×8 tile has a maximum of four colors.  For objects, the first color is transparent, so I really have _three_ colors — which is exactly why most Game Boy Color protagonists have a main color, an outline/shadow color, and a highlight color.

Let's check out that Anise in more detail.

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/hi-def-star-anise-zoom.png" alt="Star Anise at 8×">
</div>

Hm yes okay that's more than three colors.  I guess I'm going to need to draw some new sprites from scratch, somehow.

In the meantime, I optimistically notice that Star Anise's body only uses three colors, _and_ it's 8×7!  I could make a tile out of that!  I painstakingly copy the pixels into a block of those backticks, which you can kinda see is his body if you squint a bit:

```rgbasm
SECTION "Sprites", ROM0
ANISE_SPRITE:
    dw `00000000
    dw `00001333
    dw `00001323
    dw `10001233
    dw `01001333
    dw `00113332
    dw `00003002
    dw `00003002
```

The `dw` notation isn't an opcode; it tells the assembler to put two literal bytes of data in the final ROM.  A _word_ of _data_.  (Each row of a tile is two bytes, remember.)

If you think about this too hard, you start to realize that both the data and code are _just bytes_, everything is arbitrary, and true meaning is found only in the _way_ we perceive things rather than in the things themselves.

Note I didn't specify an exact address for this section, so the linker will figure out somewhere to put it and make sure all the labels are right at the end.

Now I load this into tilespace, back in my main code:

```rgbasm
    ; Define an object
    ld hl, $8800
    ld bc, ANISE_SPRITE
    REPT 16
    ld a, [bc]
    ld [hl+], a
    inc bc
    ENDR
```

This copies 16 bytes, starting from the `ANISE_SPRITE` label, to $8800.

----

Why $8800, not $8000?  _I'm so glad you asked!_

There are actually _three_ blocks of tile space, each with enough room for 128 tiles: one at $8000, one at $8800, and one at $9000.  Object tiles always use the $8000 block followed by the $8800 block, whereas background tiles can use _either_ $8000 + $8800 or $9000 + $8800.  By default, background tiles use $8000 + $8800.

All of which is to say that I got very confused reading the manual (which spends like five pages explaining the above paragraph) and put the object tiles in the wrong place.  Whoops.  It's fine; this just ends up being tile 128.

In my partial defense, looking at it now, I see the manual is _wrong_!  Bit 4 of the LCD controller register ($ff40) controls whether the background uses tiles from $8000 + $8800 (1) or $9000 + $8800 (0).  The manual says that this register defaults to $83, which has bit 4 off, suggesting that background tiles use $9000 + $8800 (i.e. start at $8800), but disassembly of the boot ROM shows that it actually defaults to $91, which has bit 4 _on_.  Thanks a lot, Nintendo!

That was quite a diversion.  Here's a chart of where the dang tiles live.  Note that the block at $8800 is always shared between objects and background tiles.  Oh, and on the Game Boy Color, all three blocks are twice as big thanks to the magic of banking.  I'll get to banking...  much later.

```
                            bit 4 ON (default)  bit 4 OFF
                            ------------------  ---------
$8000   obj tiles 0-127     bg tiles 0-127
$8800   obj tiles 128-255   bg tiles 128-255    bg tiles 128-255
$9000                                           bg tiles 0-127
```

---

Hokay.  What else?  I'm going to need a palette for this, and I don't want to use that gaudy background palette.  Actually, I _can't_ — the background and object layers have two completely separate sets of palettes.

Writing an object palette is exactly the same as writing a background palette, except with different registers.

```rgbasm
    ; This should look pretty familiar
    ld a, %10000000
    ld [$ff6a], a

    ld bc, %0000000000000000  ; transparent
    ld a, c
    ld [$ff6b], a
    ld a, b
    ld [$ff6b], a
    ld bc, %0010110100100101  ; dark
    ld a, c
    ld [$ff6b], a
    ld a, b
    ld [$ff6b], a
    ld bc, %0100000111001101  ; med
    ld a, c
    ld [$ff6b], a
    ld a, b
    ld [$ff6b], a
    ld bc, %0100001000010001  ; white
    ld a, c
    ld [$ff6b], a
    ld a, b
    ld [$ff6b], a
```

Riveting!

I wrote out those colors by hand.  The original dark color, for example, was `#264a59`.  That uses eight bits per channel, but the Game Boy Color only supports five (a factor of 8 difference), so first I rounded each channel to the nearest 8 and got `#284858`.  Swap the channels to get `58 48 28` and convert to binary (sans the trailing zeroes) to get `01011 01001 00101`.

Note to self: probably write a macro or whatever so I can define colors like a goddamn human being.  Also why am I not putting the colors in a ROM section too?

Almost there.  I still need to write out those four bytes that specify the tile and where it goes.  I can't actually write them to OAM yet, so I need some scratch space in regular RAM — _working RAM_.

```rgbasm
SECTION "OAM Buffer", WRAM0[$C100]
oam_buffer:
    ds 4 * 40
```

The `ds` notation is another "data" variant, except it can take a size and reserves space for a whole _string_ of data.  Note that I didn't put any actual data here — this section is in RAM, which only exists while the game is running, so there'd be nowhere to _put_ data.

Also note that I gave an explicit address this time.  The buffer has to start at an address ending in 00, for reasons that will become clear momentarily.  The space from $c000 to $dfff is available as working RAM, and I chose $c100 for…  reasons that will also become clear momentarily.

Now to write four bytes to it at runtime:

```rgbasm
    ; Put an object on the screen
    ld hl, oam_buffer
    ; y-coord
    ld a, 64
    ld [hl+], a
    ; x-coord
    ld [hl+], a
    ; tile index
    ld a, 128
    ld [hl+], a
    ; attributes, including palette, which are all zero
    ld a, %00000000
    ld [hl+], a
```

(I tried writing directly to OAM on my first attempt.  Nothing happened!  Very exciting.)

But how to get this into OAM so it'll actually show on-screen?  For that, I need to do a _DMA transfer_.


## DMA

DMA, or _direct memory access_, is one of those things the Game Boy programming manual seems to think everyone is already familiar with.  It refers generally to features that allow some other hardware to access memory, without going through the CPU.  In the case of the Game Boy, it's used to copy data from working RAM to OAM.  _Only_ to OAM.  It's very specific.

Performing a DMA transfer is super easy!  I write the high byte of the _source_ address to the DMA register ($ff46), and then _some magic happens_, and 160 bytes from the source address appear in OAM.  In other words:

```rgbasm
    ld a, $c1       ; copy from $c100
    ld [$ff46], a   ; perform DMA transfer
    ; now $c000 through $c09f have been copied into OAM!
```

It's almost too good to be true!  And it is.  There are some wrinkles.

First, the transfer takes some time, during which I almost certainly don't want to be doing anything else.

Second, during the transfer, the CPU can only read from "high RAM" — $ff80 and higher.  Wait, uh oh.

The usual workaround here is to copy a very short function into high RAM to perform the actual transfer and wait for it to finish, then call _that_ instead of starting a transfer directly.  Well, that sounds like a pain, so I break my rule of accounting for every byte and [find someone else who's done it](https://exez.in/gameboy-dma).  Conveniently enough, that post is by the author of the [small template project](https://github.com/exezin/gb-template) I've been glancing at.

I end up with something like the following.

```rgbasm
    ; Copy the little DMA routine into high RAM
    ld bc, DMA_BYTECODE
    ld hl, $ff80
    ; DMA routine is 13 bytes long
    REPT 13
    ld a, [bc]
    inc bc
    ld [hl+], a
    ENDR

; ...

SECTION "DMA Bytecode", ROM0
DMA_BYTECODE:
    db $F5, $3E, $C1, $EA, $46, $FF, $3E, $28, $3D, $20, $FD, $F1, $D9
```

That's compiled assembly, written inline as bytes.  Oh boy.  The original code looks like:

```rgbasm
    ; start the transfer, as shown above
    ld a, $c1
    ld [$ff46], a

    ; wait 160 cycles/microseconds, the time it takes for the
    ; transfer to finish; this works because 'dec' is 1 cycle
    ; and 'jr' is 3, for 4 cycles done 40 times
    ld      a, 40
loop:
    dec     a
    jr      nz, loop

    ; return
    ret
```

Now you can see why I used $c100 for my OAM buffer: because it's the address this person used.

(Hm, the [opcode reference](http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html) I usually use seems to have all the timings multiplied by a factor of 4 without comment?  Odd.  The rgbds [reference](https://rednex.github.io/rgbds/gbz80.7.html) is correct.)

(Also, here's a fun fact: the stack starts at $fffe and grows backwards.  If it grows too big, the very first thing it'll overwrite is this DMA routine!  I bet that'll have some fun effects.)

At this point I have a thought.  (Okay, I had the thought a bit later, but it works better narratively if I have it now.)  I've already demonstrated that the line between code and data is a bit fuzzy here.  So _why does this code need to be pre-assembled_?

And a similar thought: why is the length hardcoded?  Surely, we can do a little better.  What if we shuffle things around a bit...

```rgbasm
SECTION "init", ROM0[$0100]
    nop
    ; Jump to a named label instead of an address
    jp main

SECTION "main", ROM0[$0150]
; DMA copy routine, copied into high RAM at startup.
; Never actually called where it is.
dma_copy:
    ld a, $c1
    ld [$ff46], a
    ld a, 40
.loop:
    dec a
    jr nz, .loop
    ret
dma_copy_end:
    nop

main:
    ; ... all previous code is here now ...

    ; Copy the little DMA routine into high RAM
    ld bc, dma_copy
    ld hl, $ff80
    ; DMA routine is 13 bytes long
    REPT dma_copy_end - dma_copy
    ld a, [bc]
    inc bc
    ld [hl+], a
    ENDR
```

This is very similar to what I just had, except that the code is left as _code_, and its length is computed by having another label at the end — so I'm free to edit it later if I want to.  It all ends up as bytes in the ROM, so the code ends up exactly the same as writing out the bytes with `db`.  Come to think of it, I don't even need to hardcode the `$c1` there; I could replace it with `oam_buffer >> 8` and avoid repeating myself.

(I put the code at $0150 because rgbasm can't subtract labels that appear later in the same source file — I presume because this is done by the single-pass assembler, not the linker — and it just seemed weird to have a floating section lexically _before_ the entry point.)

I'm actually surprised that the author of the above post didn't think to do this?  Maybe it's dirty even by assembly standards.


## Timing, vblank, and some cool trickery

Okay, so, as I was writing that last section, I got really curious about whether and when I'm _actually_ allowed to write to OAM.  Or tile RAM, for that matter.

I found/consulted the Game Boy dev wiki, and [the rules](http://gbdev.gg8.se/wiki/articles/Video_Display#FF41_-_STAT_-_LCDC_Status_.28R.2FW.29) match what's in the manual, albeit with a chart that makes things a little more clear.

My understanding is as follows.  The LCD draws the screen one row of pixels at a time, and each row has the following steps:

1. Look through OAM to see if any sprites are on this row.  OAM is inaccessible to the CPU.

2. Draw the row.  OAM, VRAM, and palettes are all inaccessible.

3. Finish the row and continue on to the beginning of the next row.  This takes a nonzero amount of time, called the _horizontal blanking period_, during which the CPU can access everything freely.

Once the LCD reaches the bottom, it continues to "draw" a number of faux rows below the bottom of the visible screen (_vertical blanking_), and the CPU can again do whatever it wants.  Eventually it returns to the top-left corner to draw again, concluding a single frame.  The entire process happens 59.7 times per second.

There's one exception: DMA transfers can happen any time, _but_ the LCD will simply not draw sprites during the transfer.

So I _probably shouldn't_ be writing to tiles and palettes willy-nilly.  I _suspect_ I got away with it because it happened in that first OAM-searching stage…  and/or because I did it on emulators which are a bit more flexible than the original hardware.

_In fact..._

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/101-first-frame.png" alt="Same screenshot as above, but the first row of pixels is corrupt">
</div>

I took this screenshot by loading the ROM I have so far, pausing it, resetting it, and then advancing a single frame.  This is the very first frame my game shows.  If you look closely at the first row of pixels, you can see they're actually corrupt — they're being drawn before I've set up the palette!  You can even see _each palette entry_ taking effect along the row.

This is _very cool_.  It also means my current code _would not work at all_ on actual hardware.  I should probably just turn the screen off while I'm doing setup like this.

It's interesting that only OAM gets a special workaround in the form of a DMA transfer — I imagine because sprites move around much more often than the tileset changes — but having the LCD stop drawing sprites in the meantime is quite a limitation.  Surely, you'd only want to do a DMA transfer during vblank anyway?  It _is_ much faster than copying by hand, so I'll still take it.

All of this is to say: I'm gonna need to care about vblanks.

----

_Incidentally_, the presence of hblank is _very cool_ and can be used for a number of neat effects, especially when combined with the Game Boy's ability to call back into user code when the LCD reaches a specific _row_:

- The GBC Zelda games use it for map scrolling.  The status bar at the top is in one of the two background maps, and as soon as that finishes drawing, the game switches to the other one, which contains the world.

- Those same games also use it for a horizontal wavy effect, both when warping around and when underwater — all they need to do is change the background layer's x offset during each hblank!

- The wiki points out that OAM could be written to _in the middle of_ a screen update, thus bypassing the 40-object restriction: draw 40 objects on the top half of the screen, swap out OAM midway, and then the LCD will draw a different 40 on the bottom half!

- I imagine you could also change palettes midway through a redraw and exceed the usual limit of 56 colors on screen at a time!  No telling whether this sort of trick would work on an emulator, though.

I am _very excited_ at the prospects here.

I'm also slightly terrified.  I have a fixed amount of time between frames, and with the LCD as separate hardware, there's no such thing as a slow frame.  If I don't finish, things go bad.  And that time is measured _in instructions_ — an `ld` always takes the same number of cycles!  There's no faster computer or reducing GC pressure.  There's just me.  Yikes.


## Back to drawing a sprite

I haven't had a single new screenshot this entire post!  This is ridiculous.  All I want is to draw a thing to the screen.

I have some data in my OAM buffer.  I have DMA set up.  All I _should_ need to do now is start a transfer.

```rgbasm
    call $ff80
```

And…  nothing.  mGBA's memory viewer confirms everything's in the right place, but nothing's on the screen.

Whoops!  Remember that LCD controller register, and how it defaults to $91?  Well, bit 1 is whether to show objects _at all_, and it defaults to _off_.  So let's fix that.

```rgbasm
    ld a, %10010011  ; $91 plus bit 2
    ld [$ff40], a
```

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/102-first-object.png" alt="The same gaudy background, but now with a partial Anise sprite on top">
</div>

***SUCCESS!***

It doesn't look like much, but it took a _lot_ of flailing to get here, and I was [overjoyed when I first saw it](http://rampantgames.com/blog/?p=7745).  The rest should be a breeze!  Right?


## To be continued

That doesn't even get us all the way through [commit `1b17c7`](https://github.com/eevee/anise-cheezball-rising/commit/1b17c709f44718983015539ceb8709fb5ed8edbd), but this is already more than enough.

Next time: input, and moderately less eye-searing art!
