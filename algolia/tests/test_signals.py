# -*- coding: utf-8 -*-
import pytest

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete

from .fixtures import BaseSignalProcessor, RealtimeSignalProcessor


def assert_true(*args, **kwars):
    assert True


def assert_false(*args, **kwargs):
    assert False


@pytest.fixture()
def indexer_on_valid_mode():
    indexer = BaseSignalProcessor().indexer
    indexer.is_valid = True
    indexer.save = assert_true
    indexer.delete = assert_true
    return indexer


@pytest.fixture()
def indexer_on_test_mode():
    indexer = indexer_on_valid_mode()
    indexer.configs = {'TEST_MODE': True}
    return indexer


@pytest.fixture()
def base_processor():
    return BaseSignalProcessor()


@pytest.fixture()
def realtime_processor():
    return RealtimeSignalProcessor(indexer_on_valid_mode())


@pytest.fixture()
def managed_class():
    class MyClass():
        ALGOLIA_INDEX_FIELDS = ['some', 'fields']
    return MyClass


@pytest.fixture()
def managed_instance():
    return managed_class()()


def test_base_init(base_processor, indexer_on_test_mode):
    base_processor.setup = assert_false
    base_processor.__init__(indexer_on_test_mode)
    assert True


def test_base_setup(base_processor):
    try:
        base_processor.setup()
        assert False
    except NotImplementedError:
        # BaseSignalProcessor raise a NotImplementedError at the setup
        # So at this point, the test is done
        assert True


def test_base_teardown(base_processor):
    try:
        base_processor.teardown()
        assert False
    except NotImplementedError:
        # BaseSignalProcessor raise a NotImplementedError at the teardown
        # So at this point, the test is done
        assert True


def test_realtime_setup(indexer_on_test_mode):
    realtime_processor = RealtimeSignalProcessor(indexer_on_test_mode)

    assert len(post_save.receivers) == 0
    assert len(pre_delete.receivers) == 0

    realtime_processor.setup()

    assert len(post_save.receivers) == 1
    assert len(pre_delete.receivers) == 1


def test_realtime_teardown(realtime_processor):
    assert len(post_save.receivers) == 1
    assert len(pre_delete.receivers) == 1

    realtime_processor.teardown()

    assert len(post_save.receivers) == 0
    assert len(pre_delete.receivers) == 0


def test_realtime_handle_save(realtime_processor, managed_class, managed_instance):
    realtime_processor.handle_save(managed_class, managed_instance, True)
    realtime_processor.handle_save(managed_class, managed_instance, False)


def test_realtime_handle_delete(realtime_processor, managed_class, managed_instance):
    realtime_processor.handle_delete(managed_class, managed_instance)
