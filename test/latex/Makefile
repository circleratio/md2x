TARGET = test.pdf
RM = rm -f

all: $(TARGET)

%.tex: %.md
	python ../../md2x.py --latex $<

%.pdf: %.tex
	lualatex $<
	lualatex $<

clean:
	$(RM) *.tex *.aux *.log *.dvi *.nav *.snm *.toc *.out

distclean: clean
	$(RM) $(TARGET)

rebuild: distclean $(TARGET)
