# -*- coding: utf-8 -*-
r"""
Library for shell commands and sub processes.
Adapted from Moritz Goerzen's library 08.2018 (Spintronic Theory Kiel).
"""
import os
import platform
import subprocess
import sys
import shellcommands.constants as const
from contextlib import contextmanager
from pathlib import Path
from typing import Union, TypeVar


PathLike = TypeVar("PathLike", str, Path)

# operating system
OPERATINGSYSTEM = platform.system()


@contextmanager
def change_directory(newdir: PathLike) -> None:
    r"""
    Changes the directory using context manager. Will automatically put everything before the yield statement into the
    __enter__-method and everythin behind in the __exit__method.

    Args:
        newdir(str): name of the directory. Has to be a subdirectory of the actual directory.
    """
    prevdir = Path.cwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def copy_element(target: PathLike, destination: PathLike) -> None:
    r"""
    Copies an element (target) to a destination. Chooses the command based on OS. On windows the shell=True flag
    must be set. Should be replaced someday by shutil.which
    (https://stackoverflow.com/questions/3022013/windows-cant-find-the-file-on-subprocess-call)

    Args:
        target(PathLike): target file
        destination(PathLike): destination file
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "copy " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "cp " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def make_directory(directory: PathLike) -> None:
    r"""
    Creates directory. Chooses the command based on OS. It is possible to create multiple nested directories. It is
    highly recommended to use the input type of pathlibs Path then. Otherwise one has to set the correct back- or
    forward slashes. This destroys the benefit of this platform indepent implementation.

    Args:
        directory(PathLike): new directory
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "md " + str(directory)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "mkdir " + str(directory)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def copy_folder(target: PathLike, destination: PathLike) -> None:
    r"""
    Copies folder from target to destination. Chooses the command based on Os. For windows the /i flag supresses asking
    whether copying and the /e flag enables empty copying.
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "xcopy " + str(target) + " " + str(destination) + "/i /e"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "cp -r " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def remove_element(filename: PathLike) -> None:
    r"""
    Removes element (filename). Chooses the command based on Os. The windows /q flag is for silent removing. If the file
    is given as a path it is highly recomm. to use pathlibs Path for platform indepent input.
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "del " + str(filename) + " /q"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "rm" + str(filename)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def remove_folder(directory: PathLike) -> None:
    r"""
    Removes directory with everything inside. Chooses the command based on Os. The windows /s flag is for
    deleting subfolders and files and the /q flag is for silent modus.
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "rmdir " + str(directory) + " /s /q"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "rm -r" + str(directory)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def call_povray(script: PathLike, w: int = 2000, h: int = 2000) -> None:
    r"""
    Calls a povray script from the command line. For windows the environment variable pvengine has to be set. This
    interface is programmed for Povray3.7 GUI for windows.

    Args:
        script(PathLike): .pov file
        w(int, Optional): width. Default is 2000
        h(int, Optional): height. Default is 2000
    """
    if OPERATINGSYSTEM == 'Windows':
        command = 'pvengine /NR /EXIT /RENDER ' + str(script) + ' -d' + ' -w' + str(w) + ' -h' + str(h)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "povray -d" + " -w" + str(w) + " -h" + str(h) + " " + str(script)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()


def call_spin(pathtoexecutable: PathLike = None) -> None:
    r"""
    Calls the spin D algorithm

    Args:
        pathtoexecutable(PathLike, Optional): the path to the SpinD executable. The default is None. In that case the
        default Linux or Windows paths is chosen based on the OS.
    """
    if pathtoexecutable is None:
        if OPERATINGSYSTEM == 'Windows':
            command = const.SPIND_WINDOWS
        elif OPERATINGSYSTEM == 'Linux':
            command = const.SPIND_LINUX
        else:
            raise Exception('operating system not yet coded.')
    else:
        command = pathtoexecutable
    with open('job.out','a') as f:
        process = subprocess.Popen(command.split(), stdout=f, shell=True)
    output, error = process.communicate()
