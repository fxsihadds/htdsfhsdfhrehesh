_D='view_msg'
_C='refresh'
_B='generate'
_A='close'
from pyrogram import Client,filters
import requests as re
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import wget,os
buttons=InlineKeyboardMarkup([[InlineKeyboardButton('Generate',callback_data=_B),InlineKeyboardButton('Refresh',callback_data=_C),InlineKeyboardButton('Close',callback_data=_A)]])
msg_buttons=InlineKeyboardMarkup([[InlineKeyboardButton('View message',callback_data=_D),InlineKeyboardButton('Close',callback_data=_A)]])
email=''
def register(app):
	@app.on_message(filters.command('temp'))
	async def A(client,message):
		A=message
		with open(file='users/premium.txt',mode='r+',encoding='utf-8')as B:C=B.readlines()
		if str(A.from_user.id)+'\n'in C:global email;email='';await A.reply(f"""**Hey {A.from_user.first_name}!!**
 <b>@checktbgbot is a free service that allows you to generate and receive emails at a temporary address that self-destructs after a certain time elapses.

**__ How It Safeguards You??__**
- Using temporary mail allows you to completely protect your real mailbox against the loss of personal information. Your temporary e-mail address is completely anonymous. Your details: information about your person and users with whom you communicate, IP-address, e-mail address are protected and completely confidential.

Further Queries @FxSihad🌚</b>""");await A.reply('<b>⎚ `**Generate an Email Now**`</b>',reply_markup=buttons)
		else:await A.reply('<b>Only For Premium Members</b>')
		@app.on_callback_query()
		async def D(client,message):
			M='subject';L='from';K='&domain=';B='@';A=message;global email;D=A.data
			if D==_B:email=re.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()[0];await A.edit_message_text(f"<b>**Your Temporary E-mail:** <b>`{email}`",reply_markup=buttons)
			elif D==_C:
				try:
					if email=='':await A.edit_message_text('<b>Generate an email</b>',reply_markup=buttons)
					else:
						N='https://www.1secmail.com/api/v1/?action=getMessages&login='+email[:email.find(B)]+K+email[email.find(B)+1:];E=re.get(N).json()
						if E:global idnum;idnum=str(E[0]['id']);O=E[0][L];P=E[0][M];Q=f"You have a message from {O}\n\nSubject: {P}";await A.edit_message_text(Q,reply_markup=msg_buttons)
						else:await A.answer(f"<b>No messages were received in your Mailbox {email}</b>")
				except Exception as F:print(F);await A.answer('<b>An error occurred while fetching messages.</b>')
			elif D==_D:
				try:
					C=re.get('https://www.1secmail.com/api/v1/?action=readMessage&login='+email[:email.find(B)]+K+email[email.find(B)+1:]+'&id='+idnum).json();R=C[L];S=C['date'];T=C[M];G=C.get('attachments',[]);U=C['body'];H=f"""ID No: {idnum}
From: {R}
Date: {S}
Subject: {T}
Message:
{U}"""
					if not G:await A.edit_message_text(H,reply_markup=buttons);await A.answer('<b>No Messages Were Received.</b>',show_alert=True)
					else:I=G[0]['filename'];J=f"https://www.1secmail.com/api/v1/?action=download&login={email[:email.find(B)]}&domain={email[email.find(B)+1:]}&id={idnum}&file={I}";V=f"{H}\n\n[Download]({J}) Attachments";W=wget.download(J);await A.edit_message_text(V,reply_markup=buttons);os.remove(I)
				except Exception as F:print(F);await A.answer('<b>An error occurred while viewing the message.</b>')
			elif D==_A:await A.edit_message_text('<b>Session Closed✅</b>')
