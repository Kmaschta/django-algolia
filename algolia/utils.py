# -*- coding: utf-8 -*-
import warnings

from django.conf import settings
from django.utils import importlib

__all__ = ['get_signal_processor_class', 'is_algolia_managed']

if not settings.configured:
    settings.configure(DEBUG=True, ALGOLIA={'QUIET': True})

def import_class(path):
    """Import a class from pattern like : path.to.the.Class"""

    path_bits = path.split('.')
    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = importlib.import_module(module_path)

    if not hasattr(module_itself, class_name):
        raise ImportError("The Python module '%s' has no '%s' class." % (module_path, class_name))

    return getattr(module_itself, class_name)


def get_settings():
    """Return Algolia settings as a dict"""
    return getattr(settings, 'ALGOLIA', {})


def get_signal_processor_class():
    """Return the signal processor class selected in Algolia settings"""

    algolia_settings = get_settings()
    signal_processor_path = algolia_settings.get(
        'SIGNAL_PROCESSOR',
        'algolia.signals.RealtimeSignalProcessor'
    )
    try:
        return import_class(signal_processor_path)
    except ImportError:
        warnings.warn('Could not run Algolia signals processing because '
                      'your settings are misconfigured. Check your configuration.')
        return object


def get_instance_fields(instance):
    return getattr(instance, 'ALGOLIA_INDEX_FIELDS', [])


def is_algolia_managed(instance):
    return hasattr(instance, 'ALGOLIA_INDEX_FIELDS')
