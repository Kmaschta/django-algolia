# -*- coding: utf-8 -*-
import warnings

from django.conf import settings
from django.db.models import get_models
from django.core.exceptions import ImproperlyConfigured

from algoliasearch import algoliasearch

from .utils import get_instance_fields, is_algolia_managed
from .models import AlgoliaIndex

__all__ = ['AlgoliaIndexer']


class AlgoliaIndexer(object):
    """Algolia Indexer uses 'algoliasearch' library and django signals to automatically
    register and update Algolia index at model's saving or deletion

    See:
        https://github.com/algolia/algoliasearch-client-python

    Settings:
        ALGOLIA = {
            # Required settings
            'API_KEY': '********',
            'API_SECRET': '***************************',
            # Defaults settings
            'SIGNAL_PROCESSOR': 'algolia.signals.RealtimeSignalProcessor',
            'SUFFIX_MY_INDEX': True,
            'INDEX_SUFFIX': 'DjangoAlgolia',
            'TEST_MODE': False,
        }
    """

    client = None
    is_valid = False

    # Returned content for test mode
    test_response = {
        u'hits': [],
        u'processingTimeMS': 1,
        u'nbHits': 0,
        u'hitsPerPage': 20,
        u'params':
        u'query=',
        u'nbPages': 0,
        u'query': u'',
        u'page': 0,
    }

    def __init__(self, configs=None):
        """Loads Algolia settings, check settings and loads algolia client"""
        if configs:
            self.configs = configs
        else:
            self.configs = getattr(settings, 'ALGOLIA', {})

        quiet = self.configs.get('QUIET', False) or self.configs.get('TEST_MODE', False)
        self.check_settings(quiet)
        self.get_client()

    def check_settings(self, quiet=False):
        """Checks if all settings are correctly set"""
        settings_to_check = ['API_KEY', 'API_SECRET']
        error_found = False

        for setting in settings_to_check:
            if not self.configs.get(setting, False):
                error_found = True
                if not quiet:
                    raise ImproperlyConfigured('Algolia {} setting is required'.format(setting))

        self.is_valid = not error_found

    def get_client(self, force_refresh=False):
        """Returns and caches the algolia's client"""
        if not self.client or force_refresh:
            self.client = algoliasearch.Client(
                self.configs.get('API_KEY'),
                self.configs.get('API_SECRET'),
            )
        return self.client

    def _get_index_name(self, instance=None, model=None, with_suffix=True):
        """Return the name of index for a specific instance or model"""
        if instance and not model:
            model = instance.__class__
        elif model and not instance:
            pass
        else:
            raise ValueError('You must specify instance or model')

        index_name = getattr(model, 'ALGOLIA_INDEX', model.__name__)

        # By default, add a suffix to index name
        # Useful to dissociate production indexes from tests indexes
        if with_suffix and self.configs.get('SUFFIX_MY_INDEX', True):
            index_name = index_name + self.configs.get('INDEX_SUFFIX', 'DjangoAlgolia')

        return index_name

    def get_index(self, instance=None, model=None, index_name=None, with_suffix=True):
        """Useful to dissociate the production indexes and the test indexes

        Use:
            instance = Model()
            get_index(instance)
            get_index(model=Model)
            get_index(index_name='MyAlgoliaIndex')
        """
        if not index_name:
            index_name = self._get_index_name(instance, model, with_suffix=with_suffix)

        return self.get_client().init_index(index_name)

    def search(self, model, query, *args, **kwargs):
        """
        Makes a query to Algolia API and return the response as a dict

        See:
            https://github.com/algolia/algoliasearch-client-python#search

        Use:
            indexer = AlgoliaIndexer()
            response = indexer.search(School, 'Hardvard')

        Note that you can specify all parameters which you can specify
        to algolia's "search" function.
        """
        if self.configs.get('TEST_MODE', False):
            return self.test_response

        index = self.get_index(model=model)
        return index.search(query, *args, **kwargs)

    def get_algolia_index(self, instance):
        """Returns the index of a specific instance"""
        index = self.get_index(instance=instance)
        return index, AlgoliaIndex.get_object_or_none(index.index_name, instance)

    def get_or_create_algolia_index(self, instance):
        """Returns the index of a specific instance and create it if necessary"""
        index, algolia_index = self.get_algolia_index(instance)
        if not algolia_index:
            algolia_index = AlgoliaIndex.create_object(index.index_name, instance)
        return index, algolia_index

    def save(self, instance, created=False):
        """Stores or updates index of a model on Algolia API"""
        fields = get_instance_fields(instance)
        kwargs = {}

        for field in fields:
            value = getattr(instance, field, None)

            try:
                value = unicode(value)
            except ValueError:
                message = ('{0}.{1} "{2}" can not be cast into a string '
                           'to be stored to Algolia Index')
                warnings.warn(message.format(instance.__class__.__name__,
                                             field, value))

            kwargs[field] = value

        index, algolia_index = self.get_or_create_algolia_index(instance)

        kwargs['objectID'] = algolia_index.id
        kwargs['__unicode__'] = unicode(instance)

        if created:
            return index.save_object(kwargs)
        else:
            return index.partial_update_object(kwargs)

    def delete(self, instance):
        """Removes index of a model on Algolia API"""
        index, algolia_index = self.get_algolia_index(instance)
        if algolia_index:
            algolia_index.delete()
            return index.delete_object(algolia_index.id)
        return None

    def is_indexed_by(self, index, model):
        if not is_algolia_managed(model):
            return False

        model_index = self.get_index(model=model)
        return model_index.index_name == index.index_name

    def get_models(self, index):
        """Get models for a given index"""
        return [model for model in get_models() if self.is_indexed_by(index, model)]

    def rebuild_index(self, index):
        """Clears index and reconstructs it from all associated models

        Be careful, this process can be very long."""
        index.clear_index()
        index_name = index.index_name

        queryset = AlgoliaIndex.objects.filter(index=index_name)
        queryset.delete()

        for model in self.get_models(index):
            for instance in model.objects.all():
                self.save(instance)
