======================
pyams_template package
======================

This doctests are based on z3c.template doctests.

First let's show how to produce content from a view:

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_template import includeme as include_template
    >>> include_template(config)

    >>> root = {}

    >>> import os, tempfile
    >>> temp_dir = tempfile.mkdtemp()


Content template
----------------

Let's start by adding a template to produce content from a view:

    >>> content_template = os.path.join(temp_dir, 'content-template.pt')
    >>> with open(content_template, 'w') as file:
    ...     _ = file.write('<div>Base template content</div>')

We can now register a view class implementing an interface:

    >>> from zope.interface import implementer, Interface
    >>> from pyams_template.interfaces import IContentTemplate, IPageTemplate

    >>> class IMyView(Interface):
    ...     """View marker interface"""

    >>> @implementer(IMyView)
    ... class MyView:
    ...     template = None
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    ...     def __call__(self):
    ...         if self.template is None:
    ...             template = config.registry.getMultiAdapter((self.context, self.request, self),
    ...                                                        IContentTemplate)
    ...             return template()
    ...         return self.template()

Let's now call the view and check the output:

    >>> from pyramid.testing import DummyRequest
    >>> root = object()
    >>> request = DummyRequest()
    >>> view = MyView(root, request)

Since the template is not yet registered, rendering may fail:

    >>> view()
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

So let's now register the template; this is commonly done using "template_config" decorator, or
using ZCML:

    >>> from pyams_template.template import TemplateFactory
    >>> factory = TemplateFactory(content_template, 'text/html')
    >>> factory
    <pyams_template.template.TemplateFactory object at ...>

    >>> from pyramid.interfaces import IRequest
    >>> config.registry.registerAdapter(factory, (None, IRequest, Interface), IContentTemplate)
    >>> config.registry.getMultiAdapter((root, request, view), IPageTemplate)
    <PyramidPageTemplateFile .../content-template.pt>

    >>> print(view())
    <div>Base template content</div>

Now we can register another template for this view:

    >>> my_template = os.path.join(temp_dir, 'my-template.pt')
    >>> with open(my_template, 'w') as file:
    ...     _ = file.write('<div>This is my custom template</div>')
    >>> factory = TemplateFactory(my_template, 'text/html')
    >>> config.registry.registerAdapter(factory, (None, IRequest, IMyView), IContentTemplate)
    >>> print(view())
    <div>This is my custom template</div>

It's generally easier to use a decorator to register templates:

    >>> from pyramid.view import view_config
    >>> from pyams_template.template import template_config

    >>> my_other_template = os.path.join(temp_dir, 'my-other-template.pt')
    >>> with open(my_other_template, 'w') as file:
    ...     _ = file.write('<div>This is my template for view 2</div>')

    >>> @template_config(template=my_other_template)
    ... class MyView2(MyView):
    ...     """Simple view subclass"""

In testing mode we always have to register template manually because venusian can't scan test
unit:

    >>> factory = TemplateFactory(my_other_template, 'text/html')
    >>> config.registry.registerAdapter(factory, (None, IRequest, MyView2), IContentTemplate)

    >>> view = MyView2(root, request)
    >>> print(view())
    <div>This is my template for view 2</div>

We can also always override a template without creating another class:

    >>> from pyams_template.template import override_template
    >>> overriden_template = os.path.join(temp_dir, 'override-template.pt')
    >>> with open(overriden_template, 'w') as file:
    ...     _ = file.write('<div>This is an overriden content</div>')

    >>> from zope.interface import directlyProvides
    >>> class IMyLayer(IRequest):
    ...     """Layer marker interface"""
    >>> directlyProvides(request, *(IMyLayer,))
    >>> override_template(registry=config.registry, view=MyView2,
    ...                   layer=IMyLayer)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: No template specified
    >>> override_template(registry=config.registry, view=MyView2,
    ...                   template='/missing-filename.pt', layer=IMyLayer)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: ('No such file', '/missing-filename.pt')
    >>> override_template(registry=config.registry, view=MyView2,
    ...                   template=overriden_template, layer=IMyLayer)
    >>> print(view())
    <div>This is an overriden content</div>


