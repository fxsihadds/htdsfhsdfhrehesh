import os, time
import yt_dlp
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message


def register(app):
    @app.on_message(filters.command("dlink"))
    async def register_command(client:Client, message:Message):
        pass
