# -*- coding: utf-8 -*-
from .indexer import AlgoliaIndexer
from .utils import get_instance_settings


def make_request(model, query, query_params, indexer=None, *args, **kwargs):
    # Retrieve an indexer
    if not indexer:
        indexer = AlgoliaIndexer()

    # If test mode, return a test pool of data
    if indexer.configs.get('TEST_MODE', False):
        return indexer.test_response

    # Retrieve an algolia index
    index = indexer.get_index(model=model)

    return index.search(query, query_params, *args, **kwargs)


class AlgoliaResult(object):
    """Algolia Result"""

    def __init__(self, model, raw, query=None, query_params={}, indexer=None):
        self.raw = raw
        self.model = model
        self.query = query
        self.query_params = query_params
        self.indexer = indexer

    @property
    def hits(self):
        return self.raw.get('hits', [])

    @property
    def instances(self):
        ids = [hit['id'] for hit in self.hits]
        return self.model.objects.filter(id__in=ids)

    @property
    def count(self):
        return self.raw.get('nbHits', 0)

    @property
    def page(self):
        return self.raw.get('page', 0) + 1

    @property
    def nb_pages(self):
        return self.raw.get('nbPages', 1)

    @property
    def facets(self):
        return self.raw.get('facets', {})

    @property
    def facets_stats(self):
        return self.raw.get('facets_stats', {})

    @property
    def __dict__(self):
        return {
            'model': self.model,
            'instances': self.instances,
            'count': self.count,
            'page': '{}/{}'.format(self.page, self.nb_pages),
        }

    def __unicode__(self):
        return u'AlgoliaResult({})'.format(self.__dict__)

    def __repr__(self):
        return unicode(self)

    def copy(self, raw=None, query=None, query_params=None):
        if not raw:
            raw = self.raw
        if not query:
            query = self.query
        if not query_params:
            query_params = self.query_params

        return AlgoliaResult(
            self.model,
            raw,
            query,
            query_params,
            indexer=self.indexer,
        )

    def get_page(self, page, query_params=None):
        if not query_params:
            query_params = self.query_params
        query_params.update({'page': page - 1})

        raw = make_request(self.model, self.query, query_params,
                           indexer=self.indexer)

        return self.copy(raw, query_params=query_params)

    def next(self):
        page = self.page + 1

        if page > self.nb_pages:
            raise StopIteration

        return self.get_page(page)


def search(model, query='', params={}, page=1, indexer=None, *args, **kwargs):
    """
    Makes a query to Algolia API and return the response as an AlgoliaResponse

    See:
        https://github.com/algolia/algoliasearch-client-python#search

    Use:
        import algolia
        algolia.search(School, 'Hardvard', params={...})

    Note that you can specify all parameters which you can specify
    to algolia's "search" function.
    """

    # Build query
    query_params = get_instance_settings(model).get('query_default_params', {})
    query_params.update(params)
    query_params.update({'page': page - 1})

    response = make_request(model, query, query_params, indexer=indexer, *args, **kwargs)
    return AlgoliaResult(model, response, query, query_params)
