title: JavaScript got better while I wasn't looking
date: 2017-10-07 10:05
category: blog
tags: tech, patreon

[IndustrialRobot](https://www.patreon.com/user/creators?u=199476) has generously donated in order to inquire:

> In the last few years there seems to have been a lot of activity with adding emojis to Unicode. Has there been an equal effort to add 'real' languages/glyph systems/etc?
>
> And as always, if you don't have anything to say on that topic, feel free to choose your own. :p

Yes.

I mean, each release of Unicode lists major new additions right at the top — [Unicode 10](http://www.unicode.org/versions/Unicode10.0.0/#Summary), [Unicode 9](http://www.unicode.org/versions/Unicode9.0.0/#Summary), [Unicode 8](http://www.unicode.org/versions/Unicode8.0.0/#Summary), etc.  They also keep fastidious notes, so you can also dig into how and why these new scripts came from, by reading e.g. [the proposal for the addition of Zanabazar Square](http://www.unicode.org/L2/L2015/15337-zanabazar-square.pdf).  I don't think I have much to add here; I'm not a real linguist, I only play one on TV.

So with that out of the way, here's something completely different!

<!-- more -->


## A brief history of JavaScript

JavaScript was created in seven days, about eight thousand years ago.  It was pretty rough, and it stayed rough for most of its life.  But that was fine, because no one used it for anything besides having a trail of sparkles follow your mouse on their Xanga profile.

Then people discovered you could actually do a handful of useful things with JavaScript, and it saw a sharp uptick in usage.  Alas, it stayed pretty rough.  So we came up with polyfills and jQuerys and all kinds of miscellaneous things that tried to smooth over the rough parts, to varying degrees of success.

And...  that's it.  That's pretty much how things stayed for a while.

----

I have complicated feelings about JavaScript.  I don't _hate_ it…  but I certainly don't _enjoy_ it, either.  It has some pretty neat ideas, like prototypical inheritance and "everything is a value", but it buries them under a pile of annoying quirks and a woefully inadequate standard library.  The DOM APIs don't make things much better — they seem to be designed as though the target language were Java, rarely taking advantage of any interesting JavaScript features.  And the places where the APIs overlap with the language are a hilarious mess: I have to check documentation _every single time_ I use any API that returns a set of things, because there are at least three totally different conventions for handling that and I can't keep them straight.

The funny thing is that I've been fairly happy to work with Lua, even though it shares most of the same obvious quirks as JavaScript.  Both languages are weakly typed; both treat nonexistent variables and keys as simply false values, rather than errors; both have a single data structure that doubles as both a list and a map; both use 64-bit floating-point as their only numeric type (though Lua added integers very recently); both lack a standard object model; both have very tiny standard libraries.  Hell, Lua doesn't even have exceptions, not really — you have to fake them in much the same style as Perl.

And yet none of this bothers me nearly as much in Lua.  The _differences_ between the languages are very subtle, but combined they make a huge impact.

- Lua has separate operators for addition and concatenation, so `+` is never ambiguous.  It also has `printf`-style string formatting in the standard library.

- Lua's method calls are syntactic sugar: `foo:bar()` just means `foo.bar(foo)`.  Lua doesn't even have a special `this` or `self` value; the invocant just becomes the first argument.  In contrast, JavaScript invokes some hand-waved magic to set its contextual `this` variable, which has led to no end of confusion.

- Lua has an [iteration protocol]({filename}/2016-11-18-iteration-in-one-language-then-all-the-others.markdown), as well as built-in iterators for dealing with list-style or map-style data.  JavaScript has a special dedicated `Array` type and clumsy built-in iteration syntax.

- Lua has operator overloading and (surprisingly flexible) module importing.

- Lua allows the keys of a map to be any value (though non-scalars are always compared by identity).  JavaScript implicitly converts keys to strings — and since there's no operator overloading, there's no way to natively fix this.

These are fairly minor differences, in the grand scheme of language design.  And almost every feature in Lua is implemented in a ridiculously simple way; in fact the entire language is described in complete detail in a [single web page](https://www.lua.org/manual/5.3/manual.html).  So writing JavaScript is always frustrating for me: the language is _so close_ to being much more ergonomic, and yet, it isn't.

Or, so I thought.  As it turns out, while I've been off doing other stuff for a few years, browser vendors have been implementing all this pie-in-the-sky stuff from "ES5" and "ES6", whatever those are.  People even upgrade their browsers now.  Lo and behold, the last time I went to write JavaScript, I found out that a number of papercuts had actually been _solved_, and the solutions were sufficiently widely available that I could actually _use them in web code_.

The weird thing is that I _do_ hear a lot about JavaScript, but the feature I've seen raved the most about _by far_ is probably...  built-in types for working with arrays of bytes?  That's cool and all, but not exactly the most pressing concern for me.

Anyway, if you also haven't been keeping tabs on the world of JavaScript, here are some things we missed.


## `let`

_[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let) — supported in Firefox 44, Chrome 41, IE 11, Safari 10_

I'm pretty sure I first saw `let` over a decade ago.  Firefox has supported it for ages, but you actually had to _opt in_ by specifying JavaScript version 1.7.  Remember JavaScript versions?  You know, from back in the days when people actually [suggested you write stuff like this](http://www.webreference.com/js/column26/version.html):

```html
<SCRIPT LANGUAGE="JavaScript1.2" TYPE="text/javascript">
```

Yikes.

Anyway, so, `let` declares a variable — but scoped to the immediately containing _block_, unlike `var`, which scopes to the innermost _function_.  The trouble with `var` was that it was very easy to make misleading:

```javascript
// foo exists here
while (true) {
    var foo = ...;
    ...
}
// foo exists here too
```

If you reused the same temporary variable name in a different block, or if you expected to be shadowing an outer `foo`, or if you were trying to do something with creating closures in a loop, this would cause you some trouble.

But no more, because `let` actually scopes the way it looks like it should, the way variable declarations do in C and friends.  As an added bonus, if you refer to a variable declared with `let` _outside_ of where it's valid, you'll get a `ReferenceError` instead of a silent `undefined` value.  Hooray!

There's one other interesting quirk to `let` that I can't find explicitly documented.  Consider:

```javascript
let closures = [];
for (let i = 0; i < 4; i++) {
    closures.push(function() { console.log(i); });
}
for (let j = 0; j < closures.length; j++) {
    closures[j]();
}
```

If this code had used `var i`, then it would print `4` four times, because the function-scoped `var i` means each closure is sharing the same `i`, whose final value is `4`.  With `let`, the output is `0 1 2 3`, as you might expect, because each run through the loop gets its own `i`.

But wait, hang on.

The semantics of a C-style `for` are that the first expression is only evaluated _once_, at the very beginning.  So there's only one `let i`.  In fact, it makes no sense for each run through the loop to have a distinct `i`, because the whole idea of the loop is to _modify_ `i` each time with `i++`.

I assume this is simply a special case, since it's what everyone expects.  We expect it _so_ much that I can't find anyone pointing out that the usual explanation for why it works makes no sense.  It has the interesting side effect that `for` no longer de-sugars to a `while` the same way as in C, since this will print all `4`s:

```javascript
closures = [];
let i = 0;
while (i < 4) {
    closures.push(function() { console.log(i); });
    i++;
}
for (let j = 0; j < closures.length; j++) {
    closures[j]();
}
```

You'd need to introduce an anonymous temporary state variable to recreate the same effect.  This isn't a problem — I'm _glad_ `let` works this way! — it just stands out to me as interesting.  Lua doesn't need a special case here, since it uses an iterator protocol that produces values rather than mutating a visible state variable, so there's no problem with having the loop variable be truly distinct on each run through the loop.


## Classes

_[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) — supported in Firefox 45, Chrome 42, Safari 9, Edge 13_

Prototypical inheritance is pretty cool.  The way JavaScript presents it is a _little bit_ opaque, unfortunately, which seems to confuse a lot of people.  JavaScript gives you enough functionality to make it work, and even makes it sound like a first-class feature with a property outright called `prototype`...  but to actually _use_ it, you have to do a bunch of weird stuff that doesn't much look like constructing an object or type.

The funny thing is, people with almost any background get along with Python just fine, and _Python uses prototypical inheritance_!  Nobody ever seems to notice this, because Python tucks it neatly behind a `class` block that works _enough_ like a Java-style class.  (Python also handles inheritance without using the prototype, so it's a little different...  but I digress.  Maybe in another post.)

The point is, there's nothing fundamentally _wrong_ with how JavaScript handles objects; the ergonomics are just terrible.

Lo!  They finally added a `class` keyword.  Or, rather, they finally made the `class` keyword _do_ something; it's been reserved this entire time.

```javascript
class Vector {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    get magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    dot(other) {
        return this.x * other.x + this.y * other.y;
    }
}
```

This is all just sugar for existing features: creating a `Vector` function to act as the constructor, assigning a function to `Vector.prototype.dot`, and whatever it is you do to make a property.  (Oh, there are properties.  I'll get to that in a bit.)

The `class` block can be used as an expression, with or without a name.  It also supports prototypical inheritance with an `extends` clause and has a `super` pseudo-value for superclass calls.

It's a _little_ weird that the inside of the `class` block has its own special syntax, with `function` omitted and whatnot, but honestly you'd have a hard time making a `class` block _without_ special syntax.

One severe omission here is that you can't declare _values_ inside the block, i.e. you can't just drop a `bar = 3;` in there if you want all your objects to share a default attribute.  The workaround is to just do `this.bar = 3;` inside the constructor, but I find that unsatisfying, since it defeats half the point of using prototypes.


## Properties

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty) — supported in Firefox 4, Chrome 5, IE 9, Safari 5.1*

JavaScript historically didn't have a way to intercept attribute access, which is a _travesty_.  And by "intercept attribute access", I mean that you couldn't design a value `foo` such that evaluating `foo.bar` runs some code you wrote.

Exciting news: now it does.  Or, rather, you can intercept _specific_ attributes, like in the class example above.  The above `magnitude` definition is equivalent to:

```javascript
Object.defineProperty(Vector.prototype, 'magnitude', {
    configurable: true,
    enumerable: true,
    get: function() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    },
});
```

Beautiful.

And what even are these `configurable` and `enumerable` things?  It seems that _every single key on every single object_ now has its own set of three Boolean twiddles:

- `configurable` means the property itself can be reconfigured with another call to `Object.defineProperty`.
- `enumerable` means the property appears in `for..in` or `Object.keys()`.
- `writable` means the property value can be changed, which only applies to properties with real values rather than accessor functions.

The incredibly wild thing is that for properties defined by `Object.defineProperty`, `configurable` and `enumerable` default to _`false`_, meaning that by default accessor properties are immutable _and invisible_.  Super weird.

Nice to have, though.  And luckily, it turns out the same syntax as in `class` also works in object literals.

```javascript
Vector.prototype = {
    get magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    },
    ...
};
```

In fact, the syntax in `class` works in _all_ object literals, by which I mean you can define functions like so:

```javascript
Vector.prototype = {
    dot(other) {
        return this.x * other.x + this.y * other.y;
    },
    ...
};
```

Alas, I'm not aware of a way to intercept _arbitrary_ attribute access.

Another feature along the same lines is [`Object.seal()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal), which marks all of an object's properties as non-configurable _and_ prevents any new properties from being added to the object.  The object is still mutable, but its "shape" can't be changed.  And of course you can just make the object completely immutable if you want, via setting all its properties non-writable, or just using [`Object.freeze()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze).

I have mixed feelings about the ability to irrevocably change something about a dynamic runtime.  It would certainly solve some gripes of former Haskell-minded colleagues, and I don't have any compelling argument against it, but it feels like it violates some unwritten contract about dynamic languages — surely any structural change made by user code should also be able to be _undone_ by user code?


## Slurpy arguments

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters) — supported in Firefox 15, Chrome 47, Edge 12, Safari 10*

Officially this feature is called "rest parameters", but that's a terrible name, no one cares about "arguments" vs "parameters", and "slurpy" is a good word.  Bless you, Perl.

```javascript
function foo(a, b, ...args) {
    // ...
}
```

Now you can call `foo` with as many arguments as you want, and every argument after the second will be collected in `args` as a regular array.

You can also do the reverse with the [spread operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_operator):

```javascript
let args = [];
args.push(1);
args.push(2);
args.push(3);
foo(...args);
```

It even works in array literals, even multiple times:

```javascript
let args2 = [...args, ...args];
console.log(args2);  // [1, 2, 3, 1, 2, 3]
```

Apparently there's also a proposal for allowing the same thing with objects inside object literals.


## Default arguments

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters) — supported in Firefox 15, Chrome 49, Edge 14, Safari 10*

Yes, arguments can have defaults now.  It's more like Sass than Python — default expressions are evaluated once _per call_, and later default expressions can refer to earlier arguments.  I don't know how I feel about that but whatever.

```javascript
function foo(n = 1, m = n + 1, list = []) {
    ...
}
```

Also, unlike Python, you can have an argument with a default and follow it with an argument _without_ a default, since the default default (!) is and always has been defined as `undefined`.  Er, let me just write it out.

```javascript
function bar(a = 5, b) {
    ...
}
```


## Arrow functions

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions) — supported in Firefox 22, Chrome 45, Edge 12, Safari 10*

Perhaps the most humble improvement is the arrow function.  It's a slightly shorter way to write an anonymous function.

```javascript
(a, b, c) => { ... }
a => { ... }
() => { ... }
```

An arrow function _does not_ set `this` or some other magical values, so you can safely use an arrow function as a quick closure inside a method without having to rebind `this`.  Hooray!

Otherwise, arrow functions act pretty much like regular functions; you can even use all the features of regular function signatures.

Arrow functions are particularly nice in combination with all the combinator-style array functions that were added a while ago, like [`Array.forEach`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach).

```javascript
[7, 8, 9].forEach(value => {
    console.log(value);
});
```


## Symbol

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol) — supported in Firefox 36, Chrome 38, Edge 12, Safari 9*

