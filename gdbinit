# Save history in gdb.
set history save

# Always display the three next instructions, in intel syntax.
set disassembly-flavor intel

set $display_instr_done = 0
define hook-run
    if ! $display_instr_done
        display/3i $pc
        set $display_instr_done = 1
    end
end

# Follow childs in forks most of the time, so default policy.
set follow-fork-mode child

# Per computer safe-paths are configured here.
source ~/.gdbinit_safepaths

# vim: filetype=gdb
