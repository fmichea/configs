" epita-cpp.vim
" Configuration for EPITA C++ coding style

function Epita_cpp_insert_guards()
    let basename=substitute(@%, "[^/]*/", "", "g")
    let underscored=substitute(basename, "[^a-zA-Z_]", "_", "g")
    let const=substitute(underscored, ".*", "\\U\\0", "")."_"
    exe "normal i#ifndef ".const."\r\e"
    exe "normal i# define ".const."\r\r\r\r\e"
    exe "normal i#endif // !".const."\e"
    exe "normal 4G"
endfunction

au BufNewFile,BufRead *.h{h,xx,pp} set ft=cpp
au BufNewFile *.h{h,xx,pp} call Epita_cpp_insert_guards()
