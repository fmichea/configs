" indent_guides.vim - Indent Guides plugin configuration

let g:indent_guides_enable_on_vim_startup = 1

let g:indent_guides_start_level = 2
let g:indent_guides_guide_size = 1

if !has("gui_running") && &t_Co == 256
    let g:indent_guides_auto_colors = 0
    autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd ctermbg=236
    autocmd VimEnter,Colorscheme * :hi IndentGuidesEven ctermbg=234
endif
