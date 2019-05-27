all: cv-en-tomMOULARD
all: cv-fr-tomMOULARD
# all: clean

all-pdf:
	pdflatex *.tex

%: %.pdf
	pdflatex --shell-escape $@.tex

clean-pdf:
	rm -f *.pdf

clean:
	rm -f *.aux *.log *.out
