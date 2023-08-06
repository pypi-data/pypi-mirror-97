# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hs_formation', 'hs_formation.middleware']

package_data = \
{'': ['*']}

install_requires = \
['aiobreaker>=1.1.0,<2.0.0',
 'aiohttp>=3.7.3,<4.0.0',
 'attrs-serde>=0.2.2,<0.3.0',
 'attrs>=19.1,<20.0',
 'cytoolz>=0.9.0,<0.10.0',
 'lxml>=4.2,<5.0',
 'pybreaker>=0.4.5,<0.5.0',
 'requests>=2.20,<3.0',
 'toolz>=0.9.0,<0.10.0',
 'xmltodict>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'hs-formation',
    'version': '4.3.5',
    'description': 'A generic functional middleware infrastructure for Python.',
    'long_description': '<!-- ![](media/cover.png) -->\n\n# Formation\n<!-- [![Build Status](https://travis-ci.org/jondot/formation.svg?branch=master)](https://travis-ci.org/jondot/formation.svg)\n[![Coverage Status](https://coveralls.io/repos/github/jondot/formation/badge.svg?branch=master)](https://coveralls.io/github/jondot/formation?branch=master) -->\n\nA generic functional middleware infrastructure for Python.\n\nTake a look:\n\n```py\nfrom datetime.datetime import now\nfrom hs_formation import wrap\nfrom requests import get\n\ndef log(ctx, call):\n    print("started")\n    ctx = call(ctx)\n    print("ended")\n    return ctx\n\ndef timeit(ctx, call):\n    started = now()\n    ctx = call(ctx)\n    ended = now() - started\n    ctx[\'duration\'] = ended\n    return ctx\n\ndef to_requests(ctx):\n    get(ctx[\'url\'])\n    return ctx\n\nfancy_get = wrap(to_requests, middleware=[log, timeit])\nfancy_get({\'url\':\'https://google.com\'})\n```\n\n## Quick Start\n\nInstall using pip/pipenv/etc. (we recommend [poetry](https://github.com/sdispater/poetry) for sane dependency management):\n\n```\n$ poetry add formation\n```\n\n## Best Practices\n\nA `context` object is a loose bag of objects. With that freedom comes responsibility and opinion.\n\nFor example, this is how Formation models a `requests` integration, with data flowing inside `context`:\n\n\n* It models a `FormationHttpRequest` which abstracts the essentials of making an HTTP request (later shipped to `requests` itself in the way that it likes)\n* It tucks `FormationHttpRequest` under the `fmtn.req` key.\n* Additional information regarding such a request is kept _alongside_ `fmtn.req`. For example a request id is kept in the `req.id` key. This creates a flat (good thing) dict to probe. The reason additional data does not have the `fmtn` prefix is that you can always build your own that uses a different prefix (which you cant say about internal Formation inner workings).\n\n\n### added support for async http client via aio_http\nYou can use this via ```for_aio_http```\n\n\n\n### Thanks:\n\nTo all [Contributors](https://github.com/jondot/formation/graphs/contributors) - you make this happen, thanks!\n\n# Copyright\n\nCopyright (c) 2018 [@jondot](http://twitter.com/jondot). See [LICENSE](LICENSE.txt) for further details.\n',
    'author': 'Dotan Nahum',
    'author_email': 'jondotan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HiredScorelabs/hs-formation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
