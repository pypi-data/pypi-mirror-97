# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_rss', 'telegram_rss.commands', 'telegram_rss.feed']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'attrs>=20.3.0,<21.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'bleach>=3.2.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'feedparser>=6.0.2,<7.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-telegram-bot>=13.1,<14.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['telegram-rss = telegram_rss.main:main']}

setup_kwargs = {
    'name': 'telegram-rss',
    'version': '0.8.1',
    'description': 'Fetch rss and send the latest update to telegram.',
    'long_description': '# Telegram RSS\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/telegram-rss)](https://pypi.org/project/telegram-rss/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/telegram-rss)](https://pypi.org/project/telegram-rss/)\n[![LICENSE](https://img.shields.io/github/license/pentatester/telegram-rss)](https://github.com/pentatester/telegram-rss/blob/master/LICENSE)\n[![Wiki Page](https://img.shields.io/badge/wiki-telegram--rss-blue)](https://github.com/pentatester/telegram-rss/wiki)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)\n\nFetch rss and send the latest update to telegram. **This project is still in active development**\n\n## Usage\n\n### Setup\n\n- Make sure you have python installed.\n- Open command line.\n- Install `pip install --upgrade telegram-rss`\n- Run `python -m telegram_rss`\n- Add bot token, feeds, [user\'s id](#how-to-get-ids), and/or [channel\'s id](#how-to-get-ids) inside telegram-rss/config.toml\n- Run `python -m telegram_rss update` to send initial update (*use personal id to send initial update*)\n\nIf your system support entry_points, you can execute `python -m telegram_rss` with `telegram-rss`.\n\n## Checking update\n\nRun `python -m telegram_rss update` to check and send the latest feeds\n\n## Example config\n\n```toml\nbot_token = "987654321:ASDASDASD-1sda2eas3asd-91sdajh28j"\nenv_token = "TOKEN"\nusers = [ 123456789,]\nchannels = [ -123456789,]\ngroups = [ 1234567890,]\nweb_page_preview = true\nmessage_delay = 0.05\nread_more_button = "Read more"\n\n[[feeds]]\nname = "Feed example online"\nsource = "http://feedparser.org/docs/examples/atom10.xml"\nfooter_link = "http://feedparser.org/docs/"\nchannels = [ -123456789,]\nonly_today = true\n\n[[feeds]]\nname = "Feed example local"\nsource = "c:\\\\incoming\\\\atom10.xml"\nsave_bandwith = false\nonly_today = false\nusers = [ 987654321,]\ngroups = [ 111111111,]\nfooter = false\n\n[template_data]\nauthor = "Author"\nsource = "Source"\n\n```\n\n- Send feed if published today (when we checked) `only_today = true`.\n- Disable web preview in chat by `web_page_preview = false`.\n- If you don\'t want read_more_button under the message, set `read_more_button = ""`.\n- Don\'t set message_delay too low, it can be detected as spam.\n\n## Template\n\n`template.html` is loaded using jinja2, [Learn more](https://jinja.palletsprojects.com/en/2.11.x/ "Jinja2 documentation").\nDefault template is\n\n```html\n<a href="{{ entry.link }}">{{ entry.safe_title }}</a>\n<i>{{ author }}</i>: <b>{{ entry.author }}</b>\n{{ entry.safe_description }}\n<i>{{ source }}</i>: <a href="{{ channel.link }}">{{ channel.safe_title }}</a>\n```\n\nMore about [objects in template](#template-objects)\n\n## How to get token\n\nJust create a new bot account using [@BotFather](https://t.me/BotFather). **Don\'t forget to add the bot as channel\'s admin**\n\n## How to get ids\n\nSend / forward a message (user or channel) to [@JsonDumpBot](https://t.me/JsonDumpBot)\n\n## Template objects\n\n### entry\n\n```python\nclass Entry:\n    title: str\n    link: str\n    description: str\n    author: str\n    published: Optional[str]\n    time: Optional[datetime]\n    safe_title: str\n    safe_description: str\n```\n\n### channel\n\n```python\nclass Channel:\n    title: str\n    link: str\n    description: str\n    safe_title: str\n    safe_description: str\n```\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pentatester/telegram-rss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
