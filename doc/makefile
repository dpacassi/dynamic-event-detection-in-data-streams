PAPER	= thesis

main: # Compiling with bibtex requires two build steps
		pdflatex $(PAPER)
		bibtex $(PAPER)
		pdflatex $(PAPER)

clean:
		rm -f *.aux $(PAPER).log $(PAPER).pdf $(PAPER).out
		rm -f $(PAPER).bbl $(PAPER).blg $(PAPER).toc $(PAPER).out
