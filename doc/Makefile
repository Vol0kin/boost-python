all: memoria

.PHONY: all clean

memoria:
	pandoc memoria.md -o memoria.pdf --template eisvogel --variable urlcolor=cyan --highlight-style tango

clean:
	rm -f *.pdf
