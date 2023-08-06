# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dpytools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dpytools',
    'version': '0.0.13a0',
    'description': 'Simple tools to build discord bots using discord.py',
    'long_description': '# dpytools\nToolset to speed up developing discord bots using discord.py\n\n<hr>\n\n## Status of the project\n\nEarly development. As such its expected to be unstable and unsuited for production.\n\n## Components\n### menus\n#### arrows\nDisplays a menu made from passed Embeds with navigation by reaction.\n#### confirm \nReturns the user reaction to confirm or deny a passed message.\n\n### embeds\n#### paginate_to_embeds\nPaginates a long text into a list of embeds.\n\n### parsers\n#### parse_time\nParses strings with the format "2h15m" to a timedelta object.\n\n### owner_cog\nCog with different command useful for the owner of the bot\n#### Commands\n##### cogs \nlists, loads, unloads and reloads cogs in bulk or individually\n\n### checks\n#### admin_or_roles\nCheck if command user is an admin or has any of passed roles\n#### only_this_guild\nCheck that limits the command to a specific guild.\n#### dm_from_this_guild\nLimits a command to direct messages while also checking if the user comes from a particular guild\n\n<hr>\n\n# Contributing\nFeel free to make a pull request.',
    'author': 'chrisdewa',
    'author_email': 'alexdewa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrisdewa/dpytools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
