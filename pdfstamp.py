#!/usr/bin/env python3

import string
import tempfile
import os, os.path
import subprocess
import shutil
import PyPDF2 as pdf
import decimal

template = string.Template(r"""\documentclass{article}
\usepackage[paperwidth=${w}pt,paperheight=${h}pt,margin=0pt]{geometry}
\font\stampfont=phvb at 8pt
\setlength{\unitlength}{1pt}
\begin{document}
\noindent
\begin{picture}(${w},${h})
\put($x,$y){\makebox[0pt][c]{\stampfont $stamp}}%
\end{picture}
\end{document}
""")

def papersize(inpdf):
    bbox = pdf.PdfFileReader(open(inpdf, 'rb')).getPage(0).mediaBox
    x1, y1 = bbox.lowerLeft
    x2, y2 = bbox.upperRight
    bp_to_pt = decimal.Decimal(72.27) / decimal.Decimal(72)
    w = (x2-x1) * bp_to_pt
    h = (y2-y1) * bp_to_pt
    return w, h

def pdfstamp(inpdf, outpdf, stamp, pdflatex):
    w, h = papersize(inpdf)
    y = h - decimal.Decimal(42) # 42pt from top
    x = w / decimal.Decimal(2)
        
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "stamp.tex"), "w") as f:
            f.write(template.substitute(stamp=stamp, w=w, h=h, x=x, y=y))
        subprocess.run([pdflatex, "stamp.tex"], cwd=tmpdir)

        stampreader = pdf.PdfFileReader(open(os.path.join(tmpdir, "stamp.pdf"), "rb"))
        reader = pdf.PdfFileReader(open(inpdf, "rb"))
        writer = pdf.PdfFileWriter()
        for i in range(reader.numPages):
            page = reader.getPage(i)
            page.mergePage(stampreader.getPage(0))
            writer.addPage(page)
        for dest in reader.namedDestinations.values():
            writer.addNamedDestinationObject(dest)
        with open(outpdf, "wb") as outfile:
            writer.write(outfile)

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Add a stamp to a PDF file.")
    parser.add_argument('--stamp', help="Stamp text to add")
    parser.add_argument('--infile', help="Input PDF file")
    parser.add_argument('--outfile', help="Output PDF file")
    parser.add_argument('--pdflatex', help="Location of pdfLaTeX", default="/usr/bin/pdflatex")
    args = parser.parse_args()

    pdfstamp(args.infile, args.outfile, args.stamp, pdflatex=args.pdflatex)
