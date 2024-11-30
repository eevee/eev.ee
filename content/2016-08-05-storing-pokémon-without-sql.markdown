title: Storing Pokémon without SQL
date: 2016-08-05 12:14
category: process
tags: tech, veekun, pokemon

I run [veekun](http://veekun.com/), a little niche Pokédex website that mostly focuses on (a) very accurate data for every version, derived directly from the games and (b) a bunch of nerdy nerd tools.

It's been languishing for a few years.  (Sorry.)  Part of it is that the team has never been very big, and all of us have either drifted away or gotten tied up in other things.

And part of it is that the schema absolutely sucks to work with.  I've been planning to fix it for a year or two now, and with Sun/Moon on the horizon, it's time I actually got around to doing that.

Alas!  I'm still unsure on some of the details.  I'm hoping if I talk them out, a clear best answer will present itself.  It's like advanced rubber duck debugging, with the added bonus that maybe a bunch of strangers will validate my thinking.

(Spoilers: I think I figured some stuff out by the end, so you don't actually need to read any of this.)

<!-- more -->

## The data

Pokémon has a lot of stuff going on under the hood.

- The Pokémon themselves have one or two types; a set of abilities; moves they might learn at a given level _or_ from a certain "tutor" NPC _or_ via a specific item; evolution via one of at least twelve different mechanisms and which may branch; items they may be holding in the wild; six stats, plus effort for those six stats; flavor text; and a variety of other little data.

- A number of Pokémon also have multiple forms, which can mean any number of differences that still "count" as the same Pokémon.  Some forms are purely cosmetic ([Unown](http://veekun.com/dex/pokemon/unown)); some affect the Pokémon's type ([Arceus](http://veekun.com/dex/pokemon/arceus)); some affect stats ([Pumpkaboo](http://veekun.com/dex/pokemon/pumpkaboo)); some affect learned moves ([Meowstic](http://veekun.com/dex/pokemon/meowstic)); some _swap out_ a signature move ([Rotom](http://veekun.com/dex/pokemon/rotom)); some disable evolution ([Pichu](http://veekun.com/dex/pokemon/pichu)).  Some forms can be switched at will; some switch automatically; some cannot be switched between at all.  There aren't really any hard and fast rules here.  They're effectively different Pokémon with the same name, except _most_ of the properties are the same.

- Moves are _fairly_ straightforward, except that their effects vary wildly and it would be mighty convenient to be able to categorize them in a way that's useful to a computer.  After 17 years of trying, I've still not managed this.

- Places connect to each other in various directions.  They also may have some number of wild Pokémon, which appear at given levels with given probability.  Oh, but certain conditions can change _some_ — but not all! — of the possible encounters in an area, making for a UI nightmare.  It gets particularly bad in Heart Gold and Soul Silver, where encounters (and their rates) are affected by time of day (morning, midday, night) _and_ the music you're playing (Sinnoh, Hoenn, none) _and_ whether there's an active swarm.  Try to make sense of [Rattata on Route 3](http://veekun.com/dex/pokemon/rattata/locations).

- Event Pokémon — those received from giveaways — may be given in several different ways, to several different regions, and may "lock" any of the Pokémon's attributes either to a specific value or a choice of values.

- And of course, all of this exists in at least eight different languages, plus a few languages with their own fanon vernacular, plus romanization for katakana and Hangul.

Even that would be all well and good, but the biggest problem of all is that _any and all of this can change_ between games.  Pairs of games — say, Red and Blue — tend to be mostly identical except for the encounters, since they come out at the same time.  [Spiky-Eared Pichu](http://veekun.com/dex/pokemon/pichu/flavor?form=spiky-eared) exists only in HGSS, and never appears again.  The move [Hypnosis](http://veekun.com/dex/moves/hypnosis) has 60% accuracy in every game, except in Diamond and Pearl, where it has 70% accuracy.  [Sand Attack](http://veekun.com/dex/moves/sand%20attack) is ground-type, except in the first generation of games, where it was normal.  Several Pokémon change how they evolve in later games, because they relied on a mechanic that was dropped.  The type strength/weakness chart has been updated a couple times.  And so on.

Oh, and there are several spin-off series, which often reuse the names of moves but completely change how they work.  The entire Mystery Dungeon series, for example.  Or even Pokémon Go.

This is awful.


## The current approach

Since time immemorial, veekun has used a relational database.  (Except for that one time I tried a single massive XML file, but let's not talk about that.)  It's already straining the limits of this format, and it doesn't even include half the stuff I just mentioned, like event Pokémon or where the move tutors are or Spiky-Eared Pichu's disabled evolution.

Just the basic information about the Pokémon themselves is spread across three tables: `pokemon_species`, `pokemon`, and `pokemon_forms`.  "Species" is supposed to be the pure essence of the name, so it contains stuff like "is this a baby" or "what does this evolve from/into" (which, in the case of Pichu, is already wrong!).  `pokemon_forms` contains every form imaginable, including all 28 Unown, and tries to loosely categorize them — but it also treats Pokémon _without_ forms as having a single "default" form.  And then `pokemon` contains a somewhat arbitrary subset of forms and tacks other data onto them.  Other tables arbitrarily join to whichever of these is most appropriate.

Tables may also be segmented by "version" (Red), "version group" (Red and Blue), or "generation" (Red, Blue, and Yellow), depending on when the data tends to vary.  Oh, but there are also a number of `conquest_*` tables for Pokémon Conquest, which doesn't have a row in `versions` since it's not a mainline version.  And I think there's a goofy hack for Stadium in there somewhere.

For data that virtually never varies, except that one time it did, we...  don't really do anything.  Base EXP was completely overhauled in X and Y, for example, and we only have a single `base_experience` column in the `pokemon` table, so it just contains the new X and Y values.  What if you want to know about experience for an older game?  Well, oops.  Similarly, the type chart is the one from X and Y, which is no longer correct for previous games.

Aligning entities across games can be a little tricky, too.  Earlier games had the Itemfinder, gen 5 had the Dowsing MCHN, and now we have the Dowsing Machine.  These are all clearly the same item, but only the name Dowsing Machine appears anywhere in veekun, because there's no support for changing _names_ across games.  The last few games also technically "renamed" every move and Pokémon from all-caps to title case, but this isn't reflected anywhere.  In fact, the all-caps names have never appeared on veekun.

_All_ canonical textual data, including the names of fundamental entities like Pokémon and moves, are in separate tables so they can be separated by language as well.  Numerous combinations of languages/games are missing, and I don't think we actually have a list of which games were even released in which languages.

The result is a massive spread of tables, many of them very narrow but very tall, with joins that are not obvious if you're not a DBA.  I forget how half of it works if I haven't looked at it in at least a month.  I make this stuff [available for anyone to use](https://github.com/veekun/pokedex/), too, so I would greatly prefer if it were (a) understandable by mortals and (b) not comically incomplete in poorly-documented ways.

I think a lot of this is a fear of massively duplicating the pile of data we've already got.  Fixing the Dowsing Machine thing, for example, would require duplicating the name of _every single item_ for _every single game_, just to fix this one item that was renamed twice.  Fixing the base EXP problem would require yet another new table _just_ for base experience, solely because it changed once.

It's long past time to fix this.


## SQL is bad, actually

(Let me cut you off right now: NoSQL is worse.)

I like the _idea_ of a relational database.  You have a schema describing your data, and you can link it together in myriad different ways, and it's all built around set operations, and wow that's pretty cool.

The actual implementation leaves a little to be desired.  You can really only describe _anything_ as flat tuples.  You want to have things that can contain several other things, perhaps in order?  Great!  Make another flat tuple describing that, and make sure you remember to ask for the order explicitly, every single time you query.

Oh boy, querying.  Querying is so, _so_ tedious.  You can't even use all your carefully-constructed foreign key constraints as a shortcut; you have to write out `foo.bar_id = bar.id` in full every single time.

There are GUIs and whatnot, but the focus is all wrong.  It's on tables.  Of _course_ it's on tables, but a single table is frequently not a useful thing to see on its own.  For any given kind of entity (as defined however you think about your application), a table probably only contains a slice of what the entity is about, but it contains that slice for every single instance.  Meanwhile, you can't actually see a single entity on its own.

I'll repeat that: you _cannot_.

Consider, for example, a Pokémon.  A Pokémon has up to two types, which are rather fundamental properties.  How do you view or fetch the Pokémon and its types?

Fuck you, that's how.  If you join `pokemon` to `pokemon_types`, you get this goofy result where everything about the Pokémon is potentially duplicated, but each row contains a distinct type.

Want to see abilities as well?  There can be up to three of those!  Join to _both_ `pokemon_abilities` and `pokemon_types`, and now you get up to _six_ rows, which looks increasingly not at all like what you actually wanted.  Want moves as well?  Good luck.

I don't understand how this is still the case.  SQL is 42 years old!  How has it not evolved to have even the slightest nod towards the existence of nested data?  This isn't some niche use case; it's responsible for at least a third of veekun's tables!

This die-hard focus on data-as-spreadsheets is probably why we've tried so hard to avoid "duplication", even when it's the correct thing to do.  The fundamental unit of a relational database is the _table_, and seeing a table full of the same information copied over and over just _feels wrong_.

But it's really the focus on tables that's wrong.  The important point isn't that Bulbasaur is named "BULBASAUR" in ten different games; it's that each of those games has a name for Bulbasaur, and it happens to be the same much of the time.

NoSQL exists, yes, but I don't trust anyone who looked at SQL and decided that the _real_ problem was that it has too _much_ schema.

I _know_ the structure of my data, and I'm happy to have it be enforced.  The problem isn't that writing a schema is hard.  The problem is that any schema that doesn't look like a bank ledger maps fairly poorly to SQL primitives.  It works, and it's correct (if you can figure out how to express what you want), but the ergonomics are atrocious.

We've papered over some of this with SQLAlchemy's excellent ORM, but you have to be _very good_ at SQLAlchemy to make the mapping natural, which is the whole goal of using an ORM.  I'm _pretty_ good, and it's still fairly clumsy.


## A new idea

So.  How about YAML?

See, despite our hesitation to duplicate everything, the dataset really isn't that big.  All of the data combined are a paltry 17MB, which could fit in RAM without much trouble; then we could search and wrangle it with regular Python operations.  I could still have a schema, remember, because [I wrote a thing for that]({filename}/release/2015-10-15-dont-use-pickle-use-camel.markdown).  And other people could probably make more sense of some YAML files than CSV dumps (!) of a tangled relational database.

The idea is to re-dump every game into its own set of YAML files, describing just the raw data in a form generic enough that it can handle every (main series) game.  I did a [proof of concept of this](https://gist.github.com/eevee/b53b4babd7a0fc8aead7) for Pokémon earlier this year, and it looks like:

```yaml
%TAG !dex! tag:veekun.com,2005:pokedex/
--- !!omap
- bulbasaur: !dex!pokemon
    name: BULBASAUR
    types:
    - grass
    - poison
    base-stats:
      attack: 49
      defense: 49
      hp: 45
      special: 65
      speed: 45
    growth-rate: medium-slow
    base-experience: 64
    pokedex-numbers:
      kanto: 1
    evolutions:
    - into: ivysaur
      minimum-level: 16
      trigger: level-up
    species: SEED
    flavor-text: "A strange seed was\nplanted on its\nback at birth.\fThe plant sprouts\nand
      grows with\nthis POKéMON."
    height: 28
    weight: 150
    moves:
      level-up:
      - 1: tackle
      # ...
    game-index: 153
```

This is all just regular ol' [YAML syntax](http://camel.readthedocs.io/en/latest/yamlref.html).  This is for English Red; there'd also be one for French Red, Spanish Red, etc.  Ultimately, there'd be a _lot_ of files, with a separate set for every game in every language.

The UI will have to figure out when some datum was the same in every game, but it frequently does that even _now_, so that's not a significant new burden.  If anything, it's an improvement, since now it'll be happening only in one place; right now there are a lot of ad-hoc "deduplication" steps done behind the scenes when we add new data.

I like this idea, but I still feel very uneasy about it for unclear reasons.  It _is_ a wee bit out there.  I could just take this same approach of "fuck it, store everything" and still use a relational database.  But look at this little chunk of data; it already tells you plenty of interesting facts about Bulbasaur and _only_ Bulbasaur, yet it would need at least half a dozen tables to express in a relational database.  And you couldn't inspect _just Bulbasaur_, and you'd have to do multiple queries to actually get everything, and there'd be no useful way to work with the data independently of the app, and so on.  Worst of all, the structure is often not remotely obvious from looking at the tables, whereas you can literally _see it_ in YAML syntax.

There are other advantages, as well:

- A schema can still be enforced Python-side, using the `camel` loader, which by the way will produce _objects_ rather than plain dicts.  (That's what the `!dex!pokemon` [tag](http://camel.readthedocs.io/en/latest/yamlref.html#tags) is for.)
- If you don't care about veekun at all and just want data, you have it in a straightforward format, for any version you like.
- YAML libraries are fairly common, and even someone with very limited programming experience can make sense of the above structure.  Currently we store CSV database dumps and offer a tool to load into an RDBMS, which has led to a number of bug reports about obscure compatibility issues with various databases, as well as numerous emails from people who are confused about how to load the data or even about what a database is.
- It's much more obvious what's missing.  If there's no directory for Pokémon Yellow, surprise!  That means we don't have Pokémon Yellow.  If the directory exists but there's no `places.yaml`, guess what we're missing!  Figuring out what's there and what's not in a relational system is much more difficult; I only recently realized that we don't have flavor text for any game before Black/White.
- I'll never again have to rearchitect the schema because a new game changed something I didn't expect could ever change.  Similarly, the UI can drop a lot of special cases for "this changes between games", "this changes between generations", etc. and treat it all consistently.
- Pokémon forms can just be two Pokémon with the same species name.  Fuck it, store everything.  YAML even has ["merge" syntax](http://camel.readthedocs.io/en/latest/yamlref.html#merge-keys) built right in that can elide the common parts.  (This isn't shown above, and I don't know exactly what the syntax looks like yet.)

Good idea?  Sure, maybe?  Okay let's look at some details, where the devil's in.


## Problems

There are several, and they are blocking my progress on this, and I only have three months to go.

### Speed

There will be a _lot_ of YAML, and loading a _lot_ of YAML is not particularly quick, even with pyyaml's C loader.  YAML is a complicated format and this is a lot of text to chew through.  I won't know for sure how slow this is until I actually have more than a handful of games in this format, though.

I have a similar concern about memory use, since I'll suddenly be storing a _whole lot_ of identical data.  I do have an idea for reducing memory use for strings, which is basically manual interning:

```python
string_datum = big_ol_string_dict.setdefault(string_datum, string_datum)
```

If I load two YAML files that contain the same string, I can reuse the first one instead of keeping two copies around for no reason.  (Strings are immutable in Python, so this is fine.)

Alas, I've seen this done before, and it does have a teeny bit of overhead, which might make the speed issue even worse.

So I think what I'm going to do is load everything into objects, resolve duplicate strings, and then...  store it all in a pickle!  Then the next time the app goes to load the data, if the pickle is newer than any of the files, just load the pickle instead.  Pickle is a well-specified binary format (much faster to parse) and should be able to remember that strings have already been de-duplicated.

I know, I know: I said [don't use pickle]({filename}/release/2015-10-15-dont-use-pickle-use-camel.markdown).  This is the _one_ case where pickle is actually useful: as a disposable cache.  It doesn't leave the machine, so there are no security concerns; it's not shared between multiple copies of the app at the same time; and if it fails to load for any reason at all, the app can silently trash it and load the data directly.

I just hope that pickle will be quick enough, or this whole idea falls apart.  Trouble is, I can't know for _sure_ until I'm halfway done.


### Languages versus games

Earlier I implied that every single game would get its own set of data: English Red has a set of files, French Red has the same set of files, etc.

For the very early games, this directly reflects their structure: each region got its own cartridge with the game in a single language.  Different languages might have different character sets, [different UI](https://tcrf.net/Pok%C3%A9mon_Gold_and_Silver#Summary_Screens), different encounters (Phanpy and Teddiursa were swapped in Gold and Silver's Western releases), different mechanics (leech moves fail against a Substitute in gen 1, but only in Japanese), and different graphics (several Gold and Silver trainer classes were [slightly censored](https://tcrf.net/Pok%C3%A9mon_Gold_and_Silver/Changed_Graphics) outside of Japan).  You could very well argue that they're distinct games.

The increased storage space of the Nintendo DS changed things.  The games were still released regionally, but every game contains every language's flavor text and "genus (the stuff you see in the Pokédex).  This was an actual feature of the game: if you received a Pokémon caught in another language — made much easier by the introduction of online trading — then you'd get the flavor text _for that language_ in your Pokédex.

The DS versions also use a filesystem rather than baking everything into the binary, so very little _code_ needed to change between languages; everything of interest was in text files.

From X and Y, there _are no_ localizations.  Every game contains the full names and descriptions of everything, plus the _entire game script_, in every language.  In fact, you can choose which language to play the game in — in an almost unprecedented move for a Nintendo game, an American player with the American copy of the game can play the entire thing in Japanese.

(If this weren't the case, you'd need an entire separate 3DS to do that, since the 3DS is region-locked.  Thanks, Nintendo.)

The question, then, is how to sensibly store all this.

----

With the example YAML above, human-language details like names and flavor text are baked right into the Pokémon.  This makes sense in the context of a single game, where those _are_ properties of a Pokémon.  If you take that to be the schema, then the obvious thing to do is to have a separate file for every game in every language: `/red/en/pokemon.yaml`, `/red/fr/pokemon.yaml`, and so on.

This isn't _ideal_, since _most_ of the other data is going to be the same.  But those games are also the smallest, and anyway this captures the rare oddball difference like Phanpy and Teddiursa (though hell if I know how to express that in the UI).

With X and Y, everything goes out the window.  There are effectively no separate games any more, so `/x/en` versus `/x/fr` makes no sense.  It's very clear now that flavor text — and even names — aren't direct properties of the Pokémon, but of some combination of the Pokémon and the _player_.

----

One option is to put some flexibility in the directory structure.

```text
/red
  /en
    pokemon.yaml
    pokemon-text.yaml
  /ja
    pokemon.yaml
    pokemon-text.yaml
...
/x
  pokemon.yaml
  /en
    pokemon-text.yaml
  /ja
    pokemon-text.yaml
```

A `pokemon-text.yaml` file would be a very simple mapping.

```yaml
bulbasaur:
    name: BULBASAUR
    species: SEED
    flavor-text: "A strange seed was\nplanted on its\nback at birth.\fThe plant sprouts\nand
      grows with\nthis POKéMON."
ivysaur:
    ...
```

(Note that the lower-case keys like `bulbasaur` are _identifiers_, not names — they're human-readable and obviously based on the English names, but they're supposed to be treated as opaque dev-only keys.  In fact I might try to obfuscate them further, to discourage anyone from title-casing them and calling them names.)

Something about this doesn't sit well.  I think part of it is that the structure in `pokemon-text.yaml` doesn't represent a meaningful _thing_, which is somewhat at odds with the idea of loading each file directly into a set of objects.  With this approach, I have to patchwork update existing objects as I go.

It's kind of a philosophical quibble, granted.

----

An extreme solution would be to _pretend_ that X and Y are several different games: have `/x/en` and `/x/fr`, even though they contain _mostly_ the same information taken from the same source.

I don't think that's a great idea, especially since the merged approach will surely be how all future games work as well.

----

At the other extreme, I could treat the older games as though they were separate versions themselves.  Add a grouping called "cartridge" or something that's a subset of "version".  Many of the oddball differences are between the Japanese version and _everyone else_, too.

There's even a little justification for this in the way the first few games were released.  Japan first got Red and Green, which had goofy art and were very buggy; they were later polished and released as the _single_ version Japanese Blue, which became the basis for worldwide releases of Red and Blue.  Japanese Red is a fairly different game from American Red; Japanese Blue is closer to American Blue but still not really the same.  veekun already has a couple of nods towards this, such as having separate Red/Green and Red/Blue sprite art.

That would lead to a list of games like `jp-red`, `jp-green`, `jp-blue`, `ww-red`, `ww-blue`, `yellow` (I think they were similar across the board), `jp-gold`, `jp-silver`, `ww-gold`, `ww-silver`, `crystal` (again, I don't think there were any differences), and so on.  The schema would look like:

```yaml
bulbasaur:
    name:
        en: BULBASAUR
        fr: BULBIZARRE
        es: BULBASAUR
        ...
    flavor-text:
        en: "A strange seed was\nplanted on its\nback at birth.\fThe plant sprouts\nand
          grows with\nthis POKéMON."
        ...
```

The Japanese games, of course, would only have Japanese entries.  A huge advantage of this approach is that it also works perfectly with the newer games, where this is effectively the structure of the original data anyway.

This does raise the question of exactly how I generate such a file without constantly reloading and redumping it.  I guess I could dump every language game at the same time.  That would also let me verify that there are no differences besides text.

The downside is mostly that the UI would have to consolidate this, and the results might be a little funky.  Merging `jp-gold` with `ww-gold` and just calling it "Gold" when the information is the same, okay, sure, that's easy and makes sense.  `jp-red` versus `ww-red` is a bit weirder of a case.  On the other hand, veekun currently pretends Red and Green didn't even exist, which is certainly wrong.

I'd have to look more into the precise differences to be sure this would actually work, but the more I think about it, the more reasonable this sounds.  Probably the biggest benefit is that non-text data would only differ across games, not potentially across games _and_ languages.

Wow, this might be a really good idea.  And it had never occurred to me before writing this section.  This rubber duck thing really works, thanks!


### Forms

As mentioned above, rather than try to group forms into various different tiers based on how much they differ, I might as well just go whole hog and have every form act as a completely distinct Pokémon.

Doing this with YAML's merge syntax would even make the differences crystal clear:

```yaml
plant-wormadam:
    &plant-wormadam
    types: [bug, grass]
    abilities:
        1: anticipation
        2: anticipation
        hidden: overcoat
    moves:
        ...
    # etc
trash-wormadam:
    <<: *plant-wormadam  # means "merge in everything from this other node"
    types: [bug, ground]
    moves:
        ...
# Even better:
unown-a:
    &unown-a
    types: [psychic]
    name: ...
    # whatever else
unown-c:
    <<: *unown-a
unown-d:
    <<: *unown-a
unown-e:
    <<: *unown-a
```

One catch is that I don't know how to convince PyYAML to _output_ merge nodes, though it's perfectly happy to read them.

But wait, hang on.  This is a list of _Pokémon_, not forms.  Wormadam is a Pokémon.  Plant Wormadam is a form.

Right?

This distinction has haunted us rather thoroughly since we first tried to support it with Diamond and Pearl.  The website is still a little weird about this: it acts as though "Plant Wormadam" is the name of a distinct Pokémon (because it affects type) and has distinct pages for Sandy and Trash Wormadam, but "Burmy" is a single page, even though Wormadam evolves from Burmy and they have the same forms.  (In Burmy's case, though, form only affects the sprite and nothing else.)  You can also get distinct forms in search results, which may or may not be what you want — but it also may or may not make sense to "ignore" forms when searching.  In many cases we've arbitrarily chosen a form as the "default" even when there isn't a clear one, just so you get something useful when you type in "wormadam".

Either way, there needs to be _something_ connecting them.  Merge keys are only a shorthand for writing YAML; they're completely invisible to app code and don't exist in the deserialized data.

YAML does have a nice shorthand syntax for a list of mappings:

```yaml
bulbasaur:
-   name: ...
    types: ...
unown:
-   &unown-a
    name: ...
    types: ...
    form: a
-   <<: *unown-a
    form: b
-   <<: *unown-a
    form: c
...
```

Hm, now we lose the `unown-a` that functions as the actual identifier for the form.

Alternatively, there could be an entire separate _type_ for sets of forms, since we do have tags here.

```yaml
bulbasaur: !dex!pokemon
    name: ...
unown: !dex!pokemon-form-set
    unown-a: !dex!pokemon
        name: ...
    unown-b: !dex!pokemon
        ...
```

An unadorned `Pokemon` could act as a set of 1, then?  I guess?

Come to think of it, this knits with another question: where does data specific to a _set of forms_ go?  Data like "can you switch between forms" and "is this purely cosmetic".  We can't readily get that from the games, since it's code rather than data.

It's also _extremely_ unlikely to ever change, since it's a fundamental part of each multi-form Pokémon's in-universe lore.  So it makes sense to store that stuff in some separate manually-curated place, right?  In which case, we could do the same for storing which sets of forms "count" as the same Pokémon.  That is, the data files could contain `plant-wormadam` and `sandy-wormadam` as though they were completely distinct, and then we'd have our own bits on top (which we _need anyway_) to say that, hey, those are both forms of the same thing, `wormadam`.

That mirrors how the actual games handle this, too — the three Wormadam forms have completely separate stat/etc. structs.

Ah, but the games _don't_ store the Burmy or Unown forms separately, because they're cosmetic.  How does _our_ code handle that?  I guess there's only one `unown`, and then we also know that there are 28 possible sprites?

But Arceus's forms have different types, and they're not stored separately either.  (I think you could argue that Arceus is cosmetic-only, the cosmetic form is changed by Arceus's type, and Arceus's type is really just changed by Arceus's ability.  I'm pretty sure the ability doesn't work if you hack it onto any other Pokémon, but I can't remember whether Arceus still changes type if hacked to have a different ability.)

Relying too much on outside information also makes the data a teeny bit harder for anyone else to use; suddenly they have three Wormadams, none of which are quite called "Wormadam", but all of which share the same Pokédex number.  (Oh, right, we could just link them by Pokédex number.)  That _feels_ goofy, but if what you're after is something with a definitive set of types, there _is_ nothing called simply "Wormadam".

Oh, and there's a minigame that only exists in Heart Gold and Soul Silver, but that has different stats even for cosmetic forms.  Christ.

I don't think there's any perfect answer here.  I have a [list of all the forms](https://gist.github.com/eevee/15a92e26088d79a77fca) if you'd like to see more of this madness.


### The Python API

So you want to load all this data and do stuff with it.  Cool.  There'll be a class like this:

```python
class Pokemon(Locus):
    types = List(Type, min=1, max=2)
    growth_rate = Scalar(GrowthRate)
    game_index = Scalar(int)
    ...
```

You know, a little declarative schema that matches the YAML structure.  I love declarative classes.

The big question here is what a `Pokemon` _is_.  (Besides whether it's a form or not.)  Is it a wrapper around all the possible data from every possible game, or just the data from one particular game?  Probably the former, since the latter would mean having some twenty different `Pokemon` all called `bulbasaur` and that's weird.

(Arguably, the former would be wrong because much of this stuff only applies to the main games and not Mystery Dungeon or Ranger or whatever else.  That's a very different problem that I'll worry about later.)

I guess then a `Pokemon` would wrap all its attributes in a kind of amalgamation object:

```python
print(pokemon)                          # <Pokemon: bulbasaur>
print(pokemon.growth_rate)              # <MultiValue: bulbasaur.growth_rate>
current = Game.latest
print(current)                          # <Game: alpha-sapphire>
print(pokemon.growth_rate[current])     # <GrowthRate: medium-slow>
pokemonv = pokemon.for_version(current)
print(pokemonv)                         # <Pokemon: bulbsaur/alpha-sapphire>
print(pokemonv.growth_rate)             # <GrowthRate: medium-slow>
```

There's one more level you might want: a wrapper that slices by language solely for your own convenience, so you can say `print(some_pokemon.name)` and get a single string rather than a thing that contains all of them.

Should you be able to slice by language but _not_ by version, so `pokemon.name` is a thing containing all English names across all the games?  I guess that sounds reasonable to want, right?  It would also let you treat text like any other property, which could be handy.

```python
print(pokemon)                          # <Pokemon: bulbasaur>
print(pokemon.growth_rate)              # <MultiValue: bulbasaur.growth_rate>
# I'm making up method names on the fly here, so.
# Also there will probably be a few ways to group together changed properties,
# depending entirely on what the UI needs.
print(pokemon.growth_rate.meld())       # [((...every game...), <GrowthRate: medium-slow>)]
print(pokemon.growth_rate.unify())      # <GrowthRate: medium-slow>
pokemonl = pokemon.for_language(Language['en'])
print(pokemonl.name)                    # <MultiValue: bulbasaur.name>
print(pokemonl.name.meld())             # [((<Game: ww-red>, ...), 'BULBASAUR'), ((<Game: x>, ...), 'Bulbasaur')]
print(pokemonl.name.unify())            # None, maybe ValueError?
```

(Having written all of this, I suddenly realize that I'm targeting Python 3, where I can use é in class names.  Which I am probably going to do a lot.)

I think...  this all...  seems reasonable and doable.  It'll require some clever wrapper types, but that's okay.


## Hmm

I know these are relatively minor problems in the grand scheme of things.  People handle hundreds of millions of rows in poorly-designed MySQL tables all the time and manage just fine.  I'm mostly waffling because this is a lot of (hobby!) work and I've already been through several of these rearchitecturings and I'm tired of discovering the dozens of drawbacks only _after_ all the work is done.

Writing this out has provided some clarity, though, and I think I have a better idea of what I want to do.  So, thanks.

I'd like to have a proof of concept of this, covering some arbitrary but representative subset of games, by the end of the month.  Keep your eyes peeled.
