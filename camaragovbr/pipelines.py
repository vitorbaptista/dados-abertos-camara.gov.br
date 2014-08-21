# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import camaragovbr.items


class RemoveDuplicateProposicoesPipeline(object):
    def __init__(self):
        self.hashes_proposicoes = set()

    def process_item(self, item, spider):
        if isinstance(item, camaragovbr.items.ProposicaoItem):
            itemHash = str(item['codigo']) + str(item['data_votacao'])
            if itemHash in self.hashes_proposicoes:
                raise DropItem('Proposicao duplicada codigo %s e data %s' %
                               (item['codigo'], item['data_votacao']))
            else:
                self.hashes_proposicoes.add(itemHash)
        return item
