import mdfig
from reportlab.lib.units import mm

def StepUp(canvas, texts, color_theme, x, y, width, height):
    #canvas.rect(x, y, width, height) # for debug
    num = len(texts)
    box_w = width / num * 1.25
    box_h = height / num
    margin = box_h / 20
    step_x = (width - box_w) / (num - 1)
    step_y = height / num

    for i in range(num):
        sc = color_theme['plain']['fg']
        tc = color_theme['block_body']['fg']
        fc = color_theme['block_body']['bg']
        mdfig.mdfig.stringBox(canvas, texts[i], 24, tc, sc, fc, x + margin + step_x * i, y + margin + step_y * i, box_w - margin * 2, box_h - margin * 2, 5*mm, 2.5*mm)

    arrow_x1 = x + margin + step_x * 3 / 4
    arrow_x2 = x + margin + step_x
    arrow_y = y - margin + step_y
    arrow_h = step_y / 2
    for i in range(len(texts) - 1):
        canvas.line(arrow_x1, arrow_y, arrow_x1, arrow_y + arrow_h)
        canvas.line(arrow_x1, arrow_y + arrow_h, arrow_x2, arrow_y + arrow_h)
        mdfig.mdfig.arrowHead(canvas, arrow_x1, arrow_y + arrow_h, arrow_x2, arrow_y + arrow_h, 10, 5)
        arrow_x1 = arrow_x1 + step_x
        arrow_x2 = arrow_x2 + step_x
        arrow_y = arrow_y + step_y
