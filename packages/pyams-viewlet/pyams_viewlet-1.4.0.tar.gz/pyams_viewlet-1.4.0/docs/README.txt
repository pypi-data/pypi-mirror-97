=====================
PyAMS_viewlet package
=====================

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
<https://github.com/py-ams>`_. Complete doctests are available in *doctests* source folder.


What is PyAMS_viewlet?
======================

PyAMS_viewlet is a package which defines components called "content providers"; these content
providers are named adapters which can be used inside Chameleon templates throught a custom
*provider:* TALES expression.

PyAMS_viewlet is an adaptation of zope.viewlet package to be used inside Pyramid, with a few
additional features.
