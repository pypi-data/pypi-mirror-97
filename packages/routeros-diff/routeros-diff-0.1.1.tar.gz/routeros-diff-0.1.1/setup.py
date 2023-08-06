# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routeros_diff', 'routeros_diff.commands']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['ros_diff = routeros_diff.commands.diff:run',
                     'ros_prettify = routeros_diff.commands.prettify:run',
                     'routeros_diff = routeros_diff.commands.diff:run',
                     'routeros_prettify = routeros_diff.commands.prettify:run']}

setup_kwargs = {
    'name': 'routeros-diff',
    'version': '0.1.1',
    'description': 'Tools for parsing & diffing RouterOS configuration files. Can produce config file patches.',
    'long_description': '# Diff and prettify RouterOS configuration files\n\n[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)\n[![Tests](https://github.com/gardunha/routeros-diff/actions/workflows/ci.yaml/badge.svg)](https://github.com/gardunha/routeros-diff/actions/workflows/ci.yaml)\n\n## Installation\n\nInstall using your favourite Python package manager. For example:\n\n    pip install routeros-diff\n\n## Get a diff\n\nThe `routeros_diff` (alias `ros_diff`) command will take two RouterOS files and diff them:\n\n    routeros_diff old_config.rsc new_config.rsc\n\nOr using Python:\n\n```python\nfrom routeros_diff.parser import RouterOSConfig\nold = RouterOSConfig.parse(old_config_string)\nnew = RouterOSConfig.parse(new_config_string)\nprint(old.diff(new))\n```\n\n## Examples:\n\nA simple example first:\n\n```r\n# Old:\n/routing ospf instance\nadd name=core router-id=100.127.0.1\n\n# New:\n/routing ospf instance\nadd name=core router-id=100.127.0.99\n\n# Diff:\n/routing ospf instance\nset [ find name=core ] router-id=100.127.0.99\n```\n\nHere is a more complex example where we use custom IDs in order to maintain \nexpression ordering (see \'Natural Keys & IDs\' below for details):\n\n```r\n# Old:\n/ip firewall nat \nadd chain=a comment="Example text [ ID:1 ]"\nadd chain=c comment="[ ID:3 ]"\n\n# New:\n/ip firewall nat \nadd chain=a comment="Example text [ ID:1 ]"\nadd chain=b comment="[ ID:2 ]"\nadd chain=c comment="[ ID:3 ]"\n\n# Diff:\n/ip firewall nat \nadd chain=b comment="[ ID:2 ]" place-before=[ find where comment~ID:3 ]\n```\n\n### Usage & limitations\n\nThis aim is for this diffing process to work well within a limited range of conditions.\nThe configuration format is an entire scripting language in itself, and so this library\ncannot sensibly hope to parse any arbitrary input. As a rule of thumb, this library should\nbe able to diff anything produced by `/export`.\n\n### Sections and expressions\n\nThe following is NOT supported:\n\n```r\n## NOT SUPPORTED, DONT DO THIS ##\n/routing ospf instance add name=core router-id=100.127.0.1\n```\n\nRather, this must be formatted as separate \'sections\' and \'expressions\' on different lines. For example:\n\n```r\n/routing ospf instance \nadd name=core router-id=100.127.0.1\n```\n\nThe section in this example is `/routing ospf instance`, and the expression is `add name=core router-id=100.127.0.1`.\nEach section may contain multiple expressions (just like the output you see from `/export`).\n\n### Natural Keys & IDs\n\nThe parser will try to uniquely identify each expression. This allows the parser to be intelligent regarding\nadditions, modifications, deletions, and ordering.\n\nThe parser refers to these unique identities as naturals keys & natural IDs. For example:\n\n```r\nadd name=core router-id=100.127.0.1\n```\n\nHere the natural key is `name` and the natural ID is `core`. The parser assumes `name` will be the natural key,\nbut is configured to use other keys in some situations (see `NATURAL_KEYS`).\n\nAdditionally, you can choose to manually add your own IDs to expressions. This is done using comments.\nFor example:\n\n```r\nadd chain=a comment="[ ID:1 ]"\n```\n\nThese comment-based IDs take priority over whatever the parser may have otherwise used.\nIf using comment IDs, you should make sure you set them for all expressions in\nthat section.\n\nThis is especially useful for firewall rules. The order of firewall rules is important, and they have no\nobvious natural keys/IDs. Using comments IDs for your firewall rules allows the parser to\nintelligently maintain order. For example:\n\n```r\n# Old:\n/ip firewall nat \nadd chain=a comment="Example text [ ID:1 ]"\nadd chain=c comment="[ ID:3 ]"\n\n# New:\n/ip firewall nat \nadd chain=a comment="Example text [ ID:1 ]"\nadd chain=b comment="[ ID:2 ]"\nadd chain=c comment="[ ID:3 ]"\n\n# Diff:\n/ip firewall nat \nadd chain=b comment="[ ID:2 ]" place-before=[ find where comment~ID:3 ]\n```\n\nNote that the parser uses `place-before` to correctly place the new firewall rule.\n\n*Without using comment IDs, the parse would have to drop and recreate all firewall rules.* This would\nbe non-ideal for reasons of both security and reliability.\n\n### Reporting errors\n\nSeeing something strange in your diff output? Please report the error with the following information:\n\n* The input\n* The actual output\n* What you think the output should be instead\n\nPlease minimise the size of this data as much as possible. The smaller and more specific the example of the problem,\nthe easier it will be for us to find a resolution.\n\n## Prettify\n\nThe `routeros_prettify` (alias `ros_prettify`) command will parse an existing configuration and re-print it in a\nstandard format with common sections collapsed:\n\n```r\nrouteros_prettify old_config.rsc new_config.rsc\n```\n\nOr using Python:\n\n```python\nfrom routeros_diff.parser import RouterOSConfig\nconfig = RouterOSConfig.parse(config_string)\nprint(config)\n```\n\n## Concepts\n\nThis is a **section** with a path of `/ip address` and two expressions:\n\n```r\n/ip address\nadd address=1.2.3.4\nadd address=5.6.7.8\n```\n\nThis is an **expression** with a command of **add**, and a key-value argument of `address=1.2.3.4`:\n\n```r\nadd address=1.2.3.4\n```\n\n# Release process:\n\n```bash\nexport VERSION=a.b.c\n\npoetry version $VERSION\ndephell convert\nblack setup.py\n\ngit add .\ngit commit -m "Releasing version $VERSION"\n\ngit tag "v$VERSION"\ngit branch "v$VERSION"\ngit push origin \\\n    refs/tags/"v$VERSION" \\\n    refs/heads/"v$VERSION" \\\n    main\n\n# Wait for CI to pass\n\npoetry publish --build\n```\n',
    'author': 'Adam Charnock',
    'author_email': 'adam.charnock@gardunha.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gardunha/routeros-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
