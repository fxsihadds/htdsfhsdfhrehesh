from pyrogram import Client, filters
from pyrogram.types import Message


def write_text(text):
    with open("temp.txt", "w+", encoding="utf-8") as temp_file:
        temp_file.write(text)
    return "temp.txt"


def register(app):
    @app.on_message(filters.command("txt"))
    async def text_cmd(client: Client, message: Message):
        text_to_write = message.text
        if not text_to_write:
            await message.reply("OPPS")
        elif message.reply_to_message:
            text_to_write = message.reply_to_message.text
        else:
            await message.reply("<b>⎚ Please use <code>/txt text to Create txt File</code></b>")
            return

        status = await message.reply_text("<b>⎚ `Creating TxT file...`</b>")

        file_name = write_text(text_to_write)
        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
        )
        await status.delete()
