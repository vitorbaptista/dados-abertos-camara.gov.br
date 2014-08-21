# -*- coding: utf-8 -*-
import csv
import scrapy.contrib.spiders as spiders
import xmltodict
import camaragovbr.items


class VotacoesProposicoesSpider(spiders.XMLFeedSpider):
    name = 'votacoes_proposicoes'
    allowed_domains = ['http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao']
    iterator = 'xml'
    itertag = './proposicao'
    PROPOSICOES_VOTADAS_FILE_PATH = 'data/proposicoes_votadas.csv'

    def start_requests(self):
        url = "http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo={0}&numero={1}&ano={2}"

        with open(self.PROPOSICOES_VOTADAS_FILE_PATH, 'rb') as f:
            reader = csv.DictReader(f)
            urls = {url.format(v['tipo'], v['numero'], v['ano'])
                    for v in reader}

        return [self.make_requests_from_url(u) for u in urls]

    def parse_node(self, response, node):
        votacao = camaragovbr.items.VotacaoProposicaoItem()
        proposicao = xmltodict.parse(node.extract())['proposicao']
        votacao['sigla'] = proposicao['Sigla']
        votacao['numero'] = int(proposicao['Numero'])
        votacao['ano'] = int(proposicao['Ano'])

        votacao['votacoes'] = self._parse_votacoes(proposicao['Votacoes']['Votacao'])

        yield votacao

    def _parse_votacoes(self, votacoes):
        result = []
        if hasattr(votacoes, 'keys'):
            votacoes = [votacoes]
        for votacao in votacoes:
            aux = {
                'resumo': votacao['@Resumo'],
                'data': votacao['@Data'],
                'hora': votacao['@Hora'],
                'obj_votacao': votacao['@ObjVotacao'],
                'cod_sessao': int(votacao['@codSessao']),
            }
            orientacaoBancada = votacao.get('orientacaoBancada')
            if orientacaoBancada:
                aux['orientacao_bancada'] = self._parse_orientacao_bancada(orientacaoBancada['bancada'])
            votos = votacao.get('votos')
            if votos:
                aux['votos'] = self._parse_votos(votos['Deputado'])
            result.append(aux)
        return result

    def _parse_orientacao_bancada(self, orientacoes):
        result = []
        for orientacao in orientacoes:
            aux = {
                'sigla': orientacao['@Sigla'],
                'orientacao': orientacao['@orientacao'].strip()
            }
            result.append(aux)
        return result

    def _parse_votos(self, votos):
        result = []
        for voto in votos:
            aux = {
                'nome': voto['@Nome'],
                'partido': voto['@Partido'].strip(),
                'uf': voto['@UF'].strip(),
                'voto': voto['@Voto'].strip()
            }
            ide_cadastro = voto['@ideCadastro']
            if ide_cadastro:
                aux['ide_cadastro'] = int(ide_cadastro)
            result.append(aux)
        return result
