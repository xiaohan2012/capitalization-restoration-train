all:
	pandoc  report.md -f markdown -t latex -o report.pdf
	mv report.pdf ~/public_html/capitalization-restoration.pdf
	chmod a+r ~/public_html/capitalization-restoration.pdf
