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

imap <silent> <F2> <ESC>:w<CR>
map <silent> <F2> :w<CR>
imap <silent> <F3> <ESC>:x<CR>
map <silent> <F3> :x<CR>
imap <silent> <F4> <ESC>:q<CR>
map <silent> <F4> :q<CR>
