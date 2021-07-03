import os
import io
from tswift import Song
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls_wrapper import Wrapper

import youtube_dl
from youtube_search import YoutubeSearch
import requests
import time

StartTime = time.time()


API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
SESSION = os.environ.get("SESSION", None) 
PREFIX = os.environ.get("PREFIX", None) 
YT_URL = os.environ.get("YT_URL", None)


app = Client(
      session_name=SESSION,
      api_id=API_ID,
      api_hash=API_HASH,
)


pytgcalls = PyTgCalls(app)
wrapper = Wrapper(pytgcalls, "raw")

REPOLINK = """ Source code: [Github](https://github.com/Moezilla/vc-userbot)
License: [ GPL-3.0 License](https://github.com/moezilla/vc-userbot/blob/master/LICENSE.md)"""

# ......................................................................................................... 
# credits xditya sir 😁😁😅
class Text():
    how_to = "`Either reply to an audio file or give me a youtube link to play from!`"
    not_yet = "`This is not yet supported!`"
    dl = "`Downloading...`"
    
async def play_a_song(wrapper, m, song):
    try:
        await wrapper.stream(message.chat.id, song)
    except Exception as e:
        await m.reply_text(f"ERROR:\n{e}")

@app.on_message(filters.command("play", PREFIX))
async def play(_, m):
    txt = m.text.split(' ', 1)
    type_ = None
    try:
        song_name = txt[1]
        type_ = "url"
    except IndexError:
        reply = m.reply_to_message
        if reply:
            if reply.audio:
                med = reply.audio
            elif reply.video:
                med = reply.video
            elif reply.voice:
                med = reply.voice
            else:
                return await m.reply_text(Text.how_to)
            song_name = med.file_name
            type_ = "tg"
    if type_ == "url":
        if "youtube" not in song_name and "youtu.be" not in song_name:
            return await m.reply_text(Text.not_yet)
        await m.reply_text("Playing `{}`".format(song_name))
        await play_a_song(pycalls, m, song_name)
    elif type_ == "tg":
        x = await m.reply_text(Text.dl)
        file_ = await reply.download()
        await x.edit("`Play`")
        await play_a_song(wrapper, m, file_)
        remove(file_)
    else:
        return await m.reply_text(Text.how_to)

# ...................................................................................... 

@app.on_message(filters.command("stream", PREFIX))
async def stream(_, m): 
    await wrapper.stream(m.chat.id, YT_URL)
    await m.reply_text("Playing song")


@app.on_message(filters.command("pause", PREFIX))
async def pause(_, m):
    wrapper.pause(m.chat.id)
    await m.reply_text("Paused Song.")



@app.on_message(filters.command("resume", PREFIX))
async def resume(_, m):
    wrapper.resume(m.chat.id)
    await m.reply_text("Resume Song.")


@app.on_message(filters.command("song", PREFIX))
def song(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('Searching the song...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Found nothing. Try changing the spelling a little.')
            return
    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("⏬ Downloading.")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 **Title**: [{title[:35]}]({link})\n⏳ **Duration**: `{duration}`\n👁‍🗨 **Views**: `{views}`'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('❌ Error')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


@app.on_message(filters.command("ping", PREFIX))
async def ping(_, message):
    start_time = time.time()
    m = await message.reply_text("Ping")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    uptime = get_readable_time((time.time() - StartTime))
    await m.edit_text(f"Ping - `{ping_time}ms`\nUptime - {uptime}", parse_mode='markdown')

@app.on_message(filters.command("ping", PREFIX))
async def repo(_, message):
    await message.reply_text(REPOLINK)

pytgcalls.run()
