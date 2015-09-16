Django-algolia has only a few settings, most are configured by default.

```python
ALGOLIA = {
    # Required settings
    'API_KEY': '********',
    'API_SECRET': '***************************',
    # Defaults settings
    'SIGNAL_PROCESSOR': 'algolia.signals.RealtimeSignalProcessor',
    'SUFFIX_MY_INDEX': True,
    'INDEX_SUFFIX': 'DjangoAlgolia',
    'TEST_MODE': False,
}
```

### API_KEY & API_SECRET

These credentials are provided when you register on [Algolia](https://www.algolia.com/). These are the only necessary settings.

### SIGNAL_PROCESSOR

The signal processor is the class which attaches the signals to Django Models for updates Algolia search indexes when you change save your datas.

**Default:** `algolia.signals.RealtimeSignalProcessor`

### SUFFIX_MY_INDEX

When you save an instance of Django Model in your database, Django-Algolia retrieve its informations for store them into a index.

This index is defined by the name of Django Model. If your class is called `MyLittlePony`, by default its index will be called `MyLittlePonyDjangoAlgolia`.

There is multiple good reasons to suffix these indexes, but you can desactivate this feature or change the suffix by default.

**Default:** `True`

### INDEX_SUFFIX

If SUFFIX_MY_INDEX is set to `True`, Django-Algolia add the content of this setting after the name of model for build the name of its index.

It's very useful if you are many developers with the same API's credentials :

- `'INDEX_SUFFIX': 'AnisIndex'`
- `'INDEX_SUFFIX': 'KevinIndex'`
- ...

Or if you have several settings file for different use case :

- `'INDEX_SUFFIX': 'ProductionIndex'`
- `'INDEX_SUFFIX': 'StagingIndex'`
- `'INDEX_SUFFIX': 'TestIndex'`
- ...

**Default:** `DjangoAlgolia`

### TEST_MODE

You can activate a test mode. If this is the case, Django-Algolia will no longer request the Algolia's API and when yo'll do a search query, it will return a "test data" defined in the AlgoliaIndexer (actually empty).

Useful if you run unit tests or if you have an integration continue system.