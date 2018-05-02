# pdfstamp

Writes some text centered at the top of each page of a PDF file.

Usage:

    pdfstamp.py --stamp <text> --infile <filename> --outfile <filename> --papersize <size>

where

- `--stamp <text>`       specifies the text to write at the top of each page
- `--infile <filename>`  specifies the PDF file to read
- `--outfile <filename>` specifies the PDF file to write to
- `--papersize <size>`   specifies the paper size (`a4` or `letter`; default `a4`)

