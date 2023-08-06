from pick import pick
import os
import os.path


def select_file(title='Choose a file.', exts=('',)):
    file_selected = False
    path = os.getcwd()
    while not file_selected:
        files = ['../']
        for name in os.listdir(path):
            if not name.lower().endswith(exts) and os.path.isfile(os.path.join(path, name)):
                continue
            files.append(
                name + ('/' if os.path.isdir(os.path.join(path, name)) else ''))
        selection = pick(files, f'{title} CWD: {path}')
        path = os.path.join(path, selection[0])
        path = os.path.abspath(path)
        if os.path.isfile(path):
            file_selected = True
    return path


def select_folder(title='Choose a folder.'):
    selected = False
    path = os.getcwd()
    while not selected:
        folders = ['../']
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                continue
            folders.append(name + '/')
        folders.append('Choose current folder')
        selection = pick(
            folders, f'{title} CWD: {path}')
        if selection[0] == 'Choose current folder':
            return path
        path = os.path.join(path, selection[0])
        path = os.path.abspath(path)
