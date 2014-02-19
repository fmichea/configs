" Enable Django template highlighting in HTML files.

function HTML_configure()
    setlocal filetype=htmldjango

    setlocal tabstop=2
    setlocal softtabstop=2
    setlocal shiftwidth=2
endfunction

au BufRead,BufNewFile *.html call HTML_configure()
