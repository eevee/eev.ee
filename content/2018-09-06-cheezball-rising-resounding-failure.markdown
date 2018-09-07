title: Cheezball Rising: Resounding failure
date: 2018-09-06 05:00
category: blog
tags: tech, gamedev, cheezball rising

This is a series about [**Star Anise Chronicles: Cheezball Rising**](https://github.com/eevee/anise-cheezball-rising), an expansive adventure game about my cat for the Game Boy Color.  Follow along as I struggle to make something with this bleeding-edge console!
 
GitHub has [intermittent prebuilt ROMs](https://github.com/eevee/anise-cheezball-rising/releases), or you can get them a week early [on Patreon](https://www.patreon.com/eevee/posts?tag=cheezball%20rising) if you pledge $4.  More details in the [README](https://github.com/eevee/anise-cheezball-rising)!

----

In this issue, I <s>cannot</s> get a goddamn Game Boy to meow at me!!

Previously: [maps and sprites]({filename}/2018-07-15-cheezball-rising-maps-and-sprites.markdown).  
Next: text!

<!-- more -->


## Recap

With the power of Aseprite, Tiled, and some Python I slopped together, the game has evolved beyond Test Art and into Regular Art.

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/04l-go-anise-go-again.gif" alt="Star Anise walking around a moon environment in-game, animated in all four directions">
</div>

I've got so much work to do on this, so it's time to prioritize.  What is absolutely _crucial_ to this game?

The answer, of course, is to make Anise meow.  Specifically, to make him [AOOOWR](http://floraverse.com/comic/oneshots/568-aooowr/).


## Brief audio primer

What we perceive as sound is the vibration of our eardrums, caused by vibration of the air against them.  Eardrums can only move along a single axis (in or out), so no matter what chaotic things the air is doing, what we hear at a given instant is flattened down to a single scalar number: how far the eardrum has displaced from its normal position.

(There's also a bunch of stuff about tiny hairs in the back of your ear, but, close enough.  Also it's really _two_ numbers since you have two ears, but stereo channels tend to be handled separately.)

Digital audio is nothing more than a sequence of those numbers.  Of course, we can't record the displacement at every single instant, because there are infinitely many instants; instead, we take measurements (_samples_) at regular intervals.  The interval is called the _sample rate_, is usually a very small fraction of a second, and is generally measured in Hertz/Hz (which just means "per second").  A very common sample rate is 44100 Hz, which means a measurement was taken every 0.0000227 seconds.

I say "measurement" but the same idea applies for _generating_ sounds, which is what the Game Boy does.  Want to make a square wave?  Just generate a block of all the same positive sample, then another block of all the same negative sample, and alternate back and forth.  That's why it's depicted as a square — that's the _graph_ of how the samples vary over time.

Okay!  I hope that was enough because it's like 80% of everything I know about audio.  Let's get to the Game Boy.


## Game Boy audio

The Game Boy contains, within its mysterious depths, a teeny tiny synthesizer.  It offers a vast array of _four_ whole channels (instruments) to choose from: a square wave, also a square wave, a wavetable, and white noise.  They can each be controlled with a handful of registers, and will continually produce whatever tone they're configured for.  By changing their parameters at regular intervals, you can create a pleasing sequence of varying tones, which you humans call "music".

Making music is, I'm sure, going to be an absolute nightmare.  What music authoring tools am I possibly going to dig up that exactly conform to the Game Boy hardware?  I can't even begin to imagine what this pipeline might look like.

Luckily, that's not what this post is about, because I chickened out and tried something way easier instead.

Before I set out into the wilderness myself, I _did_ want to get an emulator to create any kind of noise at all, just to give myself a starting point.  There are an awful lot of audio twiddles, so I dug up a [Game Boy sound tutorial](http://gbdev.gg8.se/wiki/articles/Sound_tutorial).

I became a little skeptical when the author admitted they didn't know what a square wave was, but they did provide a brief snippet of code at the end that's claimed to produce a sound:

```c
NR52_REG = 0x80;
NR51_REG = 0x11;
NR50_REG = 0x77;

NR10_REG = 0x1E;
NR11_REG = 0x10;
NR12_REG = 0xF3;
NR13_REG = 0x00;
NR14_REG = 0x87;
```

That's C, written for the much-maligned GBDK, which for some reason uses regular assignment to write to a specific address?  It's easy enough to translate to rgbasm:

```rgbasm
    ; Enable sound globally
    ld a, $80
    ldh [rAUDENA], a
    ; Enable channel 1 in stereo
    ld a, $11
    ldh [rAUDTERM], a
    ; Set volume
    ld a, $77
    ldh [rAUDVOL], a

    ; Configure channel 1.  See below
    ld a, $1e
    ldh [rAUD1SWEEP], a
    ld a, $10
    ldh [rAUD1LEN], a
    ld a, $f3
    ldh [rAUD1ENV], a
    ld a, $00
    ldh [rAUD1LOW], a
    ld a, $85
    ldh [rAUD1HIGH], a
```

It sounds like this.

<audio controls src="{filename}/media/cheezball/05a-example-square-wave.wav"></audio>

Some explanation may be in order.  This is a big ol' mess and you could just as well read [the wiki's article on the sound controller](http://gbdev.gg8.se/wiki/articles/Sound_Controller), so feel free to skip ahead a bit.

First, the official names for all of the sound registers are terrible.  They're all named "NRxy" — "noise register" perhaps? — where _x_ is the channel number (or 5 for master settings) and _y_ is just whatever.  Thankfully, hardware.inc provides some aliases that make a _little_ more sense, and those are what I've used above.

The very first thing I _have_ to do is set the high bit of AUDENA (NR52), which toggles sound on or off entirely.  The sound system isn't like the LCD, which I might turn off temporarily while doing a lot of graphics loading; when the high bit of AUDENA is off, _all the other sound registers_ are wiped to zero and cannot be written until sound is enabled again.

The other important master registers are AUDVOL (NR50) and AUDTERM (NR51).  Both of them are split into two identical nybbles, each controlling the left or right output channel.  AUDVOL controls the master volume, from 0 to 7.  (As I understand it, the high bit is used to enable audio output from extra synthesizer hardware on the _cartridge_, a feature I don't believe any game ever actually used.)  AUDTERM enables channels/instruments, one bit per channel.  The above code turns on channel 1, the square wave, at max volume in stereo.

Then there's just, you know, _sound stuff_.

AUD1HIGH (NR14) and AUD1LOW (NR13) are a bit of a clusterfuck, and one shared by all except the white noise channel.  The high bit of AUD1HIGH is the "init" bit and triggers the sound to actually play (or restart), which is why it's set last.  The second highest bit, bit 6, controls timing: if it's set, then the channel will only play for as long as a time given by AUD1LEN; if not, the channel will play indefinitely.

Finally, the interesting part: the lower three bits of AUD1HIGH and the entirety of AUD1LOW combine to make an 11-bit frequency.  Or, rather, if those 11 bits are $n$, then the frequency is $\frac{131072}{2048-n}$.  (Since their value appears in the denominator, they really express…  _inverse time_, not frequency, but that's neither here nor there.)  The code above sets that 11-bit value to $500, for a frequency of 171 Hz, which in A440 is about an F<sub>3</sub>.

AUD1SWEEP (NR10) can automatically slide the frequency over time.  It distinguishes channel 1 from channel 2, which is otherwise identical but doesn't have sweep functionality.  The lower three bits are the magnitude of each change; bit 3 is a sign bit (0 for up, 1 for down), and bits 6–4 are a time that control how often the frequency changes.  (Setting the time to zero disables the sweep.)  Given a magnitude of $n$ and time $t$, every $\frac{t}{128}$ seconds, the frequency is multiplied by $1 ± \frac{1}{2^n}$.

Note that when I say "frequency" here, I'm referring to the 11-bit "frequency" value, **not** the actual frequency in Hz.  A "frequency" of $400 corresponds to 128 Hz, but halving it to $200 produces 85 Hz, a decrease of about a third.  Doubling it is _impossible_, because $800 doesn't fit in 11 bits.  This setup seems, ah, interesting to make music with.  Can't wait!

The above code sets this register to &#x24;1e, so $t = 1$, $n = 6$, and the frequency is decreasing; thus every $\frac{1}{128}$ seconds, the "frequency" drops by $\frac{1}{64}$.

Next is AUD1LEN (NR11), so named because its lower six bits set how long the sound will play.  Again we have inverse time: given a value $t$ in the low six bits, the sound will play for $\frac{64-t}{256}$ seconds.  Here those six bits are &x#24;10 or 16, so the sound lasts for $\frac{48}{256} = \frac{3}{16} = 0.1875$ seconds.  _Except_…  as mentioned above, this only applies if bit 6 of AUD1HIGH is set, which it isn't, so this doesn't apply at all and there's no point in setting any of these bits.  Hm.

The two high bits of AUD1LEN select the duty cycle, which is how long the square wave is high versus low.  (A "normal" square wave thus has a duty of 50%.)  Our value of 0 selects 12.5% high; the other values are 25% for 1, 50% for 2, or 75% for 3.  I do wonder if the author of this code meant to use 50% duty and put the bit in the wrong place?  If so, AUD1LEN should be $80, not $10.

Finally, AUD1ENV selects the volume envelope, which can increase or decrease over time.  Curiously, the resolution is higher here than in AUDVOL — the entire high nybble is the value of the envelope.  This value can be changed automatically over time in increments of 1: bit 3 controls the direction (0 to decrease, 1 to increase) and the low three bits control how often the value changes, counted in $\frac{1}{64}$ seconds.  For our value of &#x24;f3, the volume starts out at max and decreases every $\frac{3}{64}$ seconds, so it'll stop completely (or at least be muted?) after fifteen steps or $\frac{45}{64} ≈ 0.7$ seconds.

And hey, that's all more or less what I see if I record mGBA's output in Audacity!

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/05b-demo-sound-audacity.png" alt="Waveform of the above sound">
</div>

Boy!  What a horrible slog.  Don't worry; that's a good 75% of everything there is to know about the sound registers.  The second square wave is exactly the same except it can't do a frequency sweep.  The white noise channel is similar, except that instead of frequency, it has a few knobs for controlling how the noise is generated.  And the waveform channel is what the rest of this post is about—

"Hang on!" I hear you cry.  "That's a mighty funny-looking 'square' wave."

It sure is!  The Game Boy has some mighty funny sound hardware.  Don't worry about it.  I don't have any explanation, anyway.  I know the weird slope shapes are due to a high-pass filter capacitor that constantly degrades the signal gradually towards silence, but I don't know why the waveform isn't centered at zero.  (Note that mGBA has a bug and currently generates audio inverted, which is hard to notice audibly but which means the above graph is upside-down.)


## The thing I actually wanted to do

Right, back to the thing I actually wanted to do.

I have a sound.  I want to play it on a Game Boy.  I know this is possible, because Pokémon Yellow does it.

Channel 3 is a wavetable channel, which means I can define a completely arbitrary waveform (read: sound) and channel 3 will play it for me.  The correct approach seems obvious: slice the sound into small chunks and ask channel 3 to play them in sequence.

_How hard could this possibly be?_


### Channel 3

Channel 3 plays a waveform from _waveform RAM_, which is a block of 16 bytes in register space, from $FF30 through $FF3F.  Each nybble is one sample, so I have 32 samples whose values can range from 0 to 15.

32 samples is not a _whole_ lot; remember, a common audio rate is 44100 Hz.  To keep that up, I'd need to fill the buffer almost 1400 times per second.  I can use a lower sample rate, but what?  I guess I'll figure that out later.

First things first: I need to take my sound and cram it into this format, somehow.  Here's the sound I'm starting with.

<audio controls src="{filename}/media/cheezball/05c-aowr-original.wav"></audio>

The original recording was a bit quiet, so I popped it open in Audacity and stretched it to max volume.  I only have 4-bit samples, remember, and trying to cram a quiet sound into a low bitrate will lose most of the detail.

(A very weird thing about sound is that samples are really just measurements of _volume_.  Every feature of sound is nothing more than a change in volume.)

Now I need to turn this into a sequence of nybbles.  From [previous adventures]({filename}/2016-05-30-extracting-music-from-the-pico-8.markdown), I know that Python has a handy [`wave` module](https://docs.python.org/3/library/wave.html) for reading sample data directly from a WAV file, and so I wrote a crappy resampler:

```python
import wave

TARGET_RATE = 32768

with wave.open('aowr.wav') as w:
    nchannels, sample_width, framerate, nframes, _, _ = w.getparams()
    outdata = bytearray()
    gbdata = bytearray()

    frames_per_note = framerate // TARGET_RATE
    nybble = None
    while True:
        data = w.readframes(frames_per_note)
        if not data:
            break

        n = 0
        total = 0
        # Left and right channels are interleaved; this will pick up data from only channel 0
        for i in range(0, len(data), nchannels * sample_width):
            frame = int.from_bytes(data[i : i + sample_width], 'little', signed=True)
            n += 1
            total += frame

        # Crush the new sample to a nybble
        crushed_frame = int(total / n) >> (sample_width * 8 - 4)
        # Expand it back to the full sample size, to make a WAV simulating how it should sound
        encoded_crushed_frame = (crushed_frame << (sample_width * 8 - 4)).to_bytes(2, 'little', signed=True)
        outdata.extend(encoded_crushed_frame * (nchannels * frames_per_note))

        # Combine every two nybbles together.  The manual shows that the high nybble plays first.
        # WAV data is signed, but Game Boy nybbles are not, so add the rough midpoint of 7
        if nybble is None:
            nybble = crushed_frame + 7
        else:
            byte = (nybble << 4) | (crushed_frame + 7)
            gbdata.append(byte)
            nybble = None

    with wave.open('aowrcrush.wav', 'wb') as wout:
        wout.setparams(w.getparams())
        wout.writeframes(outdata)

with open('build/aowr.dat', 'wb') as f:
    f.write(gbdata)
```

This is incredibly bad.  It integer-divides the original rate by the target rate, so if I try to resample 44100 to 32768, I'll end up recreating the same sound again.

I don't know why I started with 32768, either.  The resulting data is too big to even fit in a section!  Kicking it down to 8192 is a bit better (5 samples to 1, so the real final rate is 8820), but if I get any smaller, too many samples cancel each other out and I end up with silence!  I have no idea what I am doing help.

The `aowrcrush.wav` file sounds a _little_ atrocious, fair warning.

<audio controls src="{filename}/media/cheezball/05d-aowr-crushed.wav"></audio>

But it seems to be correct, if I open it alongside the original:

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/05e-audacity-crush-comparison.png" alt="Waveforms of the original sound and its bitcrushed form; the latter is very blocky">
</div>

Crushing it to four bits caused the graph to stay fixed to only 16 possible values, which is why it's less smooth.  Reducing the sample rate made each sample last longer, which is why it's made up of short horizontal chunks.  (I resampled it back to 44100 for this comparison, so _really_ it's made of short horizontal chunks because each sample appears five times; Audacity wouldn't show an actual 8192 Hz file like this.)

It doesn't sound _great_, but maybe it'll be softened when played through a Game Boy.  Worst case, I can try cleaning it up later.  Let's get to the good part: playing it!


### Playing with channel 3

Here we go!  First the global setup stuff I had before.

```rgbasm
    ; Enable sound globally
    ld a, $80
    ldh [rAUDENA], a
    ; Map instruments to channels
    ld a, $44
    ldh [rAUDTERM], a
    ; Set volume
    ld a, $77
    ldh [rAUDVOL], a
```

Then some bits specific to channel 3.

```rgbasm
    ld a, $80
    ldh [rAUD3ENA], a
    ld a, $ff
    ldh [rAUD3LEN], a
    ld a, $20
    ldh [rAUD3LEVEL], a
SAMPLE_RATE EQU 8192
CH3_FREQUENCY set 2048 - 65536/(SAMPLE_RATE / 32)
    ld a, LOW(CH3_FREQUENCY)
    ldh [rAUD3LOW], a
    ld a, $80 | HIGH(CH3_FREQUENCY)
    ldh [rAUD3HIGH], a
```

Channel 3 has its own bit for toggling it on or off in AUD3ENA (NR30); none of the other bits are used.  The other new register is AUD3LEVEL (NR32), which is sort of a global volume control.  The only bits used are 6 and 5, which make a two-bit selector.  The options are:

- 00: mute
- 01: play nybbles as given
- 10: play nybbles shifted right 1
- 11: play nybbles shifted right 2

Three of those are obviously useless, so 01 it is!  That's where I get the $20.

Figuring out the frequency is a little more clumsy.  I used some rgbasm features here to do it for me, and it took a bit of fiddling to get it right.  For example, why am I using 65536 instead of 131072, the factor I said was used for the square wave?

The answer is that for the longest time I kept getting this absolutely horrible output, recorded directly from mGBA:

<audio controls src="{filename}/media/cheezball/05f-aowr-horrible.wav"></audio>

I had no idea what this was supposed to be.  Turns out it's, well, roughly what happens when you halve the Game Boy's idea of frequency.  I _finally_ found out this coefficient was different from [the gbdev wiki](http://gbdev.gg8.se/wiki/articles/Sound_Controller#FF1D_-_NR33_-_Channel_3_Frequency.27s_lower_data_.28W.29).  I'm guessing the factor of 2 has something to do with there being two nybbles per byte?

Then there's the division by 32, which _neither_ the manual _nor_ the gbdev wiki mention.  The frequency isn't actually the time it takes to play one _sample_, but the time it takes to play the entire _buffer_.  Which does make some sense — the "normal" use for the channel 3 is as a custom instrument, so you'd want to apply the frequency to the entire waveform to get the right notes out.  This was even more of a nightmare to figure out, since it produced…  well, mostly just garbage.  I'll leave it to your imagination.

```rgbasm
    ld a, 256 - 4096 / (SAMPLE_RATE / 32)
    ldh [rTMA], a
    ld a, 4
    ldh [rTAC], a
```

Oho!  TMA and TAC are new.

The CPU has a timer register, TIMA, which counts up every…  well, every so often.  It's only a single byte, and when it overflows, it generates a _timer interrupt_.  It then resets to the value of TMA.

TAC is the timer controller.  Bit 2 enables the timer, and the lower two bits select how fast the clock counts up.

Above, I'm using clock speed 00, which is 4096 Hz.  The expression for TMA computes `SAMPLE_RATE / 32`, which is the number of times per second that the entire waveform should play, and then divides that into 4096 to get the number of timer ticks that the waveform plays for.  Subtract that from 256, and I have the value TIMA should start with to ensure that it overflows at the right intervals.

I note that this will cause a timer interrupt _256 times per second_, which sounds like a lot on a CPU-constrained system.  It's only 4 or 5 interrupts per _frame_, though, so maybe it won't intrude too much.  I'll burn down that bridge when I come to it.

Now I just need to enable timer interrupts:

```rgbasm
start:
    ; Enable interrupts
    ld a, IEF_TIMER | IEF_VBLANK
    ldh [rIE], a
```

And of course do a call in the timer interrupt, which you may remember is a fixed place in the header:

```rgbasm
SECTION "Timer overflow interrupt", ROM0[$0050]
    call update_aowr
    reti
```

One last gotcha: I discovered that timer interrupts can fire _during OAM DMA_, a time when most of the memory map is inaccessible.  That's pretty bad!  So I also added `di` and `ei` around my DMA call.

Okay!  I'm so close!  All that's left is the implementation of `update_aowr`.

### Updating the waveform

```rgbasm
aowr:
INCBIN "build/aowr.dat"
aowr_end:

; ...

update_aowr:
    push hl
    push bc
    push de
    push af

    ; The current play position is stored in music_offset, a
    ; word in RAM somewhere.  Load its value into de
    ld hl, music_offset
    ld d, [hl]
    inc hl
    ld e, [hl]

    ; Compare this to aowr_end.  If it's >=, we've reached the
    ; end of the sound, so stop here.  (Note that the timer
    ; interrupt will keep firing!  This code is a first pass.)
    ld hl, aowr_end
    ld a, d
    cp a, h
    jr nc, .done
    jr nz, .continue
    ld a, e
    cp a, l
    jr nc, .done
    jr z, .done
.continue:

    ; Copy the play position back into hl, and copy 16 bytes
    ; into waveform RAM.  This unrolled loop is as quick as
    ; possible, to keep the gap between chunks short.
    ld h, d
    ld l, e
_addr = _AUD3WAVERAM
    REPT 16
    ld a, [hl+]
    ldh [_addr], a
_addr = _addr + 1
    ENDR

    ; Write the new play position into music_offset
    ld d, h
    ld e, l
    ld hl, music_offset
    ld [hl], d
    inc hl
    ld [hl], e
.done:
    pop af
    pop de
    pop bc
    pop hl
    ret
```

Perfect!  Let's give it a try.

<audio controls src="{filename}/media/cheezball/05g-aowr-mgba.wav"></audio>

Hey, that's not too bad!  I can see wiring that up to a button and pressing it relentlessly.  It's a bit rough, but it's not bad for this first attempt.

…

That _was_ mGBA, though, and I've had surprising problems before because I was reading or writing when the actual hardware wouldn't let me.  I guess it wouldn't hurt to try in bgb.  (_warning: very bad_)

<audio controls src="{filename}/media/cheezball/05h-disaster.wav"></audio>

**OH NO**

What has happened.


## Tragedy

A lot of fussing around, reading about [obscure trivia](http://gbdev.gg8.se/wiki/articles/Gameboy_sound_hardware#Obscure_Behavior), and being directed to [SamplePlayer](https://github.com/DevEd2/SamplePlayer) taught me a valuable lesson: you cannot write to waveform RAM while the wave channel is playing.

Okay.  No problem.  I'll just turn it off, write to wave RAM, then turn it back on.  Turning it off clears the frequency, but that's fine, I can just write it again.

```rgbasm
    ; Disable channel 3 to allow writing to wave RAM
    xor a
    ldh [rAUD3ENA], a

    ; ... do the copy ...

    ld a, $80
    ldh [rAUD3ENA], a
    ld a, LOW(CH3_FREQUENCY)
    ldh [rAUD3LOW], a
    ld a, $80 | HIGH(CH3_FREQUENCY)
    ldh [rAUD3HIGH], a
```

Okay!  Perfect!  I'm so ready for a meow!!!

<audio controls src="{filename}/media/cheezball/05i-spiky.wav"></audio>

_why god why_

This is what I get in mGBA and SameBoy.  Ironically, it plays fine in bgb.

It seems I have come to an impasse.

### Why

After a Herculean amount of debugging and discussion with people who actually know what they're talking about, here's what I understand to be happening.

When the wave channel first starts playing, it doesn't correctly read the very first nybble; instead, it uses the high nybble of whatever was already in its own internal buffer.

Disabling the wave channel sets its internal buffer to all zeroes.

I disable the wave channel every time it plays.  Effectively, every 32nd sample starting with the first is treated as zero, which is the most extreme negative value, which is why the playback looks like this (bearing in mind that mGBA's audio is currently upside-down):

<div class="prose-full-illustration">
<img src="{filename}/media/cheezball/05j-spike-visualized.png" alt="The above sound's waveform, which resembles the original, but with regularly spaced spikes">
</div>

For whatever reason, bgb doesn't emulate this spiking, so it plays fine.  I'm told the spiking also happens on actual hardware, but the speakers are cheap so it's harder to notice.

SamplePlayer isn't much help here, because it's subject to the same problem.

### A ray of hope, dashed

But wait!  There's one last thing I can try.  Pokémon Yellow has freeform sounds in it, and it doesn't have this spiking!  There's even a fan disassembly of it!

Alas.  Pokémon Yellow doesn't use channel 3 to play back sounds.  It uses channel _1_.

How, you ask?  Remember when I said earlier that hearing is really just detecting changes in volume?  Pokémon Yellow plays a constant square wave and simply _toggles it on and off_, very rapidly.  Channel 3 is 4-bit; the sounds Pokémon Yellow plays are _1-bit_, on or off.  It's baffling, but it does work.

I don't think it'll work for _me_, since that means 32 times as many interrupts.  In fact, Pokémon Yellow uses a busy loop as a timer, so it effectively freezes the entire rest of the game anytime it plays a Pikachu sound.  I'd rather not do that, but…  I don't seem to have a lot of options.

And so I've reached a dead end.  The spiking seems to be a fundamental bug with the Game Boy sound hardware.  I've found evidence that it may even still exist in the GBA, which uses a superset of the same hardware.  I can't fix it, I don't see how to work around it, and it sounds _really incredibly bad_.

After days of effort trying to get this to work, I had to shelve it.

The title of this post is a sort of _pun_, you see, a play on words—


## UPDATE: DRAMATIC TURNAROUND

HOT DAMN

With the problem laid bare, the homebrew community came through with a brilliant suggestion.

1. Re-enable channel 3, _but mute it_.
2. Start playing at a very high frequency, to get through the first sample as quickly as possible.
3. Change the frequency back to normal and _restart the channel_, via the high bit in `AUD3HIGH`.  Since the first byte is now in the buffer, the first sample should play correctly!
4. Don't forget to unmute the channel!

There are some tricky bits here.

The first is how to mute the channel.  The manual _claims_ that using zero in `AUD3LEVEL` will mute the sound, but both mGBA and SameBoy seem to agree that it actually plays _all zeroes_ — maximum negative amplitude.  That'll just recreate the spikes again, so that's out.  There's also the master volume knob `AUDVOL`, but that won't work if I ever try to play a sound at the same time as I'm playing music or something.  That basically just leaves `AUDTERM`, which lets me unplug the wave channel entirely — and luckily, the hardware is still generating output even if it's not going anywhere.

The second is _what_ frequency to use, exactly.  The obvious thing to try is the maximum possible frequency, which turns out to be 2 MHz…  but the Game Boy CPU only runs at 1 MHz, and it takes a couple instructions to change the frequency a second time, so a whole bunch of samples will have played in the meantime.

Instead, I worked backwards.  If I want a sample to last $n$ cycles, then the entire waveform lasts $32 n$ cycles, for a frequency of $\frac{2^{20}}{32 n} = \frac{2^{15}}{n}$ Hz (obtained by dividing into the CPU speed).  The frequency value I need is thus $2048 - \frac{65536}{\frac{2^{15}}{n}} = 2048 - 2 n$.  Counting the actual work I need to do: `ld a, CONSTANT` takes 2 cycles, and `ldh [CONSTANT], a` takes 3, so changing the frequency takes 10 cycles.  I need to be _between_ the first and second samples at this point, so let's say one sample takes 8 cycles to play, and the value I want is 2032.  Cool.

I tried this all out, and…  it totally didn't work!  _In mGBA._  But it _did_ work in SameBoy (which I am told has very very good audio emulation), so this still gave me a(nother) ray of hope.

I sprinkled mGBA with debug code and finally discovered something suspicious.  Its "mixer" looks like this (simplified):

```c
    int dcOffset = 8;
    int sample = dcOffset;

	if (audio->playingCh1) {
        sample -= audio->ch1.sample;
	}
	if (audio->playingCh2) {
        sample -= audio->ch2.sample;
	}
	if (audio->playingCh3) {
        sample -= audio->ch3.sample;
	}
	if (audio->playingCh4) {
        sample -= audio->ch4.sample;
	}

    return sample;
```

As we've seen, channel 3 uses unsigned values for its samples, so to convert them to virtually any modern audio format, you do need to subtract a midpoint to get a signed value.  That's what a DC offset is.

But this code isn't _quite_ doing that.  It applies the DC offset _once_ for the entire mixer, even though all four channels are unsigned.

This explains why I was still spiking in mGBA, though!  Once I'd unplugged channel 3, the audio system was still enabled _but zero channels were playing_, so the above code would produce `8`, which is interpreted as a signed value, which is… maximum amplitude!  Aha!  Spikes!

I changed it to this:

```c
    int dcOffset = 8;
    int sample = 0;

	if (audio->playingCh1) {
        sample += audio->ch1.sample - dcOffset;
	}
	if (audio->playingCh2) {
        sample += audio->ch2.sample - dcOffset;
	}
	if (audio->playingCh3) {
        sample += audio->ch3.sample - dcOffset;
	}
	if (audio->playingCh4) {
        sample += audio->ch4.sample - dcOffset;
	}

    return sample;
```

And the spikes went away!  As an added bonus, waveforms are no longer upside-down!  The result is so, so beautiful, _and_ virtually identical in every emulator:

<audio controls src="{filename}/media/cheezball/05k-aowr-success.wav"></audio>

***YES!!!***

I _think_ this problem was never noticeable on most games because it only ever adds a constant bias (based on the number of active channels, which would usually change infrequently), and a constant shift up or down sounds almost the same.  I've sent a PR to mGBA, and hopefully I'll have understood this correctly.  If not, well, back to despair.

Wow!  I did it.  Cool.  It took a mighty long time to get this working, and now I feel a bit silly since I don't have an inventory or even an audio engine to really plug this into yet.  I also want to capture a much more pestful meow from Anise, which is a little difficult since he only does his loudest meowing when we're not around.  This is fantastic progress, though!


## To be continued

This work doesn't correspond to a commit at all; it exists only as a local stash.  I'll clean it up later, once I figure out what to actually do with it.

Next time: _dialogue_!  With moderately less suffering along the way!
