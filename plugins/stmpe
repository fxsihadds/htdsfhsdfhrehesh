_A='result'
from pyrogram import Client,filters
from pyrogram.types import Message
import os,requests
@Client.on_message(filters.command(['streampate','smp'])&filters.private)
async def streampate(bot,cmd):
	A=cmd;global status;status=await A.reply_text('<b>⎚ `Downloading...`</b>')
	if A.reply_to_message:
		if A.reply_to_message.document or A.reply_to_message.video or A.reply_to_message.audio:
			C=A.reply_to_message.document or A.reply_to_message.video or A.reply_to_message.audio;B=await bot.download_media(C)
			if C:
				if B:await uploadfunc(bot,A,files=B);os.remove(B)
				else:await status.edit_text('File Not Found!')
			else:await status.edit_text('Unsupported file format. Please provide a valid file.')
		else:await status.edit_text('Please Provide Valid Document, Video, or Audio File')
	else:await status.edit_text('Please reply with a Message, Document, Video, or Audio File!')
def get_upload_url(api_login,api_key,sha256,httponly=False):
	B='https://api.streamtape.com/file/ul';C={'login':api_login,'key':api_key,'sha256':sha256,'httponly':httponly};A=requests.get(B,params=C)
	if A.status_code==200:return A.json().get(_A,{}).get('url')
	else:print(f"Error getting upload URL. Status code: {A.status_code}");return
async def uploadfunc(bot,cmd,files):
	B=files;A=cmd;G='894087923f51d8018514';H='wdeq0wlyyaHJqeZ';I='ca247fe30e68d516a54e7a57247724617c345daa88168f6264f756d7125ee9eb';J=False;E=get_upload_url(G,H,I,J)
	if E:
		await status.edit_text('<b>⎚ `Uploading...`</b>');F=E
		if F:
			try:
				B={'file':open(B,'rb')};C=requests.post(F,files=B)
				if C.status_code==200:D=C.json();K=D.get('msg',{});L=D.get(_A,{}).get('url');M=D.get(_A,{}).get('name');N=f"""
▓▆▅▃▂▁𝐔𝐩𝐥𝐨𝐚𝐝 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧▁▂▃▅▆▓
<b>𝐅𝐢𝐥𝐞 𝐒𝐭𝐚𝐭𝐮𝐬</b>: {K}
<b>𝐅𝐢𝐥𝐞 𝐍𝐚𝐦𝐞</b>: {M}
<b>𝐔𝐫𝐥</b>: <code>{L}<code>
<b>⎚ 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐁𝐲</b>: @{A.from_user.username}
                    """;await status.edit_text(N)
				else:await A.reply_text(f"Failed to upload file. Status code: {C.status_code}")
			except Exception as O:await A.reply_text(f"Error during file upload: {O}")
		else:await A.reply_text('Upload URL not found in the response.')
	else:await A.reply_text('Failed to get upload URL.')
