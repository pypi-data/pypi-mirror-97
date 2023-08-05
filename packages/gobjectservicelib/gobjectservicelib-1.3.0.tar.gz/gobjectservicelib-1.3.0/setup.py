# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gobjectservicelib']

package_data = \
{'': ['*']}

install_requires = \
['datastreamservicelib>=1.10,<2.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'gobjectservicelib',
    'version': '1.3.0',
    'description': 'GObject mainloop implementation of https://gitlab.com/advian-oss/python-datastreamservicelib',
    'long_description': '=================\ngobjectservicelib\n=================\n\nGObject mainloop enabled version of https://gitlab.com/advian-oss/python-datastreamservicelib\n(runs GObject mainloop in a thread, asyncio is still the main threads mainloop).\n\nNotable helpers\n---------------\n\nServiceWidgetBase/ServiceWindowBase (in widgets.py) and the aio decorator (in eventloop.py), the first should be used\nas baseclass for your own widgets/windows that need a reference to the main service and aio mainloop.\nThe latter is a decorator that can be applied to a method of subclass of ServiceWidgetBase to\nmake said method run in the aio mainloop.\n\nAnd of course the GObject mainloop enabled SimpleService which extends the one in datastreamservicelib\n\nDocker\n------\n\nThis depends on GObject libraries etc from the operating system level, easiest way\nto get hacking is to build the docker image and work inside it.\n\nSSH agent forwarding\n^^^^^^^^^^^^^^^^^^^^\n\nWe need buildkit_::\n\n    export DOCKER_BUILDKIT=1\n\n.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/\n\nAnd also the exact way for forwarding agent to running instance is different on OSX::\n\n    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"\n\nand Linux::\n\n    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"\n\n\nCreating the container\n^^^^^^^^^^^^^^^^^^^^^^\n\nMake sure you have defined DOCKER_DISPLAY above.\n\nBuild image, create container and start it::\n\n    docker build --ssh default --target devel_shell -t gobjectservicelib:devel_shell .\n    docker create --name gobjectservicelib_devel -v `pwd`":/app" -it  -v /tmp:/tmp `echo $DOCKER_SSHAGENT` gobjectservicelib:devel_shell\n    docker start -i gobjectservicelib_devel\n\nThis will give you a shell with system level dependencies installed, you should do any shell things (like\nrun tests, pre-commit checks etc) there.\n\n\npre-commit considerations\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nIf working in Docker instead of native env you need to run the pre-commit checks in docker too::\n\n    docker exec -i gobjectservicelib_devel /bin/bash -c "pre-commit install"\n    docker exec -i gobjectservicelib_devel /bin/bash -c "pre-commit run --all-files"\n\nYou need to have the container running, see above. Or alternatively use the docker run syntax but using\nthe running container is faster::\n\n    docker run --rm -v `pwd`":/app" gobjectservicelib:devel_shell -c "pre-commit run --all-files"\n\n\nTest suite\n^^^^^^^^^^\n\nYou can use the devel shell to run py.test when doing development, for CI use\nthe "test" target in the Dockerfile::\n\n    docker build --ssh default --target test -t gobjectservicelib:test .\n    docker run --rm -it -v `pwd`":/app" `echo $DOCKER_SSHAGENT` gobjectservicelib:test\n\n\nLocal Development\n-----------------\n\nTLDR:\n\n- Check dockerfile for system dependencies and adapt according to your env\n- Create and activate a Python 3.7 virtualenv (assuming virtualenvwrapper)::\n\n    mkvirtualenv -p `which python3.7` my_virtualenv\n\n- change to a branch::\n\n    git checkout -b my_branch\n\n- install Poetry: https://python-poetry.org/docs/#installation\n- Install project deps and pre-commit hooks::\n\n    poetry install\n    pre-commit install\n    pre-commit run --all-files\n\n- Ready to go.\n\nRemember to activate your virtualenv whenever working on the repo, this is needed\nbecause pylint and mypy pre-commit hooks use the "system" python for now (because reasons).\n',
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@advian.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/advian-oss/python-gobjectservicelib/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
