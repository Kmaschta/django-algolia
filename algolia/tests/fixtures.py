# -*- coding: utf-8 -*-
import pytest

from algolia.indexer import AlgoliaIndexer
from algolia.signals import BaseSignalProcessor, RealtimeSignalProcessor


@pytest.fixture()
def configs_success():
    return {
        'API_KEY': 'some-api-key',
        'API_SECRET': 'some-api-secret',
    }


@pytest.fixture()
def configs_wrong():
    return {'QUIET': False}


@pytest.fixture()
def indexer(configs_success):
    return AlgoliaIndexer(configs_success)
