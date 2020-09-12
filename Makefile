SRC:=menu.py

all:	flake8 pylint

flake8:
	flake8 ${SRC}

pylint:
	pylint --rcfile=.pylintrc ${SRC}

package:
	cxfreeze menu.py
