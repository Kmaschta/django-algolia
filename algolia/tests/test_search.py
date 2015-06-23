# -*- coding: utf-8 -*-
import pytest

import algolia
from algolia.search import AlgoliaResult
from algolia.utils import test_algolia_response

from .fixtures import configs_success, indexer


def test_algolia_result(indexer):
    # Prepare fixtures
    class MyModel():
        pass

    raw = test_algolia_response
    query = 'jim'
    query_params = {'some': ['great', 'params']}
    indexer.configs['TEST_MODE'] = True

    # Building result
    result = AlgoliaResult(MyModel, raw, query, query_params, indexer=indexer)

    # Attributes
    assert result.raw == raw
    assert result.model == MyModel
    assert result.query == query
    assert result.query_params == query_params
    assert result.indexer == indexer

    # Properties
    assert result.hits == raw.get('hits')
    assert result.count == raw.get('nbHits')
    assert result.page == raw.get('page') + 1
    assert result.nb_pages == raw.get('nbPages') + 1
    assert result.facets == raw.get('facets')
    assert result.facets_stats == raw.get('facets_stats')

    # @TODO: Fake DB query or mock
    # ids = [hit['id'] for hit in raw.get('hits')]
    # assert result.instances == MyModel.objects.filter(id__in=ids)

    # Iteration of next page
    next_result = result.next()
    assert result != next_result
    # @TODO : Check if next page is page + 1, avoid test_response


def test_search(indexer):
    class MyModel():
        pass

    indexer.configs['TEST_MODE'] = True
    result = algolia.search(MyModel, 'test', indexer=indexer)
    assert result.raw == indexer.test_response
