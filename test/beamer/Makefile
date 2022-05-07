TARGET = test.pdf
TEXLOG = $(TARGET:.pdf=.log)

RM = rm -f

.SUFFIXES: .tex .dvi .md .pdf

all: $(TARGET)

.dvi.pdf:
	dvipdfmx $<

.tex.dvi:
	uplatex $<
	uplatex $<
	python ../../chk_graphics.py $(TEXLOG)

.md.tex:
	python ../../md2x.py --beamer $<

clean:
	$(RM) *.tex *.aux *.log *.dvi *.nav *.snm *.toc *.out *.vrb out/*.pdf

distclean: clean
	$(RM) $(TARGET)

rebuild: distclean $(TARGET)
