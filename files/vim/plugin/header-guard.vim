" epita-c.vim

function C_insert_guards()
    let gatename = substitute(toupper(expand("%:t")), "\\.", "_", "g") . "_"
    exe "normal i#ifndef ".gatename."\r\e"
    exe "normal i# define ".gatename."\r\r\r\r\e"
    exe "normal i#endif /* !".gatename." */\e"
    exe "normal 4G"
endfunction

au Bufnewfile,Bufread *.h set ft=c
au Bufnewfile *.h call C_insert_guards()

au BufNewFile,BufRead *.h{h,xx,pp} set ft=cpp
au BufNewFile *.h{h,xx,pp} call C_insert_guards()
