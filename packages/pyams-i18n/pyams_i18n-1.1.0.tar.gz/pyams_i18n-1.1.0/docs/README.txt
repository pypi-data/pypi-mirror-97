==================
PyAMS_i18n package
==================

.. contents::


What is PyAMS
=============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage web sites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_; source code
is available on `Gitlab <https://gitlab.com/pyams>`_ and pushed to `Github
<https://github.com/py-ams>`_.


What is PyAMS_i18n?
===================

PyAMS_i18n is a package dedicated to contents internationalization management. It allows to define
an I18n negotiator utility, which will handle langue negotiation against browser settings, and
provides custom schema fields for text or images which will allow to store a given property in
several languages, and to display the correct version.
