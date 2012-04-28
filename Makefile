TEX = env TEXINPUTS=:$(CURDIR)/../../packages/iopart:$(CURDIR)/../../packages/iopart-num: pdflatex -file-line-error -halt-on-error
BIBTEX = env BSTINPUTS=:$(CURDIR)/../../packages/iopart-num: TEXINPUTS=:$(CURDIR)/../../packages/iopart:$(CURDIR)/../../packages/iopart-num: bibtex

all: ms.pdf

PREREQS: ms.tex aas_macros.sty acronyms.tex apj-jour.bib telescope.bib

ms.pdf: $(PREREQS)
	$(TEX) -draftmode $(patsubst %.pdf,%,$@)
	$(BIBTEX) $(patsubst %.pdf,%,$@)
	$(TEX) -draftmode $(patsubst %.pdf,%,$@)
	$(TEX) $(patsubst %.pdf,%,$@)

clean:
	rm -f ms.{aux,log,out,bbl,blg,pdf}
