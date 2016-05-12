clean:
	rm -f *~
	bash -c 'rm -f README.{out,tex,log,aux}'
	(cd lines/; make clean)
	(cd ../)
	(cd data/; make cleaner)

cleaner: clean
	rm -rf html
	rm -f TAGS
	rm -rf README.pdf
	(cd lines/; make cleaner)
	(cd ../)
	(cd data/; make cleaner)

check:
	pychecker *.py

tags:
	etags *.py

html:
	mkdir -p doc
	mkdir -p doc/html
	(cd lines; pydoc -w ./*.py; mv *.html ../doc/html)

tgz:
	(cd ..; tar zcvf /tmp/five-or-more.tgz ./five-or-more_basic)

README.pdf: README.txt
	rst2pdf.sh $<
