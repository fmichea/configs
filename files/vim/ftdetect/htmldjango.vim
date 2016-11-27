" Enable Django template highlighting in HTML files.

function! HTML_indent()
    setlocal tabstop=2
    setlocal softtabstop=2
    setlocal shiftwidth=2
endfunction

function! HTML_configure()
    setlocal filetype=htmldjango
    call HTML_indent()
endfunction

au BufRead,BufNewFile *.html call HTML_configure()
au BufRead,BufNewFile *.{css,scss,js} call HTML_indent()
