" set nocompatible              " be iMproved, required
" filetype off                  " required
" set the runtime path to include Vundle and initialize
" set rtp+=~/.vim/bundle/Vundle.vim
" call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')
" let Vundle manage Vundle, required
" Plugin 'VundleVim/Vundle.vim'
" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
" Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
" Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
" Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Avoid a name conflict with L9
" Plugin 'user/L9', {'name': 'newL9'}
" Plugin 'fatih/vim-go'
" Plugin 'majutsushi/tagbar'
" Plugin 'taglist.vim'
" Plugin 'The-NERD-tree'
" Plugin 'c.vim'
" Plugin 'Emmet.vim'
" All of your Plugins must be added before the following line
" call vundle#end()            " required
" filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
" set mapleader
let mapleader = ","
au BufRead,BufNewFile *.go set filetype=go
au FileType go nmap <Leader>s <Plug>(go-implements)
au FileType go nmap <Leader>i <Plug>(go-info)
au FileType go nmap <Leader>gd <Plug>(go-doc)
au FileType go nmap <Leader>gv <Plug>(go-doc-vertical)
au FileType go nmap <leader>r <Plug>(go-run)
au FileType go nmap <leader>b <Plug>(go-build)
au FileType go nmap <leader>t <Plug>(go-test)
au FileType go nmap <leader>c <Plug>(go-coverage)
au FileType go nmap <Leader>ds <Plug>(go-def-split)
au FileType go nmap <Leader>dv <Plug>(go-def-vertical)
au FileType go nmap <Leader>dt <Plug>(go-def-tab)
au FileType go nmap <Leader>e <Plug>(go-rename)
let g:go_highlight_functions = 1
let g:go_highlight_methods = 1
let g:go_highlight_structs = 1
let g:go_highlight_operators = 1
let g:go_highlight_build_constraints = 1
let g:go_bin_path = "/root/gobin/bin"
let g:go_fmt_command = "goimports"
nmap <F6> :TagbarToggle<CR>
" Tag list (ctags)"
let Tlist_Auto_Open = 1
let Tlist_Ctags_Cmd = '/usr/bin/ctags'
let Tlist_Show_One_File = 1
let Tlist_Exit_OnlyWindow = 1
let Tlist_Use_Right_Window = 1
let Tlist_File_Fold_Auto_Close = 1
let Tlist_Process_File_Always=1
let Tlist_Enable_Fold_Column=1
"NERDTree"
map <F5> :NERDTreeToggle<CR>
"Matrix"
"map <F4> :Matrix<CR>
"basic config"
map <F3> gg=G<CR>
map <F4> "+y
filetype on "自动文件类型识别，基于后缀
filetype plugin on
filetype plugin indent on "支持python的自动对齐
autocmd FileType python setlocal et sta sw=4 sts=4 "支持pthon的只能缩进
"set fileencodings=utf-8, ucs-bom,,cp936,gb18030,big5,euc-jp,euc-kr,latin1  "设置若打开的文件编码方式与VIM的encoding不同时使用的解码方式为这些依次进行，顺序很重要，因为宽松的编码如latin1放在前面将导致误判
set fileencodings=utf-8
set mouse=a "支持鼠标
set nu"显示行号
set tabstop=4 "缩进tab为4个字符
set shiftwidth=4
set wrap
set ruler
syntax enable "只能语法识别，使用配色
syntax on
set incsearch
set hlsearch "高亮搜索
set cindent "智能缩进
set autoindent
set smartindent
set showmatch
set whichwrap+=h,l
set t_Co=256
if has("vms") "设置是否使用.bak文件
set nobackup
"else
"set backup
endif
let mapleader=","
map <Leader>m :%s/<C-Q><C-M>/\r/g<CR> "删除从window拷贝过来时产生的回车符
"map <Leader>m :g/^\s*$/d<CR>
"wsl
if &term =~ '^xterm'
        " Cursor in terminal:
        " Link: https://vim.fandom.com/wiki/Configuring_the_cursor
        " 0 -> blinking block not working in wsl
        " 1 -> blinking block
        " 2 -> solid block
        " 3 -> blinking underscore
        " 4 -> solid underscore
        " Recent versions of xterm (282 or above) also support
        " 5 -> blinking vertical bar
        " 6 -> solid vertical bar
        " normal mode
        let &t_EI .= "\e[1 q"
        " insert mode
        let &t_SI .= "\e[5 q"
        augroup windows_term
                autocmd!
                autocmd VimEnter * silent !echo -ne "\e[1 q"
                autocmd VimLeave * silent !echo -ne "\e[5 q"
        augroup END
endif
