from __future__ import unicode_literals
import youtube_dl
import os

from tgbot.config import BASE_DIR

ydl_opts = {
    "format": "bestaudio/best",
    #"quiet": "--quiet",
    "forcefilename": "True",
    "getfilename": "--get-filename",
    "--get-filename": True,
    "outtmpl": "%(id)s.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

def download(url=None, messages=False):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            audio = ydl.extract_info(url, download=False)
            ydl.download([url])
            if messages:
                print(f"Downloaded: {audio['title']}")

        return audio
    
    except Exception as error:
        print(str(error))


if "__main__" == __name__:
    download()