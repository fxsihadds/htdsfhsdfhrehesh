from pyrogram import Client, filters


def register(app):
    @app.on_message(filters.command("userinfo"))
    async def userinfo_command(client: Client, message):
        if len(message.command) > 1:
            username = message.command[1]
            try:
                user = await app.get_users(username)
                await message.reply_text(
                    f"User ID: {user.id}\nUsername: {user.username}\nFirst Name: {user.first_name}")
            except Exception as e:
                await message.reply_text(f"An error occurred while fetching user info: {e}")
        elif message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            first_name = message.reply_to_message.from_user.first_name

            await message.reply_text(f"User ID: {user_id}\nUsername: {username}\nFirst Name: {first_name}")
        else:
            await message.reply_text("Please reply to a user's message or provide a username to get user information.")
