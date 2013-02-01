TEX = env TEXINPUTS=:$(CURDIR)/iopart: pdflatex -file-line-error -halt-on-error
BIBTEX = env BIBINPUTS=:$(CURDIR)/astronat/apj: TEXINPUTS=:$(CURDIR)/iopart: bibtex

all: ms.pdf

PREREQS = ms.tex bib/aas_macros.sty ligo-acronyms/acronyms.tex bib/telescope.bib

ms.pdf: $(PREREQS)
	$(TEX) -draftmode $(patsubst %.pdf,%,$@)
	$(BIBTEX) $(patsubst %.pdf,%,$@)
	$(TEX) -draftmode $(patsubst %.pdf,%,$@)
	$(TEX) $(patsubst %.pdf,%,$@)

clean:
	rm -f ms.{aux,log,out,bbl,blg,pdf}
