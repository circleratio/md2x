import mdfig
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

def Desc(canvas, texts, color_theme, x, y, width, height):
    #canvas.rect(x, y, width, height) # for debug
    box_margin = 2.5*mm
    desc_margin = 10*mm
    num = len(texts)
    step = height / num
    title_w = width * 0.25
    desc_w = width * 0.75 - desc_margin * 2
    args = list(reversed(texts))

    style_dict = {
        "name":"normal",
        "fontName":"Meiryo UI",
        "fontSize":24,
        "leading":24,
        "alignment":TA_CENTER,
    }
    title_style = ParagraphStyle(**style_dict)
    
    style_dict = {
        "name":"normal",
        "fontName":"Meiryo UI",
        "fontSize":20,
        "leading":20,
        "alignment":TA_JUSTIFY,
    }
    desc_style = ParagraphStyle(**style_dict)

    # measure the offset from the font size
    pp = Paragraph('A', style=desc_style)
    w, h = pp.wrapOn(canvas, width, height)
    font_offset = h / 4

    # measure the maximum height of paragraphs.
    max_height = 0
    for i in range(num):
        pp = Paragraph(args[i][0], style=title_style)
        w, h = pp.wrapOn(canvas, title_w - box_margin * 4, height)
        if h > max_height:
            max_height = h
        pp = Paragraph(args[i][1], style=desc_style)
        w, h = pp.wrapOn(canvas, desc_w, height)
        if h > max_height:
            max_height = h
            
    step = max_height + box_margin * 2
    for i in range(num):
        #canvas.rect(x, y + step * i, width, step) # for debug
        sc = color_theme['plain']['fg']
        tc = color_theme['block_title']['fg']
        fc = color_theme['block_title']['bg']
        mdfig.mdfig.stringBox(canvas, args[i][0], 24, tc, sc, fc, x + box_margin, y + step * i + box_margin, title_w - box_margin * 2, step - box_margin * 2, 1*mm, box_margin)
        pp = Paragraph(args[i][1], style=desc_style)
        w, h = pp.wrapOn(canvas, desc_w, step)
        offset = (step - h) / 2
        pp.drawOn(canvas, x + title_w + desc_margin, y + step * i + offset + font_offset)