This isn't quite what I'd call an exciting feature, but it's necessary for explaining the next one.  It's actually...  extremely weird.

`symbol` is a new kind of _primitive_ (like `number` and `string`), not an object (like, er, `Number` and `String`).  A symbol is created with `Symbol('foo')`.  No, not `new Symbol('foo')`; that throws a `TypeError`, for, uh, some reason.

The only point of a symbol is as a unique _key_.  You see, symbols have one very special property: they can be used as object keys, and _will not_ be stringified.  Remember, only strings can be keys in JavaScript — even the indices of an array are, semantically speaking, still strings.  Symbols are a new exception to this rule.

Also, like other objects, two symbols don't compare equal to each other: `Symbol('foo') != Symbol('foo')`.

The result is that symbols solve one of the problems that plagues most object systems, something I've talked about before: _interfaces_.  Since an interface might be implemented by any arbitrary type, and any arbitrary type might want to implement any number of arbitrary interfaces, all the method names on an interface are effectively part of a single **global** namespace.

I think I need to take a moment to justify that.  If you have `IFoo` and `IBar`, both with a method called `method`, and you want to implement both on the same type...  you have a problem.  Because most object systems consider "interface" to mean "I have a method called `method`", with no way to say _which interface's_ `method` you mean.  This is a hard problem to avoid, because `IFoo` and `IBar` might not even come from the same library.  Occasionally languages offer a clumsy way to "rename" one method or the other, but the most common approach seems to be for interface designers to avoid names that sound "too common".  You end up with redundant mouthfuls like `IFoo.foo_method`.

