# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['publ', 'publ.image']

package_data = \
{'': ['*'], 'publ': ['default_template/*']}

install_requires = \
['Flask-Caching>=1.9.0,<2.0.0',
 'Flask>=1.1.2,<2.0.0',
 'Pillow>=8.0.1,<9.0.0',
 'Pygments>=2.7.3,<3.0.0',
 'Werkzeug>=1.0.1,<2.0.0',
 'Whoosh>=2.7.4,<3.0.0',
 'arrow>=0.17.0,<0.18.0',
 'atomicwrites>=1.4.0,<2.0.0',
 'authl>=0.4.2,<0.5.0',
 'awesome-slugify>=1.6.5,<2.0.0',
 'misaka>=2.1.1,<3.0.0',
 'pony>=0.7.14,<0.8.0',
 'watchdog>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'publ',
    'version': '0.7.1',
    'description': 'A flexible web-based publishing framework',
    'long_description': "# Publ\n\nA personal publishing platform. Like a static publishing system, only dynamic.\n\n## Motivation\n\nI make a lot of different things — comics, music, art, code, games — and none of\nthe existing content management systems I found quite satisfy my use cases.\nEither they don't allow enough flexibility in the sorts of content that they can\nprovide, or the complexity in managing the content makes it more complicated than\nsimply hand-authoring a site.\n\nI want to bring the best of the classic static web to a more dynamic publishing\nsystem; scheduled posts, category-based templates, and built-in support for\nimage renditions (including thumbnails, high-DPI support, and image galleries).\nAnd I want to do it all using simple Markdown files organized in a sensible\nfile hierarchy.\n\n## Basic tenets\n\n* Containerized web app that's deployable with little friction (hopefully)\n* Do one thing (present heterogeneous content), do it well (hopefully)\n* Use external tools for site content editing\n* Be CDN-friendly\n* High-DPI images and image sets as first-class citizens\n* Interoperate with everything that's open for interoperation (especially [IndieWeb](http://indieweb.org))\n\n## See it in action\n\nThe main demonstration site is at http://beesbuzz.biz/ — it is of course a\nwork in progress! The documentation site for Publ itself (which is also a work in progress) lives at http://publ.beesbuzz.biz/\n\n## Operating requirements\n\nI am designing this to work in any WSGI-capable environment with a supported\nversion of Python. This means that it will, for example, be deployable on any\nshared hosting which has Passenger support (such as Dreamhost), as well as on\nHeroku, Google AppEngine, S3, or any other simple containerized deployment\ntarget.\n\nThe file system is the ground truth for all site data, and while it does use a\ndatabase as a content index, the actual choice of database shouldn't matter all\nthat much. I am targeting SQLite for development, but mysql and Postgres should\nbe supported as well.\n\n## Additional resources\n\nThe [Publ-site](https://github.com/PlaidWeb/Publ-site) repository stores all of\nthe templates, site content, and configuration for the [Publ\nsite](http://publ.beesbuzz.biz).\n\nThe\n[Publ-templates-beesbuzz.biz](https://github.com/PlaidWeb/Publ-templates-beesbuzz.biz)\nrepository provides a stripped-down sample site based on [my personal\nhomepage](http://beesbuzz.biz).\n\n## Authors\n\nIn order of first contribution:\n\n* [fluffy](https://github.com/fluffy-critter)\n* [karinassuni](https://github.com/karinassuni)\n",
    'author': 'fluffy',
    'author_email': 'fluffy@beesbuzz.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://publ.beesbuzz.biz/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
