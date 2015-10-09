title: A new use for StackOverflow
date: 2013-01-15 16:39
tags: php, pyramid, python, rust, web, plt
category: blog

It's hard to get a feel for a new tool.  Is it any good?  Does it do anything I can't already do?  What's the community like?  Tough questions to answer without diving in and using it for a significant amount of time—and then you risk not liking the answers you get.

But fear not!  I have discovered a new and brilliant way to discern the novel features of a tool, the vibrance of its community, and its range of users all at once.  In mere minutes.

Look at its ten highest-voted questions on [StackOverflow][].

I'm totally serious.  Watch.

<!-- more -->


## Python

[The list](http://stackoverflow.com/questions/tagged/python?sort=votes&pagesize=10).

The first three ask about how to use [generators](http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained), [metaclasses](http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python), and [decorators](http://stackoverflow.com/questions/739654/understanding-python-decorators)—probably Python's three neatest metaprogrammingish features.

Number 4 asks about [running Python on Android](http://stackoverflow.com/questions/101754/is-there-any-way-to-run-python-on-android), a common question that hints at Python's popularity as a dynamic Java alternative.

Number 5 is about the [equivalent of `enum`](http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python), which is a pretty common question (and garnered 35 answers, wow) about how to structure your program.

6, 7, and 8 are about [checking for a file's existence](http://stackoverflow.com/questions/82831/how-do-i-check-if-a-file-exists-using-python), [becoming an expert in Python](http://stackoverflow.com/questions/2573135/python-progression-path-from-apprentice-to-guru), and [running an external command](http://stackoverflow.com/questions/89228/calling-an-external-command-in-python).  Seems there are people who jumped to Python from shell scripting, and want to know how to use it more seriously.

9 is about the [ternary operator](http://stackoverflow.com/questions/394809/ternary-conditional-operator-in-python), which was new at the time (and which is unusual enough that most newcomers don't know it's there).

10 is, um, [Peak detection in a 2D array](http://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array).  Clearly some people are doing some cool number crunching and visualization with Python.

So what can we take from this?

* New Python developers are interesting in becoming proficient;
* Python has some novel features that developers are interested in understanding;
* Python appeals to sysadmins, app developers, and scientific computing.

Sounds pretty accurate to me.  Let's try something else.


## PHP

[The list](http://stackoverflow.com/questions/tagged/php?sort=votes&pagesize=10).

Question 1 is about [preventing SQL injection](http://stackoverflow.com/questions/60174/how-to-prevent-sql-injection-in-php).  Appropriately, question 10 is about [which of the solutions to use](http://stackoverflow.com/questions/13569/mysqli-or-pdo-what-are-the-pros-and-cons).

Number 2 is about [whether to use `DATETIME` or `TIMESTAMP` in MySQL](http://stackoverflow.com/questions/409286/datetime-vs-timestamp).  No, don't worry, you didn't miss anything; this actually has nothing to do with PHP whatsoever.

3 is a [massive syntax reference](http://stackoverflow.com/questions/3737139/reference-what-does-this-symbol-mean-in-php).  I've actually never seen a meta-question like this on SO before.

4 asks [how to parse HTML](http://stackoverflow.com/questions/3577641/how-to-parse-and-process-html-xml-with-php).  7 asks about [long polling](http://stackoverflow.com/questions/333664/simple-long-polling-example-code), though the ultimate answer is more about JavaScript and Apache.

5, 8, and 9 are about [how to store passwords](http://stackoverflow.com/questions/2283937/how-should-i-ethically-approach-user-password-storage-for-later-plaintext-retrie), [how to use bcrypt for passwords](http://stackoverflow.com/questions/4795385/how-do-you-use-bcrypt-for-hashing-passwords-in-php), and [how to hash passwords](http://stackoverflow.com/questions/401656/secure-hash-and-salt-for-php-passwords).

These are substantively different types of questions.

* PHP is used overwhelmingly for Web development, and commonly with MySQL.
* PHP developers are confused by its syntax, and the documentation isn't sufficiently helpful.
* Four of these questions are about security issues.  You might take this to mean that PHP developers are security-conscious...  or you might take it to mean that a lot of PHP code has security issues and nobody knows how to fix them.  The interpretation is up to you, but do note that most StackOverflow questions are asked reactively.

It's kind of hard to see what problems PHP is commonly used to solve; the only question about solving a particular problem in PHP asks how to parse HTML, and the answers are just "use one of these ten libraries".

But PHP is aimed at the Web, so naturally it would be tied to a bunch of Web questions.  I wonder what people ask about my pet Web framework?


## Pyramid

[The list](http://stackoverflow.com/questions/tagged/pyramid?sort=votes&pagesize=10).  Note that these questions have _far_ fewer upvotes than the top questions for PHP or Python, which makes them less likely to be statistically significant.

The first two ask about [Pyramid vs Pylons](http://stackoverflow.com/questions/4313715/should-i-use-pylons-or-pyramid) and [whether Pyramid is production-ready](http://stackoverflow.com/questions/4482879/is-pyramid-ready-recommended-for-prime-time).

3 asks about [output formats](http://stackoverflow.com/questions/4633320/is-there-a-better-way-to-switch-between-html-and-json-output-in-pyramid).  4 asks about [user auth](http://stackoverflow.com/questions/7792769/user-authentication-in-pyramid).  5 asks about [form libraries](http://stackoverflow.com/questions/5665541/pyramid-simpleform-or-deform).  10 asks about [templating engines](http://stackoverflow.com/questions/5321789/python-template-engines-chameleon-vs-jinja2).

6 is a sort of code review request for [a file upload implementation](http://stackoverflow.com/questions/6836029/help-improve-my-file-upload-method-pyramid-framework).  The asker also asks if there are any unobvious vulnerabilities, and indeed the lone answer points one out.

7 asks about [gzip compression](http://stackoverflow.com/questions/6618985/gzipping-all-http-traffic-with-pyramid), which doesn't really have anything to do with Pyramid, but the top answer finds a solution anyway.  9 asks a strange, sparsely-detailed question [about sqlalchemy](http://stackoverflow.com/questions/8024602/sqlalchemy-staledataerror-on-deleting-items-inserted-via-orm-sqlalchemy-orm-exc) that again has nothing to do with Pyramid.

8 asks how to [debug Pylons apps with Eclipse](http://stackoverflow.com/questions/147650/debug-pylons-application-through-eclipse).  Neat.

These don't really look like the PHP questions, either.

* Early adopters wanted to know whether Pyramid is stable yet.  I expect this would happen with most technologies newer than StackOverflow; the oldest, and most relevant at the time, questions will be about what it can do and whether to use it.
* Pyramid users are interested in its builtin web development tools (templating, etc.) and how to use them.
* Along the same lines, Pyramid users want to use their fancy-pants debugging IDE with it.
* At least this one guy is interested in security issues _he has not yet predicted_.  This is very different from asking about how to prevent a vulnerability you know only by name.
* Apparently, web developers _in general_ can't tell where their framework ends and other pieces begin.

This is fascinating, but time-consuming, so I'll only do one more.  I'm curious to see...


## Rust

[The list](http://stackoverflow.com/questions/tagged/rust?sort=votes&pagesize=10).  Again, these questions have very few upvotes, since Rust is a new and unfinished thing.  Let's look anyway.

1 asks how [Erlang compares to Rust](http://stackoverflow.com/questions/9339560/erlang-versus-go-versus-rust-comparison).  3 asks if [anyone has used Rust at all](http://stackoverflow.com/questions/4419433/any-one-tried-mozillas-programming-language-rust-yet), and 4 wants some [examples of Rust projects](http://stackoverflow.com/questions/9350125/applications-and-libraries-written-in-rust).

2 asks about [typestate](http://stackoverflow.com/questions/3210025/what-is-typestate).  6 is confused about [what "monomorphization" is, in either Rust or C++](http://stackoverflow.com/questions/14189604/what-is-monomorphisation-with-context-to-c).

5 is about [ranges](http://stackoverflow.com/questions/9271970/how-do-you-make-a-range-in-rust), 7 is about [accessing enum fields](http://stackoverflow.com/questions/9109872/rust-how-to-access-user-defined-types-instance), and 9 features [abuses of pattern matching](http://stackoverflow.com/questions/9282805/rust-pattern-matching-over-a-vector).  10 wants to know how to use [sockets](http://stackoverflow.com/questions/8984174/sockets-in-rust).

8 reveals a [weird cargo error](http://stackoverflow.com/questions/9646490/rust-cargo-init-occur-signature-verification-failed).

So.

* Rust is new.  Surprise!
* Rust is getting people interested in type system theory, which is cool.  The typestate answer explains the concept in fantastic detail, as well as hinting at why the feature was effectively removed from Rust several releases ago.
* Rust users are not clear on how to use some of its features.  This isn't surprising, since Rust deliberately bucks some trends, but it does point to some potential deficiencies in the tutorial.


## End

Okay, maybe this isn't scientifically rigorous.  Upvotes don't have a precise meaning, and top questions will tend to stay at the top, and older questions have a bias, and genuine problems with a tool may have been fixed since the question was asked, and so forth.

But since upvotes are all about _people_, the top questions can tell you what _other people_ think a technology is about, what they're doing with it, and what problems they're experiencing.  Maybe give it a shot next time you're thinking about trying out a new language, or deciding between two libraries.

Remember, there are no stupid questions!  Only stupid software.


[StackOverflow]: http://www.stackoverflow.com/
