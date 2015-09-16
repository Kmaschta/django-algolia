# What is Django-Algolia ?

Django-Algolia helps you to synchronize your models with the [Algolia](https://www.algolia.com/)'s API and makes your search or autocomplete system easier.

## Algolia

In their own words:

> A powerful API built for developers, Algolia delivers relevant results in your mobile apps and websites from the first keystroke.

This django app has been built to connect to Algolia API and you have to create an account on their website if you want to use it.

# Compatibilities & Requirements

- algoliasearch >= 1.5.2

|Language  | 2.7 | 3.4  |
|:--------:|:---:|:----:|
|**Python**| V   | V    |

|Framework | 1.6 | 1.7  | 1.8 |
|:--------:|:---:|:----:|:---:|
|**Django**| V   | V    | V   |

The compatibility to the latest versions are planned, you can participate if you want : Feel free to [open an issue](https://github.com/Kmaschta/django-algolia/issues/new).

# TL;DR - Getting started

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
    'hits': [
      {...}
    ],
    'processingTimeMS': 1,
    'nbHits': 0,
    'hitsPerPage': 20,
    'params':
    'query=Rainbow Dash',
    'nbPages': 0,
    'query': '',
    'page': 0,
}
```
