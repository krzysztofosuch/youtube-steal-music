import youtube_dl
import pydub
import re
import eyed3
def read_lines(msg):
    print(msg)
    buf = []
    while True:
        line = input()
        if line:
            buf.append(line)
        else:
            break
    return buf

def process_file(arg):
    if arg['status'] == 'finished':
        recode_file(arg["filename"])

def recode_file(filename):
    audio = pydub.AudioSegment.from_file(filename, "webm")
    for n, line in enumerate(split):
        if line:
            (time, tags) = line.split(" ", 1)
            seconds = time_to_sec(time)
            print(n, split[n])
            if n+1 < len(split) and split[n+1]:
                (time2, _) = split[n+1].split(" ", 1);
                seconds_end = time_to_sec(time2)
            else:
                seconds_end = None
            if (seconds_end):
                song = audio[seconds*1000:seconds_end*1000]
            else:
                song = audio[seconds*1000:]
            if (reverse_tag):
                (title, artist) = re.split(':|—|\W-\W', tags, 1)
            else:
                (artist, title) = re.split(':|—|\W-\W', tags, 1)
            mp3path = "download/%s-%s.mp3"%(artist.strip(), title.strip())
            song.export(mp3path, format="mp3", bitrate="320k")
            audiofile = eyed3.load(mp3path)
            audiofile.tag.artist = artist.strip()
            audiofile.tag.album = filename[:-17].strip()
            audiofile.tag.title = title.strip()
            audiofile.tag.track_num = n
            audiofile.tag.save()
            
def time_to_sec(time):
    seconds = 0;
    for place, num in enumerate(reversed(time.split(":"))):
        seconds += (60**place)*int(num)
    return seconds
url = input("Youtube URL?")
split = read_lines("How to split them?")
reverse_tag = input("reverse title-artist order? [y/N]").lower() == 'y'

if len(split)<2:
    split = None
ydl_opts = {
    "format": "bestaudio/none",
    "progress_hooks": [process_file]
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

