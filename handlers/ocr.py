import asyncio
import os
import zipfile
import threading
import io
import httplib2
from pyrogram import Client, filters
from apiclient import discovery
from oauth2client import client
from oauth2client import clientsecrets
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from pathlib import Path
import shutil
from tqdm import tqdm
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize your Pyrogram bot (replace with your API ID, API HASH, and bot token)
api_id = "2069099"
api_hash = "c9083372a4110877c8a42a27c9ee1c9e"
bot_token = "6261764188:AAGyO88OpD38AjDpaZFO2OEOHaP_d4kSA-I"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define the directory paths
download_dir_name = "download"  # Use your 'download' folder's name
texts_path = "texts"
raw_texts_dir = "raw_texts"
texts_dir = "texts"
output_zip = "output.zip"

# Create the 'download' directory if it doesn't exist
if not os.path.exists(download_dir_name):
    os.makedirs(download_dir_name)

# Create the 'texts' directory if it doesn't exist
if not os.path.exists(texts_path):
    os.makedirs(texts_path)

# Create the 'raw_texts' directory if it doesn't exist
if not os.path.exists(raw_texts_dir):
    os.makedirs(raw_texts_dir)

# Google Drive API Constants
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
THREADS = 25

total_images = 0
completed_scans = 0
scan_lock = threading.Lock()
srt_file_list = {}


def get_credentials():
    try:
        credential_path = os.path.join("./", 'token.json')
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            try:
                flow = client.flow_from_clientsecrets(
                    CLIENT_SECRET_FILE, SCOPES)
                flow.user_agent = APPLICATION_NAME

                if flags:
                    credentials = tools.run_flow(flow, store, flags)
                else:
                    credentials = tools.run(flow, store)

                print('Storing credentials to ' + credential_path)
            except clientsecrets.InvalidClientSecretsError as e:
                print("Error opening client secrets file:", e)

        return credentials

    except FileNotFoundError as e:
        print("Token file not found:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def register(app):
    @app.on_message(filters.command("ocr"))
    async def ocr_command(client, message):
        if message.reply_to_message and message.reply_to_message.document:
            if message.reply_to_message.document.file_name.lower() == "images.zip":
                await message.reply_text("Processing images...")

                # Download the 'images.zip' file from Telegram to the 'download' directory
                download_dir = download_dir_name  # Update this to your download directory
                download_path = os.path.join(download_dir, "images.zip")
                await message.reply_to_message.download(download_path)

                # Specify the 'download' directory
                download_dir = Path(download_dir)

                # Extract the contents of 'images.zip'
                with zipfile.ZipFile(download_dir / "images.zip", 'r') as zip_ref:
                    zip_ref.extractall(download_dir)

                # Process extracted images and create text files (implement your processing logic here)
                images_dir = Path(download_dir)
                images = list(images_dir.glob("*.jpg")) + \
                    list(images_dir.glob("*.jpeg")) + \
                    list(images_dir.glob("*.png"))

                total_images = len(images)
                completed_scans = 0

                # Implement your OCR and text extraction logic here
                # You can use the existing logic you provided in your original script

                # Initialize the progress bar message
                progress_percentage = 0
                progress_text = f"Processing Images: {progress_percentage:.2f}% " \
                                f"({completed_scans}/{total_images}), Available={total_images - completed_scans}"

                # Create an inline keyboard with a progress bar button
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text='Progress', callback_data='progress')],
                ])

                # Send the initial progress message with the inline keyboard
                progress_message = await message.reply_text(progress_text, reply_markup=keyboard)

                # Use tqdm to create a progress bar
                with tqdm(total=total_images, desc="Processing Images") as pbar:
                    for image in images:
                        # Pass credentials and current_directory here
                        ocr_image(image, message.chat.id,
                                  get_credentials(), download_dir)

                        completed_scans += 1
                        available = total_images - completed_scans

                        # Calculate the progress percentage
                        progress_percentage = (
                            completed_scans / total_images) * 100

                        # Update the progress bar message
                        progress_text = f"Processing Images: {progress_percentage:.2f}% " \
                                        f"({completed_scans}/{total_images}), Available={available}"
                        await progress_message.edit_text(progress_text, reply_markup=keyboard)

                        pbar.update(1)  # Update the tqdm progress bar

                # Create a zip file with text files
                zip_output(output_zip, texts_path)

                # Upload the zip file to Telegram
                with open(output_zip, "rb") as zip_file:
                    await client.send_document(
                        chat_id=message.chat.id,
                        document=zip_file,
                        caption="Processed text files"
                    )

                # Clean up: Delete unnecessary files and directories
                # Delete extracted images and texts
                shutil.rmtree(download_dir)

                # Delete 'images.zip' if it exists
                images_zip_path = os.path.join(download_dir_name, "images.zip")
                try:
                    os.remove(images_zip_path)
                except FileNotFoundError:
                    pass  # File doesn't exist, no need to delete

                # Delete the raw text files
                for text_file in os.listdir(raw_texts_dir):
                    text_file_path = os.path.join(raw_texts_dir, text_file)
                    try:
                        os.remove(text_file_path)
                    except FileNotFoundError:
                        pass  # File doesn't exist, no need to delete

                # Delete the processed text files
                for text_file in os.listdir(texts_dir):
                    text_file_path = os.path.join(texts_dir, text_file)
                    try:
                        os.remove(text_file_path)
                    except FileNotFoundError:
                        pass  # File doesn't exist, no need to delete

                # Delete the output.zip file
                try:
                    os.remove(output_zip)
                except FileNotFoundError:
                    pass  # File doesn't exist, no need to delete

                # Send a completion message
                completion_message = "Image processing complete!"
                await progress_message.edit_text(completion_message)

                # Remove the "Processing images..." message after a brief delay
                await asyncio.sleep(3)  # Wait for 3 seconds (you can adjust the delay as needed)
                await progress_message.delete()

        else:
            await message.reply_text("Please reply to a message containing an 'images.zip' document to perform OCR.")


