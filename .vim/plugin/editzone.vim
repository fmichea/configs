" editzone.vim

set number

set laststatus=2
set statusline=%f\ %l:%c\ %m%=%p%%\ %y\ %r

set noerrorbells
set novisualbell

set cursorline

set wrap
set textwidth=79
if version >= 703
   set colorcolumn=+1
endif

set list
set listchars=tab:.\ ,eol:¬
