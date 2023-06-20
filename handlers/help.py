from pyrogram import filters


def register(app):
    @app.on_message(filters.command('help'))
    def help_command(client, message):
        client.send_message(
            chat_id=message.chat.id,
            text='Available commands:\n'
                 '/start - Start the bot\n'
                 '/help - Get help and command list\n'
                 '/Gscraper - Perform scraping operation\n'
                 '/screenshot - To take Screenshot Using Url\n'
                 '/sms - Send Custom Sms Your Favorite One\n'
                 '/hoichoi - Send Custom Sms Your Favorite One\n'
        )
