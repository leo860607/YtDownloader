#ProgressBar >> tdqm : https://tqdm.github.io/docs/tqdm/#update
#Pytube >> pytube3 : https://python-pytube.readthedocs.io/en/latest/api.html
#Pack to exe >> pyinstaller : https://medium.com/pyladies-taiwan/python-%E5%B0%87python%E6%89%93%E5%8C%85%E6%88%90exe%E6%AA%94-32a4bacbe351
#get audio part >> MoviePy : https://stackoverflow.com/questions/55081352/how-to-convert-mp4-to-mp3-using-python

from pytube import YouTube
from tqdm import tqdm
from moviepy.editor import *
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
#add "ascii=True" to fix the progress bar problem that it can't display in same line on windows command line 
pbar=tqdm(total=stream.filesize, position=0, leave=True,ascii = True)
with pbar:
    stream.download(str(SavePath)+"/YTdownloads")
pbar.close()
print("Done Video download >> ")

#USE Moviepy to clip the audio part from mp4
mp3Chose=input("Want to convert to mp3 ?(Y/N) ")
if mp3Chose == "Y":
    video = VideoFileClip(str(SavePath)+"/YTdownloads/"+stream.default_filename)
    #Since default_filename has .mp4 suffix, Replace it with mp3 before saveing file
    mp3filename=stream.default_filename.replace("mp4","mp3")
    video.audio.write_audiofile(str(SavePath)+"/YTdownloads/"+stream.default_filename+".mp3")
print("MP3 convert done >> ")
os.system("pause")


