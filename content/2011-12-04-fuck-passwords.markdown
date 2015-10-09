title: FUCK PASSWORDS
date: 2011-12-04 17:47:00
category: blog
tags: infosec, tech, yelling

I'm so tired of passwords.  So, so, _so tired_.

Most people don't understand this.  Most people use the same password everywhere.  Most people can just mechanically type out `password3` in every password box, smirking to themselves at how clever they are, because who would ever guess `3` instead of `1`?

I don't do that.  Let me tell you what i do.

I generate a different password for every service, based on a convoluted master password and the name of the thing.  I do this because it's what you're _supposed_ to do; it's what security nerds (including myself for the purposes of this post) tell everyone else to do.  "Ho ho!" we all chuckled to ourselves after the Gawker leak, and the subsequent breakins to various other things that used the same passwords.  "If only these chumps had been generating different random passwords for every service!"

So my passwords look like ``'fC`29ap5w78r3IJ``, or `Ab3HE4 2Iv5hJk\K`, or `mw@\_h<~o04neHiJ{`.  Those are actual examples i just generated.  I'm eating my own [dogfood][], so to speak.

It's not without its drawbacks.

<!-- more -->

* I don't know my Google password.  I think there's an `h` in it somewhere?  So when Google asks me to verify my password–which seems like once every 18 hours–I have to either go generate it again and copy/paste, or log out and back in again.  This happens virtually any time i try to look at public Google Groups postings, for reasons i cannot fathom, which has made error-googling into a far more aggravating experience.  If i actually used gmail i would probably have to kill myself.

* Sometimes, the generated password doesn't fit the password policy some idiot in a suit came up with.  Now i'm just fucked; i have to either invent a password manually (guaranteeing i won't remember it) or reuse a fallback password (which also contains punctuation, so sometimes _that_ isn't good enough either).

    But it gets better: the services with restrictive password policies are, **without fail**, big companies with direct access to my dollars.  Who are, thus, forcing me to use a less secure password that i would otherwise.  I'll get to that at the end, because it deserves its own rant.

* Copy-pasting passwords is pretty lame, admittedly.

I know there are fancy-pants password managers like [LastPass][] (nice SSL there, dudes), but let's think about this for a moment.  I have the choice of either making my passwords so memorable and reused that i'm at a grave security risk, or of making them so secure that i need a _computer program_ to store them for me.  This is fucked up.  This is fucking broken.  This should not be allowed to go on.

I'm tired of passwords.


## Hurr durr what else can we do Eevee??  Passwords are ALL WE HAVE

When i do my hacker thing and connect to a server from a terminal/console/black box with letters in it, it uses [public-key cryptography][] to prove who i am.  I have a private key and a public key.  The public key can be used to lock boxes in such a way that only my private key can unlock them again.  I give out my public key; the server picks some big random number and encrypts it; if i can tell the server what random number it picked, then it knows i have the private key and must be who i say i am.

