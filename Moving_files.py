import os
import shutil
cwd=os.getcwd()	#sourcepath=cwd
cwd
sourcefiles = os.listdir(cwd)
destinationpath = './Results_OUTB'
for file in sourcefiles:
    if file.endswith('.outb'):
        shutil.move(os.path.join(cwd,file), os.path.join(destinationpath,file))

destinationpath2 = './Results_SUM'
for file in sourcefiles:
    if file.endswith('.sum'):
        shutil.move(os.path.join(cwd,file), os.path.join(destinationpath2,file))