Layout template
---------------

We first need to register a new view class using a layout template. This view is using the
__call__ method to invoke it's template:

    >>> from pyams_template.interfaces import ILayoutTemplate

    >>> class ILayoutView(Interface):
    ...     """View with layout marker interface"""

    >>> @implementer(ILayoutView)
    ... class LayoutView:
    ...     layout = None
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    ...     def __call__(self):
    ...         if self.layout is None:
    ...             layout = config.registry.getMultiAdapter((self.context, self.request, self),
    ...                                                      ILayoutTemplate)
    ...             return layout()
    ...         return self.layout()
    >>> layout_view = LayoutView(root, request)

We can now define and register a new layout template:

    >>> layout_template = os.path.join(temp_dir, 'layout-template.pt')
    >>> with open(layout_template, 'w') as file:
    ...     _ = file.write('<div>demo layout</div>')
    >>> factory = TemplateFactory(layout_template, 'text/html')

The template factory is then registered for a view interface and a request layer; this is generally
done using a decorator:

    >>> config.registry.registerAdapter(factory, (None, IRequest, Interface), ILayoutTemplate)
    >>> config.registry.getMultiAdapter((root, request, layout_view), ILayoutTemplate)
    <PyramidPageTemplateFile .../layout-template.pt>

    >>> print(layout_view())
    <div>demo layout</div>

We can now register another layout for a more specific interface:

    >>> from pyams_template.template import layout_config

    >>> my_other_layout = os.path.join(temp_dir, 'my-other-layout.pt')
    >>> with open(my_other_layout, 'w') as file:
    ...     _ = file.write('<div>This is my layout template for my view 2</div>')

    >>> @template_config(template=my_other_layout)
    ... class MyLayoutView2(LayoutView):
    ...     """Simple view subclass"""


In testing mode we always have to register layout manually because venusian can't scan test
unit:

    >>> factory = TemplateFactory(my_other_layout, 'text/html')
    >>> config.registry.registerAdapter(factory, (None, IRequest, MyLayoutView2), ILayoutTemplate)

    >>> view = MyLayoutView2(root, request)
    >>> print(view())
    <div>This is my layout template for my view 2</div>

It's also possible to set the layout template directly, without using an adapter:

    >>> from pyramid_chameleon.zpt import PyramidPageTemplateFile

    >>> @implementer(ILayoutView)
    ... class LayoutViewWithTemplate(LayoutView):
    ...     layout = PyramidPageTemplateFile(my_other_layout, macro=None)

    >>> layout_view = LayoutViewWithTemplate(root, request)
    >>> print(layout_view())
    <div>This is my layout template for my view 2</div>

We can also always override a layout without creating another class:

    >>> from pyams_template.template import override_layout
    >>> overriden_layout = os.path.join(temp_dir, 'override-layout.pt')
    >>> with open(overriden_layout, 'w') as file:
    ...     _ = file.write('<div>This is an overriden layout</div>')

    >>> override_layout(registry=config.registry, view=MyLayoutView2,
    ...                 layer=IMyLayer)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: No template specified
    >>> override_layout(registry=config.registry, view=MyLayoutView2,
    ...                 template='/missing-filename.pt', layer=IMyLayer)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: ('No such file', '/missing-filename.pt')

    >>> override_layout(registry=config.registry, view=MyLayoutView2,
    ...                 template=overriden_layout, layer=IMyLayer)
    >>> print(view())
    <div>This is an overriden layout</div>


Mixing content and layout templates
-----------------------------------

