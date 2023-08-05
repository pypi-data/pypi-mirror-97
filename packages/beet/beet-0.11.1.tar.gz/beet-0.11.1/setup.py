# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beet', 'beet.contrib', 'beet.core', 'beet.library', 'beet.toolchain']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'Pillow>=8.0.1,<9.0.0',
 'click-help-colors>=0.9,<0.10',
 'click>=7.1.2,<8.0.0',
 'nbtlib>=1.8.2,<2.0.0',
 'pathspec>=0.8.1,<0.9.0',
 'pydantic>=1.7.3,<2.0.0']

extras_require = \
{':sys_platform == "win32"': ['colorama']}

entry_points = \
{'console_scripts': ['beet = beet.toolchain.cli:main'],
 'pytest11': ['beet = beet.pytest_plugin']}

setup_kwargs = {
    'name': 'beet',
    'version': '0.11.1',
    'description': 'The Minecraft pack development kit',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/mcbeet/beet/main/logo.png?sanitize=true" alt="logo" width="76">\n\n# Beet\n\n[![GitHub Actions](https://github.com/mcbeet/beet/workflows/CI/badge.svg)](https://github.com/mcbeet/beet/actions)\n[![PyPI](https://img.shields.io/pypi/v/beet.svg)](https://pypi.org/project/beet/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beet.svg)](https://pypi.org/project/beet/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> The Minecraft pack development kit.\n\n## Introduction\n\nMinecraft [resource packs](https://minecraft.gamepedia.com/Resource_Pack) and [data packs](https://minecraft.gamepedia.com/Data_Pack) work well as _distribution_ formats but can be pretty limiting as _authoring_ formats. Without the ability to parametrize or create abstractions over assets and data pack resources, projects and libraries created by the community are greatly limited when it comes to reusability and interoperability.\n\nThere\'s been a lot of attempts at establishing standardized tooling to improve the development experience and it\'s becoming more and more apparent that the problem space is fundamentally multi-paradigm. Different problems require different solutions, so providing unified cross-project reusability needs to involve an interoperability layer that\'s sufficiently unopinionated to let all these paradigms shine through.\n\nThe `beet` project is meant to serve as a platform for building a cooperative tooling ecosystem by providing a flexible composition model and a user-friendly development workflow.\n\n### Screencasts\n\n- **Quick start** [https://youtu.be/JGrJTOhG3pY](https://youtu.be/JGrJTOhG3pY)\n- **Command-line** [https://youtu.be/fQ9up0ELPNE](https://youtu.be/fQ9up0ELPNE)\n- **Library overview** [https://youtu.be/LDvV4_l-PSc](https://youtu.be/LDvV4_l-PSc)\n- **Plugins basics** [https://youtu.be/XTzKmvHqd1g](https://youtu.be/XTzKmvHqd1g)\n- **Pipeline configuration** [https://youtu.be/QsnQncGxAAs](https://youtu.be/QsnQncGxAAs)\n\n### Library\n\n> [Documentation](https://mcbeet.dev/library/)\n\n```python\nfrom beet import ResourcePack, Texture\n\n# Open a zipped resource pack and add a custom stone texture\nwith ResourcePack(path="stone.zip") as assets:\n    assets["minecraft:block/stone"] = Texture(source_path="custom.png")\n```\n\nThe `beet` library provides carefully crafted primitives for working with Minecraft resource packs and data packs.\n\n- Create, read, edit and merge resource packs and data packs\n- Handle zipped and unzipped packs\n- Fast and lazy by default, files are transparently loaded when needed\n- Statically typed API enabling rich intellisense and autocompletion\n\n### Toolchain\n\n> [Documentation](https://mcbeet.dev/toolchain/)\n\n```python\nfrom beet import Context, Function\n\ndef greet(ctx: Context):\n    """Plugin that adds a function for greeting the player."""\n    ctx.data["greet:hello"] = Function(["say hello"], tags=["minecraft:load"])\n```\n\nThe `beet` toolchain is designed to support a wide range of use-cases. The most basic pipeline will let you create configurable resource packs and data packs, but plugins make it easy to implement arbitrarily advanced workflows and tools like linters, asset generators and function pre-processors.\n\n- Compose plugins that can inspect and edit the generated resource pack and data pack\n- Configure powerful build systems for development and creating releases\n- First-class template integration approachable without prior Python knowledge\n- Link the generated resource pack and data pack to Minecraft\n- Automatically rebuild the project on file changes with watch mode\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install beet\n```\n\nYou can make sure that `beet` was successfully installed by trying to use the toolchain from the command-line.\n\n```bash\n$ beet --help\nUsage: beet [OPTIONS] COMMAND [ARGS]...\n\n  The beet toolchain.\n\nOptions:\n  -d, --directory DIRECTORY  Use the specified project directory.\n  -c, --config FILE          Use the specified config file.\n  -v, --version              Show the version and exit.\n  -h, --help                 Show this message and exit.\n\nCommands:\n  build  Build the current project.\n  cache  Inspect or clear the cache.\n  link   Link the generated resource pack and data pack to Minecraft.\n  watch  Watch the project directory and build on file changes.\n```\n\n## Status\n\nYou can expect current releases to be pretty stable, but the project as a whole should still be considered alpha.\n\nThe main reason is that resource pack and data pack coverage is currently lacking in certain areas. Exposing a consistent interface for every data pack and resource pack feature can involve design decisions that aren\'t immediately obvious. You\'re welcome to open an issue to discuss the implementation of currently unsupported resources. And feel free to ask questions, report bugs, and share your thoughts and impressions.\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`. We use [`pytest-minecraft`](https://github.com/vberlier/pytest-minecraft) to run tests against actual Minecraft releases.\n\n```bash\n$ poetry run pytest\n$ poetry run pytest --minecraft-latest\n```\n\nWe also use [`pytest-insta`](https://github.com/vberlier/pytest-minecraft) for snapshot testing. Data pack and resource pack snapshots make it easy to monitor and review changes.\n\n```bash\n$ poetry run pytest --insta review\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort beet tests\n$ poetry run black beet tests\n$ poetry run black --check beet tests\n```\n\n---\n\nLicense - [MIT](https://github.com/mcbeet/beet/blob/main/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcbeet/beet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
