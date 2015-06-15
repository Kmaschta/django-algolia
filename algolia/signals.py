# -*- coding: utf-8 -*-
import warnings

from django.db import models

from .utils import is_algolia_managed
from .indexer import AlgoliaIndexer

__all__ = ['RealtimeSignalProcessor']


class BaseSignalProcessor(object):
    """Abstract base class for Algolia signal processing"""

    def __init__(self, indexer=None):
        """
        Loads Algolia settings and its indexer before to run the signal setup.
        """
        if indexer:
            self.indexer = indexer
        else:
            self.indexer = AlgoliaIndexer()

        if self.indexer.is_valid:
            if not self.indexer.configs.get('TEST_MODE', False):
                self.setup()
        else:
            warnings.warn('Could not run Algolia signals processing because '
                          'your settings are misconfigured. Check your configuration.')

    def setup(self):
        """Sets up the signal processing"""
        raise NotImplementedError(
            'BaseSignalProcessor is an abstract class, '
            'you have to build a child class which inherit from it'
        )

    def teardown(self):
        """Tears down the signal processing"""
        raise NotImplementedError(
            'BaseSignalProcessor is an abstract class, '
            'you have to build a child class which inherit from it'
        )

    def handle_save(self, *args, **kwargs):
        """Function that will be executed on the instance's storing"""
        # Do the flop
        pass

    def handle_delete(self, *args, **kwargs):
        """Function that will be executed on the instance's deletion"""
        # Don't do the flop
        pass


class RealtimeSignalProcessor(BaseSignalProcessor):
    """
    Real time signal processing for django models which have 'ALGOLIA_INDEX' constant specified.

    At the instance creation and deletion, this signal processor will update the Algolia Index
    and store the information on a AlgoliaIndex object.

    Use:
        class MyPony(models.Model):
            ALGOLIA_INDEX = 'MyPonyIndex'
            ALGOLIA_INDEX_FIELDS = ('name', 'clogs_number',)

            name = models.CharField(max_length=255)
            clogs_number = models.IntegerField()
    """

    def setup(self):
        """Attaches signals to all models"""
        models.signals.post_save.connect(self.handle_save)
        models.signals.pre_delete.connect(self.handle_delete)

    def teardown(self):
        """Removes the signals from models"""
        models.signals.post_save.disconnect(self.handle_save)
        models.signals.pre_delete.disconnect(self.handle_delete)

    def handle_save(self, sender, instance, created=False, *args, **kwargs):
        """If this model is managed by the library save it to the algolia index"""
        if is_algolia_managed(instance):
            self.indexer.save(instance, created=created)

    def handle_delete(self, sender, instance, *args, **kwargs):
        """If this model is managed by the library, delete it from the algolia index"""
        if is_algolia_managed(instance):
            self.indexer.delete(instance)
