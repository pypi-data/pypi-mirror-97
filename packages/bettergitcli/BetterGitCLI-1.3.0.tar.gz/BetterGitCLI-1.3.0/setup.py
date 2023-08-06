# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['better_git_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub', 'PyInquirer', 'colorama']

entry_points = \
{'console_scripts': ['bettergitcli = better_git_cli.main:cli_main']}

setup_kwargs = {
    'name': 'bettergitcli',
    'version': '1.3.0',
    'description': 'GitHub CLI with intuitive UI and keyboard controls!',
    'long_description': '![BannerImg](https://user-images.githubusercontent.com/43642399/108777456-bab79800-755b-11eb-8325-7904e0face0f.png)\n\n<p align="center">\n    <a href="https://github.com/PiotrRut/BetterGitCLI/actions/workflows/codeql-analysis.yml">\n        <img src="https://github.com/PiotrRut/BetterGitCLI/actions/workflows/codeql-analysis.yml/badge.svg" />\n    </a>\n    <img src="https://travis-ci.com/PiotrRut/BetterGitCLI.svg?token=WYp4pRfPB9puZwpAYdtc&branch=master" />\n    <img src="https://img.shields.io/badge/python-3.6%20%2B-blue">\n    <a href="https://pypi.org/project/bettergitcli/">\n      <img src="https://img.shields.io/pypi/v/bettergitcli">\n    </a>\n</p>\n\n> Disclaimer: BetterGitCLI is **not** official GitHub software, nor is it in any way affiliated with GitHub.\n\nBetterGitCli is a third party GitHub CLI made with Python, providing easier access to managing your\nGitHub account directly from your shell with simple and intuitive UI. It\'s based on [PyGithub](https://pypi.org/project/PyGithub/) which is a wrapper library around the official GitHub REST API.\n\n## Configuration\n\nSee below for instructions on how to configure BetterGitCLI. Note that Python 3.6 or higher is required to run this program.\n\n### GitHub access\n\nIn order to gain access to your GitHub account you will need to authenticate with your GitHub access token. You can find instructions\non how to obtain it [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).\n\nYour token must grant access to _"repo"_, _"user"_, _"delete_repo"_ and _"admin:public_key"_. After generating\nyour token, export it as an environmental variable in your shell 👇🏻\n\n```bash\n# bash / zsh\n$ export GITHUB_AUTH_TOKEN=<token>\n\n# powershell\n$env:GITHUB_AUTH_TOKEN = "token"\n```\n\n🚨 BetterGitCLI will never store your access token, and it will *only be stored locally* on your machine.\n\n### Installation\nYou can either install this program using [pip](https://pip.pypa.io/en/stable/installing/) or [pipenv](https://pipenv.pypa.io/en/latest/), or clone it and run locally with Python. Click on one of the\noptions down below to reveal the instructions 👇🏻\n\n<details open>\n  <summary><i><b>Install package with pip (preferred)</b></i></summary>\n  <p>\n\n  Install BetterGitCLI using this command:\n\n  ```bash\n  $ pip install bettergitcli\n  ```\n\n  After installation, you can run it from anywhere in your shell 🎉\n\n  ```bash\n  $ bettergitcli\n  ```\n\n  </p>\n</details>\n\n<details>\n  <summary><i><b>Clone and run locally with Python</b></i></summary>\n  <p>\n\n  If you prefer to clone this repository and run BetterGitCLI locally using your Python interpreter, you can\n  do that as well. Just remember that in this case you will have to install these dependencies manually:\n\n  - *PyInquirer, PyGithub, colorama*\n\n  This can be done easily using the provided `requirements.txt` file by running this in the project root:\n  ```bash\n  $ pip install -r requirements.txt\n  ```\n\n  After installation, run the program inside the `/better_git_cli` directory:\n\n  ```bash\n  $ python main.py\n  ```\n\n  </p>\n</details>\n\n\n## Usage\nTo navigate the UI, use your arrow keys (up and down) and select options\nusing <kbd>Enter</kbd>. You can also exit the program at any time by using the <kbd>^C</kbd> (<kbd>Ctrl+C</kbd>) combination,\nor by choosing the _"Exit to shell"_ option.\n\nVia the UI, you can view all your repositories, manage branches and deployments, manage your\npersonal user details and much more! **Current functions include**:\n\n- Repository management\n    - View and edit repository details, such as the description, default branches, visibility and more!\n    - Delete repositories\n    - Create a new repository\n- User management\n    - View and edit your personal details like your name, location or bio\n- SSH keys management\n    - View, create and delete SSH keys linked to your GitHub account\n- Language statistics\n  - See what your top languages are\n\n\n## Changelog\nYou can view the changelog [here](https://github.com/PiotrRut/BetterGitCLI/blob/master/CHANGELOG.md).\n\n## Contributing\nAll contributions to add new features, fix any bugs (if you spot any) or make the code better or more efficient\nare more than welcome - please feel free to raise an [issue](https://github.com/PiotrRut/BetterGitCLI/issues/new) or open up a pull request 💫\n',
    'author': 'Piotr Rutkowski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PiotrRut/BetterGitCLI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
