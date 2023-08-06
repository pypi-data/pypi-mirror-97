# NFilePicker

A Python package that creates a file/folder picker
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
'/Users/person/Desktop/list.db'
>>> select_folder('Choose a folder.')
'/usr/libexec'
```

## Prerequisites
On Windows, this package requires the `windows-curses` package.

## Features
Version 1.0.2 has the ability to select files case insensitively. This
version of NFilePicker will display ABC123.JPG (Note the capitalized 'JPG')
as a *.jpg file.
