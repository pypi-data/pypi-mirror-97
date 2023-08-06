# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treefrog',
 'treefrog.flatten',
 'treefrog.organize',
 'treefrog.parse',
 'treefrog.rename']

package_data = \
{'': ['*']}

install_requires = \
['py-slippi>=1.6.1,<2.0.0', 'tqdm>=4.56.2,<5.0.0']

entry_points = \
{'console_scripts': ['treefrog = treefrog.__main__:main']}

setup_kwargs = {
    'name': 'treefrog',
    'version': '0.6.1',
    'description': 'Organize the Slippi game files in your filesystem according to their attributes',
    'long_description': '# `treefrog`\n\n[![pypi version](https://img.shields.io/pypi/v/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)\n[![downloads](https://pepy.tech/badge/treefrog)](https://pepy.tech/project/treefrog)\n[![build status](https://github.com/dawsonbooth/treefrog/workflows/build/badge.svg)](https://github.com/dawsonbooth/treefrog/actions?workflow=build)\n[![python versions](https://img.shields.io/pypi/pyversions/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)\n[![format](https://img.shields.io/pypi/format/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)\n[![license](https://img.shields.io/pypi/l/treefrog.svg?style=flat)](https://github.com/dawsonbooth/treefrog/blob/master/LICENSE)\n\n## Description\n\nOrganize the Slippi game files in your filesystem according to their attributes.\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npython -m pip install treefrog\n```\n\n## Usage\n\n### Module\n\nCurrently, the package supports organizing the files according to a supplied ordering of parsers, flattening the files against the supplied root folder, and renaming all the files according to their attributes. These may be accomplished programmatically with the use of the `Tree` class or through the command-line interface.\n\n#### Organize\n\nThe `organize` method serves the purpose of moving each game file found (deeply or otherwise) under the root folder to its proper location according to the supplied ordering of parsers. If no ordering is given, then treefrog will use its default. Here is a simple example of calling this method:\n\n```python\nfrom treefrog import Tree\nfrom treefrog.parse.parsers import year, month, matchup, stage\n\nordering = (\n    year,\n    month,\n    matchup,\n    stage\n) # An iterable of the desired levels of the hierarchy\n\nwith Tree("slp/", show_progress=True) as tree:\n    tree.organize(ordering) # Organize the files into subfolders according to the supplied attributes\n```\n\nFeel free to provide your own logic for formatting the names of the folders at a particular level with a corresponding iterable of functions:\n\n```python\nfrom treefrog import Tree\nfrom treefrog.parse.parsers import year, month, stage\nfrom treefrog.parse.utils import character_name, most_used_character, opponent, user\n\ndef ordered_matchup(game):\n    p1 = user(game, "DTB#566")\n    p2 = opponent(game, "DTB#566")\n    return f"{character_name(most_used_character(p1))} vs {character_name(most_used_character(p2))}"\n\nordering = (\n    year,\n    month,\n    lambda game: opponent(game, "DTB#566").netplay.code,\n    ordered_matchup,\n    stage\n)\n\nwith Tree("slp/", show_progress=True) as tree:\n    tree.organize(ordering)\n```\n\nAny custom parser you provide will need to be a `Callable` that takes in a `Game` instance and returns a `str`.\n\nFurther, you can use cascading methods to simplify your programming. Each of the methods `organize`, `flatten`, and `rename` will return a reference to the instance object on which it was called. Something like this: `tree.organize().rename()` will both organize and rename the game files.\n\n#### Flatten\n\nThe `flatten` method serves the simple purpose of moving each game file found (deeply or otherwise) under the root folder back to the root folder itself. Here\'s an example of what calling this method may look like:\n\n```python\nfrom treefrog import Tree\n\ntree = Tree("slp/")\ntree.flatten().resolve()\n```\n\nNote that you do not have to use `Tree` with a context manager. If you do not use the `with` keyword as in the first couple of examples, you will need to end your operations with a call to the `resolve` method in order to see the changes reflected in your filesystem.\n\n#### Rename\n\nThe `rename` method simply renames each game file according to its attributes. Without a rename function supplied, treefrog will use the `default_filename` function found in the `treefrog.rename` module. Alternatively, you may provide your own rename function as shown below:\n\n```python\nfrom treefrog import Tree\nfrom treefrog.parse.parsers import stage, timestamp\nfrom treefrog.parse.utils import character_name, characters\n\ndef create_filename(game: Game):\n    p1, p2 = tuple(characters(game))\n    return f"{timestamp(game)} - {character_name(p1)} vs {character_name(p2)} - {stage(game)}.slp"\n\nwith Tree("slp/") as tree:\n    tree.rename(create_filename=create_filename)\n```\n\n### Command-Line\n\nThis is also command-line program, and can be executed as follows:\n\n```txt\npython -m treefrog [-h] [-g GLOB] [-c NETPLAY_CODE] [-p] [-d] [-o | -f] [-r] root_folder\n```\n\nOptions:\n\n| Argument                                       | Description                                                         |\n| ---------------------------------------------- | ------------------------------------------------------------------- |\n| `root_folder`                                  | Slippi folder root path                                             |\n| `-h, --help`                                   | show this help message and exit                                     |\n| `-g GLOB, --glob GLOB`                         | The glob pattern to search with                                     |\n| `-c NETPLAY_CODE, --netplay-code NETPLAY_CODE` | Netplay code (e.g. DTB#566)                                         |\n| `-p, --show-progress`                          | Whether to show a progress bar                                      |\n| `-d, --default-rename`                         | Whether to restore the filenames to their defaults                  |\n| `-o, --organize`                               | Whether to organize the folder hierarchy                            |\n| `-f, --flatten`                                | Whether to flatten your Slippi game files to a shared parent folder |\n| `-r, --rename`                                 | Whether to rename the files according to their features             |\n\nFor example, the following command will organize all the game files under the `slp` directory with a progress bar.\n\n```bash\npython -m treefrog "slp" -c "DTB#566" -op\n```\n\nFeel free to [check out the docs](https://dawsonbooth.com/treefrog/) for more information.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/treefrog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
