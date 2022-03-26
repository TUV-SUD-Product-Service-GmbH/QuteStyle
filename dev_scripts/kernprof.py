"""
Script to run kernprof/line_profiler.

To install line_profiler wheels file can be used like this:
$ pip install line_profiler@https://download.lfd.uci.edu/...

Uptodate urls: https://pypi.bartbroe.re/line_profiler/
"""
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run(["kernprof", "-l", "main.py"], check=False)
    subprocess.run(
        [sys.executable, "-m", "line_profiler", "main.py.lprof"], check=False
    )
