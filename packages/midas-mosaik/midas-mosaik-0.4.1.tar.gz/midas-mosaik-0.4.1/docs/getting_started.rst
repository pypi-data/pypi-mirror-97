Getting started
===============

This guide describes how to use *midas* to run some simple simulations.

Prerequisites
-------------

It is assumed that you have already followed the instructions of the
:doc:`Installation <installation>` guide.

First start
-----------

Read this section carefully, before you type any command. 
On the first start of *midas*, a short configuration routine is 
triggered. *midas* will create an .ini file to store basic 
configurations. *midas* will ask for permission to create a folder
in your home directory to store the midas.ini file. If you do not
want to create such a folder, the midas.ini file will be created
in the current directory. If you start *midas* again from another
location, the configuration routine will be triggered again unless
you move the previously created .ini file to the new location as well.

In the next (and last interactive step) of the configuration, *midas*
asks where the datasets should be stored. The default location is,
again, the midas folder in your home directory, but you can specify
any other folder you like. The recommend way is, of course, to use
the folder in your home directory.

Now type into your console:

.. code-block:: bash

    (midas) $ midascli

If you want to use the recommended configuration, just hit enter
for both prompts. If you do so, the program will start downloading
the datasets.

Running a simple scenario
-------------------------

If you selected the default answers for both prompts, the program
is probably still downloading the data or running the simulation.
If not, you should have a look at the created .ini file, use the 
console again, and type:

.. code-block:: bash

    (midas) $ midascli -d

This will do two things: First, *midas* checks if the data sets are
available in the folder specified during the setup. If that is not 
the case, the data sets will be downloaded into that folder.

Secondly, the default scenario *midasmv* will be started, which 
consists of a CIGRE medium voltage grid and household data attached
to it. Using the *-d* flag, all data will be pushed into a mosaik-hdf5
database. 

Congratulations! You have successfully run a co-simulation with 
*midas*.