This incredibly sucks, and the only languages I'm aware of that avoid the problem are the ML family and Rust.  In Rust, you define all the methods for a particular trait (interface) in a _separate block_, away from the type's "own" methods.  It's pretty slick.  You can still do `obj.method()`, and as long as there's only one `method` among all the available traits, you'll get that one.  If not, there's syntax for explicitly saying which trait you mean, which I can't remember because I've never had to use it.

Symbols are JavaScript's answer to this problem.  If you want to define some interface, you can name its methods with _symbols_, which are guaranteed to be unique.  You just have to make sure you keep the symbol around somewhere accessible so other people can actually use it.  (Or...  not?)

The interesting thing is that JavaScript now has several of its own symbols built in, allowing user objects to implement features that were previously reserved for built-in types.  For example, you can use the `Symbol.hasInstance` symbol — which is simply where the language is storing an existing symbol and is _not_ the same as `Symbol('hasInstance')`! — to override `instanceof`:

```javascript
// oh my god don't do this though
class EvenNumber {
    static [Symbol.hasInstance](obj) {
        return obj % 2 == 0;
    }
}
console.log(2 instanceof EvenNumber);  // true
console.log(3 instanceof EvenNumber);  // false
```

Oh, and those brackets around `Symbol.hasInstance` are a sort of reverse-quoting — they indicate an expression to use where the language would normally expect a literal identifier.  I think they work as object keys, too, and maybe some other places.

