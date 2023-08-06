# -*- coding: utf-8 -*-
import os
import sys
import platform
import multiprocessing

from multiprocessing import Process, Queue

from ._core import __doc__, run
from ._core import __file__ as module_file_path


# Fix for MacOS High Sierra, see:
# https://stackoverflow.com/questions/30669659/multiproccesing-and-error-the-process-has-forked-and-you-cannot-use-this-corefou
if platform.system() == "Darwin":
    multiprocessing.set_start_method('spawn', force=True)


def _run_wrapper():
    """
    A simple wrapper that changes directory before launching the SpikeRecorder pybind11 module. The module
    needs to run from its location directory because it looks for files.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(os.path.dirname(module_file_path), 'byb.log')
    run(log_file_path)


def launch(is_async: bool = False) -> multiprocessing.Process:
    """
    Lauch the Backyard Brains Spike recorder application. This function launches a subprocess.

    Args:
        is_async: Should the this function run asynchronously. That is, should it return instantly or
            block until the application closes.

    Returns:
        The Process containing the SpikeRecorder application.
    """
    p = Process(target=_run_wrapper)
    p.start()

    if not is_async:
        p.join()

    return p


def main():
    launch()


if __name__ == "__main__":
    main()

