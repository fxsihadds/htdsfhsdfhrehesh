import os,yt_dlp,time,logging,asyncio
from pyrogram import Client,filters
async def download_file(url,message,output_dir='.'):
	A=message;B={'outtmpl':os.path.join(output_dir,'%(title)s.%(ext)s'),'format':'best'}
	with yt_dlp.YoutubeDL(B)as C:
		D=await A.reply('<b>⎚ `Downloading...`</b>')
		try:C.extract_info(url);await D.delete()
		except yt_dlp.utils.DownloadError as E:await A.reply(E)
async def upload_files(dl_path,message):
	C=message;A=dl_path
	if not os.path.exists(A):os.makedirs(A)
	D=[A async for A in absolute_paths(A)]
	for B in D:
		E=await send_media(B,C)
		if E:await asyncio.sleep(1);os.remove(B)
		else:await C.reply('<b>Error uploading the file</b>');os.remove(B)
async def absolute_paths(directory):
	for(A,D,B)in os.walk(directory):
		for C in B:yield os.path.abspath(os.path.join(A,C))
async def send_media(file_name,update):
	B=update;A=file_name
	try:
		if os.path.isfile(A):
			C=A if'/'not in A else A.split('/')[-1];C=os.path.basename(A);D=await B.reply('<b>⎚ `Uploading...`</b>')
			if A.lower().endswith(('.mkv','.mp4')):await B.reply_video(A,caption=C)
			elif A.lower().endswith(('.jpg','.jpeg','.png')):await B.reply_photo(A,caption=C)
			elif A.lower().endswith('.mp3'):await B.reply_audio(A,caption=C)
			else:await B.reply_document(A,caption=C)
			await D.delete();return True
		else:logging.error(f"File not found: {A}")
	except Exception as E:logging.error(f"Error sending media: {str(E)}");return False
def register(app):
	@app.on_message(filters.command('link'))
	async def A(client,message):
		A=message;B='your_download'
		with open(file='users/premium.txt',mode='r+',encoding='utf-8')as D:E=D.readlines()
		if str(A.from_user.id)+'\n'in E:
			C=A.text.split('/link',1)[1].strip()
			if not C:await A.reply('<b>⎚ Use <code>/link</code> Url To Download Your File</b>')
			else:await download_file(C,A,B);await upload_files(B,A)
