import requests
from pyrogram import Client, filters


def register(app):
    @app.on_message(filters.command("rand"))
    async def rand_helper_command(_, message):
        status = await message.reply_text("<b>⎚ `generating...`</b>")
        api = requests.get(
            "https://randomuser.me/api/?nat=us&inc=name,location").json()

        mr = api["results"][0]["name"]["title"]
        nombre = api["results"][0]["name"]["first"]
        last = api["results"][0]["name"]["last"]
        loca = api["results"][0]["location"]["street"]["name"]
        nm = api["results"][0]["location"]["street"]["number"]
        city = api["results"][0]["location"]["city"]
        state = api["results"][0]["location"]["state"]
        country = api["results"][0]["location"]["country"]
        postcode = api["results"][0]["location"]["postcode"]
        latitude = api["results"][0]["location"]["coordinates"]["latitude"]
        longitude = api["results"][0]["location"]["coordinates"]["longitude"]

        await message.reply(f"""
<b> 
⎚ 𝐅𝐚𝐤𝐞 𝐀𝐝𝐝𝐫𝐞𝐬𝐬
⎚ 𝐍𝐚𝐦𝐞: <code>{mr} {nombre} {last}</code>
⎚ 𝐒𝐭𝐫𝐞𝐞𝐭:  <code>{state}</code>
⎚ 𝐂𝐢𝐭𝐲: <code>{city}</code>
⎚ 𝐒𝐭𝐚𝐭𝐞:<code> {loca} {nm}</code>
⎚ 𝐏𝐨𝐬𝐭𝐜𝐨𝐝𝐞: <code> {postcode}</code>
⎚ 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country}</code>
⎚ 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲 <code> @{message.from_user.username}</code>
    ━━━━━━━━━━━━━━
⎚ Create <b>Unknown</b>""")
        await status.delete()
