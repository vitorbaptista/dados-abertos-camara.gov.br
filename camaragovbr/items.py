# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProposicaoVotadaItem(scrapy.Item):
    id = scrapy.Field()
    nome = scrapy.Field()
    data_votacao = scrapy.Field()
    tipo = scrapy.Field()
    numero = scrapy.Field()
    ano = scrapy.Field()


class ProposicaoItem(scrapy.Item):
    tipo = scrapy.Field()
    numero = scrapy.Field()
    ano = scrapy.Field()
    id = scrapy.Field()
    id_proposicao_principal = scrapy.Field()
    nome = scrapy.Field()
    nome_proposicao_origem = scrapy.Field()
    tipo = scrapy.Field()
    tema = scrapy.Field()
    ementa = scrapy.Field()
    explicacao_ementa = scrapy.Field()
    autor = scrapy.Field()
    data_apresentacao = scrapy.Field()
    regime_tramitacao = scrapy.Field()
    ultimo_despacho = scrapy.Field()
    ultimo_despacho_data = scrapy.Field()
    apreciacao = scrapy.Field()
    indexacao = scrapy.Field()
    situacao = scrapy.Field()
    link_inteiro_teor = scrapy.Field()


class VotacaoProposicaoItem(scrapy.Item):
    sigla = scrapy.Field()
    numero = scrapy.Field()
    ano = scrapy.Field()
    votacoes = scrapy.Field()
