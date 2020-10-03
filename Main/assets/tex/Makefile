all: cv-en-tomMOULARD
all: clean

all-pdf:
	pdflatex *.tex

%: %.pdf
	pdflatex --shell-escape cv-all-tomMOULARD.tex
	cp cv-all-tomMOULARD.pdf $@.pdf

clean-pdf:
	rm -f *.pdf

clean:
	rm -f *.aux *.log *.out
