# -*- coding: utf-8 -*-

import scrapy.contrib.exporter as exporter
from scrapy.utils.serialize import ScrapyJSONEncoder


class SortedPrettyPrintedJsonItemExporter(exporter.JsonItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file
        kwargs['sort_keys'] = kwargs.get('sort_keys', True)
        kwargs['indent'] = kwargs.get('indent', 2)
        self.encoder = ScrapyJSONEncoder(**kwargs)
        self.first_item = True
