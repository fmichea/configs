" backup.vim

set backup
set backupdir=~/.vimtmp/backup
set directory=~/.vimtmp/temp

silent !mkdir -p ~/.vimtmp/backup
silent !mkdir -p ~/.vimtmp/temp

if version >= 703
   set undofile
   set undodir=~/.vimtmp/undo
   silent !mkdir -p ~/.vimtmp/undo
endif

let g:netrw_home=$XDG_CACHE_HOME.'/vim'
