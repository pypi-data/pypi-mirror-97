# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['junction',
 'junction.confluence',
 'junction.confluence.api',
 'junction.confluence.models',
 'junction.git',
 'junction.markdown']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.3.2,<0.4.0',
 'click>=7.0,<8.0',
 'colorama>=0.4.3,<0.5.0',
 'gitpython>=3.0.5,<4.0.0',
 'markdown-emdash>=0.1.0,<0.2.0',
 'markdown-urlize>=0.2.0,<0.3.0',
 'markdown>=3.0.1,<4.0.0',
 'markdownsubscript>=2.1.1,<3.0.0',
 'markdownsuperscript>=2.1.1,<3.0.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['junction = junction.cli:main']}

setup_kwargs = {
    'name': 'confluence-junction',
    'version': '0.1.1',
    'description': 'Publish to and manage Confluence spaces with markdown files tracked in Git.',
    'long_description': '![Junction, publish and manage Confluence with git workflows](https://github.com/HUU/Junction/raw/master/docs/logo.png?raw=true)\n\nWith Junction you can write and manage your documentation directly in your codebase, using Markdown and your existing Git workflows (pull requests, code review, release branches, etc) and then automatically publish your changes to Confluence.  This gives you the best of both worlds: in-repo documentation that fits natively into your development workflows, with the discoverability and centrality of Confluence.\n\n![MIT License](https://img.shields.io/badge/license-MIT-green) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue)](https://pypi.org/project/confluence-junction) ![Build and Test](https://github.com/HUU/Junction/workflows/Build%20and%20Test/badge.svg)\n\n# Install\n\nEnsure you are using Python 3.8 (or newer); Junction does not work with older versions of Python.  Install using `pip`:\n```sh\npip install confluence-junction\n```\nThis will install the library and CLI.\nIn your Python code:\n```python\nimport junction\n```\nIn your shell:\n```sh\njunction --help\n```\n\n# Overview\n\nJunction works by inspecting the changes made on a commit-by-commit basis to your Git repository, and determining what needs to be changed in Confluence to reflect those changes.  Junction (currently) expects to manage the entire [space in Confluence](https://confluence.atlassian.com/doc/spaces-139459.html).  Thus when using Junction you must tell it which Space to target and update.  You must not manually change, create, or modify pages in the target space, or else Junction may be unable to synchronize the state in Git with the state in Confluence.\n\nTo allow mixing code (and other items) with markdown files for Junction in a single repository, you can tell Junction a subpath within your repository that functions as the root e.g. all markdown files will be kept in `docs/`.  All files should end with the `.md` extension.\n\nThe page will gets its title from the file name, and its contents will be translated into Confluence markup.  See [this example for what output looks like in Confluence](#output-example).\n\n# Usage\n\nCollect a set of credentials that Junction will use to login to Confluence.  You will need to create an [API token](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) to use instead of a password.  **I recommend you make a dedicated user account with access permissions limited to the space(s) you want to manage with Junction**.\n\nIn your git repository, create a folder structure and markdown files you would like to publish.  Commit those changes.\n```\n.\n├── (your code and other files)\n└── docs/\n    ├── Welcome.md\n    ├── Installation.md\n    └── Advanced Usage\n    |   ├── Airflow.md\n    |   ├── Visual Studio Online.md\n    |   ├── Atlassian Bamboo.md\n    |   └── GitHub Actions.md\n    └── Credits.md\n```\n\nJunction is designed as a library, and also provides "helpers" that make using it in different contexts easy (in particularly, as part of automated workflows e.g. in post-push builds).\n\nThe simplest way to use Junction is the included CLI `junction`:\n```sh\njunction -s "SPACE_KEY" -c "https://jihugh.atlassian.net/wiki/rest/api" -u "account@email.com" -p "YOUR_API_ACCESS_TOKEN" delta --content-path docs/ HEAD~5 master\n```\n> You can put the API, user, and key into environment variables to avoid specifying them for every invocation of Junction.  The variables are `CONFLUENCE_API`, `CONFLUENCE_API_USER`, and `CONFLUENCE_API_KEY` respectively.\n\nThe CLI is fully documented, so make use of the `--help` option to navigate all of the configuration options.\n\n### Dry Run\n\nYou can check what the `junction` CLI will do to your space without actually uploading the changes to Confluence by using the `--dry-run` flag.\n\n![Dry run example output](https://github.com/HUU/Junction/raw/master/docs/dry_run_example.gif?raw=true)\n\n### Python Library\n\nUsing the Python library will let you create your own wrappers and tools, for example an AirFlow DAG.  Here is an equivalent of the above CLI usage in Python:\n\n```python\nfrom pathlib import Path\nfrom git import Repo\nfrom junction.git import find_commits_on_branch_after, filter_modifications_to_folder, get_modifications\nfrom junction.delta import Delta\nfrom junction.confluence import Confluence\n\ncf = Confluence("https://jihugh.atlassian.net/wiki/rest/api", "account@email.com", "YOUR_API_ACCESS_TOKEN", "SPACE_KEY")\nrepo = Repo("."). # current working directory must be the root of the Git repository for this to work\n\ncommits = find_commits_on_branch_after("master", "HEAD~5", repo)\ndeltas = [Delta.from_modifications(filter_modifications_to_folder(get_modification(commit), Path("docs/"))) for commit in commits]\n\nfor delta in deltas:\n    delta.execute(cf)\n```\n\n# Output Example\n\nThe following markdown sample, stored in `Sample.md`, produces a page in Confluence that looks like [this](https://github.com/HUU/Junction/blob/master/docs/example_output.png?raw=true).  This shows all of the major supported features and markup.  It is intentionally very similar to GitHub-style markdown, with some extensions and differences to account for Confluence-specific features.\n\n    # Text\n\n    It\'s very easy to make some words **bold** and other words *italic* with Markdown. You can even [link to Google!](http://google.com).\n    Even some fancy formats like Subscripts~with tilde~ and Superscripts^with caret^.\n\n    # Lists\n\n    Sometimes you want numbered lists:\n\n    1. One\n    2. Two\n    3. Three\n\n    Sometimes you want bullet points:\n\n    * Start a line with a star\n    * Profit!\n\n    Alternatively,\n\n    - Dashes work just as well\n    - And if you have sub points, put four spaces before the dash or star:\n        - Like this\n        - And this\n\n    # Headers\n\n    Sometimes it\'s useful to have different levels of headings to structure your documents. Start lines with a `#` to create headings. Multiple `##` in a row denote smaller heading sizes.\n\n    ### This is a third-tier heading\n\n    You can use one `#` all the way up to `######` six for different heading sizes.\n\n    # Blockquotes\n\n    If you\'d like to quote someone, use the > character before the line:\n\n    > Coffee. The finest organic suspension ever devised... I beat the Borg with it.\n    > - Captain Janeway\n\n    # Code\n\n    You can embed `inline code fragments` by surrounding it in backticks.  For longer blocks of\n    code, use "code fencing":\n\n    ```\n    if (isAwesome){\n      return true\n    }\n    ```\n\n    And if you\'d like to use syntax highlighting, include the language:\n\n    ```php\n    <?php\n        echo "Hello World"\n    ?>\n    ```\n\n    # Tables\n\n    You can create tables by assembling a list of words and dividing them with hyphens `-` (for the first row), and then separating each column with a pipe `|`:\n\n    First Header | Second Header\n    ------------ | -------------\n    Content from cell 1 | Content from cell 2\n    Content in the first column | Content in the second column\n\n    # Confluence-specific Elements\n\n    You can link to other wiki pages by referencing their page titles.  Use normal link syntax, but prepend a `&` like &[this](Page Title).\n\n    ## Supported Macros\n\n    You can embed the Confluence child pages macro by placing it on its own line:\n\n    :include-children:\n\n    ...or the table of contents macro:\n\n    :include-toc:\n\n    ## Status Blocks\n\n    You can create Confluence status macros (colored pills), including in the middle of the line &status-green:like this;\n\n    &status-green:Complete; &status-yellow:In Progress; &status-grey:Planning; &status-red:Failed; &status-blue:Unknown; &status-purple:Cancelled;\n\n    ## Info Panels\n\n    Info: You can create info panels by prepending a paragraph with one of `Info:`, `Warning:`, `Error:`, or `Success:`.\n\n    Warning: The prefix will be removed from the contents.\n\n    Error: You cannot put multiple paragraphs inside an info panel, just a single block of text\n    like this.\n\n    Success: like other block elements, each info panel must be located on its own line (fenced between two new lines).\n\n# Contributing\n\nThis is a hobby project of mine, and I may not be able to work on it immediately upon request.   If you are interested in contributing, feel free to open a PR by following [the contribution guidelines](https://github.com/HUU/Junction/blob/master/CONTRIBUTING.md).\n',
    'author': 'HUU',
    'author_email': 'readabook123@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HUU/Junction',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
