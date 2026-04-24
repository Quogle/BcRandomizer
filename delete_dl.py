import os
from dev.randomizer.data.filepaths import *


def kill_dl():
    files = os.listdir(DOWNLOAD_LOCAL)
    for each in files:
        os.remove(DOWNLOAD_LOCAL + each)
    print("killed all files in download local\n")

kill_dl()





