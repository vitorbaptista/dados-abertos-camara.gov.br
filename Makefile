DATA_DIR=./data

all: proposicoes_votadas.csv

proposicoes_votadas.csv: create_data_dir
	$(eval OUTFILE := $(DATA_DIR)/$@)
	scrapy crawl proposicoes_votadas_em_plenario -o $(OUTFILE)
	# Sort the file
	$(eval TMPFILE := $(shell mktemp -u))
	head -1 $(OUTFILE) > $(TMPFILE)
	sed -i -e "1d" $(OUTFILE)
	sort $(OUTFILE) >> $(TMPFILE)
	mv $(TMPFILE) $(OUTFILE)

create_data_dir:
	mkdir -p $(DATA_DIR)
