# -*- coding: utf-8 -*-
import csv
import datetime
import scrapy.contrib.spiders as spiders
import xmltodict
import camaragovbr.items


class ProposicoesSpider(spiders.XMLFeedSpider):
    name = 'proposicoes'
    allowed_domains = ['http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID']
    iterator = 'xml'
    itertag = 'proposicao'
    PROPOSICOES_VOTADAS_FILE_PATH = 'data/proposicoes_votadas.csv'

    def start_requests(self):
        url = "http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID?IdProp={0}"

        with open(self.PROPOSICOES_VOTADAS_FILE_PATH, 'rb') as f:
            reader = csv.DictReader(f)
            urls = {url.format(v['id'])
                    for v in reader}

        return (self.make_requests_from_url(u) for u in urls)

    def parse_node(self, response, node):
        proposicao = camaragovbr.items.ProposicaoItem()
        xml = xmltodict.parse(node.extract())['proposicao']
        try:
            proposicao['tipo'] = xml['@tipo'].strip()
            proposicao['numero'] = int(xml['@numero'])
            proposicao['ano'] = int(xml['@ano'])
        except KeyError:
            # Ignora proposições apensadas
            return
        proposicao['id'] = int(xml['idProposicao'])
        if xml.get('idProposicaoPrincipal'):
            proposicao['id_proposicao_principal'] = int(xml['idProposicaoPrincipal'])
        proposicao['nome'] = xml['nomeProposicao']
        proposicao['nome_proposicao_origem'] = xml['nomeProposicao']
        proposicao['tipo'] = xml['tipoProposicao']
        proposicao['tema'] = xml['tema']
        proposicao['ementa'] = xml['Ementa']
        proposicao['explicacao_ementa'] = xml['ExplicacaoEmenta']
        proposicao['autor'] = xml['Autor']
        proposicao['data_apresentacao'] = self._parse_date(xml['DataApresentacao'])
        proposicao['regime_tramitacao'] = xml['RegimeTramitacao']
        proposicao['ultimo_despacho'] = xml['UltimoDespacho'].get('#text')
        if xml['UltimoDespacho'].get('@Data'):
            proposicao['ultimo_despacho_data'] = self._parse_date(xml['UltimoDespacho']['@Data'])
        proposicao['apreciacao'] = xml['Apreciacao']
        proposicao['indexacao'] = xml['Indexacao']
        proposicao['situacao'] = xml['Situacao']
        proposicao['link_inteiro_teor'] = xml['LinkInteiroTeor']

        yield proposicao

    def _parse_date(self, date, dateFormat='%d/%m/%Y'):
        return datetime.datetime.strptime(date, dateFormat)
