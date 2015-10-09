title: Pyramid traversal: almost useful
date: 2011-07-14 20:25:00
category: blog
tags: python, pyramid, squiggle, tech, yelling

[Pyramid][] is, to skip a lot of history, a successor to [Pylons][].  It's a Web framework for Python.  (And there goes half my audience.)  This post is about dispatch: mapping URLs to the code you want to run.  (There goes the other half.)

<!-- more -->

Pyramid supports traditional URL _routing_, which looks like this:

```python
config.add_route('cats.list', '/cats')
config.add_route('cats.view', '/cats/{id}')

@view_config(route_name='cats.list', renderer='cat_list.mako')
def cat_list(context, request):
    return dict()

@view_config(route_name='cats.view', renderer='cat_view.mako')
def cat_view(context, request):
    cat = get_cat(request.matchdict['id'])
    if not cat:
        raise NotFound()
    return dict(cat=cat)
```

Gosh that's a lot of things.  The idea here is:

* If you visit `/cats`, Pyramid will find the route called `cats.list`.  That route is attached to the `cat_list` function, which will run, return a dict, and pass that off to the `cat_list.mako` template for rendering.
* If you visit `/cats/123`, Pyramid will find `cat_view` instead.  The `id` (here 123) will be in `request.matchdict`; the function has to find the cat with that id and bail if it doesn't exist.  Then template blah blah blah.

Following?  Excellent.

The immediate problem with this approach is what happens when you have a lot of cat-related URLs.  Maybe you want to show a cat's owner history and innoculations and cross-reference with funny cat videos on YouTube.  Now you have:

```python
config.add_route('cats.list', '/cats')
config.add_route('cats.view', '/cats/{id}')
config.add_route('cats.owners', '/cats/{id}/owners')
config.add_route('cats.shots', '/cats/{id}/shots')
config.add_route('cats.youtubes', '/cats/{id}/youtubes')
config.add_route('cats.hurpdurp', '/cats/{id}/hurpdurp')
```

That's not too bad, except that now you have to do the `get_cat` runaround in every one of these functions.  For simple views, that's going to be half the code you even run.

Okay, you say, so put that in a function called...  uh, `real_get_cat`.  Great, except now what about when we expand our site to funny dog videos?  Now we have another wrapper for getting a dog, and maybe one for getting rabbits.  Meanwhile, we're copy-pasting the `/cats/{id}` prefix in all the routes—if we wanted to be more specific that ids are numeric, it gets even worse, with `/cats/{id:\d+}`.

Consider URL generation, as well: you need to call `request.route_url('cats.view', id=cat.id)`.  Not so bad, I suppose, but manually plucking out the id everywhere you make a URL is a bit tedious.  And it might be different for every kind of object; maybe dogs' URLs use their names instead.  You can add a `pregenerator` to the `add_route` call, though.

So now we have:

```python
config.add_route('cats.list', '/cats')
config.add_route('cats.view', '/cats/{id:\d+}', pregenerator=make_cat_url)
config.add_route('cats.owners', '/cats/{id:\d+}/owners', pregenerator=make_cat_url)
config.add_route('cats.shots', '/cats/{id:\d+}/shots', pregenerator=make_cat_url)
config.add_route('cats.youtubes', '/cats/{id:\d+}/youtubes', pregenerator=make_cat_url)
config.add_route('cats.hurpdurp', '/cats/{id:\d+}/hurpdurp', pregenerator=make_cat_url)
config.add_route('dogs.view', '/dogs/{id:\d+}', pregenerator=make_dog_url)
config.add_route('dogs.owners', '/dogs/{id:\d+}/owners', pregenerator=make_dog_url)
config.add_route('dogs.shots', '/dogs/{id:\d+}/shots', pregenerator=make_dog_url)
config.add_route('dogs.youtubes', '/dogs/{id:\d+}/youtubes', pregenerator=make_dog_url)
config.add_route('dogs.hurpdurp', '/dogs/{id:\d+}/hurpdurp', pregenerator=make_dog_url)
```

This makes me kind of sad.

Alas, there is one last kink: I have shared comment functionality.  You can have comments on cats, or comments on dogs.  And there are several URLs relating to comments, for viewing and replying and so forth.  So I need to put all those as well, once for each kind of thing comments can be attached to, _and_ flail wildly to get the right kind of object in the actual comment code.

## Enter traversal

Traversal is the thing Pyramid did before it had routing.  The idea is that it works like a filesystem would: `/foo/bar/baz` really means "find the `foo` directory, then find the `bar` directory in that, then find something called `baz` in that".  In Pyramid, this is done with dictionary access: that same path is treated as `root['foo']['bar']['baz']`.

So you might built your site like this:

```python
site_root = dict(
    foo=dict(
        bar=dict(),
    ),
)
```

Pyramid would look up each chunk of the path in order until it ran out of chunks or couldn't go any further.  Our example URL would reach that inner empty dictionary, which would become the "context".  The "view name" would be the next unused part, `baz`, and anything else is considered the "subpath".  (There aren't any other chunks here, so the subpath is an empty tuple.)

