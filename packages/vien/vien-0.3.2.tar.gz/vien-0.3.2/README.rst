
`vien <https://github.com/rtmigo/vien#readme>`_
===================================================


.. image:: https://img.shields.io/badge/ready_for_use-maybe-orange.svg
   :target: #
   :alt: Generic badge


.. image:: https://img.shields.io/pypi/v/vien.svg
   :target: https://pypi.python.org/pypi/vien/
   :alt: PyPI version shields.io


.. image:: https://github.com/rtmigo/vien/workflows/unit%20test/badge.svg?branch=master
   :target: https://github.com/rtmigo/vien/actions
   :alt: Actions Status


.. image:: https://github.com/rtmigo/vien/workflows/pkg%20test/badge.svg?branch=master
   :target: https://github.com/rtmigo/vien/actions
   :alt: Actions Status


.. image:: https://img.shields.io/badge/OS-MacOS%20|%20Ubuntu-blue.svg
   :target: #
   :alt: Generic badge


.. image:: https://img.shields.io/badge/Python-3.7--3.9-blue.svg
   :target: #
   :alt: Generic badge


**VIEN** is a command-line tool for managing `Python Virtual Environments <https://docs.python.org/3/library/venv.html>`_.

It provides one-line shortcuts for:


* creating and deleting environments
* running commands inside environments
* switching between environments in bash shell

----

Switching between projects should be simple. Creating environments for the projects should be simple too.

Ideally it's a short command that I would type even half asleep.

Something like

.. code-block:: base

   $ vien create 
   $ vien shell

And not like

.. code-block:: base

   $ python3 -m venv ./where/to/put/this/.venv
   $ source /i/lost/that/.venv/bin/activate


.. raw:: html

   <details>
     <summary>Ready-made solutions did not help.</summary><br/>


   - [pipenv](https://pipenv.pypa.io/) kind of solved the problem, but brought new challenges unrelated to virtual environments
   - [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/) name is easier to copy-paste than to type. And its commands are too 

   </details>


So there is the ``vien``. A tool for a half asleep developer.

Install
=======


.. raw:: html

   <details>
     <summary>Get a working Python ≥3.7, pip3 and venv.</summary><br/>

   @ Ubuntu
   ```bash
   $ sudo apt install -y python3 python3-pip python3-venv
   ```

   @ macOS
   ```bash
   $ brew install python3
   ```
   Check it works
   ```bash
   $ python3 --version             # python shows its version
   $ python3 -m venv --help        # venv shows help message
   $ pip3 install --upgrade pip    # pip upgrades itself
   ```


   ----
   </details>


Then:

.. code-block:: bash

   $ pip3 install vien

Make sure it installed:

.. code-block:: bash

   $ vien      # shows help

Upgrade it later:

.. code-block:: bash

   $ pip3 install vien --upgrade

Use
===

Create a virtual environment
----------------------------

.. code-block:: bash

   $ cd /path/to/myProject
   $ vien create

By default ``vien`` will try to use ``python3`` as the interpreter for the virtual environment.


.. raw:: html

   <details>
     <summary>If you have 
   more than one Python version, provide one more argument.</summary><br/>
   Point to the proper interpreter the way you execute it.

   If you execute scripts like that

   ```bash
   $ python3.8 /path/to/script.py
   ```

   Create virtual environment like that:

   ```bash
   $ vien create python3.8
   ```

   Or provide full path to the interpreter:

   ```bash
   $ vien create /usr/local/opt/python@3.8/bin/python3
   ```
   </details>


Dive into interactive bash
--------------------------

.. code-block:: bash

   $ cd /path/to/myProject
   $ vien shell

   (myProject)$ _

Now you are inside the virtual environment.

.. code-block:: bash

   (myProject)$ which python3             # now we are using separate copy of Python
   (myProject)$ echo $PATH                # everything is slightly different

   (myProject)$ pip3 install requests     # installs packages into virtual environment
   (myProject)$ python3 use_requests.py   # runs inside the virtual environment

Get out of the virtual environment:

.. code-block:: bash

   (myProject)$ exit

   $ _

Now you're back.

Run a script inside the virtual environment
-------------------------------------------

It is ``vien run <any bash command>``

.. code-block:: bash

   $ cd /path/to/myProject
   $ vien run python3 use_requests.py arg1 arg2  # runs in virtual environment
   $ vien run pip3 install requests              # installs packages into virtual environment


.. raw:: html

   <details>
     <summary>is an equivalent to</summary><br/>

   ```bash         
   $ cd /path/to/myProject

   $ source /path/to/the/venv/bin/activate
   $ python3 use_requests.py arg1 arg2
   $ /path/to/the/venv/bin/deactivate

   $ source /path/to/the/venv/bin/activate
   $ pip3 install requests
   $ /path/to/the/venv/bin/deactivate
   ```
   </details>


Where are those virtual environments
====================================

``vien`` offers a simple rule of where to keep the environments.

.. list-table::
   :header-rows: 1

   * - project dir
     - virtual environment dir
   * - ``/abc/thisProject``
     - ``$HOME/.vien/thisProject_venv``
   * - ``/abc/otherProject``
     - ``$HOME/.vien/otherProject_venv``
   * - ``/moved/to/otherProject``
     - ``$HOME/.vien/otherProject_venv``


So only the local name of the project directory matters. And all the virtual environments 
are in ``$HOME/.vien``. 

If you're not happy with the default, you can set the environment variable ``VIENDIR``\ :

.. code-block:: bash

   $ export VIENDIR="/x/y/z"

So for the project ``aaa`` the virtual environment will be located in ``/x/y/z/aaa_venv``.

The ``_venv`` suffix tells the utility that this directory can be safely removed.

Other commands
==============

Delete virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   $ cd /path/to/myProject
   $ vien delete

Delete old and create new virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Useful, when you want to start from scratch.

.. code-block:: bash

   $ cd /path/to/myProject
   $ vien recreate

Or upgrade it from an old Python to a new one:

.. code-block:: bash

   $ cd /path/to/myProject
   $ vien recreate /usr/local/opt/python@3.10/bin/python3

Shell prompt
============

By default the ``vien shell`` adds a prefix to the `\ ``$PS1`` <https://wiki.archlinux.org/index.php/Bash/Prompt_customization>`_ 
bash prompt.

.. code-block:: bash

   user@host$ cd /abc/myProject
   user@host$ vien shell

   (myProject)user@host$ _

So you can see, which virtual environment you're using.

If you customized your ``PS1``\ , it may not work as expected.  

.. code-block:: bash

   personalized:prompt> cd /abc/myProject
   personalized:prompt> vien shell

   (myProject)user@host$ _

It can be fixed by providing ``PS1`` variable to ``vien`` like that: 

.. code-block:: bash

   personalized:prompt> cd /abc/myProject
   personalized:prompt> PS1=$PS1 vien shell

   (myProject)personalized:prompt> _

To avoid doing this each time, ``export`` your ``PS1`` to make it available for subprocesses.
