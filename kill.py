import os, psutil

command = 'taskkill /F /IM python.exe'
os.system(command)
exit()
for p in psutil.pids():
    name = psutil.Process(p).name()
    if name == "python.exe":
        print psutil.Process(p).pid
        command = 'taskkill ' + str(psutil.Process(p).pid)
        os.system(command)

