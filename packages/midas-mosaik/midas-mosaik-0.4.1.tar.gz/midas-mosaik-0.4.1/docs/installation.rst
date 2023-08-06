Installation
============

This guide describes how to install *midas* on :ref:`linux`,
:ref:`os-x`, and :ref:`windows`. 

.. _linux:

Linux
-----

This guide is based on *Manjaro 20.1.1 Mikah, 64bit*, but this should
for work for other distributions as well.

The *midas* package requires `Python`__ >= 3.6. We recommend to use 
a `virtualenv`__ to avoid messing up your system environment. Use 
your distributions' package manager to install pip and virtualenv.

.. code-block:: bash

    $ virtualenv ~/.virtualenvs/midas 
    $ source ~/.virtualenv/midas/bin/activate

If your distribution still relies on Python 2.x, make sure that you
actually create a virtualenv environment for Python 3.

.. code-block:: bash

    $ virtualenv -p /usr/bin/python3 ~/.virtualenvs/midas
    $ source ~/.virtualenv/midas/bin/activate

Now you can install *midas* from the pypi package repository

.. code-block:: bash

    (midas) $ pip install midas  # TODO insert pypi name
    
or from the source code.

.. code-block:: bash

    (midas) $ pip install git+https://gitlab.com/midas-mosaik/midas.git

Finally, you can test your installation by typing:

.. code-block:: bash

    (midas) $ midascli --help 

into the console, which should print information about the command line 
tool of *midas*.

__ https://www.python.org/
__ https://virtualenv.readthedocs.org

.. _os-x:

OS-X
----

10.15 Catalina
(Coming soon)

.. _windows:

Windows
-------

(Coming soon)

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned