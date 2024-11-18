import os
import shutil
from pathlib import Path

# # run the user's program in our generated folders
os.chdir('module/root_folder')


def ls(args):
    flags = ''
    for arg in args:
        if arg.startswith('-'):
            flags += arg[1:]

    entries = os.listdir()
    directories = []
    files = []

    for entry in entries:
        full_path = Path(entry)
        if full_path.is_dir():
            directories.append(full_path)
        else:
            files.append(full_path)

    for directory in directories:
        print(directory.name)

    if 'l' in flags:
        for file in files:
            stat = file.stat()
            size = stat.st_size
            if 'h' in flags:
                unit = 'B'
                for u in ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
                    if size < 1024:
                        break
                    unit = u
                    size /= 1024.0
                size_str = f"{size:.0f}{unit}"
                print(f'{file.name} {size_str}')
            else:
                print(f'{file.name} {size}')
    else:
        for file in files:
            print(file.name)


while True:
    line = input()
    tokens = line.split()

    match tokens:
        case ['pwd']:
            print(Path.cwd())
        case ['cd', *path]:
            directory = ''.join(path)
            try:
                os.chdir(directory)
            except FileNotFoundError:
                print('Directory does not exist')
            path = Path.cwd()
            print(path.name)
        case ['ls', *args]:
            ls(args)
        case ['rm', *path]:
            path = ''.join(path)
            if not path:
                print('Specify the file or directory')
            else:
                if len(path) > 1 and path.startswith('.'):
                    glob_files = list(Path.cwd().glob(f'*{path}'))
                    if glob_files:
                        for f in glob_files:
                            f.unlink()
                    else:
                        print(f'File extension {path} not found in this directory')
                else:
                    path = Path(path)
                    if path.exists():
                        if path.is_dir():
                            shutil.rmtree(path)
                        else:
                            path.unlink()
                    else:
                        print('No such file or directory')
        case ['mv', *args]:
            if len(args) != 2:
                # print line unit test specs changed for test #6
                print('Specify the current name of the file or directory and the new location and/or name')
                continue
            file_from, file_to = Path(args[0]), Path(args[1])
            if len(args[0]) > 1 and args[0].startswith('.'):
                glob_files = list(Path.cwd().glob(f'*{args[0]}'))
                if glob_files:
                    for f in glob_files:
                        if (file_to/f).exists():
                            while True:
                                print(f'{f} already exists in this directory. Replace? (y/n)')
                                line = input()
                                match line:
                                    case 'y':
                                        shutil.move(file_from, file_to)
                                    case 'n':
                                        break
                                    case _:
                                        continue
                        else:
                            shutil.move(file_from, file_to)
                else:
                    print(f'File extension {args[0]} not found in this directory')

            if not file_from.exists():
                print('No such file or directory')
                continue
            if file_to.is_dir():
                if (file_from / file_to).exists():
                    print('The file or directory already exists')
                    continue
                file_from.rename(file_to/file_from)
            else:
                if file_to.exists():
                    print('The file or directory already exists')
                    continue
                file_from.rename(file_to)
        case ['mkdir']:
            print('Specify the name of the directory to be made')
        case ['mkdir', path]:
            path = Path(path)
            if path.exists():
                print('The directory already exists')
            else:
                path.mkdir()
        case ['cp', *args]:
            if len(args) == 0:
                print('Specify the file')
                continue
            if len(args) != 2:
                print('Specify the current name of the file or directory and the new location and/or name')
                continue
            file_from, file_to = Path(args[0]), Path(args[1])
            if len(args[0]) > 1 and args[0].startswith('.'):
                glob_files = list(Path.cwd().glob(f'*{args[0]}'))
                if glob_files:
                    print(glob_files)
                    for f in glob_files:
                        print('checking', (file_to/f), Path.cwd())
                        if (file_to/f).exists():
                            while True:
                                print(f'{f.name} already exists in this directory. Replace? (y/n)')
                                line = input()
                                match line:
                                    case 'y':
                                        shutil.copy(f, file_to)
                                        break
                                    case 'n':
                                        break
                                    case _:
                                        continue
                        else:
                            shutil.copy(f, file_to)
                else:
                    print(f'File extension {args[0]} not found in this directory')
            if not file_from.exists():
                print('No such file or directory')
                continue
            if file_to.is_dir():
                if (file_from/file_to).exists():
                    print(f'{file_from} already exists in this directory')
                    continue
            else:  # lacks file_from.exists() check?
                print(f'{file_from} already exists in this directory')
                continue
            if file_from.is_dir():
                shutil.copytree(file_from, file_to)
            else:
                shutil.copy(file_from, file_to)
        case [_]:
            print('Invalid command')
        case ['quit']:
            break
