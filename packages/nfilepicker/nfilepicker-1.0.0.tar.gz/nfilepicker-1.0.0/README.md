# NFilePicker

A Python package that creats a file/folder picker
with `ncurses`.

## Getting Started

```py
>>> from nfilepicker import (
...  select_file,
...  select_folder
... )
>>> select_file(
...  'Choose a database.',
...  (
...    '.db',
...    '.sqlite3',
...  )
... )
'/Users/person/Desktop/file.txt'
>>> select_folder('Choose a folder.')
'/usr/libexec'
```

## Prerequisites
On Windows, this package requires the `windows-curses` package.