pdfseparate -f %2 -l %2 %1 %~n1-work-%%d.pdf
pdfcrop %~n1-work-%2.pdf
mv %~n1-work-%2-crop.pdf %3
rm -f %~n1-work-%2.pdf
