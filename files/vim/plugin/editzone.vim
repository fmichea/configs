" editzone.vim

set number
set relativenumber

if version >= 704
    autocmd WinEnter,FocusGained * :setlocal number relativenumber
    autocmd WinLeave,FocusLost   * :setlocal number norelativenumber
endif

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

set timeout timeoutlen=5000 ttimeoutlen=100

" Size of the ctrlp buffer.
let g:ctrlp_max_height = 20