The equivalent in Python is to implement a method called `__instancecheck__`, a name which is not special in any way except that Python has reserved all method names of the form `__foo__`.  That's great for Python, but doesn't really help user code.  JavaScript has actually outclassed (ho ho) Python here.

Of course, `obj[BobNamespace.some_method]()` is not the prettiest way to call an interface method, so it's not _perfect_.  I imagine this would be best implemented in user code by exposing a polymorphic function, similar to how Python's `len(obj)` pretty much just calls `obj.__len__()`.

I only bring this up because it's the plumbing behind one of the most incredible things in JavaScript that I didn't even know about until I started writing this post.  I'm so excited oh my gosh.  Are you ready?  It's:


## Iteration protocol

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols) — supported in Firefox 27, Chrome 39, Safari 10; still experimental in Edge*

Yes!  Amazing!  JavaScript has first-class support for iteration!  I can't even believe this.

It works pretty much [how you'd expect]({filename}/2016-11-18-iteration-in-one-language-then-all-the-others.markdown), or at least, how _I'd_ expect.  You give your object a method called `Symbol.iterator`, and that returns an iterator.

What's an iterator?  It's an object with a `next()` method that returns the next value and whether the iterator is exhausted.

Wait, wait, wait a second.  Hang on.  The method is called `next`?  Really?  You didn't go for `Symbol.next`?  Python 2 did exactly the same thing, then realized its mistake and changed it to `__next__` in Python 3.  Why did you do this?

Well, anyway.  My go-to test of an iterator protocol is how hard it is to write an equivalent to Python's `enumerate()`, which takes a list and iterates over its values _and_ their indices.  In Python it looks like this:

```python
for i, value in enumerate(['one', 'two', 'three']):
    print(i, value)
# 0 one
# 1 two
# 2 three
```

It's super nice to have, and I'm always amazed when languages with "strong" "support" for iteration don't have it.  Like, C# doesn't.  So if you want to iterate over a list but also need indices, you need to fall back to a C-style `for` loop.  And if you want to iterate over a _lazy_ or _arbitrary_ iterable but also need indices, you need to track it yourself with a counter.  Ridiculous.

Here's my attempt at building it in JavaScript.

```javascript
function enumerate(iterable) {
    // Return a new iter*able* object with a Symbol.iterator method that
    // returns an iterator.
    return {
        [Symbol.iterator]: function() {
            let iterator = iterable[Symbol.iterator]();
            let i = 0;

            return {
                next: function() {
                    let nextval = iterator.next();
                    if (! nextval.done) {
                        nextval.value = [i, nextval.value];
                        i++;
                    }
                    return nextval;
                },
            };
        },
    };
}
for (let [i, value] of enumerate(['one', 'two', 'three'])) {
    console.log(i, value);
}
// 0 one
// 1 two
// 2 three
```

Incidentally, `for..of` (which iterates over a sequence, unlike `for..in` which iterates over keys — _obviously_) is finally supported in Edge 12.  Hallelujah.

Oh, and `let [i, value]` is [destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment), which is _also_ a thing now and works with objects as well.  You can even use the splat operator with it!  Like Python!  (And you can use it in function signatures!  Like Python!  Wait, no, Python decided that was terrible and removed it in 3...)

```javascript
let [x, y, ...others] = ['apple', 'orange', 'cherry', 'banana'];
```

It's a Halloween miracle.  🎃


## Generators

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function%2a) — supported in Firefox 26, Chrome 39, Edge 13, Safari 10*