Instead of a route name, the view name and context's class get used for finding the code to run.  In practice, the above example isn't very useful; you can't easily tell those `dict`s apart.  You might want something more like this:

```python
class Root(object):
    def __getitem__(self, key):
        if key == 'cats':
            return CatList()
        raise KeyError

class CatList(object):
    def __getitem__(self, key):
        # Find a cat
        cat = get_cat(key)
        if cat:
            return cat
        else:
            raise KeyError

site_root = Root()

@view_config(context=CatList, renderer='cat_list.mako')
def cat_list(context, request):
    return dict()

@view_config(context=Cat, name='', renderer='cat_view.mako')
def cat_view(context, request):
    return dict(cat=context)

@view_config(context=Cat, name='owners', renderer='cat_owners.mako')
def cat_owners(context, request):
    return dict(cat=context)
```

Note that the `context` argument is the traversal context: the last thing Pyramid found.  I included the argument in the routing example, too, but it wasn't anything useful there.

Now when we ask for `/cats/123/owners`, the following happens:

1. Start at the `site_root`.
2. Check for the key `cats`.  Get a `CatList` object back.
3. Check for the key `123`.  Get a `Cat` object back.
4. Check for the key `owners`.  `Cat` objects don't support subscripting, so stop here.  The `Cat` is the context; `owners` is the view name; the subpath is empty again.

This is looking kind of promising.  It's more verbose, but since it's all classes, I can add new ones with less effort than it takes to make a new set of routes.  The code for finding a cat or bailing is in one obvious place; I have less copy/paste of arcane route declarations; and I can do my comments structure fairly easily, by just making both `Cat` and `Dog` return a `CommentList` sort of object that remembers the cat/dog I already found.

## The Bad, The Ugly

So I tried actually applying this to floof.  It seemed like such a nice idea, really.  Obviously I wouldn't be writing this if I hadn't hit a ton of roadblocks.

* The subpath.  There's no way to match against it in `@view_config`, nor any way to disable it.  This means that `/cats/123/owners` does exactly the same thing as `/cats/123/owners/durp/blah/foo/junk/whatever`.  The extra stuff just gets tucked away in `request.subpath`.  Maybe I shouldn't care, but this really bothers me.

* There's no way to force a 404 within traversal; a node/resource can only say "I contain this" or "I don't contain this".  So if you request `/cats/456`, but there's no cat number 456, Pyramid will make `CatList` the context and `456` the view name.

* Naturally, it's possible to take a context object and get back a URL: `request.resource_url(cat, 'owners')` for cat number 123 will theoretically generate `/cats/123/owners`.

    Alas, this works by looking at `__name__` and `__parent__` properties on the context object; here `__name__` should be 123 and `__parent__` should be some `CatList()`, which will have its own name and parent.  If you're using some existing classes as context (say, SQLAlchemy objects), then these properties won't be there!  You can add a `@property` to the classes to generate them, but why on Earth would I want my data to contain references to my URL structure?

    Another alternative is to create a `CatPage` class to wrap the actual cat object and put the special properties on that class, instead...  but then you can't call `resource_url()` on an arbitrary cat object!  You have to wrap it manually, instead.

* `request.resource_url(cat, 'owners')` produces `/cats/123/owners`.  `request.resource_url(cat)` produces `/cats/123/`.  The rationale is something about "relative URLs in your page" that makes no sense to me at all.

* If you write `request.route_url('cats.foo')`, and `cats.foo` isn't a known route name, the page will just fail to render.  This is fantastic: you can catch bad URLs almost immediately.  Unfortunately, `request.resource_url(cat, 'foo')` won't check whether there's a view named `foo` for `Cat` objects; you'll just find out, maybe, when it 404s.

## Dammit

Neither routing nor traversal seems to reflect how anyone builds Web applications—or at least not how I build Web applications.

Routing works well for a few pages with specific URLs, but doing anything structured requires a lot of repetition—and while you could wrap routing in loops and functions, that rapidly becomes confusing to read, losing one of the advantages of routing in the first place.

Traversal works well for serving files from a directory, but...  honestly, not much else!  Every problem listed above seems to reflect a bias towards serving an actual filesystem.

Pyramid does have a lot of hooks; it's possible to replace the traversal mechanism entirely.  I just don't really want to do that to get around these strange little problems.  A lot of the resource stuff also assumes pretty firmly that you're using the `__parent__` mechanism.

I have URLs that represent objects.  They look like `/things/identifier`.  Sometimes that's followed by a page name (`/posts/123/edit`).  Sometimes that's followed by a representation of a child object (`/posts/123/attachments/456`).  Isn't this [pretty common][REST]?  Why is it so hard?

[Pyramid]: http://pylonsproject.org/projects/pyramid/about
[Pylons]: http://docs.pylonsproject.org/docs/pylons.html
[REST]: http://en.wikipedia.org/wiki/Representational_State_Transfer
