import time
from pyrogram import Client, filters
from pyrogram.types import Message


def register(app):
    @app.on_message(filters.command("stats"))
    async def stats_command(_, message):
        await stats_helper_command(app, message)

    async def stats_helper_command(app: Client, message: Message):
        start_time = time.time()

        uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))

        ping_start = time.time()
        response = await message.reply_text("Calculating ping...")
        ping_end = time.time()
        ping_duration = (ping_end - ping_start) * 1000

        speed_start = time.time()
        await response.edit_text("Calculating speed...")
        speed_end = time.time()
        speed_duration = (speed_end - speed_start) * 1000

        # Format the stats message
        stats_message = (
            f"<b>Bot Stats:</b>\n"
            f"Uptime: {uptime}\n"
            f"Ping: {ping_duration:.2f} ms\n"
            f"Speed: {speed_duration:.2f} ms"
        )

        await message.reply_text(stats_message)
        await response.delete()
