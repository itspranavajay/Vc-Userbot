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



API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
SESSION = os.environ.get("SESSION", None) 
PREFIX = os.environ.get("PREFIX", None) 
YT_URL = os.environ.get("YT_URL", None)
SUDO_USER = os.environ.get('SUDO_USER')
SUDO_USER = list(map(int, SUDO_USER.split(' '))) if SUDO_USER else []
GROUP_USER = os.environ.get('SUDO_USER')
GROUP_USER = list(map(int, SUDO_USER.split(' '))) if SUDO_USER else []
MOE_USER = SUDO_USER + GROUP_USER


app = Client(
      session_name=SESSION,
      api_id=API_ID,
      api_hash=API_HASH,
)


pytgcalls = PyTgCalls(app)
wrapper = Wrapper(pytgcalls, "raw")

REPOLINK = """ Source code: [Github](https://github.com/Moezilla/vc-userbot)
License: [ GPL-3.0 License](https://github.com/moezilla/vc-userbot/blob/master/LICENSE.md)"""


@app.on_message(filters.me & filters.command("stream", PREFIX) & filters.chat(MOE_USER))
async def stream(_, m): 
    await wrapper.stream(m.chat.id, YT_URL)
    await m.reply_text("Playing song")


@app.on_message(filters.me & filters.command("pause", PREFIX) & filters.chat(MOE_USER))
async def pause(_, m):
    wrapper.pause(m.chat.id)
    await m.reply_text("Paused Song.")



@app.on_message(filters.me & filters.command("resume", PREFIX) & filters.chat(MOE_USER))
async def resume(_, m):
    wrapper.resume(m.chat.id)
    await m.reply_text("Resume Song.")


@app.on_message(filters.me & filters.command("song", PREFIX) & filters.chat(MOE_USER))
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

@app.on_message(filters.me & filters.command("repo", PREFIX) & filters.chat(MOE_USER))
async def repo(_, message):
    await message.reply_text(REPOLINK)

pytgcalls.run()
