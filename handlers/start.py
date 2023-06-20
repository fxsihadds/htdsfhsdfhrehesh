from pyrogram import filters


def register(app):
    @app.on_message(filters.command('start'))
    def start_command(client, message):
        client.send_message(
            chat_id=message.chat.id,
            text='Hello! - Iam a Powerfull Checker'
        )
