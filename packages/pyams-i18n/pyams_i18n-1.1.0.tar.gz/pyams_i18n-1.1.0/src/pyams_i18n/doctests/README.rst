
==================
PyAMS_i18n package
==================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application, which
allows to provide translations to any property using custom I18n schema fields.


Site upgrade
------------

PyAMS_i18n provides a site generation utility, which automatically create a negotiator utility:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_i18n import includeme as include_i18n
    >>> include_i18n(config)


Using negotiator
----------------

A negotiator is a registered utility which can be used to define how language selection is made;
several policies are available, between:

 - browser: used language is based on browser's settings, transmitted into requests headers

 - session: the session is stored into a user's attribute which is stored into it's session

 - server: the language is extrated from server settings.

You can also choose to select a "combined" policy, which will scan several options before chossing
a language, for example "session -> browser -> server" (which is the default).

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyramid.threadlocal import manager
    >>> from pyams_utils.registry import handle_site_before_traverse, get_local_registry
    >>> from pyams_site.generations import upgrade_site

    >>> request = DummyRequest(headers={'Accept-Language': 'en'})
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS I18n to generation 1...

    >>> handle_site_before_traverse(BeforeTraverseEvent(app, request))

    >>> 'Language negotiator' in app.getSiteManager()
    True
    >>> negotiator = app.getSiteManager()['Language negotiator']
    >>> negotiator.policy
    'session --> browser --> server'
    >>> negotiator.server_language
    'en'
    >>> negotiator.offered_languages
    {'en'}
    >>> negotiator.cache_enabled
    False

PyAMS_i18n also defines request properties, like locale and localizer:

    >>> loc = request.localizer
    >>> loc
    <pyramid.i18n.Localizer object at 0x...>
    >>> loc.locale_name
    'en'

Language can also be set using a request parameter:

    >>> request2 = DummyRequest(params={'lang': 'fr'})
    >>> negotiator.get_language(request2)
    'fr'

We can try to activate cache; iin this case negotiator changes won't impact request:

    >>> negotiator.cache_enabled = True

    >>> request3 = DummyRequest()
    >>> request3.session['language'] = 'it'
    >>> negotiator.get_language(request3)
    'en'
    >>> negotiator.clear_cache(request3)

    >>> request3.annotations = {}
    >>> negotiator.get_language(request3)
    'it'
    >>> negotiator.get_language(request3)
    'it'

    >>> negotiator.clear_cache(request3)
    >>> negotiator.server_language = 'en'
    >>> negotiator.cache_enabled = False


Using ++lang++ namespace traverser
----------------------------------

The "++lang++" namespace traverser is a custom traverser which was used before and was kept
for compatibility; using the "lang=" request parameter is actually preferred:

    >>> from pyams_i18n.negotiator import LangNamespaceTraverser

    >>> context = object()
    >>> request4 = DummyRequest()
    >>> traverser = LangNamespaceTraverser(context, request4)
    >>> traverser.traverse('fr') is context
    True
    >>> request4.params.get('lang')
    'fr'


Languages vocabularies
----------------------

