DATA_DIR=./data

.PHONY: clean

all: $(DATA_DIR)/proposicoes_votadas.csv $(DATA_DIR)/votacoes_proposicoes.json $(DATA_DIR)/proposicoes.csv

clean:
	rm -rf $(DATA_DIR)

$(DATA_DIR)/proposicoes_votadas.csv:
	mkdir -p $(DATA_DIR)
	$(eval OUTFILE := $@)
	rm -f $(OUTFILE) # scrapy doesn't support incrementally updating files
	scrapy crawl proposicoes_votadas_em_plenario -L INFO -o $(OUTFILE)
	# Sort the file
	$(eval TMPFILE := $(shell mktemp -u))
	head -1 $(OUTFILE) > $(TMPFILE)
	sed -i -e "1d" $(OUTFILE)
	sort $(OUTFILE) >> $(TMPFILE)
	mv $(TMPFILE) $(OUTFILE)
	touch $(OUTFILE)

$(DATA_DIR)/votacoes_proposicoes.json: $(DATA_DIR)/proposicoes_votadas.csv
	mkdir -p $(DATA_DIR)
	$(eval OUTFILE := $@)
	rm -f $(OUTFILE) # scrapy doesn't support incrementally updating files
	scrapy crawl votacoes_proposicoes -L INFO -o $(OUTFILE)

$(DATA_DIR)/proposicoes.csv: $(DATA_DIR)/proposicoes_votadas.csv
	mkdir -p $(DATA_DIR)
	$(eval OUTFILE := $@)
	rm -f $(OUTFILE) # scrapy doesn't support incrementally updating files
	scrapy crawl proposicoes -L INFO -o $(OUTFILE)
