clean:
	rm -f *~
	rm -f *.pyo *.pyc
	find . ! -name "makefile" ! -name ".last_path.txt" -delete # delete saved games in data/
	echo "./data/">.last_path.txt # set the default path for saved games

cleaner: clean
	rm -f TAGS

check:
	pychecker *.py
