# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdbundle_debuginfod', 'gdbundle_debuginfod.scripts']

package_data = \
{'': ['*']}

install_requires = \
['pydebuginfod>=0.2.0,<0.3.0',
 'pyelftools>=0.27,<0.28',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'gdbundle-debuginfod',
    'version': '0.4.0',
    'description': 'GDB and LLDB plugins to enable older versions of GDB and LLDB to support debuginfod',
    'long_description': "# Debuginfod Plugins\n\n![PyPI](https://img.shields.io/pypi/v/gdbundle-debuginfod)\n![Build](https://github.com/schultetwin1/gdbundle-debuginfod/workflows/CI/badge.svg)\n\n\nThis repo contains both a GDB and LLDB plugin to support\n[debuginfod](https://www.mankier.com/8/debuginfod#) in the versions of GDB and\nLLDB which not do have debuginfod built in.\n\nWARNING: Currently these plugins only support downloading symbols/ These\nplugin **do not** support sources.\n\n## Supported Environments\n\nThis works in both LLDB and GDB. As of GDB 10.1, debuginfod support is built\ninto GDB and so this plugin is not needed.\n\n\n## Installation\n\nThese plugins can be installed in two different ways:\n\n* Using [gdbundle](https://github.com/memfault/gdbundle). A GDB/LLDB plugin\n  manager from [MemFault](https://interrupt.memfault.com/blog/gdbundle-plugin-manager). (Preferred method)\n\n* Manual\n\n### Using gdbundle\n\nFirst follow gdbundle's install [steps](https://github.com/memfault/gdbundle#quickstart).\n\nThen install the debuginfod plugins with the following command:\n\n```shell\npip install gdbundle-debuginfod-plugin\n```\n### Manual Install\n\nInstructions to come...\n\n## Usage\n\nOnce installed, you will have access to the `dbgd` command in both GDB and\nLLDB. Run `dbgd --help` to see the full list of commands. Normal usage will\nbe covered here.\n\nBy default, symbols will load automatically. :warning: This feature is not\nyet implemented on LLDB! :warning:\n\n### Load symbols manually\n\n```\ndebugger> dbgd symbols load\n```\n\n### Turn on / off auto loading of symbols\n\n```\ndebugger> dbgd symbols autoload on\ndebugger> dbgd symbols autoload off\n```\n\n### List loaded symbols\n\n```\ndebugger> dbgd symbols list\n```\n\n### List all debuginfod servers\n\n```\ndebugger> dbgd servers list\n```\n\n### Add a debuginfod server\n\n```\ndebugger> dbgd servers add [url]\n```\n\n### Remove a debuginfod server\n\n```\ndebugger> dbgd servers rm [index]\n```",
    'author': 'Matt Schulte',
    'author_email': 'schultetwin1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
