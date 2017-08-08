OPT =

all: product/mozc.txt product/msime.txt

product/mozc.txt: src/*.json
	@if [ ! -d products ]; then \
		mkdir products; \
	fi
	python ./makedict.py -g src/*.json ${OPT} > products/mozc.txt

product/msime.txt: src/*.json
	@if [ ! -d products ]; then \
		mkdir products; \
	fi
	python ./makedict.py -m src/*.json ${OPT} > products/msime.txt

clean:
	rm -r products