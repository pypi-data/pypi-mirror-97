Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-l3gd20/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/l3gd20/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_L3GD20/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_L3GD20/actions
    :alt: Build Status

Adafruit 9-DOF Absolute Orientation IMU Fusion Breakout - L3GD20 Driver

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-l3gd20/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-l3gd20

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-l3gd20

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-l3gd20

Usage Example
=============

Of course, you must import the library to use it:

.. code:: python

    import adafruit_l3gd20


This driver takes an instantiated and active I2C object (from the `busio` or
the `bitbangio` library) as an argument to its constructor.  The way to create
an I2C object depends on the board you are using. For boards with labeled SCL
and SDA pins, you can:

.. code:: python

    from busio import I2C
    from board import SDA, SCL

    i2c = I2C(SCL, SDA)

Once you have the I2C object, you can create the sensor object:

.. code:: python

    sensor = adafruit_l3gd20.L3GD20_I2C(i2c)


And then you can start reading the measurements:

.. code:: python

    print(sensor.gyro)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/adafruit_CircuitPython_l3gd20/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