A layout template like this doesn't have any huge interest; it's goal is to be able to render
the view content:

    >>> class IDocumentView(Interface):
    ...     """Full view marker interface"""

    >>> @implementer(IDocumentView)
    ... class DocumentView:
    ...     layout = None
    ...     template = None
    ...     attr = None
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    ...     @property
    ...     def tmpl_dict(self):
    ...         return {'context': self.context, 'request': self.request, 'view': self}
    ...     def update(self):
    ...         self.attr = 'content updated'
    ...     def render(self):
    ...         if self.template is None:
    ...             template = config.registry.getMultiAdapter((self.context, self.request, self),
    ...                                                        IContentTemplate)
    ...             return template(**self.tmpl_dict)
    ...         return self.template(**self.tmpl_dict)
    ...     def __call__(self):
    ...         self.update()
    ...         if self.layout is None:
    ...             layout = config.registry.getMultiAdapter((self.context, self.request, self),
    ...                                                      ILayoutTemplate)
    ...             return layout(**self.tmpl_dict)
    ...         return self.layout(**self.tmpl_dict)

    >>> template = os.path.join(temp_dir, 'template.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write('''<span>${view.attr}</span>''')
    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (None, IRequest, IDocumentView), IContentTemplate)

    >>> layout = os.path.join(temp_dir, 'layout.pt')
    >>> with open(layout, 'w') as file:
    ...     _ = file.write('''<html><body><div>${structure:view.render()}</div></body></html>''')
    >>> factory = TemplateFactory(layout, 'text/html')
    >>> config.registry.registerAdapter(factory, (None, IRequest, IDocumentView), ILayoutTemplate)

    >>> document_view = DocumentView(root, request)
    >>> print(document_view())
    <html><body><div><span>content updated</span></div></body></html>

An alternative for subclasses of such a view class is to use a hook provided to call registered
templates; such templates can get called using the "get_content_template" and/or
"get_layout_template" methods, which return a registered bound ViewTemplate:

    >>> from pyams_template.template import get_content_template
    >>> class IViewWithTemplate(Interface):
    ...     """View with template marker interface"""

    >>> @implementer(IViewWithTemplate)
    ... class ViewWithTemplate:
    ...     template = get_content_template()
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request

A lookup for registered template is done automatically when the view is called:

    >>> simple_view = ViewWithTemplate(root, request)
    >>> print(simple_view.template())
    <div>Base template content</div>


Context-specific templates
--------------------------

All templates registrations accept a "context" argument, which allows to override a content or
a layout template only for a given context.


Interface-specific templates
----------------------------

You are not restricted to IContentTemplate and ILayoutTemplate interfaces when creating your
templates; these ones can be registered for any interface:

    >>> class IMyTemplate(Interface):
    ...     """Custom template interface"""

    >>> factory = TemplateFactory(content_template, 'text/html')
    >>> config.registry.registerAdapter(factory, (None, IRequest, Interface), IMyTemplate)

    >>> from pyams_template.template import get_view_template
    >>> class IMyTemplateView(Interface):
    ...     """View marker interface"""

    >>> @implementer(IMyTemplateView)
    ... class MyTemplateView:
    ...     template = get_view_template(IMyTemplate)
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request

    >>> my_view = MyTemplateView(root, request)
    >>> print(my_view.template())
    <div>Base template content</div>


Templates registration decorator
--------------------------------

Templates can be registered in a single step using the "template_config" and "layout_config"
decorators:

    >>> my_registered_template = os.path.join(temp_dir, 'my-registered-template.pt')
    >>> with open(my_registered_template, 'w') as file:
    ...     _ = file.write('<div>This is a registered template for view 2</div>')

    >>> class IMyContent(Interface):
    ...     """Content marker interface"""

    >>> @implementer(IMyContent)
    ... class Content:
    ...     """Content class"""

    >>> class MyContentView:
    ...     template = get_view_template()
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request

    >>> from pyams_template.template import template_config, layout_config
    >>> from pyams_utils.testing import call_decorator

    >>> call_decorator(config, template_config, MyContentView,
    ...                template='/missing-filename.pt',
    ...                for_=IMyContent)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: ('No such file', '/missing-filename.pt')

    >>> call_decorator(config, template_config, MyContentView,
    ...                template=my_registered_template,
    ...                for_=IMyContent)

    >>> content = Content()
    >>> print(MyContentView(root, request).template())
    <div>demo layout</div>
    >>> print(MyContentView(content, request).template())
    <div>This is a registered template for view 2</div>


Named templates
---------------

All content and layout templates can be registered with custom names.


Pagelets
--------

PyAMS_pagelet package provides another template-based layout and content rendering implementation
using PyAMS_pagelet features.


Tests cleanup:

    >>> tearDown()
