import sys
import os
import multiprocessing

#  Make sure Python can find "engine" and "main.py"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))





from engine.features import hotword
from main import start

def startJarvis():
    print("Process 1 is running.")
    start()

def listenHotword():
    print("Process 2 is running.")
    hotword()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)

    p1.start()
    p2.start()
    p1.join() 

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("system stop")


