PAPER	= thesis

main: # Compiling with bibtex requires two build steps
		pdflatex $(PAPER).tex
		biber $(PAPER)
		pdflatex $(PAPER).tex

clean:
		rm -f *.aux $(PAPER).log $(PAPER).pdf $(PAPER).out *.bcf *.lof *.lot *.run.xml
		rm -f $(PAPER).bbl $(PAPER).blg $(PAPER).toc $(PAPER).out
