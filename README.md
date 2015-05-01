# django-algolia
Synchronize your models with the Algolia API for easier and faster searches.

=> [Documentation](http://django-algolia.readthedocs.org/en/latest/) 

<a href="http://django-algolia.readthedocs.org/en/latest/" target="_blank"><img src='https://readthedocs.org/projects/django-algolia/badge/?version=latest' alt='Documentation Status' /></a>
<a href="https://travis-ci.org/Kmaschta/django-algolia" target="_blank"><img src="https://travis-ci.org/Kmaschta/django-algolia.svg?branch=master" alt='Travis CI Status' /></a>

# Compatibilities & Requirements

- algoliasearch >= 1.5.2

|Language  | 2.7 | 3.4  |
|:--------:|:---:|:----:|
|**Python**| V   | X    |

|Framework | 1.6 | 1.7  | 1.8 |
|:--------:|:---:|:----:|:---:|
|**Django**| V   | X    | X   |

The compatibility to the latest versions are planned, you can participate if you want : Feel free to [open an issue](https://github.com/Kmaschta/django-algolia/issues/new).

# TL;DR

- Install the app:
```bash
pip install -e git+https://github.com/Kmaschta/django-algolia.git#egg=dev
```

- Register to Algolia and make configure your settings:
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

- Specify what models and what fields should be indexed 
```python
class MyPony(models.Model):
  ALGOLIA_INDEX_FIELDS = ('name', 'clogs_number',)

  name = models.CharField(max_length=255)
  clogs_number = models.IntegerField()
```

- Load database migrations:
```bash
./manage.py migrate
```

- Build remote index (you don't have to do it twice)
```bash
./manage.py rebuild_algolia_index --model=MyPony
```

- Search your datas
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
