#!/usr/bin/env python

import sys
import win32com.client
import re
from pathlib import Path

def convert_name(pptx_file):
    pdf = pptx_file.with_suffix('.pdf')
    return(pdf)

def convert_pdf(pptx_file):
    app = win32com.client.gencache.EnsureDispatch('Powerpoint.Application')
    app.Visible = True
    app.DisplayAlerts = False

    pptx = Path(pptx_file).resolve()
    pdf = convert_name(pptx)

    try:
        pres = app.Presentations.Open(pptx, True)
        pres.SaveAs(pdf, 32) # 32 = PDF
    finally:
        pres.Close()
        app.Quit()

def main(files):
    for f in files:
        m = re.search('\.pptx$', f)
        if m:
            convert_pdf(f)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
