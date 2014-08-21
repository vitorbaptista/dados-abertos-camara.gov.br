# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProposicaoItem(scrapy.Item):
    codigo = scrapy.Field()
    nome = scrapy.Field()
    data_votacao = scrapy.Field()
    tipo = scrapy.Field()
    numero = scrapy.Field()
    ano = scrapy.Field()
