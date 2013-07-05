" editzone.vim

set number

set laststatus=2
set statusline=%f\ %l:%c\ %m%=%p%%\ %y\ %r

set noerrorbells
set novisualbell

set cursorline

if version >= 703
   set colorcolumn=81
endif

set list
set listchars=tab:»\ ,eol:¬
