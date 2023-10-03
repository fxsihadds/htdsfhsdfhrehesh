from pyrogram import Client, filters
import requests as re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import wget
import os

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('Generate', callback_data='generate'),
        InlineKeyboardButton('Refresh', callback_data='refresh'),
        InlineKeyboardButton('Close', callback_data='close')
    ]
])

msg_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('View message', callback_data='view_msg'),
        InlineKeyboardButton('Close', callback_data='close')
    ]
])

email = ''


def register(app):
    @app.on_message(filters.command('temp'))
    async def start_msg(client, message):
        with open(file="users/premium.txt", mode="r+", encoding="utf-8") as premium:
            premium_users = premium.readlines()
        if str(message.from_user.id)+'\n' in premium_users:
            global email
            email = ''
            await message.reply(f"**Hey {message.from_user.first_name}!!**\n <b>@checktbgbot is a free service that allows you to generate and receive emails at a temporary address that self-destructs after a certain time elapses.\n\n**__ How It Safeguards You??__**\n- Using temporary mail allows you to completely protect your real mailbox against the loss of personal information. Your temporary e-mail address is completely anonymous. Your details: information about your person and users with whom you communicate, IP-address, e-mail address are protected and completely confidential.\n\nFurther Queries @FxSihad🌚</b>")
            await message.reply("<b>⎚ `**Generate an Email Now**`</b>", reply_markup=buttons)

        else:
            await message.reply("<b>Only For Premium Members</b>")

        @app.on_callback_query()
        async def mailbox(client, message):
            global email
            response = message.data
            if response == 'generate':
                email = re.get(
                    "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
                await message.edit_message_text(f'<b>**Your Temporary E-mail:** <b>`{email}`', reply_markup=buttons)
            elif response == 'refresh':
                try:
                    if email == '':
                        await message.edit_message_text('<b>Generate an email</b>', reply_markup=buttons)
                    else:
                        get_msg_endpoint = "https://www.1secmail.com/api/v1/?action=getMessages&login=" + \
                            email[:email.find("@")] + "&domain=" + \
                            email[email.find("@") + 1:]
                        ref_response = re.get(get_msg_endpoint).json()
                        if ref_response:
                            global idnum
                            idnum = str(ref_response[0]['id'])
                            from_msg = ref_response[0]['from']
                            subject = ref_response[0]['subject']
                            refresh_reply = f'You have a message from {from_msg}\n\nSubject: {subject}'
                            await message.edit_message_text(refresh_reply, reply_markup=msg_buttons)
                        else:
                            await message.answer(f'<b>No messages were received in your Mailbox {email}</b>')
                except Exception as e:
                    print(e)
                    await message.answer('<b>An error occurred while fetching messages.</b>')
            elif response == 'view_msg':
                try:
                    msg = re.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" +
                                 email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum).json()
                    from_mail = msg['from']
                    date = msg['date']
                    subjectt = msg['subject']
                    attachments = msg.get('attachments', [])
                    body = msg['body']
                    mailbox_view = f'ID No: {idnum}\nFrom: {from_mail}\nDate: {date}\nSubject: {subjectt}\nMessage:\n{body}'
                    if not attachments:
                        await message.edit_message_text(mailbox_view, reply_markup=buttons)
                        await message.answer("<b>No Messages Were Received.</b>", show_alert=True)
                    else:
                        dl_attach = attachments[0]['filename']
                        attc = f"https://www.1secmail.com/api/v1/?action=download&login={email[:email.find('@')]}&domain={email[email.find('@') + 1:]}&id={idnum}&file={dl_attach}"
                        mailbox_vieww = f'{mailbox_view}\n\n[Download]({attc}) Attachments'
                        file_dl = wget.download(attc)
                        await message.edit_message_text(mailbox_vieww, reply_markup=buttons)
                        os.remove(dl_attach)
                except Exception as e:
                    print(e)
                    await message.answer('<b>An error occurred while viewing the message.</b>')
            elif response == 'close':
                await message.edit_message_text('<b>Session Closed✅</b>')
