import requests
from pyrogram import Client, filters


def register(app):
    @app.on_message(filters.command("bin"))
    async def cmds(client, message):
        with open(file="handlers/users/premium.txt", mode="r+", encoding='utf-8') as premium:
            premium_users = premium.readlines()

        if str(message.from_user.id) + '\n' in premium_users:
            try:
                BIN = message.text.split("/bin", 1)[1].strip()
            except IndexError:
                return await message.reply("<b>⎚ Use <code>/bin 456789</code></b>")

            if not BIN:
                return await message.reply("<b>⎚ Use <code>/bin 456789</code></b>")

            bincode = 6
            BIN = BIN[:bincode]
            req = requests.get(f"https://bins.antipublic.cc/bins/{BIN}").json()

            if 'bin' not in req:
                await message.reply_text(f'<b>⎚ 𝗕𝗶𝗻 ⇾ not found <code>{BIN} ❌</code></b>')

            else:
                brand = req['brand']
                country = req['country']
                country_name = req['country_name']
                country_flag = req['country_flag']
                country_currencies = req['country_currencies']
                bank = req['bank']
                level = req['level']
                typea = req['type']

                message_text = f"""
<b>⎚ BIN Information</b>
<b>BIN</b>: <code>{BIN}</code>
<b>Country</b>: {country} | {country_flag} | {country_name}
<b>Status</b>: Approved ✅
<b>Data</b>: {brand} - {typea} - {level}
<b>Bank</b>: {bank}
<b>Response Time</b>: <code>1.6 seconds</code>
⎚ 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: <b>@{message.from_user.username}</b>
"""
                await message.reply_text(message_text)

        else:
            await message.reply(f'<b>⎚ Register with <code>/register</code></b>')
