Troublebox
==========

A very limited Sentry_ compatible end point.
Use it for very small installations where the Sentry docker images are too big and Sentry as a service isn't an option.

.. _Sentry: https://sentry.io

.. warning::
    Do not expose to the public internet! There is no authentication or anything built in.


Basic usage
-----------

This readme uses |plaster_pastedeploy|_ for deployment.

Copy |production.ini|_ and adjust to your needs.

Run with ``pserve [your ini file name]``.

As the Sentry DSN use a URL similar to this: ``http://key@localhost:7777/42``

Replace ``localhost:7777`` with the address of the box your Troublebox instance is running on.
The ``key`` part is currently not checked, but required by Sentry libraries.
The ``42`` is the internal project id and can be an arbitrary number.

The actual address used by Sentry libraries in this example is: ``http://localhost:7777/api/42/store/``

.. |plaster_pastedeploy| replace:: ``plaster_pastedeploy``
.. _plaster_pastedeploy: https://pypi.org/project/plaster-pastedeploy/
.. |production.ini| replace:: ``production.ini``
.. _production.ini: https://github.com/fschulze/troublebox/blob/main/production.ini
