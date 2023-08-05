Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-il0398/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/il0398/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_IL0398/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_IL0398/actions
    :alt: Build Status

CircuitPython displayio drivers for IL0398 driven e-paper displays


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-il0398/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-il0398

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-il0398

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-il0398

Usage Example
=============

.. code-block:: python

    """Simple test script for 4.2" 400x300 black and white displays.

    Supported products:
      * WaveShare 4.2" Black and White
        * https://www.waveshare.com/product/modules/oleds-lcds/e-paper/4.2inch-e-paper.htm
        * https://www.waveshare.com/product/modules/oleds-lcds/e-paper/4.2inch-e-paper-module.htm
      """

    import time
    import board
    import displayio
    import adafruit_il0398

    displayio.release_displays()

    # This pinout works on a Feather M4 and may need to be altered for other boards.
    spi = board.SPI() # Uses SCK and MOSI
    epd_cs = board.D9
    epd_dc = board.D10
    epd_reset = board.D5
    epd_busy = board.D6

    display_bus = displayio.FourWire(spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset,
                                     baudrate=1000000)
    time.sleep(1)

    display = adafruit_il0398.IL0398(display_bus, width=400, height=300, seconds_per_frame=20,
                                     busy_pin=epd_busy)

    g = displayio.Group()

    f = open("/display-ruler.bmp", "rb")

    pic = displayio.OnDiskBitmap(f)
    t = displayio.TileGrid(pic, pixel_shader=displayio.ColorConverter())
    g.append(t)

    display.show(g)

    display.refresh()

    time.sleep(120)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_IL0398/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
