#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""Synchronize your models with the Algolia API for easier and faster searches"""

__version__ = '0.1'

from .utils import get_signal_processor_class
from .search import search

__all__ = ['search']

signal_processor_class = get_signal_processor_class()
signal_processor = signal_processor_class()
# At this point, all signals are attached to models
