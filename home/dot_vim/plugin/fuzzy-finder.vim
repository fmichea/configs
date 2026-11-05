" fuzzy-finder.vim - fzf.vim configuration

" Ctrl-P - find files: tracked and untracked, not ignored, in a git repository.
function! s:FindFiles() abort
    silent call system('git rev-parse --is-inside-work-tree')
    if v:shell_error == 0
        GFiles --cached --others --exclude-standard
    else
        Files
    endif
endfunction

nnoremap <silent> <C-p> :call <SID>FindFiles()<CR>
