TARGET = emacs.html
RM = rm -f

all: $(TARGET)

%.html: %.md
	python ../../md2x.py --html $<

clean:
	$(RM) *.html

distclean: clean
	$(RM) $(TARGET)

rebuild: distclean $(TARGET)
