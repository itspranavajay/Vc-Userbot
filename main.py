import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls_wrapper import Wrapper


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


@app.on_message(filters.me & filters.command("stream", PREFIX))
async def stream(_, m): 
    await wrapper.stream(m.chat.id, YT_URL)
    await m.reply_text("Downloading song")


@app.on_message(filters.me & filters.command("pause",PREFIX))
async def pause(_, m):
    wrapper.pause(m.chat.id)
    await m.reply_text("Paused Song.")



@app.on_message(filters.me & filters.command("resume", PREFIX))
async def resume(_, m):
    wrapper.resume(m.chat.id)
    await m.reply_text("Resume Song.")




pytgcalls.run()
