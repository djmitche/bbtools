" stupid typos
ab buidlbot buildbot
ab Buidlbot Buildbot

" rgrep on 'K'
set keywordprg=git\ grep

fun! <SID>display_debug_log()
    tabnew
    setlocal buftype=nofile
    setlocal bufhidden=delete
    setlocal noswapfile
    0r/tmp/trialtemp/test.log
endfun

let g:checkfile = ''
fun! <SID>set_check()
    let g:checkfile = expand("%")
    echohl Preproc
    echo 'check: ' . g:checkfile
    echohl
endfun

fun! <SID>set_check_input()
    let g:checkfile = input("check name [" . g:checkfile ."]: ", g:checkfile)
    echohl Preproc
    echo 'check: ' . g:checkfile
    echohl
endfun

fun! <SID>run_check()
    exec '!dev trial ' . g:checkfile
endfun

" display debug log
nmap <Leader>l :call <SID>display_debug_log()<cr>

" run a master or a slave
nmap <Leader>m :!dev master<cr>
nmap <Leader>s :!dev slave<cr>

" set checks
nmap <Leader>= :call <SID>set_check()<cr>
nmap <Leader>+ :call <SID>set_check_input()<cr>

" run checks
nmap <Leader><Leader> :call <SID>run_check()<cr>

" pyflakes
nmap <Leader>p :make pyflakes<cr>
nmap <Leader><tab> :cnext<cr>

" highlight "buidl"
autocmd BufWinEnter * syn match Buidl "[Bb]uidl"
autocmd BufWinEnter * hi def link Buidl SpellBad

" show tabs
set list
set listchars=tab:▷⋅,trail:⋅,nbsp:⋅

command! -nargs=? HighlightLongLines call s:HighlightLongLines('<args>')
function! <SID>HighlightLongLines(width)
    exec 'match SpellBad /\%>' . (a:width+1) . 'v/'
endfunction

" show too-long lines
autocmd BufWinEnter *.py hi def link TooLong SpellBad
autocmd BufWinEnter *.py match TooLong /\%>80v/

" alternate between files and their tests
" (see home-vimrc for how this is invoked)
function! GetAlternateFile()
    let l:fullpath = expand("%:p")
    let l:base_re = ".*\\(master\\/buildbot\\|slave\\/buildslave\\)"
    let l:test_re = l:base_re . "\\/test\\/unit\\/test_\\([a-zA-Z0-9_]*\\.py\\)"
    let l:source_re = l:base_re . "\\/\\([a-zA-Z0-9_\\/]*\\.py\\)"
    if l:fullpath =~ l:test_re
        " convert the test path to a file path
        let l:base = substitute(l:fullpath, l:test_re, "\\1", "")
        let l:test = substitute(l:fullpath, l:test_re, "\\2", "")
        let l:fname = l:base . "/" . substitute(l:test, "_", "/", "g")
        if filereadable(l:fname)
            return l:fname
        else
            " try stripping the last component
            let l:fname = substitute(l:fname, "\/[a-zA-Z0-9]*\\.py$", ".py", "")
            return l:fname
        endif
    elseif l:fullpath =~ l:source_re
        let l:base = substitute(l:fullpath, l:source_re, "\\1", "")
        let l:src = substitute(l:fullpath, l:source_re, "\\2", "")
        let l:fname = l:base . "/test/unit/test_" . substitute(l:src, "/", "_", "g")
        return l:fname
    endif
    return ''
endfunction
