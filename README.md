Dados Abertos camara.gov.br
===========================

A Câmara dos Deputados disponibiliza vários dados relacionados a atividade
legislativa e cota parlamentar em
http://www2.camara.leg.br/transparencia/dados-abertos. Infelizmente, apesar de
oferecer uma API, eles não disponibilizaram um dump com os dados completos.

Neste repositório irei organizar scrapers para a API e, na pasta `data/`, o
dump atualizado do que extraí de lá. Dessa forma, caso outra pessoa precise
dessa mesma informação, não precisará perder tempo, e nem ocupar as máquinas da
Câmara baixando os dados.

Instruções
----------

Para atualizar os dados, é preciso primeiramente instalar as dependências. Recomendo
usar o `virtualenv` para isolar as dependências desse projeto das outras no seu
computador. Para isso, faça:

```
virtualenv --no-site-packages venv
pip install -r requirements.txt
```

Uma vez instaladas, faça:

```
source ./venv
make --always-make
```

Isso irá atualizar todos os dados. Como o Scrapy não suporta atualizações incrementais,
o que é feito é apagar o que já foi baixado e buscar tudo novamente. Por isso, essa
atualização pode demorar um pouco. Se você tiver tempo para resolver esse problema,
contribuições são muito bem vindas.
