# -*- coding: utf-8 -*-
from django.db import models

__all__ = ['AlgoliaIndex']


def get_model_identifier(model):
    """Returns a model identifier string like : app.Model

    Tests:
        >>> get_model_identifier(AlgoliaIndex)
        'algolia.AlgoliaIndex'

        >>> from django.contrib.auth.models import User
        >>> get_model_identifier(User)
        'auth.User'

        >>> get_model_identifier(object)
        Traceback (most recent call last):
        AttributeError: type object 'object' has no attribute '_meta'

        >>> get_model_identifier()
        Traceback (most recent call last):
        TypeError: get_model_identifier() takes exactly 1 argument (0 given)
    """
    return '{0}.{1}'.format(model._meta.app_label, model.__name__)


def get_instance_identifier(instance):
    """
    Returns an instance identifier string like app.Model.X
    where X is primary key of instance

    Tests:
        >>> instance = AlgoliaIndex()
        >>> instance.pk = 42
        >>> get_instance_identifier(instance)
        'algolia.AlgoliaIndex.42'

        >>> wrong_instance = object()
        >>> get_instance_identifier(wrong_instance)
        Traceback (most recent call last):
        AttributeError: type object 'object' has no attribute '_meta'

        >>> get_instance_identifier()
        Traceback (most recent call last):
        TypeError: get_instance_identifier() takes exactly 1 argument (0 given)
    """
    model_identifier = get_model_identifier(instance.__class__)
    return '{0}.{1}'.format(model_identifier, instance.pk)


class AlgoliaIndex(models.Model):
    """
    A model which stores in databases all elements
    indexed on Algolia website
    """

    unique_together = ('index', 'instance_identifier')

    index = models.CharField(
        max_length=255,
        help_text='Algolia index where the model is indexed',
    )

    instance_identifier = models.CharField(
        max_length=1000,
        help_text='Instance identifier like : app.Model.X '
                  'where X is primary key of instance',
    )

    @classmethod
    def get_object_or_none(cls, index, instance):
        """
        Return the corresponding AlgoliaIndex object if it exists,
        else return None
        """
        try:
            return cls.objects.get(
                index=index,
                instance_identifier=get_instance_identifier(instance),
            )
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_object(cls, index, instance):
        """
        Creates and returns AlgoliaIndex object
        """
        obj = cls(
            index=index,
            instance_identifier=get_instance_identifier(instance),
        )
        obj.save()
        return obj

    @classmethod
    def delete_object(cls, object_id):
        """Deletes AlgoliaIndex object with the specified id"""
        try:
            obj = cls.objects.filter(id=object_id)
            obj.delete()
        except cls.DoesNotExist:
            pass
