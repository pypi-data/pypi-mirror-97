"""
Module for OS relevant functions
"""
import os
import time
import glob
import json

def find_files(directory, prefix="", postfix="", recursive=True, onlyfiles=True,
          fullpath=False, olderthan=None, inorder=False):
    """Find files in a directory.

    Parameters
    ----------
    directory : str
        Directory to search in
    prefix : str (optional)
        Only remove files with this prefix
    postfix : str (optional)
        Only remove files with the postfix
    recursive : Boolean (optional)
        Go into directories recursively. Defaults to True
    onlyfiles : Boolean (optional)
        Show only files. Defaults to True
    fullpath : Boolean (optional)
        Give full path. Defaults to False. If recursive=True, fullpath is given automatically.
    olderthan : int (optional)
        Match only files older than X seconds from now. Defaults to None
    inorder : Boolean (optional)
        Return sorted list of filenames. Defaults to False

    Returns
    -------
    files : list
        List containing file names that matches criterias

    Notes
    -----
    files = find_files('/foo/', prefix="", postfix="", recursive=False, onlyfiles=True, fullpath=True, olderthan=86400*100)
    """

    if recursive:
        fullpath = False
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(directory):
            for file in f:
                if file.startswith(prefix) and file.endswith(postfix):
                    files.append(os.path.join(r, file))

    elif not recursive:

        if onlyfiles:
            files = [f for f in os.listdir(directory) if
                     f.endswith(postfix) and f.startswith(prefix) and
                     os.path.isfile(directory+f)]

        elif not onlyfiles:
            files = [f for f in os.listdir(directory) if
                     f.endswith(postfix) and f.startswith(prefix)]

    if fullpath:
        files = [directory+f for f in files]

    if olderthan is not None:
        now = time.time()
        tfiles = []
        for f in files:
            try:
                if not fullpath:
                    if os.path.getmtime(os.path.join(directory, f)) < (now - olderthan):
                        tfiles.append(f)
                else:
                    if os.path.getmtime(f) < (now - olderthan):
                        tfiles.append(f)
            except FileNotFoundError:
                continue
            
        files = tfiles

    if inorder:
        files = list(sorted(files))

    return files


def clean(files):
    """Removes files from the system.
    Note that filenames must be given as full paths

    Parameters
    ----------
    files : list
        List of files to remove.
    """
    for f in files:
        try:
            os.remove(f)
        except OSError:
            pass
    return


def does_file_exist(f):
    """
    Check if file exist

    Parameters
    ----------
    f : str
        name of file to check

    Returns
    -------
    state : boolean
        Whether the file exist (True) or not exist (False)
    """
    state = os.path.isfile(f)
    return state


def does_dir_exist(f):
    """
    Check if directory exist

    Parameters
    ----------
    f : str
        name of directory to check

    Returns
    -------
    state : boolean
        Whether the directory exist (True) or not exist (False)
    """
    state = os.path.exists(f)
    return state