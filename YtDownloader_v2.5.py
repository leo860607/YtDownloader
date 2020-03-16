# 引入套件
import tkinter as tk
from tkinter.ttk import *
from pytube import YouTube
import time
import sys
import pathlib
import os
from moviepy.editor import *
from moviepy.audio.io.ffmpeg_audiowriter import ffmpeg_audiowrite
from proglog import ProgressBarLogger
synflag=0
tempdata=0
maxvalue=0
SavePath=pathlib.Path(__file__).parent.absolute()
# 建立主視窗和 Frame（把元件變成群組的容器）
window = tk.Tk()
window.title('Dracula')
window.configure(background='white')

# 將元件分為 top/message/bottom 三群並加入主視窗
top_frame = tk.Frame(window)
top_frame.pack(fill=tk.X)
sec_frame = tk.Frame(window)
sec_frame.pack(fill=tk.X)
trd_frame = tk.Frame(window)
trd_frame.pack(fill=tk.X)
message = tk.Frame(window)
message.pack(fill=tk.X)
progressbar1 = tk.Frame(window)
progressbar1.pack(fill=tk.X)
progressbar2 = tk.Frame(window)
progressbar2.pack(fill=tk.X)
bottom_frame = tk.Frame(window)
bottom_frame.pack(fill=tk.X)

def quit():
    window.destroy()
def progress_function(stream, chunk, bytes_remaining):
    window.update()
    global maxvalue
    progressvar["value"]=maxvalue-bytes_remaining
    progressvar.update()
def PreDownload():
    progressvar.pack_forget()
    hidden41.pack_forget()
    progressvar2.pack_forget()
    hidden51.pack_forget()
    left_button.state='DISABLED'
    downloadProgress.set("Tracking Video")
    videourl=entryURLString.get()
    if videourl == "":
        downloadProgress.set("Naughty Dude, u should paste the url in the textbox !!")
    else:
        window.update()
        #用來讓windows不要把他視為沒反應，不過好像沒有效的港覺
        DownloadVideo(0,videourl)
    left_button.state='NORMAL'
def MP3PreDownload():
    progressvar.pack_forget()
    hidden41.pack_forget()
    progressvar2.pack_forget()
    hidden51.pack_forget()
    right_button.state='DISABLED'
    downloadProgress.set("Tracking Video")
    videourl=entryURLString.get()
    if videourl == "":
        downloadProgress.set("Naughty Dude, u should paste the url in the textbox !!")
    else:
        #用來讓windows不要把他視為沒反應，不過好像沒有效的港覺
        downloadProgress.set("Tracking Video")
        window.update()
        filename=DownloadVideo(1,videourl)
        window.update()
        converttomp3(filename)
    right_button.state='NORMAL'
def MP3Convert():
    progressvar.pack_forget()
    hidden41.pack_forget()
    progressvar2.pack_forget()
    hidden51.pack_forget()
    filename=entryfileString.get()
    if not(".mp4" in filename):
        filename=filename+".mp4"
    filename=os.path.join(SavePath,"YTdownloads",filename)
    if not os.path.isfile(filename):
        downloadProgress.set("there isn't an video file in the path "+filename)
        return
    converttomp3(filename)
def DownloadVideo(flag,videourl):
    global maxvalue
    #取得影片資訊
    yt = YouTube(videourl,on_progress_callback=progress_function)
    stream = yt.streams.get_highest_resolution()
    #進度條設定
    maxvalue=stream.filesize
    progressvar["value"]=0
    progressvar["maximum"]=stream.filesize
    #add "ascii=True" to fix the progress bar problem that it can't display in same line on windows command line 
    #開始下載
    window.update()
    downloadProgress.set("Download ING")
    hidden41.pack(padx=5, pady=10,side=tk.LEFT)
    progressvar.pack(padx=5, pady=10,side=tk.LEFT)
    if flag==0:
        stream.download(os.path.join(SavePath,"YTdownloads"))
    else:
        stream.download(os.path.join(SavePath,"YTdownloads"))
    #下載完成
    if progressvar["value"]==0:
        downloadProgress.set("It has been download before \n your file is save in "+os.path.join(SavePath,"YTdownloads"))
    else:
        downloadProgress.set("Mission Complete!\n \n your file is save in \""+os.path.join(SavePath,"YTdownloads\""))
    return stream.default_filename

