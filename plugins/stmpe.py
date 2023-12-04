from pyrogram import Client, filters
from pyrogram.types import Message
import os
import requests


@Client.on_message(filters.command(['streampate', 'smp']) & filters.private)
async def streampate(bot: Client, cmd: Message):
    global status
    status = await cmd.reply_text("<b>⎚ `Downloading...`</b>")
    if cmd.reply_to_message:
        if cmd.reply_to_message.document or cmd.reply_to_message.video or cmd.reply_to_message.audio:
            media = cmd.reply_to_message.document or cmd.reply_to_message.video or cmd.reply_to_message.audio
            file_path = await bot.download_media(media)
            if media:
                if file_path:
                    await uploadfunc(bot, cmd, files=file_path)
                    os.remove(file_path)
                else:
                    await status.edit_text('File Not Found!')
            else:
                await status.edit_text('Unsupported file format. Please provide a valid file.')
        else:
            await status.edit_text('Please Provide Valid Document, Video, or Audio File')
    else:
        await status.edit_text('Please reply with a Message, Document, Video, or Audio File!')


def get_upload_url(api_login, api_key, sha256, httponly=False):
    base_url = "https://api.streamtape.com/file/ul"

    params = {
        "login": api_login,
        "key": api_key,
        "sha256": sha256,
        "httponly": httponly,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json().get("result", {}).get("url")
    else:
        print(f"Error getting upload URL. Status code: {response.status_code}")
        return None


async def uploadfunc(bot, cmd, files):
    api_login = "894087923f51d8018514"
    api_key = "wdeq0wlyyaHJqeZ"
    sha256 = "ca247fe30e68d516a54e7a57247724617c345daa88168f6264f756d7125ee9eb"
    httponly = False

    upload_url_response = get_upload_url(api_login, api_key, sha256, httponly)

    if upload_url_response:
        await status.edit_text("<b>⎚ `Uploading...`</b>")
        upload_url = upload_url_response
        if upload_url:
            try:
                files = {'file': open(files, 'rb')}
                response = requests.post(upload_url, files=files)
                if response.status_code == 200:
                    response_dict = response.json()
                    msg = response_dict.get("msg", {})
                    url = response_dict.get("result", {}).get("url")
                    name = response_dict.get("result", {}).get("name")
                    message_text = f"""
▓▆▅▃▂▁𝐔𝐩𝐥𝐨𝐚𝐝 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧▁▂▃▅▆▓
<b>𝐅𝐢𝐥𝐞 𝐒𝐭𝐚𝐭𝐮𝐬</b>: {msg}
<b>𝐅𝐢𝐥𝐞 𝐍𝐚𝐦𝐞</b>: {name}
<b>𝐔𝐫𝐥</b>: <code>{url}<code>
<b>⎚ 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐁𝐲</b>: @{cmd.from_user.username}
                    """
                    await status.edit_text(message_text)
                else:
                    await cmd.reply_text(f"Failed to upload file. Status code: {response.status_code}")
            except Exception as e:
                os.remove(files)
                await cmd.reply_text(f"Error during file upload: {e}")
        else:
            await cmd.reply_text("Upload URL not found in the response.")
    else:
        await cmd.reply_text("Failed to get upload URL.")
