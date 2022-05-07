# -*- coding: cp932 -*-

TARGET := {slide_skeleton}.pdf
RM = rm -f

.PHONY: all clean distclean rebuild
.SUFFIXES: .tex .dvi .md .pdf

all: $(TARGET)

.dvi.pdf:
	dvipdfmx $^

.tex.dvi:
	platex -interaction=nonstopmode $<
	platex -interaction=nonstopmode $<

.md.tex:
	python ../../md2x.py --beamer $<

clean:
	$(RM) *.tex *.aux *.log *.dvi *.nav *.snm *.toc *.out *.vrb out/*.pdf

distclean: clean
	$(RM) $(TARGET)

rebuild: distclean $(TARGET)
