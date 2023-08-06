# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spellapi', 'spellbot', 'spellbot.versions', 'spellbot.versions.versions']

package_data = \
{'': ['*'], 'spellbot': ['assets/*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'aiohttp==3.6.3',
 'aioredis>=1.3.1,<2.0.0',
 'alembic==1.5.5',
 'click==7.1.2',
 'coloredlogs==15.0',
 'discord.py==1.5.1',
 'dunamai==1.5.4',
 'expiringdict==1.2.1',
 'fastapi-cache2>=0.1.2,<0.2.0',
 'fastapi>=0.62,<0.64',
 'httpx>=0.16.1,<0.18.0',
 'humanize==3.2.0',
 'hupper==1.10.2',
 'itsdangerous>=1.1.0,<2.0.0',
 'psycopg2-binary==2.8.6',
 'python-dateutil==2.8.1',
 'python-dotenv==0.15.0',
 'python-jose[cryptography]>=3.2.0,<4.0.0',
 'pytz==2021.1',
 'pyyaml==5.4.1',
 'redis==3.5.3',
 'requests==2.25.1',
 'sqlalchemy==1.3.23',
 'unidecode==1.2.0',
 'uvicorn>=0.13.1,<0.14.0']

entry_points = \
{'console_scripts': ['spellapi = spellapi:main', 'spellbot = spellbot:main']}

setup_kwargs = {
    'name': 'spellbot',
    'version': '5.25.0',
    'description': 'The Discord bot for SpellTable',
    'long_description': '<img align="right" width="200" src="https://raw.githubusercontent.com/lexicalunit/spellbot/master/spellbot.png" />\n\n# SpellBot\n\n[![build][build-badge]][build]\n[![top][top-badge]][top]\n[![uptime][uptime-badge]][uptime]\n[![metrics][metrics-badge]][metrics]\n[![pypi][pypi-badge]][pypi]\n[![codecov][codecov-badge]][codecov]\n[![CodeFactor][factor-badge]][factor]\n[![CodeQL][codeql-badge]][security]\n[![python][python-badge]][python]\n[![black][black-badge]][black]\n[![mit][mit-badge]][mit]\n[![patreon][patreon-button]][patreon]\n[![follow][follow-badge]][follow]\n\nThe Discord bot for [SpellTable][spelltable].\n\n[![add-bot][add-bot-button]][add-bot]\n\n## 🤖 Using SpellBot\n\nOnce you\'ve connected the bot to your server, you can interact with it over\nDiscord via the following commands in any of the authorized channels. **Keep in\nmind that sometimes SpellBot will respond to you via Direct Message to avoid\nbeing too spammy in text channels.**\n\n- `!spellbot help`: Provides detailed help about all of the following commands.\n- `!about`: Get information about SpellBot and its creators.\n\n> **Note:** To use the\n> [commands for event runners](#%EF%B8%8F-commands-for-event-runners)\n> and [commands for admins](#-commands-for-admins), you will need to\n> [create a role on your server][create-role] called `SpellBot Admin`\n> (capitalization matters). Only users with that role will be able to use those\n> commands.\n\n### ✋ Commands for Players\n\nJust looking to play some games of Magic? These commands are for you!\n\n- `!lfg`: Find or start up a game of Magic: The Gathering!\n- `!leave`: Leave any games that you\'ve signed up for.\n- `!power`: Set your current power level.\n- `!report`: Report the results of the game you just played.\n- `!team`: Join one of the teams available on your server.\n- `!points`: Find out how many points you currently have.\n- `!block`: Block other users from joining your games.\n- `!unblock`: Unblock previously blocked users.\n\nWhen you run the `!lfg` command, SpellBot will post a message for sign ups.\n\n![lfg][lfg]\n\nOther users can react to it with the ✋ emoji to be added to the game. When the\ngame is ready, SpellBot will update the message with your SpellTable details.\n\n![ready][ready]\n\nUsers can also use the 🚫 emoji reaction to leave the game.\n\n### 🎟️ Commands for Event Runners\n\nThese commands are intended to be run by SpellBot Admins and help facilitate\nonline events.\n\n- `!game`: Directly create games for the mentioned users.\n- `!event`: Create a bunch of games all at once based on some uploaded data.\n- `!begin`: Start an event that you previously created with `!event`.\n- `!export`: Export historical game data for your server.\n\n### 👑 Commands for Admins\n\nThese commands will help you configure SpellBot for your server.\n\n- `!spellbot`: This command allows admins to configure SpellBot for their\n               server. It supports the following subcommands:\n  - `config`: Just show the current configuration for this server.\n  - `channels`: Set the channels SpellBot is allowed to operate within.\n  - `prefix`: Set the command prefix for SpellBot in text channels.\n  - `links`: Set the privacy level for generated SpellTable links.\n  - `spectate`: Add a spectator link to the posts SpellBot makes.\n  - `expire`: Set how many minutes before games are expired due to inactivity.\n  - `teams`: Sets the teams available on this server.\n  - `power`: Turns the power command on or off for this server.\n  - `voice`: When on, SpellBot will automatically create voice channels.\n  - `tags`: Turn on or off the ability to use tags. Optionally mention specific channels.\n  - `queue-time`: Turn on or off average queue time details. Optionally mention specific channels.\n  - `smotd`: Set the server message of the day.\n  - `cmotd`: Set the message of the day for the channel where you run it.\n  - `motd`: Set the privacy level for messages of the day.\n  - `size`: Sets the default game size for a specific channel.\n  - `toggle-verify`: Toggles requirement of verification for a specific channel.\n  - `auto-verify`: Set the channels that will trigger user auto verification.\n  - `unverified-only`: Set the channels that are only for unverified users.\n  - `verify-message`: Set the verification message for a specific channel.\n  - `voice-category`: Set category for voice channels created by !game.\n  - `stats`: Gets some statistics about SpellBot usage on your server.\n  - `help`: Get detailed usage help for SpellBot.\n- `!verify`: Allows moderators to verify a user on their server.\n- `!unverify`: Un-verifies a user for this server.\n- `!watch`: Allows moderators to watch a user on their server.\n- `!unwatch`: Un-watches a user for this server.\n\n### 🛋️ Ergonomics\n\nSpellBot will always try and assume useful defaults or try to do the right thing\nwhen you give it a command. For example if you use the tag <code>~modern</code>\nor other format names when creating a game, it will automatically assume the\ncorrect number of players for you. Hopefully these features are intuitive and\nhelpful 🤞 — and if not, [please report bugs and request features][issues]\nto your heart\'s content.\n\n### 🎤 Feedback\n\nThoughts and suggestions? Come join us on the\n[SpellTable Discord server][discord-invite]! Please also feel free\nto [directly report any bugs][issues] that you encounter.\n\n## 🙌 Support Me\n\nI\'m keeping SpellBot running using my own money but if you like the bot and want\nto help me out, please consider [becoming a patron][patreon].\n\n## ❤️ Contributing\n\nIf you\'d like to become a part of the SpellBot development community please\nfirst know that we have a documented [code of conduct](CODE_OF_CONDUCT.md) and\nthen see our [documentation on how to contribute](CONTRIBUTING.md) for details\non how to get started.\n\n## 🔧 Running SpellBot Yourself\n\nFirst install `spellbot` using [`pip`](https://pip.pypa.io/en/stable/):\n\n```shell\npip install spellbot\n```\n\nProvide your Discord bot token with the environment variable `SPELLBOT_TOKEN`.\nAs well as your SpellTable API authorization token via `SPELLTABLE_AUTH`.\n\nYou can get [your bot token from Discord][discord-bot-docs]. Your bot will\nneed the following permissions enabled:\n\n- Manage Channels\n- Create Instant Invite\n- View Channels\n- Send Messages\n- Manage Messages\n- Embed Links\n- Read Message History\n- Add Reactions\n\nAs for the SpellTable API authorization token, you\'ll have to talk to the\nSpellTable developers. Come join us on the\n[SpellTable Discord server][spelltable-discord].\n\nBy default SpellBot will use sqlite3 as its database. You can however choose to\nuse another database by providing a [SQLAlchemy Connection URL][db-url]. This\ncan be done via the `--database-url` command line option or the environment\nvariable `SPELLBOT_DB_URL`. Note that, at the time of this writing, SpellBot is\nonly tested against sqlite3 and PostgreSQL.\n\nMore usage help can be found by running `spellbot --help`.\n\n## 🐳 Docker Support\n\nYou can also run SpellBot via docker. Our image is published to\n[lexicalunit/spellbot][docker-hub]. See [our documentation on Docker Support](DOCKER.md) for help\nwith installing and using it.\n\n---\n\n[MIT][mit] © [amy@lexicalunit][lexicalunit] et [al][contributors]\n\n[add-bot-button]:     https://user-images.githubusercontent.com/1903876/88951823-5d6c9a00-d24b-11ea-8523-d256ccbf4a3c.png\n[add-bot]:            https://discordapp.com/api/oauth2/authorize?client_id=725510263251402832&permissions=93265&scope=bot\n[black-badge]:        https://img.shields.io/badge/code%20style-black-000000.svg\n[black]:              https://github.com/psf/black\n[build-badge]:        https://github.com/lexicalunit/spellbot/workflows/build/badge.svg\n[build]:              https://github.com/lexicalunit/spellbot/actions\n[codecov-badge]:      https://codecov.io/gh/lexicalunit/spellbot/branch/master/graph/badge.svg\n[codecov]:            https://codecov.io/gh/lexicalunit/spellbot\n[codeql-badge]:       https://github.com/lexicalunit/spellbot/workflows/CodeQL/badge.svg\n[contributors]:       https://github.com/lexicalunit/spellbot/graphs/contributors\n[create-role]:        https://support.discord.com/hc/en-us/articles/206029707-How-do-I-set-up-Permissions-\n[db-url]:             https://docs.sqlalchemy.org/en/latest/core/engines.html\n[discord-bot-docs]:   https://discord.com/developers/docs/topics/oauth2#bots\n[discord-invite]:     https://discord.gg/zXzgqMN\n[docker-hub]:         https://hub.docker.com/r/lexicalunit/spellbot\n[factor-badge]:       https://www.codefactor.io/repository/github/lexicalunit/spellbot/badge\n[factor]:             https://www.codefactor.io/repository/github/lexicalunit/spellbot\n[follow-badge]:       https://img.shields.io/twitter/follow/SpellBotIO?style=social\n[follow]:             https://twitter.com/intent/follow?screen_name=SpellBotIO\n[issues]:             https://github.com/lexicalunit/spellbot/issues\n[patreon]:            https://www.patreon.com/lexicalunit\n[patreon-button]:     https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Dlexicalunit%26type%3Dpatrons88951826-5e053080-d24b-11ea-9a81-f1b5431a5d4b.png\n[lexicalunit]:        http://github.com/lexicalunit\n[lfg]:                https://user-images.githubusercontent.com/1903876/91242259-cedd2280-e6fb-11ea-8d30-e7127b6f96e9.png\n[metrics-badge]:      https://img.shields.io/badge/metrics-grafana-orange.svg\n[metrics]:            https://lexicalunit.grafana.net/d/4TSUCbcMz/spellbot?orgId=1\n[mit-badge]:          https://img.shields.io/badge/License-MIT-yellow.svg\n[mit]:                https://opensource.org/licenses/MIT\n[pypi-badge]:         https://img.shields.io/pypi/v/spellbot\n[pypi]:               https://pypi.org/project/spellbot/\n[python-badge]:       https://img.shields.io/badge/python-3.8+-blue.svg\n[python]:             https://www.python.org/\n[ready]:              https://user-images.githubusercontent.com/1903876/91242257-cdabf580-e6fb-11ea-86ad-8f1aaf6d34dc.png\n[security]:           https://github.com/lexicalunit/spellbot/security\n[spelltable-discord]: https://discord.gg/zXzgqMN\n[spelltable]:         https://www.spelltable.com/\n[top-badge]:          https://top.gg/api/widget/status/725510263251402832.svg?noavatar=true\n[top]:                https://top.gg/bot/725510263251402832\n[uptime-badge]:       https://img.shields.io/uptimerobot/ratio/m785764282-c51c742e56a87d802968efcc\n[uptime]:             https://uptimerobot.com/dashboard#785764282\n',
    'author': 'Amy',
    'author_email': 'amy@lexicalunit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://spellbot.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
