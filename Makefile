DATA_DIR=./data

.PHONY: clean

all: $(DATA_DIR)/proposicoes_votadas.csv $(DATA_DIR)/votacoes_proposicoes.json

clean:
	rm -rf $(DATA_DIR)

$(DATA_DIR)/proposicoes_votadas.csv: $(DATA_DIR)
	$(eval OUTFILE := $@)
	scrapy crawl proposicoes_votadas_em_plenario -L INFO -o $(OUTFILE)
	# Sort the file
	$(eval TMPFILE := $(shell mktemp -u))
	head -1 $(OUTFILE) > $(TMPFILE)
	sed -i -e "1d" $(OUTFILE)
	sort $(OUTFILE) >> $(TMPFILE)
	mv $(TMPFILE) $(OUTFILE)
	touch $(OUTFILE)

$(DATA_DIR)/votacoes_proposicoes.json: $(DATA_DIR) $(DATA_DIR)/proposicoes_votadas.csv
	$(eval OUTFILE := $@)
	scrapy crawl votacoes_proposicoes -L INFO -o $(OUTFILE)

$(DATA_DIR):
	mkdir -p $(DATA_DIR)
