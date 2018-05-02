# pdfstamp

Writes some text centered at the top of each page of a PDF file.

Requires:
- [PyPDF2](https://pythonhosted.org/PyPDF2)

Usage:

    pdfstamp.py --stamp <text> --infile <filename> --outfile <filename>

where

- `--stamp <text>`       specifies the text to write at the top of each page
- `--infile <filename>`  specifies the PDF file to read
- `--outfile <filename>` specifies the PDF file to write to