def zip_output(zip_file_name, source_dir):
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(
                    os.path.join(root, file), source_dir))


def main():
    global completed_scans, total_images
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    current_directory = Path(Path.cwd())
    images_dir = Path(f'{current_directory}/images')

    # Define the srt_file variable here
    srt_file = open(
        Path(f'{current_directory}/subtitle_output.txt'), 'a', encoding='utf-8')
    line = 1

    total_images = len(os.listdir(download_dir_name))

    for image_name in os.listdir(download_dir_name):
        image_path = os.path.join(download_dir_name, image_name)
        ocr_image(image_path, line, credentials, current_directory)
        with scan_lock:
            completed_scans += 1
            available = total_images - completed_scans
            print(
                f"Available = {available} Scan = {completed_scans} Total = {total_images}", end="\r")

    print()  # To move to the next line after the final update
    for i in sorted(srt_file_list):
        srt_file.writelines(srt_file_list[i])
    srt_file.close()


# This function processes individual images
def ocr_image(image_path, line, credentials, current_directory):
    tries = 0
    while True:
        try:
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('drive', 'v3', http=http)
            imgfile = image_path
            imgname = os.path.basename(imgfile)
            raw_txtfile = f'{raw_texts_dir}/{imgname[:-5]}.txt'
            txtfile = f'{texts_dir}/{imgname[:-5]}.txt'

            mime = 'application/vnd.google-apps.document'
            res = service.files().create(
                body={
                    'name': imgname,
                    'mimeType': mime
                },
                media_body=MediaFileUpload(
                    imgfile, mimetype=mime, resumable=True)
            ).execute()
            downloader = MediaIoBaseDownload(
                io.FileIO(raw_txtfile, 'wb'),
                service.files().export_media(
                    fileId=res['id'], mimeType="text/plain")
            )
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            service.files().delete(fileId=res['id']).execute()

            with open(raw_txtfile, 'r', encoding='utf-8') as raw_text_file:
                text_content = raw_text_file.read()

            text_content = text_content.split('\n')
            text_content = ''.join(text_content[2:])

            with open(txtfile, 'w', encoding='utf-8') as text_file:
                text_file.write(text_content)

            try:
                start_hour = imgname.split('_')[0][:2]
                start_min = imgname.split('_')[1][:2]
                start_sec = imgname.split('_')[2][:2]
                start_micro = imgname.split('_')[3][:3]

                end_hour = imgname.split('__')[1].split('_')[0][:2]
                end_min = imgname.split('__')[1].split('_')[1][:2]
                end_sec = imgname.split('__')[1].split('_')[2][:2]
                end_micro = imgname.split('__')[1].split('_')[3][:3]

            except IndexError:
                print(
                    f"Error processing {imgname}: Filename format is incorrect. Please ensure the correct format is used.")
                return

            start_time = f'{start_hour}:{start_min}:{start_sec},{start_micro}'
            end_time = f'{end_hour}:{end_min}:{end_sec},{end_micro}'
            srt_file_list[line] = [
                f'{line}\n',
                f'{start_time} --> {end_time}\n',
                f'{text_content}\n\n',
                ''
            ]
            break
        except:
            tries += 1
            if tries > 5:
                raise
            continue
