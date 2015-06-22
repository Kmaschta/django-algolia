# -*- coding: utf-8 -*-
import pytest

from django.core.exceptions import ImproperlyConfigured

from yupeekapi.libs.algolia import AlgoliaIndexer


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


def test_init_success(indexer, configs_success):
    assert indexer.configs == configs_success


def test_init_wrong(configs_wrong):
    try:
        AlgoliaIndexer(configs_wrong)
        assert False
    except ImproperlyConfigured:
        assert True


def test_get_client(indexer):
    assert indexer.client == indexer.get_client()


def test_get_index_name(indexer):
    class MyModel():
        pass

    instance = MyModel()

    # Return the correct name
    assert indexer._get_index_name(instance) == 'MyModelDjangoAlgolia'
    assert indexer._get_index_name(model=MyModel) == 'MyModelDjangoAlgolia'

    assert indexer._get_index_name(instance, with_suffix=False) == 'MyModel'
    assert indexer._get_index_name(model=MyModel, with_suffix=False) == 'MyModel'

    # Raise exception if bad parameters
    try:
        indexer._get_index_name(instance, MyModel)
        assert False
    except ValueError:
        assert True

    try:
        indexer._get_index_name()
        assert False
    except ValueError:
        assert True

    # React well depending on the configurations
    indexer.configs['INDEX_SUFFIX'] = 'OtherSuffix'
    assert indexer._get_index_name(instance) == 'MyModelOtherSuffix'
    assert indexer._get_index_name(model=MyModel) == 'MyModelOtherSuffix'

    indexer.configs['SUFFIX_MY_INDEX'] = False
    assert indexer._get_index_name(instance, with_suffix=False) == 'MyModel'
    assert indexer._get_index_name(model=MyModel, with_suffix=False) == 'MyModel'


def test_search(indexer):
    class MyModel():
        pass

    indexer.configs['TEST_MODE'] = True
    assert indexer.search(MyModel, 'test') == indexer.test_response
