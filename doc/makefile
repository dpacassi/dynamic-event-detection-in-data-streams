PAPER	= thesis

main: # Compiling with bibtex requires two build steps
		pdflatex $(PAPER).tex
		biber $(PAPER)
		makeglossaries $(PAPER)
		pdflatex $(PAPER).tex

clean:
		rm -f *.aux $(PAPER).log $(PAPER).out *.bcf *.lof *.lot *.glg *.glo *.gls *.glsdefs *.ist *.sub *.suc *.syc *.sym *.run.xml
		rm -f $(PAPER).bbl $(PAPER).blg $(PAPER).toc $(PAPER).out
