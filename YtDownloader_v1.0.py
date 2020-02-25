#ProgressBar >> tdqm : https://tqdm.github.io/docs/tqdm/#update
#Pytube >> pytube3 : https://python-pytube.readthedocs.io/en/latest/api.html
#Pack to exe >> pyinstaller : https://medium.com/pyladies-taiwan/python-%E5%B0%87python%E6%89%93%E5%8C%85%E6%88%90exe%E6%AA%94-32a4bacbe351

from pytube import YouTube
from tqdm import tqdm
import time
import sys
import pathlib
import os
SavePath=pathlib.Path(__file__).parent.absolute()
tempdata=0

def progress_function(stream, chunk, bytes_remaining):
    global tempdata
    global pbar
    progress=tempdata-bytes_remaining
    pbar.update(progress)
    tempdata=bytes_remaining

videourl=input("paste video Url: ")
yt = YouTube(videourl,on_progress_callback=progress_function)
stream = yt.streams.get_highest_resolution()
tempdata=stream.filesize
pbar=tqdm(total=stream.filesize)
with pbar:
    stream.download(str(SavePath)+"/YTdownloads")
pbar.close()
print("done")
os.system("pause")


