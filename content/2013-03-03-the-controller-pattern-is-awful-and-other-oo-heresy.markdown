title: The controller pattern is awful (and other OO heresy)
date: 2013-03-03 17:33
category: blog
tags: python, plt, tech, popular

Almost a year ago now, [Jack Diederich][jackdied] gave a talk entitled "[Stop Writing Classes][]", in which he implores Python programmers to stop creating classes just for the hell of it, and specifically calls out the common pattern of a class with only a constructor/initializer and a single method—which should, of course, just be a function.

A few weeks ago, [Armin Ronacher][mitsuhiko] wrote a rebuttal entitled "[Start Writing More Classes][]", which argues that classes are essential for both writing extensible code and smoothing over crappy interfaces.  (Hm.  Now that I look at it again, if you read the post backwards, it almost sounds like he's suggesting writing a class to smooth out the crappy interface you get from using too many classes...)

I'm having some trouble here, because I agree with both points of view.  There must be a way to resolve this contradiction, a message that resonates with everyone.

I think I've found it.

**Stop writing _stupid_ classes.**

<!-- more -->


## Some context

Before I clarify what I mean, I need to establish some definitions.  Quick: off the top of your head, what is object-oriented programming _about_?

Got an idea yet?

If you thought any of the words "encapsulation", "inheritance", "polymorphism", "information hiding", "abstraction", or "vtables", you are _wrong_.

If you thought any of the words "class", "prototype", or "type", you are _still wrong_.

**Object-oriented programming is about _objects_: bundles of state and behavior.**  The rest is optional fluff.  And object-oriented _languages_ are defined only by having built-in support for bundling state and behavior, _not_ by having built-in support for classes.  You may notice we don't call it "class-oriented programming".

Quick: off the top of your head, what makes JavaScript an object-oriented language?

If you thought "what?  it's not!" then there is no hope for you and you should go back to C++.

If you thought "prototypes" or "the `new` operator", you are wrong!

The key and _only_ feature that makes JavaScript object-oriented is the humble and error-prone `this`.  Observe:

```javascript
var date = {
    year: 2013,
    month: 3,
    day: 3,
    to_iso8601: function() {
        // we'll pretend this function exists
        return sprintf("%04d-%02d-%02d", this.year, this.month, this.day);
    },
};
```

There's no `new` here.  There's no prototype.  There's just state and behavior, and that makes it an object.  What it _is_ and what it _does_.  Even if JavaScript lacked prototypes entirely, it would _still_ be object-oriented as long as you could use `this`.

"But what about classes?"  Who cares?  Worst case, you could _build your own class implementation_ by copying the method definitions into every new object you created.  Maybe you'd make a master object containing those methods, for ease of copying.  Maybe you'd make the master object track all the objects derived from it, so you could propagate any changes to the master object.  You could even give the master object a special method all its own for generating new objects based on it.  And then the master object would itself be an object, so it could be an implementation of itself.  Wow, this sounds kinda like classes!

For similar reasons, C is _not_ object-oriented.  You can write object-oriented _code_ in C, but no matter what tricks you do with storing function pointers in structs, you still have to pass the struct itself as an explicit argument.  The behavior is completely divorced from and unaware of the state.

State and behavior.

I keep repeating this in the hopes that it sticks, because too much OO code is written like Java, and too many programmers believe that OO is defined _by_ Java.  Well, you know, fuck Java.

Last pop quiz: what makes Python an object-oriented language?

Ah, hm.  It can't be classes, or I'd tell you you're wrong.  So what is it?  Attributes?  Those are just sugar for `__dict__` lookups.  `self`?  No, that's not a keyword or anything; it's just the de facto standard name for the first argument.  So what makes `self` work?

That's close enough, really.  The answer is [descriptors][], which are basically "the things that make `self` work".  A descriptor object is an attribute of a _class_, and it's invoked whenever that attribute is accessed on an _instance_ of that class.  Methods are, in fact, very simple descriptors that effectively return `partial(method, instance)`!

Descriptors are the _only_ part of Python OO that cannot be semantically reimplemented in Python itself.  Methods are easy; I just told you how to do it.  Objects are just dicts with sugar (and descriptors!) on top.  Classes are sugar for dumping a scope into a dict; you could just as well do it manually with `locals()`.  Inheritance is just chained attribute lookup.  Metaclasses are just more objects in much the same way as the JavaScript example above.  These are all convenient patterns baked into the syntax, but descriptors are what make it _work_.

State and behavior.


## Stupid classes

This almost brings me back to my thesis, but first I need some examples of stupid classes.  I'm going to be writing these examples in Python because it has the local minimum of syntactic noise, but the idea's the same basically anywhere.

### The "I'm too good for functions" antipattern

A shockingly common form is the humble "job"—a task to be scheduled and performed.  Cron job, batch job, whatever it may be.  You generally have some `Job` master class (or "abstract base class" or whatever frilly name the documentation gives it):

```python
class CleanupJob(Job):
    # configuration: run at 5am
    run_at = '05:00'

    # implementation: nuke expired sessions
    def run(self):
        delete_expired_stuff()
```

If you've watched "Stop Writing Classes", you may immediately recognize this as one of the major sins he covered: a class that only has one method, which should instead be a function.  He's right about that, but I have a different take on _why_ this is so wrong, and I think my reasoning extends better to other kinds of stupid classes.

Here's my question for you: **what is a `CleanupJob` object?**

You might say "it's a job for cleaning up stuff".  That sure _sounds_ reasonable—but then what is its state, and what is its behavior?  Its behavior appears to be deleting old things, but what does this have to do with the notion of a "job"?  What state does it have that's relevant to deleting things?  I suppose if `Job` provides a database connection, the function could make use of it, but isn't the connection itself more a part of "the job" or "your app configuration", not so much the specific task of cleanup?

This is all a little murky.  Yet `Job` itself seems self-contained and clearly defined.  Presumably it has behavior like checking the time and setting up some resources and other bookkeeping—that is, its _behavior_ is to set up some _state_ and then call this `run` method.  It almost seems like _the class itself_ is trying to be "a job for cleaning up stuff".

And we've stumbled upon the problem here: the implementation, the `run` method, **isn't behavior**.  It's the _state_!  The behavior is to _run_ this function, granted, but the function itself has _nothing to do_ with jobs.  We've just turned it into a method because...  wait, why _did_ we do that?  It's not like passing functions around as data is particularly difficult in Python.

I have a hypothesis: this pattern is so common for the simple reason that **Java doesn't have first-class functions**.  Java is one of the most common environments from which the current generation of programmers learned about object-orientation, but its inherent deficiencies mean that this simple job concept _cannot_ be implemented correctly.  And I'm not only ragging on Java: I would put C++ and PHP in second and third place, and they have the _same flaw_.  (Yes, yes, you _can_ pass function pointers around in C++, but it's so awkward that it might as well be black magic.)

What's my alternative?  Hard to say; it depends on your language's idioms.  In the case of Python, decorators.

```python
cleanup_job = Job(run_at='05:00')

@cleanup_job.run
def do_cleanup(job):
    delete_expired_stuff()
```

You may notice that this looks _pretty_ similar.  **That's good!**  It means doing this the right way is really easy.  But look what we've gained here.

* With classes like this that try to use inheritance as a configuration mechanism, you often want to reuse the same configuration.  So you make an intermediate class that has just the shared configuration.  Now you need something _slightly_ different sometimes, so you add a mixin, and now you have multiple inheritance, and overrides propagate in weird ways, and who even knows what's happening.
* The same implementation can rather naturally be attached to multiple jobs, without making even more of a mess of that artificial inheritance hierarchy.
* Need to add another kind of callback, like common pre-run bookkeeping, that only some subset of jobs share?  No problem: `cleanup_job.add_pre_run(setup_logging)`.
* You can test `Job` itself and particular jobs independently, and rather easily.  Create a `Job`-like class that has only the resources a particular job needs, and pass it in.  No need to, say, mock out all the internals to force the job to run immediately instead of at a specified time.

There's a common theme among these bullet points.  By making implementations of `Job` be subclasses instead of instances, the only tools available for factoring out common code or adding new behaviors are the tools built into the core of the class system: primarily, inheritance.  By using instances, _the entire language_ can be used however you want, because they're just objects.  The parts are clearly defined, easy to reason about, and easy to reuse.

Not convinced by any of these bullet points?  Doesn't matter; they, too, are just fluff.  The real reason here is that this is the _right_ way to structure a program, and shoehorning functions into methods is _wrong_, and that's [good enough for me][on principle].

After all, there's probably a good reason we don't all do this.

```python
class StudentGrades(object):
    alice = 100
    bob = 96
    charles = 62
    david = 85
```

Exactly the same thing.


### The controller antipattern

Here's the good part: the "state and behavior" mantra doesn't just apply to one-method wonders.  I bet you've seen this before:

```python
class LoginController(Controller):
    def register(self):
        return self.render_template('/register.mako')

    def login(self):
        if self.request.method == 'POST':
            # ...
        else:
            return self.render_template('/login.mako')

    def logout(self):
        # ...
```

This is the controller pattern.  At first glance, this might seem perfectly reasonable: there are, clearly, multiple methods here.

I ask once more: what is a `LoginController` object, and what does it do?

I can tell you what it does: it handles various auth-related page requests.  That's a little hokey, but okay.  _What **is** it?_

It's nothing.  There's no way to describe it without sounding like a blowhard.  It's not "a controller for some URL space", because _that's what the class is_.  An instance of it is utterly meaningless!

Once again, these "methods" are actually state, not behavior.  They're all attributes of some application object whose _behavior_ is to receive requests and dispatch them to the appropriate handler functions.  Turning those functions into methods muddies the distinction between your framework and your particular app.

Look at how [Flask][] does it:

```python
app = Flask(__name__)

@app.route('/')
def hello():
    return u"Hello world!"
```

The app is the object, and the various URL handlers are its state.  [Pyramid][] does the same:

###### views.py
```python
@view_config(route_name='home')
def home(request):
    return Response(u"Hello world!")
```

###### app.py
```python
config = Configurator()
config.scan()  # picks up the decorated function in views.py
app = config.make_wsgi_app()
```

The app is the object, and the various URL handlers are its state.

Think this only applies to Web frameworks?  I bet you've seen this before, too:

```python
class TestSomething(UnitTest):
    def test_one(self):
        assert True

    def test_two(self):
        assert True
```

You already know what I'm going to ask: what is a `TestSomething` object?  Less than nothing.  Does it even have any state?  It looks like it's only instantiated at all so its "methods" can be called!

I have seen some _royal_ messes result from this pattern, especially when combined with multiple-inheritance-for-sharing and extras like teardown methods.  If you get the `super`s wrong, you might not be tearing your tests down.

Here's the same test suite, rewritten with [py.test][]:

```python
def test_one():
    assert True

def test_two():
    assert True
```

py.test does support test classes, but _everything_ it can do works just as well with plain functions.  Need setup, teardown, resources, sharing?  No problem; you can define it all, scoped however you want, [far far away from your actual tests][py.test fixtures].

### And so

What's a stupid class, then?  One that produces _stupid objects_—ones that lack clear and meaningful _state and behavior_.  State and behavior.  State and behavior.  If it doesn't bundle state and behavior in a sensible way, it should not be an object, and there should not be a class that produces it.

Easy litmus test: what is an instance of your class, in no more than five words?  Most stupid classes require explanations that begin "it's an object that..." and then you only have one word left.  Sensible objects should have a _description_.  They should _be_ something.  Lists _are_ sequences of items.  Modules _are_ containers for related code.  Jobs _are_ scheduled maintenance tasks.  Applications _are_ dispatchers for an entire site.


## But Armin is right too

I hope I've made an inkling of a point by now.  If not about object design in general, at least about controller classes.  But before you run off with the impression that I think all classes are evil: remember, I agree with "Start Writing More Classes" too.

The difference is all in the examples.  Armin cites parts of Flask.

###### jinja.py
```python
def get_template(self, name, parent=None, globals=None):
    if parent is not None:
        name = self.join_path(name, parent)
    return self.loader.load(self, name, globals)
```

###### loader.py
```python
def load(self, environment, name, globals=None):
    if globals is None:
        globals = {}
    source, filename, uptodate = self.get_source(environment, name)
    code = environment.compile(source, name, filename)
    return environment.template_class.from_code(environment, code,
                                                globals, uptodate)
```

###### environment.py
```python
def compile(self, source, name, filename=None):
    # template code to jinja's abstract syntax tree
    source = self._parse(source, name, filename)
    # jinja's abstract syntax tree to python source
    source = self._generate(source, name, filename)
    # python source to bytecode
    return self._compile(source, filename)
```

The [actual article][Start Writing More Classes] has some commentary on what these parts actually _are_, but I'm interested in how they're _written_.

Because, you see, these methods are **all on different objects**.  Each of them implements a tiny fraction of a _different thing_'s behavior.  The Flask app itself knows how to get a template, but only by consulting a template loader it owns.  The template loader knows the mechanics of finding a template, but it needs to consult an environment object to know where to actually look.  The environment object knows how to compile a template, but breaks it into meaningful and independent steps.

These are all independent things that I can talk about meaningfully.  I can work on them without needing to understand the context of how they're used or what they use themselves.  I could test them without concerning myself with a thousand other intertwined code paths.  They all have _state and behavior_ that I could describe in a sentence or two, and you'd have a pretty good idea of everything they do and how they do it.

These are good classes, **because they produce good objects.**  And when you have a lot of good objects, you can certainly replace them and change them and reuse them and recombine them as Armin wishes he could do more often.  Remember py.test?  All of its shenanigans are built on objects, even if the tests themselves are not.  You know WSGI?  It's all defined in terms of callables, yet most of the time we use classes with `__call__` methods instead.  Pyramid uses _mountains_ of objects and hooks under the hood, but you'll never notice until the day you realize you need to toy with some of them.


## So

So please stop using classes as shapeless bags in which to dump functions.  Chances are, either that big ol' function is actually the state of a different kind of object entirely, or there are several smaller concerns in there you could break apart.

Hell, if you can manage it, forget about classes entirely.  They're just a convenient way to factor common behavior out of objects.  Let's design useful, scoped, meaningful objects, and _then_ write classes that produce them.



[jackdied]: http://jackdied.blogspot.com/
[Stop Writing Classes]: http://www.youtube.com/watch?v=o9pEzgHorH0
[Start Writing More Classes]: http://lucumr.pocoo.org/2013/2/13/moar-classes/
[mitsuhiko]: http://lucumr.pocoo.org/2013/2/13/moar-classes/
[descriptors]: http://me.veekun.com/blog/2012/05/23/python-faq-descriptors/
[on principle]: http://me.veekun.com/blog/2012/03/24/on-principle/
[Flask]: http://flask.pocoo.org/
[Pyramid]: http://www.pylonsproject.org/projects/pyramid/about
[py.test]: http://pytest.org/latest/
[py.test fixtures]: http://pytest.org/latest/fixture.html#fixture
