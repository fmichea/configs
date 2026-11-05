" keyboard.vim - Key Bindings

" F1 - paster mode toggler
map <F1> :set invpaste paste?<CR>
set pastetoggle=<F1>

" F2 - saving
map <silent> <F2> :w<CR>
imap <silent> <F2> <C-O>:w<CR>

" F3 - clear search highlighting
map <silent> <F3> :nohlsearch<CR>
imap <silent> <F3> <C-O>:nohlsearch<CR>

" F[4-5] - searching files with ripgrep: the word under the cursor, or a prompt.
nnoremap <F4> :Rg<Space><C-R><C-W><CR>
inoremap <F4> <ESC>:Rg<Space><C-R><C-W><CR>

nnoremap <F5> :Rg<Space>
inoremap <F5> <ESC>:Rg<Space>

" Split with Space+[vs]
" Move across buffers with Space+[hjkl] or Double space.
nnoremap <Space> <C-w>
nnoremap <Space><Space> <C-w>w

" Insert tabs using Shift+Tab disregarding tab mode.
inoremap <S-Tab> <C-V><Tab>

" Map ; to : to avoid having to use shift when using command.
nnoremap ; :
