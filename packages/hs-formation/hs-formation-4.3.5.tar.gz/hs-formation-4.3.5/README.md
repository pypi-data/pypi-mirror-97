<!-- ![](media/cover.png) -->

# Formation
<!-- [![Build Status](https://travis-ci.org/jondot/formation.svg?branch=master)](https://travis-ci.org/jondot/formation.svg)
[![Coverage Status](https://coveralls.io/repos/github/jondot/formation/badge.svg?branch=master)](https://coveralls.io/github/jondot/formation?branch=master) -->

A generic functional middleware infrastructure for Python.

Take a look:

```py
from datetime.datetime import now
from hs_formation import wrap
from requests import get

def log(ctx, call):
    print("started")
    ctx = call(ctx)
    print("ended")
    return ctx

def timeit(ctx, call):
    started = now()
    ctx = call(ctx)
    ended = now() - started
    ctx['duration'] = ended
    return ctx

def to_requests(ctx):
    get(ctx['url'])
    return ctx

fancy_get = wrap(to_requests, middleware=[log, timeit])
fancy_get({'url':'https://google.com'})
```

## Quick Start

Install using pip/pipenv/etc. (we recommend [poetry](https://github.com/sdispater/poetry) for sane dependency management):

```
$ poetry add formation
```

## Best Practices

A `context` object is a loose bag of objects. With that freedom comes responsibility and opinion.

For example, this is how Formation models a `requests` integration, with data flowing inside `context`:


* It models a `FormationHttpRequest` which abstracts the essentials of making an HTTP request (later shipped to `requests` itself in the way that it likes)
* It tucks `FormationHttpRequest` under the `fmtn.req` key.
* Additional information regarding such a request is kept _alongside_ `fmtn.req`. For example a request id is kept in the `req.id` key. This creates a flat (good thing) dict to probe. The reason additional data does not have the `fmtn` prefix is that you can always build your own that uses a different prefix (which you cant say about internal Formation inner workings).


### added support for async http client via aio_http
You can use this via ```for_aio_http```



### Thanks:

To all [Contributors](https://github.com/jondot/formation/graphs/contributors) - you make this happen, thanks!

# Copyright

Copyright (c) 2018 [@jondot](http://twitter.com/jondot). See [LICENSE](LICENSE.txt) for further details.
