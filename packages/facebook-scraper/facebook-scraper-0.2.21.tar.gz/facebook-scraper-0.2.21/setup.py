# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['facebook_scraper']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.0.0,<2.0.0', 'requests-html>=0.10.0,<0.11.0']

extras_require = \
{'youtube-dl': ['youtube_dl']}

entry_points = \
{'console_scripts': ['facebook-scraper = facebook_scraper.__main__:run']}

setup_kwargs = {
    'name': 'facebook-scraper',
    'version': '0.2.21',
    'description': 'Scrape Facebook public pages without an API key',
    'long_description': '# Facebook Scraper\n\nScrape Facebook public pages without an API key. Inspired by [twitter-scraper](https://github.com/kennethreitz/twitter-scraper).\n\n\n## Install\n\n```sh\npip install facebook-scraper\n```\n\n\n## Usage\n\nSend the unique **page name** as the first parameter and you\'re good to go:\n\n```python\n>>> from facebook_scraper import get_posts\n\n>>> for post in get_posts(\'nintendo\', pages=1):\n...     print(post[\'text\'][:50])\n...\nThe final step on the road to the Super Smash Bros\nWe’re headed to PAX East 3/28-3/31 with new games\n```\n\n\n### Optional parameters\n\n*(For the `get_posts` function)*.\n\n- **group**: group id, to scrape groups instead of pages. Default is `None`.\n- **pages**: how many pages of posts to request, the first 2 pages may have no results, so try with a number greater than 2. Default is 10.\n- **timeout**: how many seconds to wait before timing out. Default is 5.\n- **credentials**: tuple of user and password to login before requesting the posts. Default is `None`.\n- **extra_info**: bool, if true the function will try to do an extra request to get the post reactions. Default is False.\n- **youtube_dl**: bool, use Youtube-DL for (high-quality) video extraction. You need to have youtube-dl installed on your environment. Default is False.\n\n\n## CLI usage\n\n```sh\n$ facebook-scraper --filename nintendo_page_posts.csv --pages 10 nintendo\n```\n\nRun `facebook-scraper --help` for more details on CLI usage.\n\n**Note:** If you get a `UnicodeEncodeError` try adding `--encoding utf-8`.\n\n\n## Post example\n\n```python\n{\'post_id\': \'2257188721032235\',\n \'text\': \'Don’t let this diminutive version of the Hero of Time fool you, \'\n         \'Young Link is just as heroic as his fully grown version! Young Link \'\n         \'joins the Super Smash Bros. series of amiibo figures!\',\n \'time\': datetime.datetime(2019, 4, 29, 12, 0, 1),\n \'image\': \'https://scontent.flim16-1.fna.fbcdn.net\'\n          \'/v/t1.0-0/cp0/e15/q65/p320x320\'\n          \'/58680860_2257182054366235_1985558733786185728_n.jpg\'\n          \'?_nc_cat=1&_nc_ht=scontent.flim16-1.fna\'\n          \'&oh=31b0ba32ec7886e95a5478c479ba1d38&oe=5D6CDEE4\',\n \'images\': [\'https://scontent.flim16-1.fna.fbcdn.net\'\n          \'/v/t1.0-0/cp0/e15/q65/p320x320\'\n          \'/58680860_2257182054366235_1985558733786185728_n.jpg\'\n          \'?_nc_cat=1&_nc_ht=scontent.flim16-1.fna\'\n          \'&oh=31b0ba32ec7886e95a5478c479ba1d38&oe=5D6CDEE4\'],\n \'likes\': 2036,\n \'comments\': 214,\n \'shares\': 0,\n \'reactions\': {\'like\': 135, \'love\': 64, \'haha\': 10, \'wow\': 4, \'anger\': 1},  # if `extra_info` was set\n \'post_url\': \'https://m.facebook.com/story.php\'\n             \'?story_fbid=2257188721032235&id=119240841493711\',\n \'link\': \'https://bit.ly/something\', \n \'is_live\': False}\n```\n\n\n### Notes\n\n- There is no guarantee that every field will be extracted (they might be `None`).\n- Shares doesn\'t seem to work at the moment.\n- Group posts may be missing some fields like `time` and `post_url`.\n- Group scraping may return only one page and not work on private groups.\n\n\n## To-Do\n\n- Async support\n- Image galleries\n- Profiles or post authors\n- Comments\n\n\n## Alternatives and related projects\n\n- [facebook-post-scraper](https://github.com/brutalsavage/facebook-post-scraper). Has comments. Uses Selenium.\n- [facebook-scraper-selenium](https://github.com/apurvmishra99/facebook-scraper-selenium). "Scrape posts from any group or user into a .csv file without needing to register for any API access".\n- [Ultimate Facebook Scraper](https://github.com/harismuneer/Ultimate-Facebook-Scraper).  "Scrapes almost everything about a Facebook user\'s profile". Uses Selenium.\n- [Unofficial APIs](https://github.com/Rolstenhouse/unofficial-apis). List of unofficial APIs for various services, none for Facebook for now, but might be worth to check in the future.\n- [major-scrapy-spiders](https://github.com/talhashraf/major-scrapy-spiders). Has a profile spider for Scrapy.\n- [facebook-page-post-scraper](https://github.com/minimaxir/facebook-page-post-scraper). Seems abandoned.\n    - [FBLYZE](https://github.com/isaacmg/fb_scraper). Fork (?).\n- [RSSHub](https://github.com/DIYgod/RSSHub/blob/master/lib/routes/facebook/page.js). Generates an RSS feed from Facebook pages.\n- [RSS-Bridge](https://github.com/RSS-Bridge/rss-bridge/blob/master/bridges/FacebookBridge.php). Also generates RSS feeds from Facebook pages.\n',
    'author': 'Kevin Zúñiga',
    'author_email': 'kevin.zun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevinzg/facebook-scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
