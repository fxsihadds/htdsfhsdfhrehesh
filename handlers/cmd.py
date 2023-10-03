_B='others'
_A='checkers'
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
buttons=InlineKeyboardMarkup([[InlineKeyboardButton('Tool',callback_data='tool'),InlineKeyboardButton('Checkers',callback_data=_A),InlineKeyboardButton('Others',callback_data=_B)],[InlineKeyboardButton('Admin',callback_data='admin'),InlineKeyboardButton('Close',callback_data='close')]])
tools='<b>Available commands:</b>\n\n<code>/Gscraper</code> - <b>Combo Scrape</b>\n\n<code>/paste</code> - <b>Paste Any text</b>\n\n<code>/unzip</code> - <b>Unzip Your File</b>\n\n<code>/ip</code> - <b>Check Your IP address</b>\n\n<code>/rand</code> - <b>Fake Random Details</b>\n\n<code>/bomb</code> - <b>Disturb Your friend.</b>\n\n<code>/temp</code> - <b>Temp mail.</b>\n\n '
checkers='<b>Available commands:</b>\n\n<code>/hoichoi</code> - <b>Check Your Valid Hoichoi Combo</b>\n\n<code>/crunchyroll</code> - <b>Check Your Valid Crunchyroll Combo</b>\n\n<code>/chaupal</code> - <b>Check Your Valid chaupal Combo</b>\n\n'
others='<b>Available commands:</b>\n\n<code>/bin</code> - <b>Check Your Bin</b>\n\n<code>/ocr</code> - <b>Images OCR</b>\n\n<code>/redeem</code> - <b>Buy Premium</b>\n\n'
admin='\n<code>/register</code> - <b>Add users</b>\n\n<code>/unregister</code> - <b>Remove users</b>\n\n<code>/userlist</code> - <b>show users</b>\n\n<code>/redclr</code> - <b>clear Redeem code From database</b>\n\n'
def register(app):
	@app.on_message(filters.command(['help','start']))
	async def A(Client,message):
		global main_admin
		with open(file='users/admin.txt',mode='r+',encoding='utf-8')as A:main_admin=A.readlines()
		await message.reply_text('<code>Commands: </code>',reply_markup=buttons)
	@app.on_callback_query()
	async def B(Client,message):
		A=message;B=A.data
		if B=='tool':await A.edit_message_text(f"{tools}\n",reply_markup=buttons)
		elif B==_A:await A.edit_message_text(f"{checkers}\n",reply_markup=buttons)
		elif B==_B:await A.edit_message_text(f"{others}\n",reply_markup=buttons)
		elif B=='admin':
			if str(A.from_user.id)+'\n'in main_admin:await A.edit_message_text(f"{admin}\n",reply_markup=buttons)
			else:await A.answer('ou Are Not Fucking Admin🖕')
		elif B=='close':await A.edit_message_text('<code>Closed</code>')
