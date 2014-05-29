TEX = env TEXINPUTS=:$(CURDIR)/iopart: pdflatex -file-line-error -halt-on-error
BIBTEX = env BIBINPUTS=:$(CURDIR)/astronat/apj: TEXINPUTS=:$(CURDIR)/iopart: bibtex

all: ms.pdf

FIGURES = \
	inclination_integral_convergence.pdf \
	polarization_angle_integral_convergence.pdf \
	radial_integrand.pdf

PREREQS = ms.tex \
	bib/aas_macros.sty \
	ligo-acronyms/acronyms.tex \
	bib/telescope.bib \
	$(FIGURES)

ms.pdf: $(PREREQS)
	$(TEX) -draftmode $(patsubst %.pdf,%,$@)
	$(BIBTEX) $(patsubst %.pdf,%,$@)
	$(TEX) -draftmode $(patsubst %.pdf,%,$@)
	$(TEX) $(patsubst %.pdf,%,$@)

inclination_integral_convergence.pdf: scripts/inclination_integral_convergence.py matplotlibrc
	python $<

polarization_angle_integral_convergence.pdf: scripts/polarization_angle_integral_convergence.py matplotlibrc
	python $<

radial_integrand.pdf: scripts/radial_integrand.py matplotlibrc
	python $< $@

clean:
	rm -f ms.{aux,log,out,bbl,blg,pdf} $(FIGURES)
