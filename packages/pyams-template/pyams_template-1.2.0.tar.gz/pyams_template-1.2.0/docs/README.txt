======================
PyAMS_template package
======================

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


What is PyAMS_template?
=======================

PyAMS is using Chameleon internally as HTML templates engine.

This package, which is essentially an adaptation of "z3c.template" package for Pyramid, allows to
separate the definition of a view code from it's rendering template; this template selection can
actually be based on the view but also on the request layer (see "PyAMS_layer" package to get more
information about layers).

PyAMS_template package provides a "template_config" decorator, which allows you to define a template
for a given view, and a "layout_config" decorator, which allows to define a "layout" template;
layout templates are particularly useful when using "pagelets", which are defined into another
package (see PyAMS_pagelet).

You can also override a template definition for a given view, without creating a new view class,
just by using the "override_template" or "override_layout" functions.

View and layout templates can also be declared using ZCML instead of Python code, by using the
<template /> and <layout /> directives.