(Okay, that's still a bit oversimplified.  The [actual mechanism][Diffie–Hellman key exchange] for how this usually works is pretty cool, if you want to read about it.  It has a pretty picture using paint mixing.)

While my key is still protected by a password, the experience is radically different in a few critical ways.

* It's called a _passphrase_, not a password.  And, indeed, my passphrase(s) tend to be phrases, 50+ characters long, decorated with punctuation in some way that makes sense to me.  They're very easy to remember, yet i can't imagine how you'd even _approach_ trying to crack them.

* I type the passphrase in _once_, when i boot up my machine.  The private key is unlocked for the rest of the session, and it's used automatically when i connect to any server that has the corresponding public key.  Logins are instant and seamless; i log in and out of stuff all day long.

    Hell, here's what it looks like:

        eevee@perushian ~ $ ssh koiru.veekun.com
        eevee@koiru ~ $

    `perushian` is my desktop.  `koiru` is the name of the veekun IRC/etc server.  This is the extent of the effort it takes.

* The passphrase stays on my machine.  It's not sent to the server to be double-checked, like virtually all passwords on the Web are.  Something like [Firesheep][] simply cannot work; you can't sniff my passphrase out of the air if it's not there to begin with.

* Even if i connect to server A, and then hop from there to server B, i can defer all the key-checking back to my desktop.  Server A doesn't need to have my private key on it to connect somewhere else in my name.

* You know those SSL certificate warnings?  You know how you always ignore them?  Yeah, you shouldn't do that.  They're the only warning you get that someone might have hijacked the connection to your bank or whatever.  It's a shame that browsers have trained most of us to ignore the warnings, because they're the only thing making SSL useful.

    Anyway, in the case of SSH: the server has its own public key, which it broadcasts to me as part of the login process.  The first time i connect to a server, the public key is remembered on my machine.  If i ever try to connect again, and the public key is _different_, the connection stops immediately.  It's the same idea as the certificate warnings, except that public keys are supposed to last _forever_ and you don't need to bleed cash to get one, so a changed key is actually a legitimate cause for concern.  (Most SSL warnings are about a certificate that the website owner created himself, because getting a signed one is considerably pricey.)

* And best of all, i can use the same set of keys for any number of servers.  Or i can use a separate key for every server.  It's entirely up to me.  It doesn't matter what my username is on each server.  It doesn't matter whether the servers are related in any way.  It doesn't even have to be my account; any account can have any number of public keys linked to it, so sharing an account is just a matter of giving it several people's keys.

This is the experience i'm used to while doing my Linux thing.  And this is why I am ***so fucking tired*** of usernames and passwords on the Web.  Text-only technology built into every Unix-ish machine in the world makes the current state of Web logins look like a sad joke.

Granted, i'm pretty tired of having to pick unique names and verify my email address for every service i sign up for, too.  But identity is a different post.  :)

Unfortunately it's a bit difficult to implement something like this on the Web as-is.  There are SSL client certificates, which function similarly.  But i tried using them for a project recently, and they are just so full of glitches and surprises as to be virtually unusable.  (Surprise number one: logging out is really hard!)  OpenID has a few of the same principles, at least, but it's only slightly less of a clusterfuck.

I think the only real solution here lies in some distributed identity thingamajig, but nobody with the resources to pull off something usable is inclined to do so.  I try to use OpenID when i can, but it causes no end of confusion for people, and small projects don't really have the influence to fix a whole fundamental paradigm.  On the other end of the scale, I'm pretty sure Facebook is happy with the idea of using Facebook to log into everything, but less thrilled with the idea of using Google+ to log into Facebook.  And vice versa.  Which is why Google acts as an OpenID provider, but not a consumer.  Assholes.

Conclusion: everything is fucked and i hate computers.


## FUCK BANKS

So here is that other bit on financial institutions and their password policies.

Here is a list just of places i've tried to use recently:

* **[ING Direct](http://www.ingdirect.com/)**: 6–10 _digits_
* **[Chase](http://www.chase.com/)**: 7–32 letters and digits only
* **[Capital One](http://www.capitalone.com/)**: 8–15 letters, digits, underscores, hyphens.  _NOT CASE SENSITIVE_
* **[Fidelity](http://www.fidelity.com/)**: 6–12 letters and digits only
* **[TD Ameritrade](http://www.tdameritrade.com/)**: 7–15 characters, no "special characters", whatever that means.  Fun story: i used to use a different broker, which was acquired by this one.  My old, generated password had a `<` in it.  For some horrifying reason, this prevented me from logging into TD Ameritrade.  I had to call customer support, and the guy there—i am not making this up—reset my password to something like `abc123`.
* **[AT&T](http://www.att.com/)**: 6+ letters, digits, underscores, hyphens (which they incorrectly illustrate with an en dash)
* I'll give props to **[Wells Fargo](http://www.wellsfargo.com/)**, which allows 6–14 of any character.  Except my generated passwords are all 16 characters!!
* Further props: **[PayPal](http://www.paypal.com/)** claims to want merely 8 or more characters.  Too bad i hate PayPal for other _perfectly legitimate_ reasons.

Why can i not use punctuation?  Why can i not [use spaces][xkcd:password strength]??  Why is there a ***maximum*** length for passwords?!  These rules are all completely worthless.

Compare to the password policies of these totally frivolous sites.

* **[Twitter](http://www.twitter.com/)**: 6+ of any character
* **[Yelp](http://www.yelp.com/)**: 7–16 any characters (except spaces; sigh.)

Naturally, my Twitter and Yelp passwords are far more entropous than any bank i've ever done business with.

But wait, it gets _even better_!  Financial institutions are the same places that use `autocomplete="off"` on their login forms, which prevents browsers from saving passwords.  I rigged a greasemonkey script to defeat that, but their login forms are so convoluted that it's a crapshoot whether anything actually gets saved, so i'm still lucky if i can remember my _username_ sometimes.

Speaking of usernames, i've run into more than one bank that requires a digit in your username.  A digit.  In.  Your.  Username.

And then there are security questions.  Please tell me, what is the difference between this:

    password: freedom
    favorite color: red

And this:

    password: freedom red

Answer: the first case gives an attacker a big hint on what the answer might be!  Awesome, that's exactly what i want for my password.

Last year i looked into getting some US Treasury bonds, because diversifying is good or something.  They mailed me (like, in an envelope) a little card with a grid of letters on it, which i need for logging in.  Okay, cool: ask for [something i know and something i have][two-factor authentication].

I went to log in, and they asked for my password, and some letters off of the card, and the _answers to security questions i'd answered a month ago_.

I didn't know the answers.  I don't have a favorite movie.  I didn't have a childhood pet.  I grew up on seven different streets and easily confuse their names.  Did i refer to my high school mascot as "Bob", or "Bob the Bobcat"?  Was he actually a bobcat, or more of a lynx?

So tired.

So, so tired.

All of these things are optimized for people who use the same email, same password, and same answers everywhere.  They push me towards being unsafe.  I don't understand how nobody sees what a bad idea this is.

I've sent detailed emails to all of these places objecting to their password policies and use of security questions, but the most encouraging response i've gotten (naturally) is a not-quite-generated letter about valuing feedback and passing it on to engineers.  Yeah, we'll see.

In the meantime, i have a few sites to build, and no good options for letting people log in.  I might as well just ask you for your username and trust that you'd only log into your own account.



[Diffie–Hellman key exchange]: http://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
[Firesheep]: http://codebutler.com/firesheep
[LastPass]: http://lastpass.com/
[dogfood]: http://en.wikipedia.org/wiki/Eating_your_own_dog_food
[public-key cryptography]: http://en.wikipedia.org/wiki/Public-key_cryptography
[two-factor authentication]: http://en.wikipedia.org/wiki/Two-factor_authentication
[xkcd:password strength]: http://xkcd.com/936/
