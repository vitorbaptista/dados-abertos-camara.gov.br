# -*- coding: utf-8 -*-
import scrapy.contrib.spiders as spiders
import scrapy
import datetime
import camaragovbr.items


class ProposicoesVotadasEmPlenarioSpider(spiders.XMLFeedSpider):
    name = 'proposicoes_votadas_em_plenario'
    allowed_domains = ['http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesVotadasEmPlenario']
    iterator = 'xml'
    itertag = './proposicao'

    def __init__(self, start_year=1991, *args, **kwargs):
        super(ProposicoesVotadasEmPlenarioSpider, self).__init__(*args, **kwargs)
        self.start_urls = self._generate_start_urls(start_year)

    def parse_node(self, response, node):
        proposicao = camaragovbr.items.ProposicaoItem()

        codigo = int(node.xpath('./codProposicao/text()').extract()[0])
        nome = node.xpath('./nomeProposicao/text()').extract()[0].strip()
        dataVotacao = node.xpath('./dataVotacao/text()').extract()[0].strip()
        tipo = nome.split(' ')[0]
        numero, ano = nome.split(' ')[1].split('/')
        proposicao['codigo'] = codigo
        proposicao['nome'] = nome
        proposicao['data_votacao'] = dataVotacao
        proposicao['tipo'] = tipo
        proposicao['numero'] = numero
        proposicao['ano'] = ano

        yield proposicao

    def _generate_start_urls(self, start_year):
        url = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesVotadasEmPlenario?ano={YEAR}&tipo='
        start_year = int(start_year)
        current_year = datetime.date.today().year
        start_urls = [url.replace('{YEAR}', str(year))
                      for year in xrange(start_year, current_year + 1)]
    
        return start_urls
