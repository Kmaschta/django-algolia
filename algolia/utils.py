# -*- coding: utf-8 -*-
import warnings

from django.conf import settings
from django.utils import importlib

__all__ = ['get_signal_processor_class', 'is_algolia_managed',
           'get_instance_fields', 'get_instance_settings']

if not settings.configured:
    settings.configure(DEBUG=True, ALGOLIA={'QUIET': True})


def import_class(path):
    """Import a class from pattern like : path.to.the.Class

    Tests:
        >>> import_class('django.db.models.Model')
        <class 'django.db.models.base.Model'>

        >>> import_class('wrong.module.Class')
        Traceback (most recent call last):
        ImportError: No module named wrong.module

        >>> import_class('algolia.utils.WrongClass')
        Traceback (most recent call last):
        ImportError: The Python module 'algolia.utils' has no 'WrongClass' class.

        >>> import_class()
        Traceback (most recent call last):
        TypeError: import_class() takes exactly 1 argument (0 given)
    """

    path_bits = path.split('.')
    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = importlib.import_module(module_path)

    if not hasattr(module_itself, class_name):
        raise ImportError("The Python module '%s' has no '%s' class." % (module_path, class_name))

    return getattr(module_itself, class_name)


def get_signal_processor_class(algolia_settings=None):
    """Return the signal processor class selected in Algolia settings

    Tests:
        >>> good = {'SIGNAL_PROCESSOR': 'algolia.signals.RealtimeSignalProcessor'}
        >>> get_signal_processor_class(good)
        <class 'algolia.signals.RealtimeSignalProcessor'>

        >>> empty = {}
        >>> get_signal_processor_class(empty)
        <class 'algolia.signals.RealtimeSignalProcessor'>

        >>> wrong = {'SIGNAL_PROCESSOR': 'some.impossible.to.find.class'}
        >>> get_signal_processor_class(wrong)
        <type 'object'>

        >>> get_signal_processor_class()
        <class 'algolia.signals.RealtimeSignalProcessor'>
    """
    if not algolia_settings:
        algolia_settings = getattr(settings, 'ALGOLIA', {})

    signal_processor_path = algolia_settings.get(
        'SIGNAL_PROCESSOR',
        'algolia.signals.RealtimeSignalProcessor'
    )

    try:
        return import_class(signal_processor_path)
    except ImportError:
        warnings.warn('Could not run ALGOLIA signals processing because '
                      'your settings are misconfigured. Check your configuration.')
        return object


def get_instance_fields(instance):
    """Return parameter attributs managed by django-algolia

    Tests:
        >>> class ManagedClass(object): ALGOLIA_INDEX_FIELDS = ['some', 'fields']
        >>> managed_instance = ManagedClass()
        >>> get_instance_fields(ManagedClass)
        ['some', 'fields']
        >>> get_instance_fields(managed_instance)
        ['some', 'fields']

        >>> class AnotherGoodClass(object): ALGOLIA_INDEX_FIELDS = ('other', 'attrs')
        >>> another_good = AnotherGoodClass()
        >>> get_instance_fields(AnotherGoodClass)
        ('other', 'attrs')
        >>> get_instance_fields(another_good)
        ('other', 'attrs')

        >>> random_stuff = object()
        >>> get_instance_fields(random_stuff)
        []

        >>> get_instance_fields()
        Traceback (most recent call last):
        TypeError: get_instance_fields() takes exactly 1 argument (0 given)
    """
    return getattr(instance, 'ALGOLIA_INDEX_FIELDS', [])


def is_algolia_managed(instance):
    """Check if the specified parameter is managed by django-algolia

    Tests:
        >>> class ManagedClass(object): ALGOLIA_INDEX_FIELDS = ['some', 'fields']
        >>> managed_instance = ManagedClass()
        >>> is_algolia_managed(ManagedClass)
        True
        >>> is_algolia_managed(managed_instance)
        True

        >>> class NotManagedClass(object): ALGOLIA_INDEX_FIELDS = []
        >>> is_algolia_managed(NotManagedClass)
        False

        >>> random_stuff = object()
        >>> is_algolia_managed(random_stuff)
        False

        >>> is_algolia_managed()
        Traceback (most recent call last):
        TypeError: is_algolia_managed() takes exactly 1 argument (0 given)
    """
    return hasattr(instance, 'ALGOLIA_INDEX_FIELDS') and bool(get_instance_fields(instance))


def get_instance_settings(instance):
    """Returns settings of an instance algolia managed

    Tests:
        >>> class ManagedClass(object): ALGOLIA_INDEX_FIELDS = ['some', 'fields']
        >>> managed_instance = ManagedClass()
        >>> get_instance_settings(ManagedClass)
        {'query_default_params': {}, 'indexing': {'attributesToIndex': ['some,fields']}}
        >>> get_instance_settings(managed_instance)
        {'query_default_params': {}, 'indexing': {'attributesToIndex': ['some,fields']}}

        >>> class OtherClass(object): ALGOLIA_INDEX_SETTINGS = {'some': 'settings'}
        >>> other_instance = OtherClass()
        >>> get_instance_settings(OtherClass)
        {'some': 'settings'}
        >>> get_instance_settings(other_instance)
        {'some': 'settings'}

        >>> class RandomClass(object): pass
        >>> get_instance_settings(RandomClass)
        {'query_default_params': {}, 'indexing': {'attributesToIndex': ['']}}

        >>> get_instance_settings()
        Traceback (most recent call last):
        TypeError: get_instance_settings() takes exactly 1 argument (0 given)
    """

    if hasattr(instance, 'ALGOLIA_INDEX_SETTINGS'):
        return getattr(instance, 'ALGOLIA_INDEX_SETTINGS')

    return {
        # See: https://www.algolia.com/doc/python#Settings
        'indexing': {
            'attributesToIndex': [','.join(get_instance_fields(instance))],
        },
        # See: https://www.algolia.com/doc/python#QueryParameters
        # See: https://www.algolia.com/doc/python#Sorting
        # See: https://www.algolia.com/doc/python#Filtering
        # See: https://www.algolia.com/doc/python#Faceting
        # See: https://www.algolia.com/doc/python#GeoSearch
        'query_default_params': {},
    }

# Algolia documentation example
test_algolia_response = {
    # array of matched hits
    "hits": [
        {
            "objectID": "1",
            "id": 42,
            "name": "Jim",
            # [... other attributes ...]
            "_highlightResult": {
                # [...]
                # See "Highlighting" section
            },
        },
        {
            "objectID": "2",
            "id": 43,
            "name": "Jimmie",
            # [... other attributes ...]
            "_highlightResult": {
                # [...]
                # See "Highlighting" section
            },
        },
    ],
    # current page number
    "page": 0,
    # total number of matched hits in the index
    "nbHits": 2,
    # total number of accessible pages
    "nbPages": 1,
    # number of hits per page
    "hitsPerPage": 20,
    # backend processing time (in milliseconds)
    "processingTimeMS": 1,
    # the computed facets, see "Faceting" section
    "facets": {
        "city": {
            "San Francisco": 1,  # associated counts
            "NYC": 1
        },
        "title": {
            "CEO": 2
        },
        # [... other facets ...]
    },
    # numeric facet stats computed on the result set, see "Faceting" section
    "facets_stats": {
        "age": {
            "min": 21,   # minimum value
            "max": 42,   # maximum value
            "avg": 31.5  # average value
        },
        # [... other stats ...]
    },
    # full-text query
    "query": "jim",
    # query parameters
    "params": "query=jim",
}
