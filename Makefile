DATA_DIR=./data

.PHONY: clean

all: data/proposicoes_votadas.csv

clean:
	rm -rf $(DATA_DIR)

$(DATA_DIR)/proposicoes_votadas.csv: $(DATA_DIR)
	$(eval OUTFILE := $@)
	scrapy crawl proposicoes_votadas_em_plenario -o $(OUTFILE)
	# Sort the file
	$(eval TMPFILE := $(shell mktemp -u))
	head -1 $(OUTFILE) > $(TMPFILE)
	sed -i -e "1d" $(OUTFILE)
	sort $(OUTFILE) >> $(TMPFILE)
	mv $(TMPFILE) $(OUTFILE)
	touch $(OUTFILE)

$(DATA_DIR):
	mkdir -p $(DATA_DIR)
