# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canopy', 'canopy.templates']

package_data = \
{'': ['*']}

entry_points = \
{'web.apps': ['canopy = canopy:app']}

setup_kwargs = {
    'name': 'canopy-network',
    'version': '0.0.3a0',
    'description': 'A decentralized social network.',
    'long_description': '# canopy\na decentralized social network\n\nStore and display content on your own personal website. Interact richly with other sites.\n\n## Install\n\n[Create a web presence](https://github.com/angelogladding/ghost), install "GitHub Repo" `canopy`, run the canopy application and map it to your installed domain.\n\n## Features\n\n* render profile, pages, media, posts and feeds with semantic markup a la [microformats](https://indieweb.org/microformats)\n  * archive source material for [reply contexts](https://indieweb.org/reply-context)\n  * moderated threaded discussion using Webmentions with Salmention & Vouch\n  * syndicate to third-party aggregators\n* store posts:\n  * as [queryable JSON](https://www.sqlite.org/json1.html) in SQLite database\n    * [full-text search](https://www.sqlite.org/fts5.html)\n  * as JSON flat files inside Git repository for change history\n* follow by subscribing and publish to subscribers using WebSub\n* sign in to third-party applications using IndieAuth\n  * leverage third-party Micropub editors\n  * leverage third-party Microsub readers\n* import/export tools\n  * syndicate/backfeed to/from Twitter/Github/Facebook\n  * backup/restore to/from local/remote storage\n',
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
