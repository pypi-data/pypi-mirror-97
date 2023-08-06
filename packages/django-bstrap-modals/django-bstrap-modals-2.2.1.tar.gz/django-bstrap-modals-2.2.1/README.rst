django-bstrap-modals
********************

A small library to help write Bootstrap 4 modals. It includes some base
templates and some Javascript functions for quickly creating and displaying
the dialogs.


Installation
============

.. code-block:: bash

    $ pip install django-bstrap-modals

Include ``bsmodals`` in your ``INSTALLED_APPS`` and make sure that your
``APP_DIRS`` setting inside of the ``TEMPLATES`` list is set to ``True``.

Supports
========

django-bstrap-modals has been tested with:

* Django 2.2.14 using Python 3.6
* Django 3.0.8 using Python 3.6

Due to the fact that it is a few templates and some Javascript, testing is
currently manual, it likely works in other versions. Uses the new-style load
static template tag, so may have problems prior to Django 2.1.

Docs & Source
=============

Docs: http://django-bstrap-modals.readthedocs.io/en/latest/

Source: https://github.com/cltrudeau/django-bstrap-modals