That's right, JavaScript has goddamn generators now.  It's basically just copying Python and adding a lot of superfluous punctuation everywhere.  Not that I'm complaining.

Also, generators are themselves iterable, so I'm going to cut to the chase and rewrite my `enumerate()` with a generator.

```javascript
function* enumerate(iterable) {
    let i = 0;
    for (let value of iterable) {
        yield [i, value];
        i++;
    }
}
for (let [i, value] of enumerate(['one', 'two', 'three'])) {
    console.log(i, value);
}
// 0 one
// 1 two
// 2 three
```

Amazing.  You can also use generators to implement `Symbol.iterator`, much like using a generator for `__iter__` in Python.

`function*` is a pretty strange choice of syntax, but whatever?  I guess it also lets them make `yield` only act as a keyword inside a generator, for ultimate backwards compatibility.

JavaScript generators support everything Python generators do: `yield*` yields every item from a subsequence, like Python's `yield from`; generators can return final values; you can pass values back into the generator if you iterate it by hand.  No, really, I wasn't kidding, _it's basically just copying Python_.  It's great.  You could now build `asyncio` in JavaScript!

In fact, [they did that](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)!  JavaScript now has `async` and `await`.  An `async function` returns a [`Promise`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), which is also a built-in type now.  Amazing.


## Sets and maps

*[MDN docs for Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) — [MDN docs for Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) — supported in Firefox 13, Chrome 38, IE 11, Safari 7.1*

I did _not_ save the best for last.  This is much less exciting than generators.  But still exciting.

