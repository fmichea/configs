" keyboard.vim - Key Bindings

" F1
set pastetoggle=<F1>

" F[2-4]
imap <silent> <F2> <ESC>:w<CR>
imap <silent> <F3> <ESC>:x<CR>
imap <silent> <F4> <ESC>:q<CR>

map <silent> <F1> <nop>
map <silent> <F2> :w<CR>
map <silent> <F3> :x<CR>
map <silent> <F4> :q<CR>

" F[5-6]
imap <silent> <F5> <ESC>:make<CR>
imap <silent> <F6> <ESC>:cp<CR>
imap <silent> <F7> <ESC>:cn<CR>

map <silent> <F5> :make<CR>
map <silent> <F6> :cp<CR>
map <silent> <F7> :cn<CR>

" Other stuff.
map <C-f> ][%<up>0v<down>%
nnoremap <Space> <C-w>
nnoremap <Space><Space> <C-w>w

" Arrows
"imap <silent> <Left> <nop>
"imap <silent> <Up> <nop>
"imap <silent> <Right> <nop>
"imap <silent> <Down> <nop>
"
"map <silent> <Left> <nop>
"map <silent> <Up> <nop>
"map <silent> <Right> <nop>
"map <silent> <Down> <nop>