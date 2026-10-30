" Activate spell checker for text files.
au BufRead,BufNewFile *.{txt,markdown,rst} set spell
au BufRead,BufNewFile CMakeLists.txt set nospell
