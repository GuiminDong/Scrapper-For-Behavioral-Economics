import os
import time
import threading




def startThread(dir, name):
    t = threading.Thread(target=callPython, args=(dir,))
    t.setDaemon(True)
    t.setName(name)
    t.start()

def callPython(cmd):
    print cmd
    os.system("python " + cmd)



if __name__ == "__main__":
    year = 1995
    while year <= 2017:
        startThread("giustizia.py " + str(year) + " > " + str(year) + ".log", str(year))
        year += 1
    while 1:
        time.sleep(999999)
