from pyrogram import filters


def register(app):
    @app.on_message(filters.command('help'))
    def help_command(client, message):
        client.send_message(
            chat_id=message.chat.id,
            text = '<b>Available commands:</b>\n'
                   '<code>/start</code> - <b>Start the bot</b>\n'
                   '<code>/bin</code> - <b>Check Your Bin</b>\n'
                   '<code>/Gscraper</code> - <b>Combo Scrape</b>\n'
                   '<code>/paste</code> - <b>Paste Any text</b>\n'
                   '<code>/unzip</code> - <b>Unzip Your File</b>\n'
                   '<code>/hoichoi</code> - <b>Check Your Valid Hoichoi Combo</b>\n'
                   '<code>/crunchyroll</code> - <b>Check Your Valid Crunchyroll Combo</b>\n'
                   '<code>/chaupal</code> - <b>Check Your Valid chaupal Combo</b>\n'
                   '<code>/ip</code> - <b>Check Your IP address</b>\n'
                   '<code>/rand</code> - <b>Fake Random Details</b>\n'
                   '<code>/ocr</code> - <b>Images OCR</b>\n'
        )
