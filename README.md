# django-algolia
Synchronize your models with the Algolia API for easier and faster searches

# Development
Django-algolia is in development version. All that remains to be done before potentially usable version:
- Unit tests
- Documentation
- Django 1.7, 1.8 support
- Python 3.4 support

Feel free to create an issue for any question or suggestion !

# TL;DR - Getting started
Install with
```bash
pip install -e git+https://github.com/Kmaschta/django-algolia.git#egg=dev
```

Check your configuration

```python
INSTALLED_APPS = [
  # [...]
  'algolia',
]

ALGOLIA = {
  'API_KEY': '******',
  'API_SECRET': '*********************',
}
```

Load DB migrations
```bash
./manage.py migrate
```

Configure your models
```python
class MyPony(models.Model):
  ALGOLIA_INDEX_FIELDS = ('name', 'clogs_number',)

  name = models.CharField(max_length=255)
  clogs_number = models.IntegerField()
```

Build index to Algolia API for the first time (you don't have to do it twice)
```bash
./manage.py rebuild_algolia_index
```

Search your datas
```python
from algolia import AlgoliaIndexer
from my.project.models import MyPony
indexer = AlgoliaIndexer()
results = indexer.search(MyPony, 'Rainbow Dash')

# results content
{
    u'hits': [
      {...}
    ],
    u'processingTimeMS': 1,
    u'nbHits': 0,
    u'hitsPerPage': 20,
    u'params':
    u'query=Rainbow Dash',
    u'nbPages': 0,
    u'query': u'',
    u'page': 0,
}
```
