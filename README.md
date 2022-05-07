# Name
md2x: Convert Markdown document to other formats 

# Overview
This scripte converts a markdown file to other formats; HTML, plain text, Beamer(LaTeX presentation) and LaTeX.

This software is still under development and there are many missing functionalities.
You should use other existing converters, which are more stable, unless you want following charactaristics. 

* Good integration with Beamer
* Simple specification of document attributes using front matters
* Less dependency on OS and platforms

# Requirements
This script collection works on Python + TexLive environment.

* [TeX Live](https://www.tug.org/texlive/)
* TeX libralies
  - [jlisting.sty](https://osdn.net/projects/mytexpert/downloads/26068/jlisting.sty.bz2/)
* [Python](https://www.python.org)
* Python libralies 
  - reportlab for the image creation extention
  - win32com for pptx-pdf convert (it works only on Windows)

# Quick start

## Installation
1. Install required python and TeX packages.
2. Extract the archive somewhere you want.
3. Add md2x directory to your execution path.

## Customization
You have four ways to set document:
1. <system root>/config.json
2. ~/.md2x/config.json
3. <document root>/config.json
4. frontmatter in the markdown

A lower option overwrites upper ones. 

## Write and compile documents
See sample files in md2y/test directory.

# Document options

## General

|Option|Function| 
|:------|:------|
|title| Specify the document title| 
|author| Specify the author| 
|date| Specify the date. if 'today' is specified, it would be translated as the date of today.| 
|clipart_path| Specify directories of picture libraries.| 
|snippet_path| Specify directories of snippet libraries.| 

## Beamer

|Option|Function| 
|:------|:------|
|beamer.theme| Specify a Beamer theme| 
|beamer.template| Specify a Beamer template| 
|beamer.bg_titlepage| Set background image on the title page|
|beamer.bg_toc| Set background images on the TOC pages|
|beamer.bg| Set background images on the normal page|
|beamer.bg_endpage| Set background image on the ending page| 
|beamer.quote.width| Set the width of the quote box| 

## LaTeX
|Option|Function| 
|:------|:------|
|latex.template| Specify a LaTeX template.| 
|latex.footer.right| Specify a footer string at bottom-right.| 
|latex.footer.left| Specify a footer string at bottom-left.| 

## HTML
|Option|Function| 
|:------|:------|
|html.header| Specify a HTML header.| 
|html.footer| Specify a string to put at the end of the HTML document.| 

# Writing Markdown

## Insert figures

Use link notation with some syntax modification on geometry specification.
```
![geometry options](link to file)
```

* width or w: specify width of figure
* height or h: specify height of figure
* scale or s: specify height of figure
* x: specify absolute x position of the figure 
* y: specify absolute y position of the figure

## Two panes mode
```
### section {2panes: 0.5, 0.5, tf}
```

First two values specify the width of each pane (relative value to textwidth).

The third value is a two-characters string to specify the layout.
The first letter is for the left pane and the second for right.
't' specifies 'text mode' and 'f' specifies 'figure mode', which gives the better layout.

# Utilities

## bmconfig

```
Usage: bmconfig <project_name>
```

This script sets up a project directory for a beamer project: config.json, Makefile and an empty MD file.

## pptxtopdf.py

```
Usage: pptxtopdf <input_pptx>
```

This script converts a Powerpoint file to a PDF file.
It use the export function of Powerpoint and you need a Powerpoint on an Windows environment.

## pdfextract.bat

```
Usage: pdfextract <input_pdf> <page> <output_pdf> 
```

This script picks up a page from a pdf file and crops it with the pdfcrop command. 

## md2y.el and chk_graphics.py
Beamer is not very good at layouting pictures due to its nature as a typesetting software, which tries to keep sizes of input characters and pictures. 

md2y.el supports adjusting scale arguments of pictures using 'overfull' information in a LaTeX log file.
The 'md2y-update-graphics-scale' function works as the query-replace-string of Emacs and it interactively replace a scale factor in an argument with a smaller value; a product of 0.9 and the original value.

chk_graphics.py generates an input for md2y from a logfile of LaTeX.
See test/beamer/Makefile for a sample to use this script.

# Resources
* [RepoartLab](https://www.reportlab.com)

# Contributions
todo

# Acknowledgements
todo
