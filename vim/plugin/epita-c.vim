" epita-c.vim

function Epita_c_insert_guards()
  let basename=substitute(@%, "[^/]*/", "", "g")
  let underscored=tr(basename, ".", "_")
  let const=substitute(underscored, ".*", "\\U\\0", "")."_"
  exe "normal i#ifndef ".const."\r\e"
  exe "normal i# define ".const."\r\r\r\r\e"
  exe "normal i#endif /"."* !".const." */\e"
  exe "normal 4G"
endfunction

au Bufnewfile,Bufread *.h set ft=c
au Bufnewfile *.h call Epita_c_insert_guards()
