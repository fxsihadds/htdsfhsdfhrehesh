import asyncio,os,zipfile,threading,io,httplib2
from pyrogram import Client,filters
from apiclient import discovery
from oauth2client import client
from oauth2client import clientsecrets
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
from pathlib import Path
import shutil
from tqdm import tqdm
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
download_dir_name='download'
texts_path='texts'
raw_texts_dir='raw_texts'
texts_dir='texts'
output_zip='output.zip'
if not os.path.exists(download_dir_name):os.makedirs(download_dir_name)
if not os.path.exists(texts_path):os.makedirs(texts_path)
if not os.path.exists(raw_texts_dir):os.makedirs(raw_texts_dir)
SCOPES='https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE='credentials.json'
APPLICATION_NAME='Drive API Python Quickstart'
THREADS=500
total_images=0
completed_scans=0
scan_lock=threading.Lock()
srt_file_list={}
flags=True
def get_credentials():
	try:
		E=os.path.join('./','token.json');C=Storage(E);A=C.get()
		if not A or A.invalid:
			try:
				D=client.flow_from_clientsecrets(CLIENT_SECRET_FILE,SCOPES);D.user_agent=APPLICATION_NAME
				if flags:A=tools.run_flow(D,C,flags)
				else:A=tools.run(D,C)
				print('Storing credentials to '+E)
			except clientsecrets.InvalidClientSecretsError as B:print('Error opening client secrets file:',B)
		return A
	except FileNotFoundError as B:print('Token file not found:',B);return
	except Exception as B:print('An error occurred:',B);return
def register(app):
	G='drive';E='utf-8'
	@app.on_message(filters.command('ocr',['/','.']))
	async def A(client,message):
		F='images.zip';A=message
		with open(file='users/premium.txt',mode='r+',encoding=E)as Q:R=Q.readlines()
		if str(A.from_user.id)+'\n'in R:
			if A.reply_to_message and A.reply_to_message.document:
				if A.reply_to_message.document.file_name.lower()==F:
					G=await A.reply_text('Processing images...');B=download_dir_name;S=os.path.join(B,F);await A.reply_to_message.download(S);B=Path(B)
					with zipfile.ZipFile(B/F,'r')as T:T.extractall(B)
					H=Path(B);N=list(H.glob('*.jpg'))+list(H.glob('*.jpeg'))+list(H.glob('*.png'));C=len(N);D=0;I=0;J=f"Processing Images: {I:.2f}% ({D}/{C}), Available={C-D}";O=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Progress',callback_data='progress')]]);await G.edit(J,reply_markup=O)
					with tqdm(total=C,desc='Processing Images')as U:
						for V in N:M(V,A.chat.id,get_credentials(),B);D+=1;W=C-D;I=D/C*100;J=f"Processing Images: {I:.2f}% ({D}/{C}), Available={W}";await G.edit_text(J,reply_markup=O);U.update(1)
					P(output_zip,texts_path)
					with open(output_zip,'rb')as X:await client.send_document(chat_id=A.chat.id,document=X,caption='Processed text')
					shutil.rmtree(B);Y=os.path.join(download_dir_name,F)
					try:os.remove(Y)
					except FileNotFoundError:pass
					for K in os.listdir(raw_texts_dir):
						L=os.path.join(raw_texts_dir,K)
						try:os.remove(L)
						except FileNotFoundError:pass
					for K in os.listdir(texts_dir):
						L=os.path.join(texts_dir,K)
						try:os.remove(L)
						except FileNotFoundError:pass
					try:os.remove(output_zip)
					except FileNotFoundError:pass
					await G.delete()
			else:await A.reply_text('<b><i>Please reply to a message containing an <i><code>/ocr images.zip</code></b>')
		else:await A.reply_text("<b>Only For Premium Members</b>")
	def P(zip_file_name,source_dir):
		A=source_dir
		with zipfile.ZipFile(zip_file_name,'w')as D:
			for(B,F,E)in os.walk(A):
				for C in E:D.write(os.path.join(B,C),os.path.relpath(os.path.join(B,C),A))
	def B():
		global completed_scans,total_images;B=get_credentials();D=B.authorize(httplib2.Http());L=discovery.build(G,'v3',http=D);A=Path(Path.cwd());N=Path(f"{A}/images");C=open(Path(f"{A}/subtitle_output.txt"),'a',encoding=E);F=1;total_images=len(os.listdir(download_dir_name))
		for H in os.listdir(download_dir_name):
			I=os.path.join(download_dir_name,H);M(I,F,B,A)
			with scan_lock:completed_scans+=1;J=total_images-completed_scans;print(f"Available = {J} Scan = {completed_scans} Total = {total_images}",end='\r')
		print()
		for K in sorted(srt_file_list):C.writelines(srt_file_list[K])
		C.close()
	def M(image_path,line,credentials,current_directory):
		N=False;D='__';B='_';H=0
		while True:
			try:
				O=credentials.authorize(httplib2.Http());F=discovery.build(G,'v3',http=O);I=image_path;A=os.path.basename(I);J=f"{raw_texts_dir}/{A[:-5]}.txt";P=f"{texts_dir}/{A[:-5]}.txt";K='application/vnd.google-apps.document';L=F.files().create(body={'name':A,'mimeType':K},media_body=MediaFileUpload(I,mimetype=K,resumable=True)).execute();Q=MediaIoBaseDownload(io.FileIO(J,'wb'),F.files().export_media(fileId=L['id'],mimeType='text/plain'));M=N
				while M is N:d,M=Q.next_chunk()
				F.files().delete(fileId=L['id']).execute()
				with open(J,'r',encoding=E)as R:C=R.read()
				C=C.split('\n');C=''.join(C[2:])
				with open(P,'w',encoding=E)as S:S.write(C)
				try:T=A.split(B)[0][:2];U=A.split(B)[1][:2];V=A.split(B)[2][:2];W=A.split(B)[3][:3];X=A.split(D)[1].split(B)[0][:2];Y=A.split(D)[1].split(B)[1][:2];Z=A.split(D)[1].split(B)[2][:2];a=A.split(D)[1].split(B)[3][:3]
				except IndexError:print(f"<b>Error processing {A}: Filename format is incorrect. Please ensure the correct format is used.</b>");return
				b=f"{T}:{U}:{V},{W}";c=f"{X}:{Y}:{Z},{a}";srt_file_list[line]=[f"{line}\n",f"{b} --> {c}\n",f"{C}\n\n",''];break
			except:
				H+=1
				if H>5:raise
				continue
