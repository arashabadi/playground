Here I will document the setup of my macOS MacBook Pro.

## Table of Contents
- [ssh to Github](#ssh-to-github)
- [ssh to Cheaha](#ssh-to-cheaha)
- [UAB VPN](#uab-vpn)
- [Jupyter lab](#jupyter-lab)
- [VSCode](#vscode)


## Jupyter lab
This is a modified version of this [gist](https://gist.github.com/discdiver/9e00618756d120a8c9fa344ac1c375ac#file-jupyterlab_shortcuts-md) code for macOS shortcuts.

Shortcuts when in either _command mode_ (outside the cells) or _edit mode_ (inside a cell):
---
- `Shift` + `Enter` run selected cell or cells - if no cells below, insert a code cell below

- `Command` + `B` toggle hide/show left sidebar

- `Command` + `S` save and checkpoint
- `Command` + `Shift` + `S` save as
- `Command` + `F` find 

Shortcuts when in _command mode_ (outside the cells, no blinking cursor):
---
- `Enter` enter _edit mode_ in the active cell

- Scroll up with the up arrow 
- Scroll down with the down arrow

- `A` insert a new cell above the active cell
- `B` insert a new cell below the active cell

- `M` make the active cell a Markdown cell
- `Y` make the active cell a code cell

- `Shift` + `Up Arrow` select the current cell and the cell above
- `Shift` + `Down Arrow` select the current cell and the cell below
- `Command` + `A` select all cells

- `X` cut the selected cell or cells
- `C` copy the selected cell or cells
- `V` paste the cell(s) which were copied or cut most recently

- `Shift + M` merge multiple selected cells into one cell

- `DD` (`D` twice) delete the active cell
- `00` (Zero twice) restart the kernel

- `Z` undo most recent command mode action

Shortcuts when in _edit mode_ (inside a cell with a blinking cursor):
---

- `Esc` enter _command mode_

- `Tab` code completion (or indent if at start of line)
- `Shift` + `Tab` tooltip help
- `Command` + `Shift` + `-` split the active cell at the cursor

The usual commands for code editors:

- `Command` + `]` indent
- `Command` + `[` dedent

- `Command` + `/` toggle comment

Plus the usual shortcuts for select all, cut, copy, paste, undo, etc.