def converttomp3(filename):
    hidden51.pack(padx=5, pady=10,side=tk.LEFT)
    progressvar2.pack(padx=5, pady=10,side=tk.LEFT)
    progressvar.pack_forget()
    hidden41.pack_forget()
    videoname=os.path.join(SavePath,"YTdownloads",filename)
    mp3filename=os.path.join(SavePath,"YTdownloads",filename.replace("mp4","mp3"))
    downloadProgress.set("convert ING")
    window.update()
    logger = fakeprogressbar()
    #ffmpeg_tools.ffmpeg_extract_audio(videoname,mp3filename)
    video = VideoFileClip(videoname)
    totalsize = int(video.audio.fps*video.audio.duration)
    progressvar2['maximum']=totalsize
    progressvar2["value"]=0
    video.audio.write_audiofile(mp3filename,logger=logger)

    print("done convert!!!!")
    downloadProgress.set("MP3 convert Done\n\n\n your file has been saved in >>\n"+mp3filename)


class fakeprogressbar(ProgressBarLogger):
    def callback(self, **changes):
    #註解ffmpeg_audiowrite.py的160、176
    #並讓AudioClip.py回傳chunk的size

    # Every time the logger is updated, this function is called with
    # the `changes` dictionnary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            progressvar2["value"]=progressvar2["value"]+value
            progressvar2.update()
            #print ('Parameter %s is now %s' % (parameter, value))
            #progressvar2.update()


        

# 以下為 top 群組
labelURL = tk.Label(top_frame,text = "URL",width=10)
labelURL.pack(padx=5, pady=5, side=tk.LEFT)
URLString = tk.StringVar()
entryURLString = tk.Entry(top_frame, width=80, textvariable=URLString)
entryURLString.pack(padx=5, pady=5, side=tk.LEFT)
left_button = tk.Button(top_frame, text='MP4Download', fg='black',command=PreDownload,width=15)
left_button.pack(padx=5, pady=5, side=tk.LEFT)


hidden21 = tk.Label(sec_frame,width=10)
hidden21.pack(padx=5, pady=5, side=tk.LEFT)
hidden22 = tk.Label(sec_frame,width=80)
hidden22.pack(padx=5, pady=5, side=tk.LEFT)
right_button = tk.Button(sec_frame, text='MP3Download', fg='black',command=MP3PreDownload,width=15)
right_button.pack(padx=5, pady=5, side=tk.LEFT)

labelfile = tk.Label(trd_frame,text = "FileName",width=10)
labelfile.pack(padx=5, pady=5, side=tk.LEFT)
fileString = tk.StringVar()
entryfileString = tk.Entry(trd_frame, width=80, textvariable=fileString)
entryfileString.pack(padx=5, pady=5, side=tk.LEFT)
file_button = tk.Button(trd_frame, text='MP3Convert', fg='black',command=MP3Convert,width=15)
file_button.pack(padx=5, pady=5, side=tk.LEFT)
# 以下為 message 群組
hidden31 = tk.Label(message,width=10)
hidden31.pack(padx=5, pady=10, side=tk.LEFT)
downloadProgress=tk.StringVar()
downloadMessage =tk.Label(message,width=80,wraplength=550,textvariable=downloadProgress,justify=tk.LEFT)
downloadMessage.pack(padx=5, pady=10,side=tk.LEFT)

# 以下為 progressbar 群組
hidden41 = tk.Label(progressbar1,width=10,text="Download")
hidden41.pack_forget()
progressvar = Progressbar(progressbar1, length = 550, mode = 'determinate')
progressvar.pack_forget()#隱藏元件
hidden51 = tk.Label(progressbar2,width=10,text ="Convert")
hidden51.pack_forget()
progressvar2 = Progressbar(progressbar2, length = 550, mode = 'determinate')
progressvar2.pack_forget()#隱藏元件
# 以下為 bottom 群組
bottom_button = tk.Button(bottom_frame, text='QUIT', fg='black', command=quit)
bottom_button.pack(padx=5, pady=10)

downloadProgress.set(r"""
It is a tool to download Youtube video as mp4.
And it can convert it to mp3.

<<<<<<<<<<!!!!!!Warning!!!!!!>>>>>>>>>>
1. If it is stucked when u just push the button, u may be blocked ip by Youtube,
       Since u has downloaded too much films in a short time. 
2. the file you want to convert must put in the "YTdownloads" dirctory.


                        =/\                 /\=
                        / \'._   (\_/)   _.'/ \
                       / .''._'--(o.o)--'_.''. \
                      /.' _/ |`'=/ " \='`| \_ `.\
                     /` .' `\;-,'\___/',-;/` '. '\
                    /.-'       `\(-V-)/`       `-.\
                    `            "   "            `   
                                                            DRACULA 4 EVER
                                                            IU 4 EVER
""")

# 運行主程式
window.mainloop()