#!/usr/bin/env python3

import string
import tempfile
import os, os.path
import subprocess
import shutil
import PyPDF2 as pdf
import decimal

template = string.Template(r"""\documentclass{article}
\usepackage[paperwidth=${w}pt,paperheight=${h}pt]{geometry}
\usepackage{pdfpages}
\begin{document}
\includepdf[pages=-,picturecommand={\put($x,$y){\makebox[0pt][c]{\tt\small $stamp}}}]{$inpdf}%
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

def pdfstamp(inpdf, outpdf, stamp):
    w, h = papersize(inpdf)
    y = h - decimal.Decimal(24)
    x = w / decimal.Decimal(2)
        
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "stamp.tex"), "w") as f:
            shutil.copy(inpdf, os.path.join(tmpdir, "paper.pdf"))
            f.write(template.substitute(stamp=stamp, inpdf="paper.pdf", w=w, h=h, x=x, y=y))
        subprocess.run(["/Library/TeX/texbin/pdflatex", "stamp.tex"], cwd=tmpdir)
        shutil.move(os.path.join(tmpdir, "stamp.pdf"), outpdf)

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Add a stamp to a PDF file.")
    parser.add_argument('--stamp', help="Stamp text to add")
    parser.add_argument('--infile', help="Input PDF file")
    parser.add_argument('--outfile', help="Output PDF file")
    args = parser.parse_args()

    pdfstamp(args.infile, args.outfile, args.stamp)
