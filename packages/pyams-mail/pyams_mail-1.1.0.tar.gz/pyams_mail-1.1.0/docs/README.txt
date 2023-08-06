==================
PyAMS_mail package
==================

.. contents::


What is PyAMS?
==============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage web sites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_; source code
is available on `Gitlab <https://gitlab.com/pyams>`_ and pushed to `Github
<https://github.com/py-ams>`_.


What is PyAMS_mail?
===================

PyAMS_mail is a small utility package for Pyramid which allows to register several mailing servers
utilities through Pyramid's configuration file.

It also provides a few mail-related interfaces and utilities, like messages classes which
automatically provides text part of an HTML message.
