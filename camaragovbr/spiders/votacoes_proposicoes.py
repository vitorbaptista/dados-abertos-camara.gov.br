# -*- coding: utf-8 -*-
import scrapy.contrib.spiders as spiders
import xmltodict
import camaragovbr.items


class VotacoesProposicoesSpider(spiders.XMLFeedSpider):
    name = 'votacoes_proposicoes'
    allowed_domains = ['http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao']
    iterator = 'xml'
    itertag = './proposicao'

    def __init__(self, *args, **kwargs):
        super(VotacoesProposicoesSpider, self).__init__(*args, **kwargs)
        self.start_urls = self._generate_start_urls()

    def _generate_start_urls(self):
        return ["http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo=PL&numero=1992&ano=2007",
            "http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo=PLP&numero=349&ano=2002"]

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
        for votacao in votacoes:
            aux = {
                'resumo': votacao['@Resumo'],
                'data': votacao['@Data'],
                'hora': votacao['@Hora'],
                'obj_votacao': votacao['@ObjVotacao'],
                'cod_sessao': int(votacao['@codSessao']),
                'orientacao_bancada': self._parse_orientacao_bancada(votacao['orientacaoBancada']['bancada']),
                'votos': self._parse_votos(votacao['votos']['Deputado'])
            }
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
