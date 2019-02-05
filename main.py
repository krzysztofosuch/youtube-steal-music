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
            if n < len(split) and split[n+1]:
                (time2, _) = split[n+1].split(" ", 1);
                seconds_end = time_to_sec(time2)
            else:
                seconds_end = None
            if (seconds_end):
                song = audio[seconds*1000:seconds_end*1000]
            else:
                song = audio[seconds*1000:]
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
url = "https://www.youtube.com/watch?v=u__zkAPMtLc" #input("Youtube URL?")
split = """
0:10 Ляпис Трубецкой — Воины Света
3:53  Агата Кристи — Сказочная тайга
6:45  Танцы минус — Цветут цветы 
10:57  Ляпис Трубецкой — Ты Кинула 
14:56  Пикник — Кукла с человеческим лицом
18:46  Пикник — Кем Бы Ты Ни Был
22:41  ДДТ — Это все
27:31  Агата Кристи — Ковер-вертолет
30:48  Чиж & Co — Вот Пуля Просвистела 
35:17 Король и Шут — Танец злобного гения 
39:40 Ляпис Трубецкой — В Платье Белом
44:38 КняzZ — Пассажир
48:46 Король и Шут — Ели мясо мужики
51:00 Би-2 Feat. Чичерина — Мой Рок-Н-Ролл
57:45 Океан Ельзи — Там, Де Нас Нема
1:01:12 Ляпис Трубецкой — Я верю
1:04:17 СерьГа — Хоровод
1:07:09 Алиса — Трасса E-95
1:11:03 Агата Кристи — Опиум Для Никого
1:15:00 Жуки — Батарейка
1:18:46 ДДТ — Рожденный В СССР
1:23:15 Ленинград — Свобода 
1:26:25 Би-2 — Полковнику никто не пишет
1:31:18  Ольга Кормухина — Путь
1:36:16 Океан Ельзи — Без Бою
1:40:35 Ногу Свело! — Идем На Восток
1:44:06 Король и Шут — Воспоминания О Былой Любви
1:48:40 Ночные Снайперы — Ты дарила мне розы
1:51:45 Ляпис Трубецкой — Шут
1:55:08 Мумий Тролль — Дельфины
1:59:48 Би-2 Feat. Диана Арбенина — Тише И Тише
2:03:15 Ленинград — Супер Гуд
2:05:22 Lascala — Дурочка С Севера
""".split("\n")
#read_lines("How to split them?")
if len(split)<2:
    split = None
ydl_opts = {
    "format": "bestaudio/none",
    "progress_hooks": [process_file]
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

