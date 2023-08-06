# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycognitocli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0', 'libadvian>=0.2,<0.3', 'pycognito>=2021.3,<2022.0']

entry_points = \
{'console_scripts': ['pycognitocli = pycognitocli.console:pycognitocli_cli']}

setup_kwargs = {
    'name': 'pycognitocli',
    'version': '0.2.0',
    'description': 'CLI for https://pypi.org/project/pycognito/',
    'long_description': '============\npycognitocli\n============\n\nCLI for https://pypi.org/project/pycognito/\n\nTry::\n\n    pycognitocli -p "region_mypool" -a "myappid" -cs "myappsecret" token get -u "username" -pw \'password\'\n\nOr export following environment variables:\n\n  - COGNITO_POOL_ID\n  - COGNITO_APP_ID\n  - COGNITO_APP_SECRET\n  - COGNITO_USERNAME\n  - COGNITO_PASSWORD\n\nYou do not have to give the password (or username) on command-line, the app can prompt for it\n\nDocker\n------\n\nFor more controlled deployments and to get rid of "works on my computer" -syndrome, we always\nmake sure our software works under docker.\n\nIt\'s also a quick way to get started with a standard development environment.\n\nSSH agent forwarding\n^^^^^^^^^^^^^^^^^^^^\n\nWe need buildkit_::\n\n    export DOCKER_BUILDKIT=1\n\n.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/\n\nAnd also the exact way for forwarding agent to running instance is different on OSX::\n\n    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"\n\nand Linux::\n\n    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"\n\nCreating a development container\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nBuild image, create container and start it (switch the 1234 port to the port from src/pycognitocli/defaultconfig.py)::\n\n    docker build --ssh default --target devel_shell -t pycognitocli:devel_shell .\n    docker create --name pycognitocli_devel -v `pwd`":/app" -it `echo $DOCKER_SSHAGENT` pycognitocli:devel_shell\n    docker start -i pycognitocli_devel\n\npre-commit considerations\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nIf working in Docker instead of native env you need to run the pre-commit checks in docker too::\n\n    docker exec -i pycognitocli_devel /bin/bash -c "pre-commit install"\n    docker exec -i pycognitocli_devel /bin/bash -c "pre-commit run --all-files"\n\nYou need to have the container running, see above. Or alternatively use the docker run syntax but using\nthe running container is faster::\n\n    docker run -it --rm -v `pwd`":/app" pycognitocli:devel_shell -c "pre-commit run --all-files"\n\nTest suite\n^^^^^^^^^^\n\nYou can use the devel shell to run py.test when doing development, for CI use\nthe "tox" target in the Dockerfile::\n\n    docker build --ssh default --target tox -t pycognitocli:tox .\n    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` pycognitocli:tox\n\nProduction docker\n^^^^^^^^^^^^^^^^^\n\nThere\'s a "production" target as well for running the application (change the "1234" port and "myconfig.toml" for\nconfig file)::\n\n    docker build --ssh default --target production -t pycognitocli:latest .\n    docker run -it --rm pycognitocli:latest pycognitocli -p "region_mypool" -a "myappid" -cs "myappsecret" token get -u "username" -pw \'password\'\n\n\nLocal Development\n-----------------\n\nTLDR:\n\n- Create and activate a Python 3.8 virtualenv (assuming virtualenvwrapper)::\n\n    mkvirtualenv -p `which python3.8` my_virtualenv\n\n- change to a branch::\n\n    git checkout -b my_branch\n\n- install Poetry: https://python-poetry.org/docs/#installation\n- Install project deps and pre-commit hooks::\n\n    poetry install\n    pre-commit install\n    pre-commit run --all-files\n\n- Ready to go, try the following::\n\n    pycognitocli --defaultconfig >config.toml\n    pycognitocli -vv config.toml\n\nRemember to activate your virtualenv whenever working on the repo, this is needed\nbecause pylint and mypy pre-commit hooks use the "system" python for now (because reasons).\n\nRunning "pre-commit run --all-files" and "py.test -v" regularly during development and\nespecially before committing will save you some headache.\n',
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@advian.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/advian-oss/python-pycognitocli/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