The only data structure in JavaScript is the object, a map where the keys are strings.  (Or now, also symbols, I guess.)  That means you can't readily use custom values as keys, nor simulate a set of arbitrary objects.  And you have to worry about people mucking with `Object.prototype`, yikes.

But now, there's `Map` and `Set`!  Wow.

Unfortunately, because JavaScript, `Map` couldn't use the indexing operators without losing the ability to have methods, so you have to use a boring old method-based API.  But `Map` has convenient methods that plain objects don't, like `entries()` to iterate over pairs of keys and values.  In fact, you can use a map with `for..of` to get key/value pairs.  So that's nice.

Perhaps more interesting, there's also now a [`WeakMap`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap) and [`WeakSet`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet), where the keys are weak references.  I don't think JavaScript had any way to do weak references before this, so that's pretty slick.  There's no obvious way to hold a weak _value_, but I guess you could substitute a `WeakSet` with only one item.


## Template literals

*[MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals) — supported in Firefox 34, Chrome 41, Edge 12, Safari 9*

Template literals are JavaScript's answer to string interpolation, which has historically been a huge pain in the ass because it doesn't even have string formatting in the standard library.

They're just strings delimited by backticks instead of quotes.  They can span multiple lines and contain expressions.

```javascript
console.log(`one plus
two is ${1 + 2}`);
```

Someone decided it would be a good idea to allow nesting more sets of backticks inside a `${}` expression, so, good luck to syntax highlighters.

However, someone also had the most incredible idea ever, which was to add syntax allowing _user code_ to do the interpolation — so you can do custom escaping, when absolutely necessary, which is virtually never, because "escaping" means you're building a structured format by slopping strings together willy-nilly instead of using some API that works with the structure.

```javascript
// OF COURSE, YOU SHOULDN'T BE DOING THIS ANYWAY; YOU SHOULD BUILD HTML WITH
// THE DOM API AND USE .textContent FOR LITERAL TEXT.  BUT AS AN EXAMPLE:
function html(literals, ...values) {
    let ret = [];
    literals.forEach((literal, i) => {
        if (i > 0) {
            // Is there seriously still not a built-in function for doing this?
            // Well, probably because you SHOULDN'T BE DOING IT
            ret.push(values[i - 1]
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&apos;'));
        }
        ret.push(literal);
    });
    return ret.join('');
}
let username = 'Bob<script>';
let result = html`<b>Hello, ${username}!</b>`;
console.log(result);
// <b>Hello, Bob&lt;script&gt;!</b>
```

It's a shame this feature is in JavaScript, the language where you are least likely to need it.


## Trailing commas

Remember how you couldn't do this for ages, because ass-old IE considered it a syntax error and would reject the entire script?

```javascript
{
    a: 'one',
    b: 'two',
    c: 'three',  // <- THIS GUY RIGHT HERE
}
```

Well now it's part of the goddamn spec and if there's _anything_ in this post you can rely on, it's _this_.  In fact you can use AS MANY GODDAMN TRAILING COMMAS AS YOU WANT.  But only in arrays.

```javascript
[1, 2, 3,,,,,,,,,,,,,,,,,,,,,,,,,]
```

Apparently that has the bizarre side effect of reserving extra space at the end of the array, without putting values there.


## And more, probably

Like [strict mode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode), which makes a few silent "errors" be actual errors, forces you to declare variables (no implicit globals!), and forbids the completely bozotic `with` block.

Or `String.trim()`, which trims whitespace off of strings.

Or...  `Math.sign()`?  That's new?  Seriously?  Well, okay.

Or the [`Proxy`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) type, which lets you customize indexing and assignment and calling.  Oh.  I guess that _is_ possible, though this is a pretty weird way to do it; why not just use symbol-named methods?

You can write Unicode escapes for astral plane characters in strings (or identifiers!), as `\u{XXXXXXXX}`.

There's a `const` now?  I extremely don't care, just name it in all caps and don't reassign it, come on.

There's also a mountain of other minor things, which you can peruse at your leisure via MDN or the [ECMAScript compatibility tables](http://kangax.github.io/compat-table/es6/) (note the links at the top, too).

That's all I've got.  I still wouldn't say I'm a _big fan_ of JavaScript, but it's definitely making an effort to clean up some goofy inconsistencies and solve common problems.  I think I could even write some without yelling on Twitter about it now.

On the other hand, if you're still stuck supporting IE 10 for some reason...  well, er, my condolences.
