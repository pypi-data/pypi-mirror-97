.. include:: ../../README.rst

Usage
-----

pyramid_decoy's usage is pretty strightforward. It can work as a standalone app,
or other pyramid's app extension.

Extension
=========

To run it as an extension, include pyramid_decoy either by configuration:

.. code-block:: ini

    [app:main]
    # ...
    pyramid.includes = pyramid_decoy
    # ...

or within your project's main method:

.. code-block:: python

    def main(global_config, **settings):
        """Build a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        return config.make_wsgi_app()

Standalone
==========

To run as a standalone app, use paste config containing these lines:

.. code-block:: ini

    [app:main]
    use = egg:pyramid_decoy#decoy
    decoy.url = http://www.example.com/


Configuration
=============

At this moment, decoy supports only one url that it redirects to.
To set it, use **decoy.url** setting in your app:

.. code-block:: ini

    [app:main]
    #...
    decoy.url = http://www.example.com/
    #...



License
-------

Copyright (c) 2014 by pyramid_decoy authors and contributors. See :ref:`authors`

This module is part of pyramid_decoy and is released under
the MIT License (MIT): http://opensource.org/licenses/MIT
