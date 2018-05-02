#!/usr/bin/env python3

import string
import tempfile
import os, os.path
import subprocess
import shutil

template = string.Template(r"""\documentclass{article}
\usepackage[$geometry]{geometry}
\usepackage{pdfpages}
\begin{document}
\includepdf[pages=-,picturecommand={\put($x,$y){\makebox[0pt][c]{\tt\small $stamp}}}]{$inpdf}%
\end{document}
""")

def pdfstamp(inpdf, outpdf, stamp, papersize="a4"):
    papersize = papersize.lower()
    if papersize == "a4":
        width, height = 210/25.4*72.27, 297/25.4*72.27
    elif args.papersize.lower() == "letter":
        width, height = 8.5*72.27, 11*72.27
    else:
        raise ValueError("invalid paper size")

    y = height - 24
    x = width / 2
        
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "stamp.tex"), "w") as f:
            shutil.copy(inpdf, os.path.join(tmpdir, "paper.pdf"))
            f.write(template.substitute(stamp=stamp, inpdf="paper.pdf", geometry=papersize+"paper", x=x, y=y))
        subprocess.run(["/Library/TeX/texbin/pdflatex", "stamp.tex"], cwd=tmpdir)
        shutil.move(os.path.join(tmpdir, "stamp.pdf"), outpdf)

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Add a stamp to a PDF file.")
    parser.add_argument('--stamp', help="Stamp text to add")
    parser.add_argument('--infile', help="Input PDF file")
    parser.add_argument('--outfile', help="Output PDF file")
    parser.add_argument('--papersize', help="Paper size (a4 or letter)", default="a4")
    args = parser.parse_args()

    if args.papersize.lower() not in ["a4", "letter"]:
        sys.stderr.write("Invalid paper size (must be a4 or letter)\n")
        sys.exit(1)

    pdfstamp(args.infile, args.outfile, args.stamp, args.papersize)

