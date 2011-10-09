" epita-c.vim

function Epita_c_insert_guards()
   let basename=substitue(@%, "[^/]*/", "", "g")
   let underscored=tr(basename, ".", "_")
   let const=substitute(underscored, ".*", "\\U\\0", "")."_"
   exe "normal i#ifndef ".const."\n\e"
   exe "normal i# define ".const."\n\n\n\n\e"
   exe "normal i#endif /"."* !".const." */\e"
   exe "normal 4G"
endfunction

if $EPITA == 1
   au Bufnewfile,Bufread *.h set ft=c
   au Bufnewfile *.h call Epita_c_insert_guards()
endif