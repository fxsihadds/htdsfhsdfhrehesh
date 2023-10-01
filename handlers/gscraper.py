import re,os
from pyrogram import filters
EMAIL_PASSWORD_REGEX='\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}:[A-Za-z0-9]+\\b'
def extract_email_passwords(text):A=re.findall(EMAIL_PASSWORD_REGEX,text);return A
def register(app):
	@app.on_message(filters.command('gscraper'))
	async def A(client,message):
		H=client;G=None;A=message;C=await A.reply('<b>⎚ `Extracting...`</b>');B=G
		if A.reply_to_message:
			if A.reply_to_message.document:
				I=A.reply_to_message.document
				if I.file_name.endswith('.txt'):
					J=await H.download_media(I)
					with open(J,'r',encoding='utf-8')as D:B=D.read()
					os.remove(J)
				else:await C.edit_text(text='<b>Please provide a text file (.txt) to scrape email:password combinations😞.</b>');return
			elif A.reply_to_message.text:B=A.reply_to_message.text
		if B is G:
			K=A.text.split(' ',1)
			if len(K)>1:B=K[1]
		if B is G:await C.edit_text(text='<b>No text found to scrape email:password combinations😞.</b>');return
		E=extract_email_passwords(B)
		if len(E)>0:
			F='Email_Password.txt'
			with open(F,'w')as D:
				for L in E:D.write(L+'\n')
			await H.send_document(chat_id=A.chat.id,document=F,caption=f"<b>Extracted {len(E)} email:password</b>");os.remove(F);await C.delete()
		else:await C.edit_text(text='<b>No email:password combinations found in the provided text ❌.</b>')
