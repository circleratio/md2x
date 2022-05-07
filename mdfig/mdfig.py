import math
import numpy as np
import pathlib
import subprocess
import sys
import reportlab.lib.colors as colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
import mdfig.StepUp
import mdfig.Desc

def stringBox(canvas, text, font_size, text_color, stroke_color, fill_color, x, y, width, height, radius, margin):
    canvas.setDash([])
    canvas.setStrokeColorRGB(stroke_color[0]/256,
                             stroke_color[1]/256,
                             stroke_color[2]/256)
    canvas.setFillColorRGB(fill_color[0]/256,
                           fill_color[1]/256,
                           fill_color[2]/256)

    canvas.roundRect(x, y, width, height, radius=radius, fill=True)

    style_dict = {
        "name":"normal",
        "fontName":"Meiryo UI",
        "fontSize":font_size,
        "leading":font_size,
        "alignment":TA_CENTER,
        "wordWrap":"CJK",
        "textColor":(text_color[0]/256,
                     text_color[1]/256,
                     text_color[2]/256)
    }
    style = ParagraphStyle(**style_dict)

    # measure the offset from the font size
    pp = Paragraph('A', style=style)
    w, h = pp.wrapOn(canvas, width, height)
    font_offset = h / 4

    pp = Paragraph(text, style=style)
    w, h = pp.wrapOn(canvas, width - margin * 2, height - margin * 2)  # size of 'textbox' for linebreaks etc.
    offset = (height - margin * 2 - h) / 2

    pp.drawOn(canvas, x + margin, y + margin + offset + font_offset)

def arrowHead(canvas, x1, y1, x2, y2, h, w):
    v1 = np.array([x1, y1])
    v2 = np.array([x2, y2])
    v12 = v2 - v1

    v4 = v12 * (1 - h / math.sqrt(v12.dot(v12)))
    tr = v1 + v4

    # 直交ベクトルを求める
    ov = np.array([-v12[1], v12[0]])
    ov = ov * w / math.sqrt(ov.dot(ov))

    t1 = tr + ov
    t2 = tr - ov

    p = canvas.beginPath()
    p.moveTo(tr[0], tr[1])
    p.lineTo(t1[0], t1[1])
    p.lineTo(x2, y2)
    p.lineTo(t2[0], t2[1])
    p.lineTo(tr[0], tr[1])
    canvas.setStrokeColor(colors.black)
    canvas.setFillColor(colors.black)
    canvas.drawPath(p, stroke=1, fill=1)

def generatePDFFigure(type, size, args, outfile):
    path = pathlib.Path(outfile)
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    color_theme = {
        'plain': {
            'fg':[0, 0, 0],
            'bg':[255, 255, 255]
        },
        'block_title': {
            'fg':[255, 255, 255],
            'bg':[50, 80, 170]
        },
        'block_body': {
            'fg':[0, 0, 0],
            'bg':[234, 234, 246]
        },
        'block_title_alerted': {
            'fg':[0, 0, 0],
            'bg':[165, 15, 45]
        },
        'block_body_alerted': {
            'fg':[0, 0, 0],
            'bg':[246, 231, 234]
        }
    }
    
    tmpfile = str(pathlib.Path(path.parent, 'tmp-' + path.name))
    
    # bottomup=False にすると，Paragraphがうまく動作しない．テキストと枠がずれる．
    c = canvas.Canvas(tmpfile, pagesize=landscape(A4), bottomup=True)
    
    pdfmetrics.registerFont(TTFont('Meiryo UI', 'c:/Windows/Fonts/meiryo.ttc'))
    
    if type == 1:
        mdfig.StepUp.StepUp(c, args, color_theme, size[0]*mm, size[1]*mm, size[2]*mm, size[3]*mm)
    elif type == 2:
        mdfig.Desc.Desc(c, args, color_theme, size[0]*mm, size[1]*mm, size[2]*mm, size[3]*mm)
    else:
        print("Unknown Type: {type}", file=sys.stderr)
    
    c.showPage()
    c.save()

    # This requires pdfcrop bundled with TeXLive
    #pdfcrop = 'c:/texlive/2021/bin/win32/pdfcrop.exe'
    pdfcrop = 'pdfcrop'
    cmd = f'{pdfcrop} {tmpfile} {outfile}'
    subprocess.call(cmd)
    
if __name__ == "__main__":
    FILENAME = 'stepup.pdf'
    args = [
        "現在できていること",
        "目の前で重点的に達成すること",
        "長期的に実現する，あるべき姿"]
    size = [20, 10, 260, 150]
    generatePDFFigure(1, size, args, FILENAME)
    
    FILENAME = 'desc.pdf'
    args = [
        ["現在1現在2", "いま，できていること．いま，できていること．いま，できていること"],
        ["明日について話が長くなってしまうとどうなるかさてさてさて", "目の前で重点的に達成すること．目の前で重点的に達成すること．目の前で重点的に達成すること．目の前で重点的に達成すること．"],
        ["未来", "長期的に実現する，あるべき姿"]]
    size = [20, 10, 260, 150]
    generatePDFFigure(2, size, args, FILENAME)
