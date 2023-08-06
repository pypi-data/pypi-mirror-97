#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_template.template module

This module provides Pyramid decorators which can be used to register a Chameleon template for
a given view.

These templates are registered as multi-adapters, for a view and a request, so they can be
replaced or overriden easilly.
"""

import inspect
import os

import venusian
from pyramid.exceptions import ConfigurationError
from pyramid.interfaces import IRequest
from pyramid_chameleon.interfaces import IChameleonTranslate
from pyramid_chameleon.zpt import PyramidPageTemplateFile
from zope.component import queryUtility
from zope.interface import directlyProvides

from pyams_template.interfaces import IContentTemplate, ILayoutTemplate, IPageTemplate
from pyams_utils.registry import get_pyramid_registry


__docformat__ = 'restructuredtext'


CONFIGURATION_SETTINGS = {}


class TemplateFactory:
    """Base template factory"""

    template = None

    def __init__(self, filename, content_type, macro=None):
        self.content_type = content_type
        self.template = PyramidPageTemplateFile(filename,
                                                content_type=content_type,
                                                macro=macro,
                                                auto_reload=CONFIGURATION_SETTINGS.get(
                                                    'reload_templates', False),
                                                debug=CONFIGURATION_SETTINGS.get(
                                                    'debug_templates', False),
                                                translate=queryUtility(IChameleonTranslate))
        self.macro = self.template.macro = macro

    def __call__(self, context, request, view):
        return self.template


class BoundViewTemplate:
    """Bound view template"""

    __self__ = None
    __func__ = None

    def __init__(self, tmpl, obj):
        object.__setattr__(self, '__func__', tmpl)
        object.__setattr__(self, '__self__', obj)

    @property
    def im_self(self):
        """im_self property"""
        return self.__self__

    @property
    def im_func(self):
        """im_func property"""
        return self.__func__

    def __call__(self, *args, **kwargs):
        if self.__self__ is None:
            im_self, args = args[0], args[1:]
        else:
            im_self = self.__self__
        return self.__func__(im_self, *args, **kwargs)  # pylint: disable=not-callable

    def __setattr__(self, name, v):
        raise AttributeError("Can't set attribute", name)

    def __repr__(self):
        return "<BoundViewTemplate of %r>" % self.__self__


class ViewTemplate:
    """View template class"""

    def __init__(self, provides=IPageTemplate, name=''):
        self.provides = provides
        self.name = name

    def __call__(self, instance, *args, **keywords):
        context = instance.context
        request = instance.request
        registry = instance.request.registry
        template = registry.getMultiAdapter((context, request, instance),
                                            self.provides, name=self.name)

        keywords.update({
            'context': context,
            'request': request,
            'view': instance,
            'translate': queryUtility(IChameleonTranslate)
        })
        return template(*args, **keywords)

    def __get__(self, instance, type):  # pylint: disable=redefined-builtin
        return BoundViewTemplate(self, instance)


get_view_template = ViewTemplate  # pylint: disable=invalid-name


class GetContentTemplate(ViewTemplate):
    """Page template getter class"""

    def __init__(self, name=''):
        super(GetContentTemplate, self).__init__(IContentTemplate, name)


get_content_template = GetContentTemplate  # pylint: disable=invalid-name


class GetLayoutTemplate(ViewTemplate):
    """Layout template getter class"""

    def __init__(self, name=''):
        super(GetLayoutTemplate, self).__init__(ILayoutTemplate, name)


get_layout_template = GetLayoutTemplate  # pylint: disable=invalid-name


def register_template(template, view, settings, provides, registry=None):
    """Register new template"""
    if not os.path.isfile(template):
        raise ConfigurationError("No such file", template)

    content_type = settings.get('content_type', 'text/html')
    macro = settings.get('macro')
    factory = TemplateFactory(template, content_type, macro)
    provides = settings.get('provides', provides)
    directlyProvides(factory, provides)

    # check context
    required = (
        settings.get('context', None),
        settings.get('layer', IRequest),
        view
    )
    # update registry
    if registry is None:
        registry = settings.get('registry')
        if registry is None:
            registry = get_pyramid_registry()
    registry.registerAdapter(factory, required, provides, settings.get('name', ''))


class base_template_config:  # pylint: disable=invalid-name
    """Base template configuration class"""

    venusian = venusian  # for testing injection
    interface = IPageTemplate  # template interface

    def __init__(self, **settings):
        if 'for_' in settings:
            if settings.get('context') is None:
                settings['context'] = settings['for_']
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, view):
            template = os.path.join(os.path.dirname(inspect.getfile(inspect.getmodule(view))),
                                    settings.get('template'))
            if not os.path.isfile(template):
                raise ConfigurationError("No such file", template)
            # check registry
            registry = settings.get('registry')
            if registry is None:
                config = context.config.with_package(info.module)  # pylint: disable=no-member
                registry = config.registry
            register_template(template, view, settings, self.interface, registry)

        info = self.venusian.attach(wrapped, callback, category='pyams_template')
        if info.scope == 'class':  # pylint: disable=no-member
            # if the decorator was attached to a method in a class, or
            # otherwise executed at class scope, we need to set an
            # 'attr' into the settings if one isn't already in there
            if settings.get('attr') is None:
                settings['attr'] = wrapped.__name__

        settings['_info'] = info.codeinfo  # pylint: disable=no-member
        return wrapped


class template_config(base_template_config):  # pylint: disable=invalid-name
    """Class decorator used to declare a view template"""

    interface = IContentTemplate


def override_template(view, **settings):
    """Override template for a given context

    This function can be used to override a class template without using ZCML.
    Settings are the same as for @template_config decorator.
    """
    template = settings.get('template', '')
    if not template:
        raise ConfigurationError("No template specified")
    if not template.startswith('/'):
        stack = inspect.stack()[1]
        template = os.path.join(os.path.dirname(inspect.getfile(inspect.getmodule(stack[0]))),
                                template)
    register_template(template, view, settings, IContentTemplate)


class layout_config(base_template_config):  # pylint: disable=invalid-name
    """Class decorator used to declare a layout template"""

    interface = ILayoutTemplate


def override_layout(view, **settings):
    """Override layout template for a given class

    This function can be used to override a class layout template without using ZCML.
    Settings are the same as for @layout_config decorator.
    """
    template = settings.get('template', '')
    if not template:
        raise ConfigurationError("No template specified")
    if not template.startswith('/'):
        stack = inspect.stack()[1]
        template = os.path.join(os.path.dirname(inspect.getfile(inspect.getmodule(stack[0]))),
                                template)
    register_template(template, view, settings, ILayoutTemplate)
