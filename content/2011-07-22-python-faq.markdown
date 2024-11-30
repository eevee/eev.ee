title: Python FAQ
date: 2011-07-22 16:50:00
category: articles
series: python faq
tags: python, reference, tech

I lurk in [#python][].  It gets a lot of questions that are, shall we say, _frequently asked_.  This is my attempt to catalogue interesting and useful questions.  The answers will gradually become separate posts—perhaps on other blogs if someone else gets to them first.  Let me know if there should be other questions, if the answers are unclear, or the answers have bugs in them!

<!-- more -->

## The elephant in the room

* [Should I use/learn Python 2 or Python 3?  Why should I use Python 3?]({filename}2016-07-31-python-faq-why-should-i-use-python-3.markdown)
* [I have a bunch of Python 2 code.  How do I port it to Python 3?]({filename}2016-07-31-python-faq-how-do-i-port-to-python-3.markdown)

## Variables, operators, and functions

* [How do I pass by reference?  Does Python pass by reference or pass by value?][passing]
* Why can't I create closures within a loop?  How do I change a variable in an outer scope?  How is Python scoped?
* How do I access a variable whose name is in a string?  How do I use "variable variables"?
* [What does `is` do?  Should I use `is` or `==`?][equality]
* Why doesn't division work correctly?
* Why are floats inaccurate?  What type should I use to handle currency?
* How do I test whether a variable is defined?
* What is `unicode` and why do I care?  Why am I getting `UnicodeDecodeError`s?

## Classes, objects, and data

* How do I make a tuple with one element?  What's this trailing comma?
* How do I check what type a variable is?
* Why can't I just do `super(type(self), self)`?  How does `super` work?
* What's the difference between tuples and lists?
* What's the difference between `classmethod` and `staticmethod`?
* Why can't I put attribute defaults at class level?  Why doesn't my class counter work?
* How do I make a private attribute?  What's `__foo` do?
* How do I inherit from a built-in class, like `list` or `dict`?
* Why don't my imports work?
* How do I change the value of a global in another module?
* Why do I need to specify `self`?  How do I take a reference to an object's method?
* [How does `@property` work?  Why does it call my `__getattr__`?  What's a "descriptor"?][descriptors]
* How do I make a decorator with optional arguments?  How do decorators work?
* Metaclasses are insane!

## Libraries and the real world

* I come from C/Java/Prolog/something.  How do I write "natural"-looking Python?
* [I only know PHP.  How do I write a Web application in Python?][webdev]
* Okay, great; now how do I deploy it?
* How do I parse HTML?
* How do I use a single parameter with the DB-API?
* How do I write a networking application?  How do I use sockets?
* How do I do networking with a GUI?
* How do I use threads?
* How do I write a plugin system?  How do I reload a module at runtime?
* How do I write an IRC bot?

## Security

* How do I store user passwords?  How do I do anything related to encryption?
* How do I supply a password for an SSH connection or `sudo`?
* How do I encrypt my program's source code?

## Bonus question

* What are the worst features in Python?


[#python]: irc://irc.freenode.org/python
[descriptors]: /blog/2012/05/23/python-faq-descriptors/
[equality]: /blog/2012/03/24/python-faq-equality/
[passing]: /blog/2012/05/23/python-faq-passing/
[webdev]: /blog/2012/05/05/python-faq-webdev/
