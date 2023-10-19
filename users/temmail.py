import os, time
import yt_dlp
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message


def register(app):
    @app.on_message(filters.command("dlink"))
    async def register_command(client:Client, message:Message):
        dl_path = "your_download"
        with open(file="users/premium.txt", mode="r+", encoding="utf-8") as premium:
            premium_users = premium.readlines()
        if str(message.from_user.id) + '\n' in premium_users:
            urls = message.text.split("/dlink", 1)[1].strip()
            if not urls:
                await message.reply("<b>⎚ Use <code>/link</code> Url To Download Your File</b>")
            else:
                await download_file(urls, message, dl_path)
                await upload_files(dl_path, message)


async def download_file(url, message, output_dir="."):
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        status = await message.reply("<b>⎚ `Downloading...`</b>")
        try:
            ydl.extract_info(url)
            await status.delete()
        except yt_dlp.utils.DownloadError as e:
            await message.reply(e)


async def upload_files(dl_path, message):
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)
    dldirs = [i async for i in absolute_paths(dl_path)]

    for files in dldirs:
        success = await send_media(files, message)
        if success:
            await asyncio.sleep(1)
            os.remove(files)
        else:
            await message.reply("<b>Error uploading the file</b>")
            os.remove(files)


async def absolute_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


async def send_media(file_name, update):
    try:
        if os.path.isfile(file_name):
            caption = file_name if '/' not in file_name else file_name.split(
                '/')[-1]
            caption = os.path.basename(file_name)
            progress_args = await update.reply("<b>⎚ `Uploading...`</b>")

            if file_name.lower().endswith(('.mkv', '.mp4')):
                await update.reply_video(file_name, caption=caption)
            elif file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                await update.reply_photo(file_name, caption=caption)
            elif file_name.lower().endswith(('.mp3')):
                await update.reply_audio(file_name, caption=caption)
            else:
                await update.reply_document(file_name, caption=caption)

            await progress_args.delete()

            return True
        else:
            logging.error(f"File not found: {file_name}")
    except Exception as e:
        logging.error(f"Error sending media: {str(e)}")
        return False
