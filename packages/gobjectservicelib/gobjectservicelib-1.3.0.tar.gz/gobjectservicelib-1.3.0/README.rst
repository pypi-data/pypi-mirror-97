=================
gobjectservicelib
=================

GObject mainloop enabled version of https://gitlab.com/advian-oss/python-datastreamservicelib
(runs GObject mainloop in a thread, asyncio is still the main threads mainloop).

Notable helpers
---------------

ServiceWidgetBase/ServiceWindowBase (in widgets.py) and the aio decorator (in eventloop.py), the first should be used
as baseclass for your own widgets/windows that need a reference to the main service and aio mainloop.
The latter is a decorator that can be applied to a method of subclass of ServiceWidgetBase to
make said method run in the aio mainloop.

And of course the GObject mainloop enabled SimpleService which extends the one in datastreamservicelib

Docker
------

This depends on GObject libraries etc from the operating system level, easiest way
to get hacking is to build the docker image and work inside it.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"


Creating the container
^^^^^^^^^^^^^^^^^^^^^^

Make sure you have defined DOCKER_DISPLAY above.

Build image, create container and start it::

    docker build --ssh default --target devel_shell -t gobjectservicelib:devel_shell .
    docker create --name gobjectservicelib_devel -v `pwd`":/app" -it  -v /tmp:/tmp `echo $DOCKER_SSHAGENT` gobjectservicelib:devel_shell
    docker start -i gobjectservicelib_devel

This will give you a shell with system level dependencies installed, you should do any shell things (like
run tests, pre-commit checks etc) there.


pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i gobjectservicelib_devel /bin/bash -c "pre-commit install"
    docker exec -i gobjectservicelib_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run --rm -v `pwd`":/app" gobjectservicelib:devel_shell -c "pre-commit run --all-files"


Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "test" target in the Dockerfile::

    docker build --ssh default --target test -t gobjectservicelib:test .
    docker run --rm -it -v `pwd`":/app" `echo $DOCKER_SSHAGENT` gobjectservicelib:test


Local Development
-----------------

TLDR:

- Check dockerfile for system dependencies and adapt according to your env
- Create and activate a Python 3.7 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.7` my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install
    pre-commit run --all-files

- Ready to go.

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).
