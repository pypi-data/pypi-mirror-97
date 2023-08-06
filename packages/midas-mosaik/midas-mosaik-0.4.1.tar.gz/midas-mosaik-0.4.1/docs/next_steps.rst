Next steps
==========

In this part, you will learn about scenario configuration files and
the command line interface.

Scenario configuration
----------------------

If you have followed this guide from the beginning, you should by 
now have run your first simulation with *midas*. 

Inspect your current directory and you will find a new directory
*_output* and inside that directory a file called *midasmv_cfg.yml*
that contains the full configuration of the scenario you ran before. 
Note, since the file is created automatically, it is kind of unordered
(actually, the keys are ordered alphabetically). If you plan to tinker
around with that file, you should rename it. Otherwise, it will be 
overwritten when you start the *midasmv* scenario again.

.. code-block:: yaml

    myconfig: 
      start_date: 2017-01-01 00:00:00+0100
      end: 1*24*60*60
      
On the top level you find a key called *myconfig*. You can rename this
as you like (as long as it is unique). This name is to be provided if
you want to start your custom scenario (see CLI). On the second level,
global settings for the scenario are defined. With *start_date* you 
can define the start date for the simulation. Most of the data cover
one year. Therefore, the year is not that important, but month and day
will be considered. On the other side, you can freely define an hour as
start time. Minutes and seconds will probably work as well, but since
the data's resolution is 15 minutes to 1 hour, you should make sure to
use interpolation (see :doc:`Configuration <configuration>`) and 
adapt the step size accordingly.

The *end* key specifies how many simulation steps (one step is defined
as one second) will be performed. You can define the value like above,
consisting of several multiplications for better readability, or 
directly set the number you like.

Command line interface
----------------------
 
(Coming soon)