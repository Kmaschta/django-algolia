# -*- coding: utf-8 -*-
from optparse import make_option

from django.conf import settings
from django.db.models.loading import get_model
from django.core.management.base import BaseCommand, CommandError

from yupeekapi.libs.algolia import AlgoliaIndexer


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--index-name',
            action='store',
            dest='index_name',
            type='string',
            default='',
            help='Name of the index to rebuild',
        ),
    )

    option_list = option_list + (
        make_option(
            '--model',
            action='store',
            dest='model_name',
            type='string',
            default='',
            help='Name of associated model for index to rebuild',
        ),
    )

    def handle(self, *args, **options):

        index_name = options['index_name']
        model_name = options['model_name']

        if not index_name and not model_name:
            raise CommandError('Invalid index. Use the flag --model=MyModel or '
                               '--index-name=IndexName to specify it.')

        if index_name and model_name:
            raise CommandError('Invalid index. You can not specify index name and model.')

        indexer = AlgoliaIndexer()

        if model_name:
            model = None
            # @todo: Find a better way to retrieve django's apps
            apps = [app.split('.')[-1] for app in settings.INSTALLED_APPS]

            for app in apps:
                fetched_model = get_model(app, model_name)

                if fetched_model:
                    model = fetched_model

            if not model:
                raise CommandError('Unable to find "{}" model to all applications : {}'.format(
                    model_name,
                    ', '.join(apps),
                ))

            index = indexer.get_index(model=model)
        else:
            index = indexer.get_index(index_name=index_name, with_suffix=False)

        self.stdout.write('Indexing to Algolia API ...')
        indexer.rebuild_index(index)