There are two defined vocabularies concerning languages; the first on called "Offered languages",
provides a list of languages which can be selected as "server" policies, or which can be selected
when you need to provide translations of a given content:

    >>> from zope.schema.vocabulary import getVocabularyRegistry
    >>> from pyams_i18n.interfaces import OFFERED_LANGUAGES_VOCABULARY_NAME

    >>> context = {}
    >>> registry = getVocabularyRegistry()

    >>> from pyams_i18n.interfaces import INegotiator
    >>> config.registry.registerUtility(negotiator, INegotiator)
    >>> negotiator.offered_languages =  {'en', 'fr', 'es'}
    >>> languages = registry.get(context, OFFERED_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nOfferedLanguages object at 0x...>
    >>> len(languages)
    3
    >>> languages.getTermByToken('en').value
    'en'
    >>> languages.getTermByToken('en').title
    'English'
    >>> languages.getTermByToken('fr').value
    'fr'
    >>> languages.getTermByToken('fr').title
    'French'

When languagas have been selected for a given I18n content manager, you can select which languages
are selected for a given content using another vocabulary:

    >>> from pyams_i18n.interfaces import CONTENT_LANGUAGES_VOCABULARY_NAME
    >>> languages = registry.get(context, CONTENT_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nContentLanguages object at 0x...>
    >>> len(languages)
    1

There is only one language actually in this vocabulary, which is the server language:

    >>> languages.getTerm('en').title
    'English'
    >>> languages.getTerm('fr').title
    Traceback (most recent call last):
    ...
    LookupError: fr

We first have to create a I18n manager, which will be the parent of our future context:

    >>> from zope.interface import alsoProvides
    >>> from pyams_i18n.content import I18nManagerMixin

    >>> manager = I18nManagerMixin()
    >>> manager.languages = ['en', 'fr']

    >>> from zope.container.contained import Contained
    >>> context = Contained()
    >>> context.__parent__ = manager
    >>> languages = registry.get(context, CONTENT_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nContentLanguages object at 0x...>
    >>> len(languages)
    2
    >>> [t.value for t in languages]
    ['en', 'fr']
    >>> languages.getTerm('en').title
    'English'
    >>> languages.getTerm('fr').title
    'French'

Server language is automatically added to content available languages, always in first place:

    >>> manager.languages = ['fr', 'es']
    >>> languages = registry.get(context, CONTENT_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nContentLanguages object at 0x...>
    >>> len(languages)
    3
    >>> [t.value for t in languages]
    ['en', 'fr', 'es']

Another vocabulary is the ISO languages vocabulary:

    >>> from pyams_i18n.interfaces import ISO_LANGUAGES_VOCABULARY_NAME
    >>> iso_languages = registry.get(context, ISO_LANGUAGES_VOCABULARY_NAME)
    >>> iso_languages
    <...ISOLanguagesVocabulary object at 0x...>
    >>> len(iso_languages)
    232


Using I18n manager
------------------

The I18n manager is used to define, in any context, the set of languages which are "offered" for
translation; as providing translations is overloading the user interface while not being used
very often, if only by defining this at the manager level that you can really activate
translations.

    >>> from pyams_i18n.content import I18nManagerMixin
    >>> class MyI18nManager(I18nManagerMixin):
    ...     """Custom I18n manager class"""

    >>> i18n_manager = MyI18nManager()
    >>> i18n_manager.languages = ['fr', 'en', 'es']

Manager provides the full ordered list of available languages; server's language as defined into
negotiator settings is always set first, as a default fallback language, even if not included
into languages list:

    >>> i18n_manager.get_languages()
    ['en', 'es', 'fr']

    >>> i18n_manager.languages = ['fr', 'es']
    >>> i18n_manager.get_languages()
    ['en', 'es', 'fr']

I18n manager is a base class for many contents handling translations.


Defautl value mapping
---------------------

The DefaultValueMapping is a custom persistent mapping class with a default value:

    >>> from pyams_i18n.schema import DefaultValueMapping

Let's start with a mapping without default value:

    >>> mapping = DefaultValueMapping()
    >>> mapping.get('key') is None
    True
    >>> mapping.get('key', 'value')
    'value'
    >>> mapping['key']
    Traceback (most recent call last):
    ...
    KeyError: 'key'

Let's see know how it works when we define a default value:

    >>> mapping = DefaultValueMapping('default')
    >>> mapping.get('key')
    'default'

When a default value is defined, it's value takes precedence over another default value given
to the "get" method:

    >>> mapping.get('key', 'value')
    'default'
    >>> mapping['key']
    'default'

    >>> mapping['key'] = 'another value'
    >>> mapping.get('key')
    'another value'

    >>> mapping.copy().get('key2')
    'default'


I18n schema fields
------------------

PyAMS_i18n provides several custom schema fields which can be used to define properties
which can be set for several languages; they all inherit from a base I18n schema field, which
is a mapping whose keys are languages:

    >>> from pyams_i18n.schema import I18nField
    >>> field = I18nField(title='I18n base field', required=True)
    >>> field.validate(None)
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.RequiredMissing

A required I18n field is validated as soon as at least one language value is set:

    >>> field.validate({'en': None})
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.RequiredMissing

    >>> field.validate({'en': 'Text value', 'fr': None})

You can set a default value on this generic field type:

    >>> field = I18nField(title='I18n base field', required=True,
    ...                   default={'en': 'Default'})
    >>> field.validate(None)
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.RequiredMissing
    >>> field.validate({'en': 'value'})

Let's try with an I18n text line field:

    >>> from pyams_i18n.schema import I18nTextLineField
    >>> field = I18nTextLineField(title='I18n textline', required=True,
    ...                           default={'en': 'Default text'})
    >>> field.validate(None)
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.RequiredMissing
    >>> field.validate({'en': 'value'})

Validation rules are applied to each language individually:

    >>> field.validate({'en': 'Value\nwith\nbreaks'})
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.WrongContainedType: ([ConstraintNotSatisfied('Value\nwith\nbreaks', '')], '')


Translated properties
---------------------

After setting server settings, it's time to create custom interfaces to handle translated
properties:

    >>> from zope.interface import implementer, Interface
    >>> from zope.schema import TextLine
    >>> from zope.schema.fieldproperty import FieldProperty
    >>> from pyams_i18n.schema import I18nTextLineField, I18nTextField, I18nHTMLField

    >>> class IMyI18nContent(Interface):
    ...     name = TextLine(title='Name')
    ...     text_line = I18nTextLineField(title="Text line field",
    ...                                   default={'de': 'German text'})
    ...     text = I18nTextField(title="Text field")
    ...     html = I18nHTMLField(title="HTML field")

    >>> @implementer(IMyI18nContent)
    ... class MyI18nContent:
    ...     name = FieldProperty(IMyI18nContent['name'])
    ...     text_line = FieldProperty(IMyI18nContent['text_line'])
    ...     text = FieldProperty(IMyI18nContent['text'])
    ...     html = FieldProperty(IMyI18nContent['html'])

    >>> my_content = MyI18nContent()

Instance attributes are then set as mappings, where keys are the language codes and values are
classic values matching each field type:

    >>> value = {'en': "Invalid text line\n", 'fr': "Ligne de texte valide"}
    >>> IMyI18nContent['text_line'].validate(value)
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.WrongContainedType: ([ConstraintNotSatisfied('Invalid text line\n', '')], 'text_line')

    >>> value = {'en': "Text line", 'fr': "Ligne de texte"}
    >>> IMyI18nContent['text_line'].validate(value)

    >>> my_content.name = 'Name'
    >>> my_content.text_line = value


Getting translated values
-------------------------

The :py:class:`II18n <pyams_i18n.interfaces.II18n>` interface is used to query an I18n value; the
returned value is trying to match browser settings with offered languages: if a requested language
is not defined or have an empty value, the value defined for the default server language will be
used:

    >>> from pyams_i18n.interfaces import II18n
    >>> i18n = II18n(my_content)
    >>> i18n.query_attribute('text_line', request=request)
    'Text line'

Getting value of a classic attribute shouldn't raise an exception:

    >>> i18n.query_attribute('name', request=request)
    'Name'

Of course, we can change browser settings to get another translated value:

    >>> request = DummyRequest(headers={'Accept-Language': 'fr, en-US;q=0.9'})
    >>> i18n.query_attribute('text_line', request=request)
    'Ligne de texte'

    >>> request = DummyRequest(headers={'Accept-Language': 'es, en-US;q=0.9'})
    >>> i18n.query_attribute('text_line', request=request)
    'Text line'

It's also possible to get any translated value "as is", without using request headers, eventually
by providing a default value:

    >>> i18n.get_attribute('name', request=request) is None
    True
    >>> i18n.get_attribute('text_line', request=request) is None
    True
    >>> i18n.get_attribute('text_line', lang='es') is None
    True
    >>> i18n.get_attribute('text_line', lang='es', default='Linea de texto')
    'Linea de texto'
    >>> i18n.get_attribute('text_line', lang='fr', request=request)
    'Ligne de texte'

Another option is to use a request or session parameter to define user's language; this can be
helpful, for example when you want to preview your web site in different languages, without the
need to modify your browser settings (this feature is used by PyAMS_content package):

    >>> request = DummyRequest(params={'lang': 'fr'})
    >>> i18n.query_attribute('text_line', request=request)
    'Ligne de texte'

    >>> request = DummyRequest()
    >>> request.session['language'] = 'fr'
    >>> i18n.query_attribute('text_line', request=request)
    'Ligne de texte'

Getting an un-translated lang may return default value, if any:

    >>> i18n.query_attribute('text_line', lang='de', default=IMyI18nContent['text_line'].default)
    'German text'


Getting request locale
----------------------

Locale can be extracted from request:

    >>> from pyams_i18n.negotiator import locale_negotiator

    >>> request = DummyRequest(headers={'Accept-Language': 'fr, en-US;q=0.9'})
    >>> locale_negotiator(request)
    'fr'

A Zope equivalent locale is also available for compatibility:

    >>> from pyams_i18n.negotiator import get_locale

    >>> request = DummyRequest(headers={'Accept-Language': 'fr, en-US;q=0.9'})
    >>> get_locale(request)
    <zope.i18n.locales.Locale object at 0x...>


I18n TALES expression
---------------------

An "i18n:" TALES expression is available to get I18n attributes directly from Chameleon templates;
this test is using PyAMS_template template factory, but this should work with any Chameleon
template:

    >>> import os
    >>> from tempfile import mkdtemp
    >>> temp_dir = mkdtemp()
    >>> template = os.path.join(temp_dir, 'template.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write('<div>${i18n:context.text_line}</div>')

    >>> from pyramid.interfaces import IRequest
    >>> from pyams_template.interfaces import IContentTemplate
    >>> from pyams_template.template import TemplateFactory, get_content_template
    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (Interface, IRequest, Interface), IContentTemplate)

    >>> from pyams_utils.adapter import ContextRequestAdapter
    >>> @implementer(Interface)
    ... class MyContentView(ContextRequestAdapter):
    ...     template = get_content_template()
    ...     def __call__(self):
    ...         return self.template(**{'context': self.context, 'request': self.request})

    >>> my_view = MyContentView(my_content, request)
    >>> print(my_view())
    <div>Ligne de texte</div>

Using a different request setting should return another result:

    >>> request = DummyRequest()
    >>> my_view = MyContentView(my_content, request)
    >>> print(my_view())
    <div>Text line</div>

Another option is to use the "i18n" TALES extension, as provided by PyAMS_utils; the benefit of
this method is that it also provides a default value if requested property doesn't exist:

    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${tales:i18n(context, 'missing_property', 'Default value')}</div>")
    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (Interface, IRequest, Interface), IContentTemplate)

    >>> my_view = MyContentView(my_content, request)
    >>> print(my_view())
    <div>Default value</div>


I18n traverser
--------------

A "++i18n++" traverser can be used to get a direct access to an internal I18n attribute; this is
actually used to get access to I18n file fields values.

You can specify attribute name and lang like this:

    >>> from pyams_i18n.attr import I18nAttributeTraverser
    >>> traverser = I18nAttributeTraverser(my_content)
    >>> traverser.traverse('text_line:en')
    'Text line'
    >>> traverser.traverse('text_line:fr')
    'Ligne de texte'

    >>> traverser.traverse('missing_property')
    Traceback (most recent call last):
    ...
    pyramid.httpexceptions.HTTPNotFound: The resource could not be found.


Tests cleanup:

    >>> tearDown()
