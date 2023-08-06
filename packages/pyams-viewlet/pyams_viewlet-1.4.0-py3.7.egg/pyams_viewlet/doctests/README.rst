
=====================
pyams_viewlet package
=====================

These doctests are based on zope.viewlet doctests.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_template import includeme as include_template
    >>> include_template(config)
    >>> from pyams_viewlet import includeme as include_viewlet
    >>> include_viewlet(config)


Defining content providers
--------------------------

A content provider is a custom named adapter, eventually registered for a specific kind of
context, request and view, which is declared to provide HTML content through templates.

The "provider:" TALES expression is registered automatically when the package is included into
Pyramid configuraiton:

    >>> from chameleon import PageTemplateFile
    >>> from pyams_viewlet.provider import ProviderExpr

    >>> PageTemplateFile.expression_types['provider'] = ProviderExpr

    >>> import os, tempfile
    >>> temp_dir = tempfile.mkdtemp()
    >>> template = os.path.join(temp_dir, 'content-provider.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>I'm a content provider!</div>")

A custom "contentprovider_config" decorator cna be used to register a content provider:

    >>> from pyams_viewlet.viewlet import contentprovider_config
    >>> from pyams_template.template import template_config

In it's minimal form, a content provider can look like this:

    >>> @contentprovider_config(name='my-content')
    ... @template_config(template=template)
    ... class MyContentProvider:
    ...     """My content provider"""

Because we are in testing mode, we have to call these venusian decorators by hand; this doesn't
have to be done in a normal application:

    >>> from zope.interface import implementer, Interface
    >>> from pyams_utils.testing import call_decorator

    >>> call_decorator(config, contentprovider_config, MyContentProvider)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: You must provide a name for a content provider

    >>> call_decorator(config, contentprovider_config, MyContentProvider,
    ...                for_=Interface,
    ...                name='my-content',
    ...                permission='View')
    >>> call_decorator(config, template_config, MyContentProvider, template=template)

We can then create a template to include this content provider:

    >>> from pyramid_chameleon.zpt import renderer_factory
    >>> config.add_renderer('.pt', renderer_factory)

    >>> template = os.path.join(temp_dir, 'content.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:my-content}</div>")

    >>> from pyramid.renderers import render
    >>> from pyramid.testing import DummyRequest

    >>> request = DummyRequest()

    >>> class IContent(Interface):
    ...     """Content marker interface"""

    >>> @implementer(IContent)
    ... class Content:
    ...     """Content class"""
    ...     title = 'My Content'
    >>> content = Content()

    >>> from pyramid.interfaces import IView, IRequest

    >>> @implementer(IView)
    ... class View:
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    >>> view = View(content, request)

    >>> render(template, {'context': content, 'request': request, 'view': view})
    "<div><div>I'm a content provider!</div></div>"

And that's it!


Content providers with arguments
--------------------------------

You can call a content provider with arguments; these arguments will then be added to the
update method call:

    >>> from zope.location.interfaces import ILocation

    >>> @implementer(ILocation)
    ... class TitleProvider:
    ...     title = 'John Doe'
    ...     value = 'Jackson'
    ...     def update(self, prefix='Hello', title=''):
    ...         self.prefix = prefix
    ...         if title:
    ...             self.title = title
    ...     def render(self):
    ...         return '{}, {}'.format(self.prefix, self.title)

    >>> call_decorator(config, contentprovider_config, TitleProvider,
    ...                for_=Interface,
    ...                name='title-content',
    ...                permission='View')

    >>> template = os.path.join(temp_dir, 'title-content.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:title-content}!</div>")
    >>> render(template, {'context': content, 'request': request, 'view': view})
    '<div>Hello, John Doe!</div>'

    >>> template = os.path.join(temp_dir, 'title-content-2.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:title-content('Welcome')}!</div>")
    >>> render(template, {'context': content, 'request': request, 'view': view})
    '<div>Welcome, John Doe!</div>'

    >>> template = os.path.join(temp_dir, 'title-content-3.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:title-content(title='Jack')}!</div>")
    >>> render(template, {'context': content, 'request': request, 'view': view})
    '<div>Hello, Jack!</div>'

You can use dotted variables names in provider call:

    >>> template = os.path.join(temp_dir, 'title-content-4.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:title-content(title=context.title)}!</div>")
    >>> render(template, {'context': content, 'request': request, 'view': view})
    '<div>Hello, My Content!</div>'

    >>> template = os.path.join(temp_dir, 'title-content-5.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:title-content(title=123)}!</div>")
    >>> render(template, {'context': content, 'request': request, 'view': view})
    '<div>Hello, 123!</div>'

Of course, calling an unregistered content provider raises an exception:

    >>> template = os.path.join(temp_dir, 'title-content-6.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:unknown}!</div>")
    >>> render(template, {'context': content, 'request': request, 'view': view})
    Traceback (most recent call last):
    ...
    zope.contentprovider.interfaces.ContentProviderLookupError: zope.contentprovider.interfaces.ContentProviderLookupError: unknown
    ...

    >>> template = os.path.join(temp_dir, 'title-content-7.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:@123}!</div>")
    >>> render(template, {'context': content, 'request': request, 'view': view})
    Traceback (most recent call last):
    ...
    zope.contentprovider.interfaces.ContentProviderLookupError: zope.contentprovider.interfaces.ContentProviderLookupError: @123
    ...


Viewlets managers
-----------------

Viewlets managers are a specific kind of content manager.

Managers are viewlets "containers"; each manager can look for it's viewlets using a registry
lookup on adapters to IViewlet interface.

The first step is to create a manager interface:

    >>> from pyams_viewlet.interfaces import IViewletManager

    >>> class ILeftColumn(IViewletManager):
    ...     """Left column viewlet manager"""

We can then create a viewlet manager factory using this interface:

    >>> from pyams_viewlet.manager import ViewletManagerFactory
    >>> LeftColumn = ViewletManagerFactory('left-column', ILeftColumn)

Having the factory, we can instantiate it:

    >>> left_column = LeftColumn(content, request, view)

Actually, viewlet manager doesn't render anything:

    >>> left_column.update()
    >>> left_column.render()
    ''
    >>> left_column.get('text-box') is None
    True

We have to create and register viewlets for the manager:

    >>> from pyams_viewlet.interfaces import IViewlet
    >>> from pyams_viewlet.viewlet import EmptyViewlet

    >>> class TextBox(EmptyViewlet):
    ...     __name__ = None
    ...     weight = 1
    ...     def render(self):
    ...         return '<div class="text">Text box!</div>'
    ...     def __repr__(self):
    ...         return '<TextBox object at %x>' % id(self)

    >>> config.registry.registerAdapter(TextBox,
    ...                                 (Interface, IRequest, IView, ILeftColumn),
    ...                                 IViewlet, name='text-box')

    >>> left_column.get('text-box')
    <TextBox object at ...>
    >>> 'text-box' in left_column
    True
    >>> left_column.render()
    ''

Why is it empty? It's because viewlet managers are memoized on rendering, because they are
generally used only once in a given page, so we have to reset it's state if we want to render it
another time:

    >>> left_column.reset()
    >>> left_column.update()
    >>> left_column.render()
    '<div class="text">Text box!</div>'

After being registered, a viewlet manager (as any registered content provider) can be included
into a Chameleon template easilly:

    >>> from zope.contentprovider.interfaces import IContentProvider
    >>> config.registry.registerAdapter(LeftColumn, (Interface, IRequest, Interface),
    ...                                 IContentProvider, name='left-column')

    >>> template = os.path.join(temp_dir, 'text-template.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write('<div>${structure:provider:left-column}</div>')

    >>> from pyams_template.interfaces import IPageTemplate
    >>> from pyams_template.template import TemplateFactory

    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (Interface, IRequest, None), IPageTemplate)
    >>> render = config.registry.getMultiAdapter((content, request, view), IPageTemplate)
    >>> render(**{'context': content, 'request': request, 'view': view})
    '<div><div class="text">Text box!</div></div>'


Registering viewlets and viewlets managers
------------------------------------------

We generally use decorators to register viewlets and viewlets managers, as well as other content
providers, to keep the syntax simple and clean.

By default, a viewlet manager is rendered by just concatenating it's viewlets contents; but you
can also provide your own template:

    >>> from pyams_viewlet.manager import viewletmanager_config
    >>> from pyams_viewlet.viewlet import get_view_template

    >>> template = os.path.join(temp_dir, 'manager-template.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write('''<div class="column"><tal:loop repeat="viewlet view.viewlets">
    ...     ${structure:viewlet.render()}
    ... </tal:loop></div>''')

    >>> class IRightColumn(Interface):
    ...     """Right column viewlet manager"""

    >>> from pyams_viewlet.manager import ConditionalViewletManager
    >>> class RightColumn(ConditionalViewletManager):
    ...     """Right column viewlet manager"""
    ...     template = get_view_template()

    >>> call_decorator(config, viewletmanager_config, RightColumn,
    ...                provides=IRightColumn, weight=1)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: You must provide a name for a ViewletManager

    >>> call_decorator(config, viewletmanager_config, RightColumn,
    ...                for_=Interface,
    ...                name='right-column',
    ...                permission='View',
    ...                provides=IRightColumn)
    >>> call_decorator(config, template_config, RightColumn,
    ...                template=template)

    >>> right_column = config.registry.getMultiAdapter((content, request, view), IRightColumn,
    ...                                                name='right-column')
    >>> right_column
    <pyams_viewlet.manager.<ViewletManager providing IRightColumn> object at 0x...>
    >>> right_column.update()
    >>> right_column.render()
    ''

We can also, finally, declare a viewlet manager which is also a viewlet in a single step, just
by adding a "manager" argument:

    >>> class IRightInnerViewletManager(Interface):
    ...     """Inner viewlet manager marker interface"""

    >>> class RightInnerViewletManager(ConditionalViewletManager):
    ...     """Inner viewlet manager"""

    >>> call_decorator(config, viewletmanager_config, RightInnerViewletManager,
    ...                for_=Interface,
    ...                name='inner-right-column',
    ...                permission='View',
    ...                manager=RightColumn,
    ...                weight=1,
    ...                provides=IRightInnerViewletManager)


Protected viewlets
------------------

Viewlets can be protected by a permission, which can be a viewlet attribute or which can be
defined when viewlet is registered using "viewlet_config" decorator:

    >>> from pyams_viewlet.viewlet import Viewlet
    >>> class ImageBox:
    ...     def __repr__(self):
    ...         return '<ImageBox object at %x>' % id(self)

When using "viewlet_config" decorator, you can notice that it's not even required to inherit
from a Viewlet base class, the decorator taking care of adding base classes to your viewlet:

    >>> template = os.path.join(temp_dir, 'image-template.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write('<div><img src="/--static--/myimage.png" /></div>')

    >>> from pyams_viewlet.viewlet import viewlet_config

    >>> call_decorator(config, viewlet_config, TextBox)
    Traceback (most recent call last):
    ...
    pyramid.exceptions.ConfigurationError: You must provide a name for a viewlet

    >>> call_decorator(config, viewlet_config, TextBox,
    ...                name='text-box',
    ...                for_=Interface,
    ...                manager=IRightColumn,
    ...                weight=2,
    ...                permission='view')
    >>> call_decorator(config, viewlet_config, ImageBox,
    ...                name='image-box',
    ...                manager=IRightColumn,
    ...                weight=3,
    ...                permission='system.forbidden')

    >>> from pyams_template.template import template_config
    >>> call_decorator(config, template_config, ImageBox,
    ...                template=template)

    >>> right_column.reset()
    >>> right_column.update()
    >>> right_column.render()
    '<div class="column">\n    \n\n    <div class="text">Text box!</div>\n\n    <div><img src="/--static--/myimage.png" /></div>\n</div>'


Defining providers during traversal
-----------------------------------

We had a special use case where a content provider couldn't be defined only throught a simple
named adapter lookup, but was attached to a context which had been traversed during URL traversal.

To keep track of this event, you can define this custom provider during traversal, using request
annotations (typically by subscribing to an *IBeforeTraverseEvent* event):

    >>> from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
    >>> from zope.annotation.attribute import AttributeAnnotations
    >>> config.registry.registerAdapter(AttributeAnnotations, (IAttributeAnnotatable, ), IAnnotations)

    >>> from pyams_utils.request import set_request_data

    >>> template = os.path.join(temp_dir, 'custom-content.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:provider:custom-content}</div>")

    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (Interface, IRequest, None), IPageTemplate)
    >>> render = config.registry.getMultiAdapter((content, request, view), IPageTemplate)
    >>> render(**{'context': content, 'request': request, 'view': view})
    Traceback (most recent call last):
    ...
    zope.contentprovider.interfaces.ContentProviderLookupError: zope.contentprovider.interfaces.ContentProviderLookupError: custom-content
    ...

    >>> from pyams_viewlet.viewlet import ViewContentProvider
    >>> class CustomProvider(ViewContentProvider):
    ...     """Custom content provider"""
    ...     def render(self):
    ...         return '<p>This is custom content!</p>'

    >>> set_request_data(request, 'provider:custom-content:factory', CustomProvider)
    >>> render(**{'context': content, 'request': request, 'view': view})
    '<div><p>This is custom content!</p></div>'

Another option to define provider factories during traversal is to set a mapping into request
annotation instead of a simple factory; in this case, mapping keys are interfaces or classes
that the current context class have to provide or inherit from, and mapping values are the
matching provider factories. When provider is given as a dict with multiple classes or
interfaces, they should be ordered (using an *OrderedDict*) so that the most specific
interfaces or classes are provided first:

    >>> from collections import OrderedDict
    >>> set_request_data(request, 'provider:custom-content:factory', OrderedDict((
    ...     (IContent, CustomProvider),
    ... )))
    >>> render(**{'context': content, 'request': request, 'view': view})
    '<div><p>This is custom content!</p></div>'

If no factory is matching, an exception is raised:

    >>> class IAnotherInterface(Interface):
    ...     """Custom marker interface"""

    >>> set_request_data(request, 'provider:custom-content:factory', OrderedDict((
    ...     (IAnotherInterface, CustomProvider),
    ... )))
    >>> render(**{'context': content, 'request': request, 'view': view})
    Traceback (most recent call last):
    ...
    zope.contentprovider.interfaces.ContentProviderLookupError: zope.contentprovider.interfaces.ContentProviderLookupError: custom-content
    ...


Test cleanup:

    >>> tearDown()
