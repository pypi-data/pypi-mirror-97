# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tartufo', 'tartufo.commands']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=2.1.1,<4.0.0',
 'click>=7,<8',
 'toml>=0.10,<0.11',
 'truffleHogRegexes>=0.0.7,<0.0.8']

extras_require = \
{':python_version < "3.7"': ['dataclasses'],
 ':sys_platform == "win32"': ['colorama'],
 'docs': ['recommonmark>=0.6,<0.7',
          'sphinx>=3.2,<4.0',
          'sphinx-click>=2.5.0,<3.0.0',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'sphinxcontrib-spelling>=5.4.0,<6.0.0']}

entry_points = \
{'console_scripts': ['tartufo = tartufo.cli:main']}

setup_kwargs = {
    'name': 'tartufo',
    'version': '2.4.0',
    'description': 'tartufo is a tool for scanning git repositories for secrets/passwords/high-entropy data',
    'long_description': "# ![tartufo logo](docs/source/_static/img/tartufo.png)\n\n[![Join Slack](https://img.shields.io/badge/Join%20us%20on-Slack-e01563.svg)](https://www.godaddy.com/engineering/slack/)\n[![ci](https://github.com/godaddy/tartufo/workflows/ci/badge.svg)](https://github.com/godaddy/tartufo/actions?query=workflow%3Aci)\n[![Codecov](https://img.shields.io/codecov/c/github/godaddy/tartufo)](https://codecov.io/gh/godaddy/tartufo)\n[![PyPI](https://img.shields.io/pypi/v/tartufo)](https://pypi.org/project/tartufo/)\n[![PyPI - Status](https://img.shields.io/pypi/status/tartufo)](https://pypi.org/project/tartufo/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tartufo)](https://pypi.org/project/tartufo/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/tartufo)](https://pypi.org/project/tartufo/)\n[![Documentation Status](https://readthedocs.org/projects/tartufo/badge/?version=latest)](https://tartufo.readthedocs.io/en/latest/?badge=latest)\n[![License](https://img.shields.io/github/license/godaddy/tartufo)](https://github.com/godaddy/tartufo/blob/main/LICENSE)\n\n`tartufo` searches through git repositories for secrets, digging deep into\ncommit history and branches. This is effective at finding secrets accidentally\ncommitted. `tartufo` also can be used by git pre-commit scripts to screen\nchanges for secrets before they are committed to the repository.\n\nThis tool will go through the entire commit history of each branch, and check\neach diff from each commit, and check for secrets. This is both by regex and by\nentropy. For entropy checks, tartufo will evaluate the shannon entropy for both\nthe base64 char set and hexidecimal char set for every blob of text greater\nthan 20 characters comprised of those character sets in each diff. If at any\npoint a high entropy string > 20 characters is detected, it will print to the\nscreen.\n\n## Example\n\n![Example Issue](docs/source/_static/img/example_issue.png)\n\n## Documentation\n\nOur main documentation site is hosted by Read The Docs, at\n<https://tartufo.readthedocs.io>.\n\n## Usage\n\n```bash\nUsage: tartufo [OPTIONS] COMMAND [ARGS]...\n\n  Find secrets hidden in the depths of git.\n\n  Tartufo will, by default, scan the entire history of a git repository for\n  any text which looks like a secret, password, credential, etc. It can also\n  be made to work in pre-commit mode, for scanning blobs of text as a pre-\n  commit hook.\n\nOptions:\n  --json / --no-json              Output in JSON format.\n  --rules FILENAME                Path(s) to regex rules json list file(s).\n  --default-regexes / --no-default-regexes\n                                  Whether to include the default regex list\n                                  when configuring search patterns. Only\n                                  applicable if --rules is also specified.\n                                  [default: True]\n\n  --entropy / --no-entropy        Enable entropy checks.  [default: True]\n  --regex / --no-regex            Enable high signal regexes checks.\n                                  [default: False]\n\n  -i, --include-paths FILENAME    File with regular expressions (one per\n                                  line), at least one of which must match a\n                                  Git object path in order for it to be\n                                  scanned; lines starting with '#' are treated\n                                  as comments and are ignored. If empty or not\n                                  provided (default), all Git object paths are\n                                  included unless otherwise excluded via the\n                                  --exclude-paths option.\n\n  -x, --exclude-paths FILENAME    File with regular expressions (one per\n                                  line), none of which may match a Git object\n                                  path in order for it to be scanned; lines\n                                  starting with '#' are treated as comments\n                                  and are ignored. If empty or not provided\n                                  (default), no Git object paths are excluded\n                                  unless effectively excluded via the\n                                  --include-paths option.\n\n  -e, --exclude-signatures TEXT   Specify signatures of matches that you\n                                  explicitly want to exclude from the scan,\n                                  and mark as okay. These signatures are\n                                  generated during the scan process, and\n                                  reported out with each individual match.\n                                  This option can be specified multiple times,\n                                  to exclude as many signatures as you would\n                                  like.\n\n  -od, --output-dir DIRECTORY     If specified, all issues will be written out\n                                  as individual JSON files to a uniquely named\n                                  directory under this one. This will help\n                                  with keeping the results of individual runs\n                                  of tartufo separated.\n\n  --git-rules-repo TEXT           A file path, or git URL, pointing to a git\n                                  repository containing regex rules to be used\n                                  for scanning. By default, all .json files\n                                  will be loaded from the root of that\n                                  repository. --git-rules-files can be used to\n                                  override this behavior and load specific\n                                  files.\n\n  --git-rules-files TEXT          Used in conjunction with --git-rules-repo,\n                                  specify glob-style patterns for files from\n                                  which to load the regex rules. Can be\n                                  specified multiple times.\n\n  --config FILE                   Read configuration from specified file.\n                                  [default: pyproject.toml]\n\n  -V, --version                   Show the version and exit.\n  -h, --help                      Show this message and exit.\n\nCommands:\n  pre-commit        Scan staged changes in a pre-commit hook.\n  scan-remote-repo  Automatically clone and scan a remote git repository.\n  scan-local-repo   Scan a repository already cloned to your local system.\n\n```\n\n## Contributing\n\nAll contributors and contributions are welcome! Please see [our contributing\ndocs] for more information.\n\n## Attributions\n\nThis project was inspired by and built off of the work done by Dylan Ayrey on\nthe [truffleHog] project.\n\n[our contributing docs]: https://tartufo.readthedocs.io/en/latest/CONTRIBUTING.html\n[pre-commit]: https://pre-commit.com/\n[truffleHog]: https://github.com/dxa4481/truffleHog\n",
    'author': 'Dylan Ayrey',
    'author_email': 'dxa4481@rit.edu',
    'maintainer': 'GoDaddy',
    'maintainer_email': 'oss@godaddy.com',
    'url': 'https://github.com/godaddy/tartufo/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
