title: Cheezball Rising: Opening a dialogue
date: 2018-10-09 09:07
category: blog
tags: tech, gamedev, cheezball rising

This is a series about [**Star Anise Chronicles: Cheezball Rising**](https://github.com/eevee/anise-cheezball-rising), an expansive adventure game about my cat for the Game Boy Color.  Follow along as I struggle to make something with this bleeding-edge console!

GitHub has [intermittent prebuilt ROMs](https://github.com/eevee/anise-cheezball-rising/releases), or you can get them a week early [on Patreon](https://www.patreon.com/eevee/posts?tag=cheezball%20rising) if you pledge $4.  More details in the [README](https://github.com/eevee/anise-cheezball-rising)!

----

In this issue, I draw some text!

Previously: [I get a Game Boy to meow]({filename}/2018-09-06-cheezball-rising-resounding-failure.markdown).  
Next: [collision detection]({filename}/2018-11-28-cheezball-rising-collision-detection-part-1.markdown), _ohh nooo_…

<!-- more -->


## Recap

The previous episode was a diversion (and left an open problem that I only solved _after_ writing it), so the actual state of the game is unchanged.

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/04l-go-anise-go-again.gif" alt="Star Anise walking around a moon environment in-game, animated in all four directions">
</div>

Where should I _actually_ go from here?  Collision detection is an obvious place, but that's _hard_.  Let's start with something a little easier: displaying scrolling dialogue text.  This is likely to be a dialogue-heavy game, so I might as well get started on that now.


## Planning

On any other platform, I'd dive right into it: draw a box on the screen somewhere, fill it with text.

On the Game Boy, it's not quite that simple.  I can't just write text to the screen; I can only place tiles and sprites.

Let's look at how, say, Pokémon Yellow handles its menu.

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06a-pokemon-text-example.png" alt="Pokémon Yellow with several levels of menu open">
</div>

This looks — _feels_ — like it's being drawn on top of the map, and that sub-menus open on top of other menus.  But it's all an illusion!  There's no "on top" here.  This is a completely flat image made up of tiles, like anything else.

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06b-pokemon-text-grid.png" alt="The same screenshot, scaled up, with a grid showing the edges of tiles">
</div>

This is why Pokémon has such a conspicuously blocky font: all the glyphs are drawn to fit in a single 8×8 char, so "drawing" text is as simple as mapping letters to char indexes and drawing them onto the background.  The map and the menu are all on the same layer, and the game simply redraws whatever was underneath when you close something.  Part of the illusion is that the game is clever enough to hide any sprites that _would_ overlap the menu — because sprites would draw on top!  (The Game Boy Color has some twiddles for controlling this layering, but Yellow was originally designed for the monochrome Game Boy.)

A **critical** reason that this actually works is that in Pokémon, the camera is _always_ aligned to the grid.  It scrolls smoothly while you're walking, but you can't actually open the menu (or pick up an item, or talk to someone, or do anything else that might show text) until you've stopped moving.  If you could, the menu would be misaligned, because it's part of the same grid as the map!

This poses a slight problem for _my_ game.  Star Anise isn't locked to the grid like the Pokémon protagonist is, and unlike Link's Awakening, I do want to have areas larger than the screen that can scroll around freely.

I know offhand that there are a couple ways to do this.  One is the _window_, an optional extra opaque layer that draws on top of the background, with its top-left corner anchored to any point on the screen.  Another is to change some display registers in the _middle_ of the screen redrawing.  If you're thinking of any games with a status bar at the bottom or right, chances are they use the window; games with a status bar at the top have to use display register tricks.

But I don't want to worry about any of this right now, before I even have text drawing.  I know it's _possible_, so I'll deal with it later.  For now, drawing directly onto the background is good enough.

### Font decisions

Let's get back to the font itself.  I'm not in _love_ with the 8×8 aesthetic; what are my other options?  I do like the text in Oracle of Ages, so let's have a look at that:

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06c-oracle-of-ages-text-grid.png" alt="Oracle of Ages, also scaled up with a grid, showing its taller text">
</div>

Ah, this is the same approach again, except that letters are now allowed to peek up into the char above.  So these are 8×16, but the letters all occupy a box that's more like 6×9, offering much more familiar proportions.  Oracle of Ages is designed for the Game Boy Color, which has twice as much char storage space, so it makes sense that they'd take advantage of it for text like this.

It's not _bad_, but the space it affords is still fairly…  limited.  Only 16 letters will fit in a line, just as with Pokémon, and that means a lot of carefully wording things to be short and use mostly short words as well.  That's not gonna cut it for the amount of dialogue I expect to have.

(You may be wondering, as I did, how Oracle pulled off this grid-aligned textbox.  In small buildings and the overworld, each room is exactly the size of the screen, so there's no scrolling and no worry about misaligned text.  But how does the game handle showing text inside a dungeon, where a room is bigger than the screen and can scroll freely?  The answer is: [it doesn't](https://twitter.com/eevee/status/1038432032064339968)!  The textbox is just placed _as close as possible_ to the position shown in this screenshot, so the edges might be misaligned by up to 4 pixels.  In 20 years, I never noticed this until I thought to check how they were handling it.  I'm sure there's a lesson, here.)

What other options do I have?  It seems like I'm limited to multiples of 8 here, surely.  (The answer may be obvious to some of you, but shh, don't read ahead.)

The answer lies in the very last game released for the Game Boy Color: Harry Potter and the Chamber of Secrets.  Whatever deep secrets were learned during the Game Boy's lifetime will surely be encapsulated within this, er, movie tie-in game.

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06d-chamber-of-secrets-text-grid.png" alt="Harry Potter and the Chamber of Secrets, also scaled up with a grid, showing its text isn't fixed to the grid">
</div>

_Hot damn._  That is a _ton_ of text in a relatively small amount of space!  And it doesn't fit the grid!  How did they do that?

The answer is…  exactly how you'd think!

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06e-chamber-of-secrets-tiles.png" alt="Tile display for the above screenshot, showing that the text is simply written across consecutive tiles">
</div>

With a fixed-width font like in Pokémon and Zelda games, the entire character set is stored in VRAM, and text is drawn by drawing a string of characters.  With a variable-width font like in Harry Potter, a block of VRAM is reserved for text, and text is drawn _into those chars, in software_.  Essentially, some chars are used like a canvas and have text rendered to them on the fly.  The contents of the background layer might look like this in the two cases:

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06f-fixed-variable-font-comparison.png" alt="Illustration of fixed width versus variable width text">
</div>

Some pros of this approach:

- Since the number of chars required is constant and the font is never loaded directly into char memory, the font can have arbitrarily many glyphs in it.  Multiple fonts could be used at the same time, even.  (Of course, if you have more than 256 glyphs, you'll have to come up with a multi-byte encoding for actually storing the text…)

- A _lot_ more text can fit in one line while still remaining readable.

- It has the potential to look _very_ cool.  I definitely want to squeeze every last drop of fancy-pants graphical stuff that I can from this hardware.

And, cons:

- It's definitely more complicated!  But I only have to write the code once, and since the game won't be doing anything _but_ drawing dialogue while the box is up, I don't think I'll be in danger of blowing my CPU budget.

- Colored text becomes a _bit_ trickier.  But still possible, so, we can worry about that later.

- Fixed text that _doesn't_ scroll, like on menus and whatnot, will be something of a problem — this whole idea relies on amortizing the text rendering across multiple frames.  On the other hand, this game shouldn't have _too_ much of that, and this sounds like a good excuse to hand-draw fixed text (which can then be much more visually interesting).  _At worst_, I could just render the fixed text ahead of time.

Well, I'm sold.  Let's give it a shot.


## First pass

Well, I want to do something on a button press, so, let's do that.

A lot of games (older ones especially) have bugs from switching "modes" in the same frame that something else happens.  I don't entirely understand why that's so common and should probably ask some speedrunners, but I _should_ be fine if I do mode-switching first thing in the frame, and then start over a new frame when switching back to "world" mode.  Right?  Sure.

```rgbasm
    ; ... button reading code in main loop ...
    bit BUTTON_A, a
    jp nz, .do_show_dialogue

    ; ... main loop ...

    ; Loop again when done
    jp vblank_loop

.do_show_dialogue:
    call show_dialogue
    jp vblank_loop
```

The extra level of indirection added by `.do_show_dialogue` is just so the dialogue code itself isn't responsible for knowing where the main loop point is; it can just `ret`.

Now to actually do something.  This is a first pass, so I want to do as little as possible.  I'll definitely need a palette for drawing the text — and here I'm cutting into my 8-palette budget again, which I don't love, but I can figure that out later.  (Maybe with some shenanigans involving changing the palettes mid-redraw, even.)

```rgbasm
PALETTE_TEXT:
    ; Black background, white text...  then gray shadow, maybe?
    dcolor $000000
    dcolor $ffffff
    dcolor $999999
    dcolor $666666

show_dialogue:
    ; Have to disable the LCD to do video work.  Later I can do
    ; a less jarring transition
    DisableLCD

    ; Copy the palette into slot 7 for now
    ld a, %10111000
    ld [rBCPS], a
    ld hl, PALETTE_TEXT
    REPT 8
    ld a, [hl+]
    ld [rBCPD], a
    ENDR
```

I also know _ahead of time_ what chars will need to go where on the screen, so I can fill them in now.

Note that I really ought to blank them all out, especially since they may still contain text from some previous dialogue, but I don't do that yet.

An obvious question is: _which tiles_?  I think I said before that with 512 chars available, and ¾ of those still being enough to cover the entire screen in unique chars, I'm okay with dedicating a quarter of my space to UI stuff, including text.  To keep that stuff "out of the way", I'll put them at the "end" — bank 1, starting from $80.

I'm thinking of having characters be about the same proportions as in the Oracle games.  Those games use 5 rows of tiles, like this:

```
top of line 1
bottom of line 1
top of line 2
bottom of line 2
blank
```

Since the font is aligned to the bottom and only peeks a little bit into the top char, the very top row is _mostly_ blank, and that serves as a top margin.  The bottom row is explicitly blank for a bottom margin that's nearly the same size.  The space at the top of line 2 then works as line spacing.

I'm not fixed to the grid, so I can control line spacing a little more explicitly.  But I'll get to that later and do something really simple for now, where $ff is a blank tile:

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+---+
|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|...|
+--+--+--+--+--+--+--+--+--+--+--+--+--+---+
|ff|80|82|84|86|88|8a|8c|8e|90|92|94|96|...|
+--+--+--+--+--+--+--+--+--+--+--+--+--+---+
|ff|81|83|85|87|89|8b|8d|8f|91|93|95|97|...|
+--+--+--+--+--+--+--+--+--+--+--+--+--+---+
|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|ff|...|
+--+--+--+--+--+--+--+--+--+--+--+--+--+---+
```

This gives me a canvas for drawing a single line of text.  The staggering means that the first letter will draw to adjacent chars $80 and $81, rather than distant cousins like $80 and $a0.

You may notice that the below code updates chars across the entire width of the _grid_, not merely the screen.  There's not really any good reason for that.

```rgbasm
    ; Fill text rows with tiles (blank border, custom tiles)
    ; The screen has 144/8 = 18 rows, so skip the first 14 rows
    ld hl, $9800 + 32 * 14
    ; Top row, all tile 255
    ld a, 255
    ld c, 32
.loop1:
    ld [hl+], a
    dec c
    jr nz, .loop1

    ; Text row 1: 255 on the edges, then middle goes 128, 130, ...
    ld a, 255
    ld [hl+], a
    ld a, 128
    ld c, 30
.loop2:
    ld [hl+], a
    add a, 2
    dec c
    jr nz, .loop2
    ld a, 255
    ld [hl+], a

    ; Text row 2: same as above, but middle is 129, 131, ...
    ld a, 255
    ld [hl+], a
    ld a, 129
    ld c, 30
.loop3:
    ld [hl+], a
    add a, 2
    dec c
    jr nz, .loop3
    ld a, 255
    ld [hl+], a

    ; Bottom row, all tile 255
    ld a, 255
    ld c, 32
.loop4:
    ld [hl+], a
    dec c
    jr nz, .loop4
```

Now I need to repeat all of that, but in bank 1, to specify the char bank (1) and palette (7) for the corresponding tiles.  Those are the same for the entire dialogue box, though, so this part is easier.

```rgbasm
    ; Switch to VRAM bank 1
    ld a, 1
    ldh [rVBK], a

    ld a, %00001111  ; bank 1, palette 7
    ld hl, $9800 + 32 * 14
    ld c, 32 * 4  ; 4 rows
.loop5:
    ld [hl+], a
    dec c
    jr nz, .loop5

    EnableLCD
```

Time to get some real work done.  Which raises the question: how do I actually do this?

If you recall, each 8-pixel row of a char is stored in two bytes.  The two-bit palette index for each pixel is split across the corresponding bit in each byte.  If the leftmost pixel is palette index 01, then bit 7 in the first byte will be 0, and bit 7 in the second byte will be 1.

Now, a blank char is all zeroes.  To write a (left-aligned) glyph into a blank char, all I need to do is…  well, I could overwrite it, but I could just as well OR it.  To write a _second_ glyph into the unused space, all I need to do is _shift it right_ by the width of the space used so far, and OR it on top.  The unusual split layout of the palette data is actually handy here, because it means the size of the shift matches the number of pixels, _and_ I don't have to worry about overflow.

```
0 0 0 0 0 0 0 0  <- blank glyph

1 1 1 1 0 0 0 0  <- some byte from the first glyph
↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
1 1 1 1 0 0 0 0  <- ORed together to display first character

          1 1 1 1 0 0 0 0  <- some byte from the second glyph,
                              shifted by 4 (plus a kerning pixel)
↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
1 1 1 1 0 1 1 1  <- ORed together to display first two characters
```

The obvious question is, well, what happens to the bits from the second character that didn't fit?  I'll worry about that a bit later.

Oh, and finally, I'll need _a font_, plus some text to display.  This is still just a proof of concept, so I'll add in a couple glyphs by hand.

```rgbasm
; somewhere in ROM
font:
; A
    ; First byte indicates the width of the glyph, which I need
    ; to know because the width varies!
    db 6
    dw `00000000
    dw `00000000
    dw `01110000
    dw `10001000
    dw `10001000
    dw `10001000
    dw `11111000
    dw `10001000
    dw `10001000
    dw `10001000
    dw `10001000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
; B
    db 6
    dw `00000000
    dw `00000000
    dw `11110000
    dw `10001000
    dw `10001000
    dw `10001000
    dw `11110000
    dw `10001000
    dw `10001000
    dw `10001000
    dw `11110000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000
    dw `00000000

text:
    ; Shakespeare it ain't.
    ; Need to end with a NUL here so I know where the text
    ; ends.  This isn't C, there's no automatic termination!
    db "ABABAAA", 0
```

And here we go!

```rgbasm
    ; ----------------------------------------------------------
    ; Setup done!  Real work begins here
    ; b: x-offset within current tile
    ; de: text cursor + current character tiles
    ; hl: current VRAM tile being drawn into
    ld b, 0
    ld de, text
    ld hl, $8800

    ; This loop waits for the next vblank, then draws a letter.
    ; Text thus displays at ~60 characters per second.
.next_letter:
    ; This is probably way more LCD disabling than is strictly
    ; necessary, but I don't want to worry about it yet
    EnableLCD
    call wait_for_vblank
    DisableLCD

    ld a, [de]                  ; get current character
    and a                       ; if NUL, we're done!
    jr z, .done
    inc de                      ; otherwise, increment

    ; Get the glyph from the font, which means computing
    ; font + 33 * a.
    ; A little register juggling.  hl points to the current
    ; char in VRAM being drawn to, but I can only do a 16-bit
    ; add into hl.  de I don't need until the next loop,
    ; since I already read from it.  So I'm going to push de
    ; AND hl, compute the glyph address in hl, put it in de,
    ; then restore hl.
    push de
    push hl
    ; The text is written in ASCII, but the glyphs start at 0
    sub a, 65
    ld hl, font
    ld de, 33                   ; 1 width byte + 16 * 2 tiles
    ; This could probably be faster with long multiplication
    and a
.letter_stride:
    jr z, .skip_letter_stride
    add hl, de
    dec a
    jr .letter_stride
.skip_letter_stride:
    ; Move the glyph address into de, and restore hl
    ld d, h
    ld e, l
    pop hl

    ; Read the first byte, which is the character width.  This
    ; overwrites the character, but I have the glyph address,
    ; so I don't need it any more
    ld a, [de]
    inc de

    ; Copy into current chars
    ; Part 1: Copy the left part into the current chars
    push af                     ; stash width
    ; A glyph is two chars or 32 bytes, so row_copy 32 times
    ld c, 32
    ; b is the next x position we're free to write to.
    ; Incrementing it here makes the inner loop simpler, since
    ; it can't be zero.  But it also means two jumps per loop,
    ; so, ultimately this was a pretty silly idea.
    inc b
.row_copy:
    ld a, [de]                  ; read next row of character

    ; Shift right by b places with an inner loop
    push bc                     ; preserve b while shifting
    dec b
.shift:                         ; shift right by b bits
    jr z, .done_shift
    srl a
    dec b
    jr .shift
.done_shift:
    pop bc

    ; Write the updated byte to VRAM
    or a, [hl]                  ; OR with current tile
    ld [hl+], a
    inc de
    dec c
    jr nz, .row_copy
    pop af                      ; restore width

    ; Part 2: Copy whatever's left into the next char
    ; TODO  :)

    ; Cleanup for next iteration
    ; Undo the b increment from way above
    dec b
    ; It's possible I overflowed into the next column, in which
    ; case I want to leave hl where it is: pointing at the next
    ; column.  Otherwise, I need to back it up to where it was.
    ; Of course, I also need to update b, the x offset.
    add a, b                    ; a <- new x offset
    ; If the new x offset is 8 or more, that's actually the next
    ; column
    cp a, 8
    jr nc, .wrap_to_next_tile
    ld bc, -32                  ; a < 8: back hl up
    add hl, bc
    jr .done_wrap
.wrap_to_next_tile:
    sub a, 8                    ; a >= 8: subtract tile width
    ld b, a
.done_wrap:
    ; Either way, store the new x offset into b
    ld b, a

    ; And loop!
    pop de                      ; pop text pointer
    jr .next_letter

.done:
    ; Undo any goofy stuff I did, and get outta here
    EnableLCD
    ; Remember to reset bank to 0!
    xor a
    ldh [rVBK], a
    ret
```

Phew!  That was a lot, but hopefully it wasn't too bad.  I hit a few minor stumbling blocks, but as I recall, most of them were of the "I get the conditions backwards every single time I use `cp` augh" flavor.  (In fact, if you look at the [actual commit](https://github.com/eevee/anise-cheezball-rising/commit/3a8252f628e8c27c25ea28e2a1769f3429abe5f5) the above is based on, you may notice that I had the condition at the very end mixed up!  It's a miracle it managed to print part of the second letter at all.)

There are a _lot_ of caveats in this first pass, including that there's nothing to _erase_ the dialogue box and reshow the map underneath it.  (But I might end up using the window for this anyway, so there's no need for that.)

As a proof of concept, though, it's a great start!

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06g-text-attempt-1.png" alt="Screenshot of Anise, with a black dialogue box that says: A|">
</div>

That's the letter `A`, followed by the first two pixels of the letter `B`.  I didn't implement the part where letters spill into the next column, yet.

Guess I'd better do that!


## Second pass

One of the big problems with the first pass was that I had to turn the screen off to do the actual work safely.  Shifting a bunch of bytes by some amount is a _little_ slow, since I can only shift one bit at a time and have to do it within a loop, and vblank only lasts for about 6.5% of the entire duration of the frame.  If I continued like this, the screen would constantly flicker on and off every time I drew a new letter.  Yikes.

I'll solve this the same way I solve pretty much any other vblank problem: do the actual work into a buffer, then just copy that buffer during vblank.  Since I intend to draw no more than one character per frame, and each character glyph is no wider than a single char column, I only need a buffer big enough to span two columns.  Text covers two rows, also, so that's four tiles total.

I also need to zero out the tile buffer when I first start drawing text — otherwise it may still have garbage left over from the last time text was displayed! — and this seems like a great opportunity to introduce a little `fill` function.  Maybe then I'll do the right damn thing and clear out other stuff on startup.

```rgbasm
; Utility code section

; fill c bytes starting at hl with a
; NOTE: c must not be zero
fill:
    ld [hl+], a
    dec c
    jr nz, fill
    ret

; ...

; Stick this at a fixed nice address for now, just so it's easy
; for me to look at and debug
SECTION "Text buffer", WRAM0[$C200]
text_buffer:
    ; Text is up to 8x16 but may span two columns, so carve out
    ; enough space for four tiles
    ds $40

show_dialogue:
    DisableLCD
    ; ... setup stuff ...
    EnableLCD

    ; Zero out the tile buffer
    xor a
    ld hl, text_buffer
    ld c, $40
    call fill
```

That first round of disabling and enabling the LCD is still necessary, because the setup work takes a little time, but I can get rid of that later too.  For now, the priority is fixing the text scroll (and supporting text that spans more than one tile).

The code is the same up until I start copying the glyph into the tiles.  Now it doesn't go to VRAM, but into the buffer.

There's another change here, too.  Previously, I shifted the glyph right, letting bits fall off the right end and disappear.  But the bits that drop off the end are exactly the bits that I need to draw to the _next_ char.  I could do a _left_ shift to retrieve them, but I had a different idea: _rotate_ the glyph instead.

Say I want to draw a glyph offset by 3 pixels.  Then I want to do this:

```
abcdefgh  <- original glyph bits
fghabcde  <- rotate right 3
00011111  <- mask, which is just $ff shifted right 3

000abcde  <- rotated glyph AND mask gives the left part

11100000  <- mask, inverted
fgh00000  <- rotated glyph AND inverted mask gives the right part
```

The time and code savings aren't huge, exactly, and nothing else is going on while text is rendering so it's not like time is at a premium here.  But hey this feels clever so let's do it.

```rgbasm
    ; Copy into current chars
    push af                     ; stash width
    ld c, 32                    ; 32 bytes per row
    ld hl, text_buffer          ; new!
    ; This is still silly.
    inc b
.row_copy:
    ld a, [de]                  ; read next row of character
    ; Rotate right by b - 1 pixels -- remember, b contains the
    ; x-offset within the current tile where to start drawing
    push bc                     ; preserve b while shifting
    ld c, $ff                   ; initialize the mask
    dec b
    jr z, .skip_rotate
.rotate:
    ; Rotate the glyph (a), but shift the mask (c), so that the
    ; left end of the mask fills up with zeroes
    rrca
    srl c
    dec b
    jr nz, .rotate
.skip_rotate:
    push af                     ; preserve glyph
    and a, c                    ; mask right pixels
    ; Draw to left half of text buffer
    or a, [hl]                  ; OR with current tile
    ld [hl+], a
    ; Write the remaining bits to right half
    ld a, c                     ; put mask in a...
    cpl                         ; ...to invert it
    ld c, a                     ; then put it back
    pop af                      ; restore unmasked glyph
    and a, c                    ; mask left pixels
    ld [hl+], a                 ; and store them!
    ; Clean up after myself, and loop to the next row
    inc de                      ; next row of glyph
    pop bc                      ; restore counter!
    dec c
    jr nz, .row_copy
    pop af                      ; restore width
```

The use of the stack is a _little_ confusing (and don't worry, it only gets worse in later posts).  Note for example that `c` is used as the loop counter, but since I don't actually need its value _within_ the body of the loop, I can `push` it right at the beginning and use `c` to hold the mask, then `pop` the loop counter back into place at the end.

(**UPDATE**: A reader points out that I don't really need the mask at all.  The `rrca` instruction puts the lost bit in the carry flag, so I can instead follow it with `rr c`, which puts the carry flag into bit 7 of `c`.  Then I'll end up with the right bits in `c`, no masking required.  If I also used `rra` instead of `rrca`, then `a` would end up with just the left bits, and nothing needs masking at all!)

(Also, it occurs to me that I could avoid the loop entirely with a Duff's device...  but that might be a little over the top.)

This is where I first started to feel register pressure, especially when addresses eat up _two_ of them.  My options are pretty limited: I can store stuff on the stack, or store stuff in RAM.  The stack is arguably harder to follow (and easier to fuck up, which I've done several times), but either way there's the register ambiguity.

Which is shorter/faster?  Well:

* A `push`/`pop` pair takes 2 bytes and 7 cycles.

* Immediate writing to RAM and immediate reading back from it takes 6 bytes and 8 cycles, _and_ can only be done with `a`, so I'd probably have to copy into and out of some other register too.

* Putting an address in `hl`, writing to it, then reading from it takes 5 bytes and 7 cycles, _but_ requires that I can preserve `hl`.  (On the other hand, if I can preserve the value of `hl` across a loop or something, then it's amortized away and the read/write is only 2 bytes and 3 cycles.  But if that's the case, chances are that I'm not under enough register pressure to need using RAM in the first place.)

* Parts of high RAM ($ff80 and up) are available for program use, and they can be read or written with the same instructions that operate on the control knobs starting at $ff00.  A high RAM read and write takes 4 bytes and 6 cycles, which isn't too bad, but once again I have to go through the `a` register so I'll probably need some other copies.

Stack it is, then.

Anyway!  Where were we.  I need to now copy the buffer into VRAM.

You may have noticed that the buffer isn't quite populated in char format.  Instead, it's populated like one big 16-pixel char, with the first 16 bits corresponding to the 16 pixels spanning _both_ columns.  VRAM, of course, expects to get all the pixels from the first column, then all the pixels from the second column.  If that's not clear, here's what I have (where the bits are in order from left to right, top to bottom):

```
AAAAAAAA BBBBBBBB  <- high bits for first row of pixels
aaaaaaaa bbbbbbbb  <- low bits for first row of pixels
... other rows ...
```

And here's what I need to put in VRAM:

```
AAAAAAAA  <- high bits for first row of left column of pixels
aaaaaaaa  <- low bits for first row of left column of pixels
... other rows of left column ...
BBBBBBBB  <- high bits for first row of right column of pixels
bbbbbbbb  <- low bits for first row of right column of pixels
... other rows of right column ...
```

I hope that makes sense!  To fix this, I use two loops (one for each column), and in each loop I copy _every other_ byte into VRAM.  That deinterlaces the buffer.

```rgbasm
    ; Draw the buffered tiles to vram
    ; The text buffer is treated like it's 16 pixels wide, but
    ; VRAM is of course only 8 pixels wide, so we need to do
    ; this in two iterations: the left two tiles, then the right
    pop hl                      ; restore hl (VRAM)
    push af                     ; stash width, again
    call wait_for_vblank        ; always wait before drawing
    push bc
    push de
    ; Draw the left two tiles
    ld c, $20
    ld de, text_buffer
.draw_left:
    ld a, [de]
    ; This double inc fixes the interlacing
    inc de
    inc de
    ld [hl+], a
    dec c
    jr nz, .draw_left
    ; Draw the right two tiles
    ld c, $20
    ; This time, start from the SECOND byte, which will grab
    ; all the bytes skipped by the previous loop
    ld de, text_buffer + 1
.draw_right:
    ld a, [de]
    inc de
    inc de
    ld [hl+], a
    dec c
    jr nz, .draw_right
    pop de
    pop bc
    pop af                      ; restore width, again
```

Just about done!  There's one last thing to do before looping to the next character.  If this character did in fact span both columns, then the buffer needs to be moved to the left by one column.  Here's a simplified diagram, pretending chars are 5×5 and I just drew a B:

```
+-----+-----+.....+
| A  B|B    |     .
|A A B| B   |     .
|AAA B|B    |     .
|A A B| B   |     .
|A A B|B    |     .
+-----+-----+.....+
```

The left column is completely full, so I don't need to buffer it any more.  The next character wants to draw in the last _partially full_ column, which here is the one containing the B; it'll also want an empty right column to overflow into if necessary.

```rgbasm
    ; Increment the pixel offset and deal with overflow
    add a, b                    ; a <- new x offset
    ; Regardless of whether this glyph overflowed, the VRAM
    ; pointer was left at the beginning of the next (empty)
    ; column, and it needs rewinding to the right column
    ld bc, -32                  ; move the VRAM pointer back...
    add hl, bc                  ; ...to the start of the char
    cp a, 8
    jr nc, .wrap_to_next_char
    ; The new offset is less than 8, so this character didn't
    ; actually draw anything in the right column.  Move the
    ; VRAM pointer back a second time, to the left column,
    ; which still has space left
    add hl, bc
    jr .done_wrap
.wrap_to_next_char:
    ; The new offset is 8 or more, so this character drew into
    ; the next char.  Subtract 8, but also shift the text buffer
    ; by copying all the "right" chars over the "left" chars
    sub a, 8                    ; a >= 8: subtract char width
    push hl
    push af
    ; The easy way to do this is to walk backwards through the
    ; buffer.  This leaves garbage in the right column, but
    ; that's okay -- it gets overwritten in the next loop,
    ; before the buffer is copied into VRAM.
    ld hl, text_buffer + $40 - 1
    ld c, $20
.shift_buffer:
    ld a, [hl-]
    ld [hl-], a
    dec c
    jr nz, .shift_buffer
    pop af
    pop hl
.done_wrap:
    ld b, a                     ; either way, store into b

    ; Loop
    pop de                      ; pop text pointer
    jp .next_letter
```

And the test run:

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06h-text-attempt-2.png" alt="Screenshot of Anise, with a black dialogue box that says: ABABAAA">
</div>

Hey hey, success!


## Quick diversion: Anise corruption

I didn't mention it above because I didn't actually use it yet, but while doing that second pass, I split the button-polling code out into its own function, `read_input`.  I thought I might need it in dialogue as well (which has its own vblank loop and thus needs to do its own polling), but I didn't get that far yet, so it's still only called from the main loop.

While testing out the dialogue, I notice a teeny tiny problem.

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06i-anise-corruption.png" alt="A screenshot similar to the above, but with some mild graphical corruption on Anise">
</div>

Well, yes, obviously there's the problem of the textbox drawing _underneath_ the player.  Which is mostly a problem because the textbox doesn't go away, ever.  I'll worry about that later.

The _other_ problem is that Anise's sprite is corrupt.  _Again._  Argh!

A little investigation suggests that, once again, I'm blowing my vblank budget.  But this time, it's a little more reasonable.  Remember, I'm overwriting Anise's sprite _after_ handling movement.  That means I do a bunch of logic _followed by_ writing to char data.  No wonder there's a problem.  I must've just slightly overrun vblank when I split out `read_input` (or checked for the dialogue button press in the first place?), since `call` has a teeny tiny bit of overhead.

That approach is a little inconsistent, as well.  Remember how I handle OAM: I write to a buffer, which is then copied to real OAM during the next vblank.  But I'm updating the sprite _immediately_.  That means when Anise turns, the sprite updates on the very next frame, but the movement isn't visible until the frame _after_ that.  Whoops.

So, a buffer!  I could make this into a more general mechanism later, but for now I only care about fixing Anise.  I can revisit this when I have, uh, a second sprite.

```rgbasm
; in ram somewhere

anise_sprites_address:
    dw
```

Now, Anise is composed of three objects, which is six chars, which is 96 bytes.  The fastest way to copy bytes by hand is something like this:

```rgbasm
    ld hl, source
    ld de, destination
    ld c, 96
.loop:
    ld a, [hl+]
    ld [de], a
    inc de
    dec c
    jr nz, .loop
```

Each iteration of the loop copies 1 byte and takes 7 cycles.  (It's possible to shave a couple cycles off in some specific cases, and unrolling would save some time, but let's stay general for now.)  That's 672 cycles, plus 10 for the setup, minus one on the final `jr`, for 681 total.  But vblank only lasts 1140 cycles!  That's more than half the budget blown for updating a _single entity_.  This can't possibly work.

Enter a feature exclusive to the Game Boy Color: GDMA, or _general_ DMA.  This is similar to OAM DMA, except that it can copy (nearly) anything to anywhere.  Also (unlike OAM DMA), the CPU _pauses_ while the copy is taking place, so there's no need to carefully time a busy loop.  It's configured by writing to five control registers (which takes 5 cycles each), and then it copies _two bytes per cycle_, for a total of 73 cycles.  That's **9.3 times faster**.  Seems worth a try.

(Note that I'm not using double-speed CPU mode yet, as an incentive to not blow my CPU budget early on.  Turning that on would halve the time taken by the manual loop, but wouldn't affect GDMA.)

GDMA has a couple restrictions: most notably, it can only copy multiples of 16 bytes, and only to/from addresses that are aligned to 16 bytes.  But each char is 16 bytes, so that works out just fine.

The five GDMA registers are, alas, simply named 1 through 5.  The first two are the source address; the next two are the destination address; the last is the amount to copy.  Or, well, it's the amount to copy, divided by 16, minus 1.  (The high bit is reserved for turning on a different kind of DMA that operates a bit at a time during hblanks.)  Writing to the last register triggers the copy.

Plugging in this buffer is easy enough, then:

```rgbasm
    ; Update Anise's current sprite.  Use DMA here because...
    ; well, geez, it's too slow otherwise.
    ld hl, anise_sprites_address
    ld a, [hl+]
    ld [rHDMA1], a
    ld a, [hl]
    ld [rHDMA2], a
    ; I want to write to $8000 which is where Anise's sprite is
    ; hardcoded to live, and the top three bits are ignored so
    ; that the destination is always in VRAM, so $0000 works too
    ld a, HIGH($0000)
    ld [rHDMA3], a
    ld a, LOW($0000)
    ld [rHDMA4], a
    ; And copy!
    ld a, (32 * 3) / 16 - 1
    ld [rHDMA5], a
```

Finally, instead of actually overwriting Anise's sprite, I write the address of the new sprite into the buffer:

```rgbasm
    ; Store the new sprite address, to be updated during vblank
    ld a, h
    ld [anise_sprites_address], a
    ld a, l
    ld [anise_sprites_address + 1], a
```

And done!  Now I can walk around just fine.  It looks basically like the screenshot from the previous section, so I don't think you need a new one.

Note that this copy will _always_ happen, since there's no condition for skipping it when there's nothing to do.  That's fine for now; later I'll turn this into a list, and after copying everything I'll simply clear the list.

Crisis averted, or at least deferred until later.  Back to the dialogue!


## Interlude: A font

Writing out the glyphs _by hand_ is not going to cut it.  It was fairly annoying for two letters, let alone an entire alphabet.

Nothing about this part was _especially_ interesting.  I used LÖVE's font format, which puts all glyphs in a single horizontal strip.  The color of the top-left pixel is used as a sentinel; any pixel in the top row that's the same color indicates the start of a new glyph.

(I note that LÖVE actually recommends _against_ using this format, but the alternatives are more complicated and require platform-specific software — whereas I can slop this format together in any image editor without much trouble.)

I then turned this into Game Boy tiles much the same way as with the sprite loader, except with the extra logic to split on the sentinel pixels and pad each glyph to eight pixels wide.  I won't reproduce the whole script here, but it's [on GitHub](https://github.com/eevee/anise-cheezball-rising/blob/5b2fc1218d50ccc03151bcaacd0feb607fe22908/util/font-to-tiles.py) if you want to see it.

The font itself is, well, a font?  I initially tried to give it [a little personality](https://github.com/eevee/anise-cheezball-rising/blob/5b2fc1218d50ccc03151bcaacd0feb607fe22908/data/font.png), but that made some of the characters weirdly wide and was a bit hard to read, so I revisited it and ended up with this:

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06j-font.png" alt="Pixel font covering all of ASCII">
</div>

I like it, at least!  The characters all have shadows built right in, and you can see at the end that I was starting to play with some non-ASCII characters.  Because I can do that!


## Third pass

One major obstacle remains: I can only have one line of text right now, when there's plenty of space for two.

The obvious first thing I need to do is alter the dialogue box's char map.  It currently has a whole char's worth of padding on every side.  What a waste.  I want this instead:

```
+--+--+--+--+--+--+--+--+--+--+--+--+---+
|80|82|84|86|88|8a|8c|8e|90|92|94|96|...|
+--+--+--+--+--+--+--+--+--+--+--+--+---+
|81|83|85|87|89|8b|8d|8f|91|93|95|97|...|
+--+--+--+--+--+--+--+--+--+--+--+--+---+
|a8|aa|ac|ae|b0|b2|b4|b6|b8|ba|bc|be|...|
+--+--+--+--+--+--+--+--+--+--+--+--+---+
|a9|ab|ad|af|b1|b3|b5|b7|b9|bb|bd|bf|...|
+--+--+--+--+--+--+--+--+--+--+--+--+---+
```

The second row begins with char $a8 because that's $80 + 40.

Obviously I'll need to change the setup code to make the above pattern.  But _while I'm in here_...  remember, the setup code is the only remaining place that disables the LCD to do its work.  Can I do everything within vblank instead?

I'm actually not sure, but there's an easy way to reduce the CPU cost.  Instead of setting up the whole dialogue box at once, I can do it _one row at a time_, starting from the bottom.  That will cut the vblank pressure by a factor of four, _and_ it'll create a cool slide-up effect when the dialogue box opens!

Let's give it a try.  I'll move the real code into a function, since it'll run multiple times now.  I'll also introduce a few constants, since I'm getting tired of all the magic numbers everywhere.

```rgbasm
SCREEN_WIDTH_TILES EQU 20
CANVAS_WIDTH_TILES EQU 32
SCREEN_HEIGHT_TILES EQU 18
CANVAS_HEIGHT_TILES EQU 32
BYTES_PER_TILE EQU 16
TEXT_START_TILE_1 EQU 128
TEXT_START_TILE_2 EQU TEXT_START_TILE_1 + SCREEN_WIDTH_TILES * 2

; Fill a row in the tilemap in a way that's helpful to dialogue.
; hl: where to start filling
; b: tile to start with
fill_tilemap_row:
    ; Populate bank 0, the tile proper
    xor a
    ldh [rVBK], a

    ld c, SCREEN_WIDTH_TILES
    ld a, b
.loop0:
    ld [hl+], a
    ; Each successive tile in a row increases by 2!
    add a, 2
    dec c
    jr nz, .loop0

    ; Populate bank 1, the bank and palette
    ld a, 1
    ldh [rVBK], a
    ld a, %00001111  ; bank 1, palette 7
    ld c, SCREEN_WIDTH_TILES
    dec hl
.loop1:
    ld [hl-], a
    dec c
    jr nz, .loop1

    ret
```

Now replace the setup code with four calls to this function, waiting for vblank between successive calls.

```rgbasm
    ; Row 4
    ld hl, $9800 + CANVAS_WIDTH_TILES * (SCREEN_HEIGHT_TILES - 1)
    ld b, TEXT_START_TILE_2 + 1
    call fill_tilemap_row

    ; Row 3
    call wait_for_vblank
    ld hl, $9800 + CANVAS_WIDTH_TILES * (SCREEN_HEIGHT_TILES - 2)
    ld b, TEXT_START_TILE_2
    call fill_tilemap_row

    ; Row 2
    call wait_for_vblank
    ld hl, $9800 + CANVAS_WIDTH_TILES * (SCREEN_HEIGHT_TILES - 3)
    ld b, TEXT_START_TILE_1 + 1
    call fill_tilemap_row

    ; Row 1
    call wait_for_vblank
    ld hl, $9800 + CANVAS_WIDTH_TILES * (SCREEN_HEIGHT_TILES - 4)
    ld b, TEXT_START_TILE_1
    call fill_tilemap_row
```

Cool.  I have a full font now, too, so I might as well try it out with some more interesting text.

```rgbasm
SECTION "Font", ROMX
text:
    db "The quick brown fox jumps over the     lazy dog's back.  AOOWWRRR!!!!", 0
```

Now I just need to—  oh, hang on.

<div class="prose-full-illustration">
<img src="{static}/media/cheezball/06k-quickbrownfox.gif" alt="Animation of the text box sliding up and scrolling out the text">
</div>

Hey, it already works!  _Magic_.

(I did also change the initial value for the x-offset to 4 rather than 0, so the text doesn't start against the left edge of the screen.)

Well.  Not _really_.  The code I wrote doesn't actually know when to stop writing, so it continues off the end of the first line and onto the second.  You may notice the conspicuous number of extra spaces in the new text.

Still, it _looks_ right, and this was a lot of effort already, and it's not actually plugged into anything yet, so I called this a success and shelved it for now.  Quit while you're ahead, right?


## Future work

Obviously this is still a bit rough.

That thing where the player can walk on top of the textbox is a bit of a problem, since the same thing happens if the textbox opens while the player is near the bottom of the screen.  There are a couple solutions to this, and they'll really depend on how I end up deciding to display the box.

I actually wanted the glyphs to be drawn a little lower than normal on the top line, to add half a char or so of padding around them, but I tried it and got a buffer overrun that I didn't feel like investigating.  That's an obvious thing to fix next time I touch this code.

What about word wrapping?  I've [written about that before]({filename}/2016-10-20-word-wrapping-dialogue.markdown) and clearly have strong opinions about it, but I _really_ don't want to do dynamic word wrapping with a variable-width font on a _Game Boy_.  Instead, I'll probably store dialogue in some other format and use another converter script to do the word-wrapping ahead of time.  That'll also save me from writing large amounts of dialogue in, um, assembly.  And if/when I want any fancy-pants special effects within dialogue, I can describe them with a human-readable format and then convert that to more assembly-friendly bytecode instructions.

The dialogue box still doesn't _go away_, partly because it draws right on top of the map, and I don't have any easy way to repair the map right now.  I'll probably switch to one of those other mechanisms for showing the box later that won't require clobbering the map, and then this problem will pretty much solve itself.

What about menus?  Those will either have to go inside the dialogue box (which means the question being asked isn't visible, oof), or they'll have to go in a smaller box above it like in Pokémon.  But the latter solution means I can't use the window _or_ display trickery — both of those only work reliably for horizontal splits.  I'm not quite sure how to handle this, yet.

And then, what of portraits?  Most games get away without them by having a silent protagonist, which makes it obvious who's talking.  But Anise is anything but silent, so I need a stronger indicator.  I obviously can't overlay a big transparent portrait on the background, like I do in my LÖVE games.  I _think_ I can reseve space for them in the status bar, which will go underneath the dialogue box.  I'll have to see how it works out.  Maybe I could also use a different text color for every speaker?

After all _that_, I can start worrying about other frills like colored text and pauses and whatever.  Phew.


## To be continued

That brings us up to [commit a173dbb](https://github.com/eevee/anise-cheezball-rising/commit/a173dbb506b8eb56dd2d027f98d75e558a66bb2d), which is _slightly_ beyond the [second release](https://github.com/eevee/anise-cheezball-rising/releases/tag/v20180707pre) (which includes a one-line textbox)!  Also that was _three months ago_ oh dear.  I think I'll be putting out a new release soon, stay tuned!

Next time: [_collision detection_]({filename}/2018-11-28-cheezball-rising-collision-detection-part-1.markdown)!  I am doomed.
