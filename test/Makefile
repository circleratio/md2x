DIRS := beamer beamer-meiryo html latex

all:
	@for i in $(DIRS); do (cd $$i ; make); done

clean:
	@for i in $(DIRS); do (cd $$i ; make clean); done

distclean:
	@for i in $(DIRS); do (cd $$i ; make distclean); done

rebuild:
	@for i in $(DIRS); do (cd $$i ; make rebuild); done
