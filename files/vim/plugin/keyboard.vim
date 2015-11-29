" keyboard.vim - Key Bindings

" F1 - paster mode toggler
map <F1> :set invpaste paste?<CR>
set pastetoggle=<F1>

" F2 - saving
map <silent> <F2> :w<CR>
imap <silent> <F2> <C-O>:w<CR>

" F[3-4] - searching
map <silent> <F3> :nohlsearch<CR>
imap <silent> <F3> <C-O>:nohlsearch<CR>

nnoremap <F4> :Ag!<Space><cword><CR>
inoremap <F4> <ESC>:Ag!<Space><cword><CR>

nnoremap <F4> :Ag!<Space>
inoremap <F4> <ESC>:Ag!<Space>

" Split with Space+[vs]
" Move across buffers with Space+[hjkl] or Double space.
nnoremap <Space> <C-w>
nnoremap <Space><Space> <C-w>w
