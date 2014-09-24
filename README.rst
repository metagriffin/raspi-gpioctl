=================
Raspberry PI GPIO
=================

The `raspi-gpioctl` is a tiny package that provides a simple little
command line tool, `gpioctl`, that allows minimal Raspberry PI GPIO
pin state management.

Usage
=====

To read the state of pin 18 when it is in output mode and turned on:

.. code-block:: bash

  $ gpioctl 18
  function: output
  state: 1

To set pin 23 to output mode and turn it off:

.. code-block:: bash

  $ gpioctl 23 off

