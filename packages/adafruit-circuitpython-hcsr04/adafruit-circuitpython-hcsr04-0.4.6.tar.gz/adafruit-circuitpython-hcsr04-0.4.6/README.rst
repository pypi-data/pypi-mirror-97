Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-hcsr04/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/hcsr04/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_HCSR04/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_HCSR04/actions
    :alt: Build Status

.. image:: ../docs/_static/3942-02.jpg
    :alt: HC-SR04 Product Image

The HC-SR04 is an inexpensive solution for measuring distances using microcontrollers. This library provides a simple
driver for controlling these sensors from CircuitPython.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-hcsr04/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-hcsr04

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-hcsr04

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-hcsr04

Usage Example
=============

.. warning::

    The HC-SR04 uses 5V logic, so you will have to use a `level shifter
    <https://www.adafruit.com/product/2653?q=level%20shifter&>`_ between it
    and your CircuitPython board (which uses 3.3V logic).

.. note::

    If you want to use an HC-SR04 with `MicroPython <http://micropython.org/>`_, I recommend checking out `this library
    <https://github.com/andrey-git/micropython-hcsr04>`_.

You'll need to dedicate two pins to communicating with the HC-SR04. The sensor communicates in a very rudimentary
manner, so it doesn't matter which pins you choose, as long as they're digital IO pins (pins that start with "``D``"
are digital).

There are two ways of instantiating a `HCSR04` object: with or without using a context manager.

.. note::

    It is technically possible to communicate with the HC-SR04 using only one wire since the trigger and echo signals
    aren't ever active at the same time. Once I have a chance to determine a safe way to do this, I plan to add this as
    a feature to the library.

See Also:

    `Adafruit's guide on Lifetime and ContextManagers <https://circuitpython.readthedocs.io/en/latest/docs/design_guide.html#lifetime-and-contextmanagers>`_
        Gives more info on using context managers with CircuitPython drivers.

    `board <https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/__init__.html#module-board>`_
        A list of pins available on your device. To view this list, first `get a REPL
        <http://circuitpython.readthedocs.io/en/latest/docs/pyboard/tutorial/repl.html>`_ (the guide linked was written
        for the pyboard, but it still works), then input the following:

        .. code-block:: python

            import board
            dir(board)

Without a Context Manager
-------------------------

In the example below, we create the `HCSR04` object directly, get the distance every 2 seconds.

.. code-block:: python

    import time
    import board
    import adafruit_hcsr04

    sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

    while True:
        try:
            print((sonar.distance,))
        except RuntimeError:
            print("Retrying!")
        time.sleep(2)


With a Context Manager
----------------------

In the example below, we use a context manager (the `with <https://docs.python.org/3.4/reference/compound_stmts.html#with>`_ statement) to create the `HCSR04`
instance, again get the distance every 2 seconds, but then the context manager handles de-initializing the device for
us.

.. code-block:: python

    import board
    from adafruit_hcsr04 import HCSR04
    with HCSR04(trigger_pin=board.D5, echo_pin=board.D6) as sonar:
        try:
            while True:
                print(sonar.distance)
                sleep(2)
        except KeyboardInterrupt:
            pass


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_HCSR04/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
