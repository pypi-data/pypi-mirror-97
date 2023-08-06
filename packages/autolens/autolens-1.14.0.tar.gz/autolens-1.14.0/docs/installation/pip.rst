.. _pip:

Installation with pip
=====================

We strongly recommend that you install **PyAutoLens** in a
`Python virtual environment <https://www.geeksforgeeks.org/python-virtual-environment/>`_, with the link attached
describing what a virtual environment is and how to create one.

**PyAutoLens** is installed via pip as follows (note that we first upgrade pip to ensure certain libraries install):

.. code-block:: bash

    pip install --upgrade pip
    pip install autolens

If this raises no errors **PyAutoLens** is installed! If there is an error check out
the `troubleshooting section <https://pyautolens.readthedocs.io/en/latest/installation/troubleshooting.html>`_.

Next, clone the ``autolens workspace`` (the line ``--depth 1`` clones only the most recent branch on
the ``autolens_workspace``, reducing the download size):

.. code-block:: bash

   cd /path/on/your/computer/you/want/to/put/the/autolens_workspace
   git clone https://github.com/Jammy2211/autolens_workspace --depth 1
   cd autolens_workspace

Run the ``welcome.py`` script to get started!

.. code-block:: bash

   python3 welcome.py