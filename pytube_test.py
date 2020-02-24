from pytube import YouTube



videourl=input("貼上網址: ")
YouTube(videourl).streams.get_highest_resolution().download()