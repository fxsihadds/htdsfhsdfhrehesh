from pyrogram import filters


def register(app):
    @app.on_message(filters.command('help'))
    def help_command(client, message):
        client.send_message(
            chat_id=message.chat.id,
            text='Available commands:\n'
                 '/start - Start the bot\n'
                 '/help - Get help and command list\n'
                 '/userinfo - UserInfo\n'
                 '/Gscraper - Combo Scrape\n'
                 '/paste - Paste Any text\n'
                 '/unzip - Unzip Your File\n'
                 '/hoichoi - Check Your Valid Hoichoi Combo\n'
                 '/crunchyroll - Check Your Valid Crunchyroll Combo\n'
                 '/chaupal - Check Your Valid chaupal Combo\n'
                 '/ip - Check Your IP address\n'
                 '/rand - Fake Random Details\n'
                 '/ocr - Images OCR\n'
                 
        )
