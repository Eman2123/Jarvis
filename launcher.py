"""Entry point for the packaged Jarvis.exe (also works from source).

Same behaviour as www/run.py: one process runs the UI/backend, a second one
listens for the "jarvis" hotword.
"""
import multiprocessing
import sys

from engine.features import hotword
from main import start


def start_jarvis():
    start()


def listen_hotword():
    hotword()


if __name__ == "__main__":
    # Required so PyInstaller-built exes do not re-launch themselves
    # endlessly when multiprocessing spawns a child process.
    multiprocessing.freeze_support()

    p1 = multiprocessing.Process(target=start_jarvis)
    p2 = multiprocessing.Process(target=listen_hotword)

    p1.start()
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    sys.exit(0)
