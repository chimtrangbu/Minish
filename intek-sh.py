#!/usr/bin/env python3
import sys
import os
import subprocess


def _cd(directory):  # implement cd
    if directory:
        os.chdir(directory)  # change working directory
    else:  # if variable directory is empty, change working dir into homepath
        if 'HOME' not in os.environ:
            print('intek-sh: cd: HOME not set')
        else:
            homepath = os.environ['HOME']
            os.chdir(homepath)


def _printenv(variable):  # implement printenv
    if variable:
        if variable in os.environ:
            print(os.environ[variable])
    else:  # if variable is empty, print all envs
        for key, value in os.environ.items():
            print(key + '=' + value)


def _export(variables):  # implement export
    varis = variables.split()
    for item in varis:
        if '=' in item:
            params = item.split('=')
            os.environ[params[0]] = params[1]
        else:  # if variable stands alone, set its value as ''
            os.environ[item] = ''


def _unset(variable):  # implement unset
    if variable in os.environ:
        os.environ.pop(variable)


def _exit(exit_code):  # implement exit
    global w_loop
    w_loop = False
    print('exit')
    if exit_code:
        try:
            sys.exit(int(exit_code))
        except ValueError:
            print('intek-sh: exit: ', end='')
            sys.exit(exit_code)
    else:
        sys.exit()


def _else(command, whatever):
    if './' in command:
        try:
            subprocess.run(command)
        except PermissionError:
            print('intek-sh: %s: Permission denied' % command)
        except FileNotFoundError:
            print('intek-sh: %s: command not found' % command)
    elif 'PATH' in os.environ:
        paths = os.environ['PATH'].split(':')
        not_found = True
        for path in paths:
            realpath = path + '/' + command
            if os.path.exists(realpath):
                not_found = False
                subprocess.run([realpath]+whatever)
                break
        if not_found:
            print('intek-sh: %s: command not found' % command)
    else:
        print('intek-sh: %s: command not found' % command)


def main():
    builtins = ('cd', 'printenv', 'export', 'unset', 'exit')
    w_loop = True
    while w_loop:
        try:
            whatever = input('intek-sh$ ').strip(' ').split()
            while not whatever:
                whatever = input('intek-sh$ ').strip(' ').split()
            command = whatever.pop(0)
            if command in builtins:
                exec('_%s(\' \'.join(whatever))' % command)
            else:
                _else(command, whatever)
        except EOFError:
            w_loop = False


if __name__ == '__main__':
    main()
