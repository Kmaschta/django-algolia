#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Synchronize your models with the Algolia API for easier and faster searches"""

__version__ = '0.1'

from .utils import get_signal_processor_class
from .backends import AlgoliaIndexer

__all__ = ['AlgoliaIndexer']

signal_processor_class = get_signal_processor_class()
signal_processor = signal_processor_class()
# At this point, all signals are attached to models
