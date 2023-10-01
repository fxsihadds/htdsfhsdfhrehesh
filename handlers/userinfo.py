from pyrogram import Client,filters
def register(app):
	@app.on_message(filters.command('id',['/','.']))
	async def A(client,message):
		A=message
		if len(A.command)>1:
			C=A.command[1]
			try:B=await app.get_users(C);D=f"""<strong>User Information: </strong>
━━━━━━━━━━━
<b>User ID:</b> <code>{B.id}</code>
<b>Username:</b> <code>{B.username}</code>
<b>First Name:</b> <code>{B.first_name}</code>
<b>Last Name:</b> <code>{B.last_name}</code>
<b>DC ID:</b> <code>{B.dc_id}</code>
<b>Is Bot:</b> <code>{B.is_bot}</code>
<b>Language Code:</b> <code>{B.language_code}</code>
<b>Last Online Date:</b> <code>{B.last_online_date}</code>
""";await A.reply_text(D)
			except Exception as E:await A.reply_text(f"An error occurred while fetching user info: {E}")
		else:F=A.from_user.id;C=A.from_user.username;G=A.from_user.first_name;H=A.from_user.last_name;I=A.from_user.dc_id;J=A.from_user.is_bot;K=A.from_user.language_code;L=A.from_user.last_online_date;D=f"""<strong>User Information: </strong>
━━━━━━━━━━━
<b>User ID:</b> <code>{F}</code>
<b>Username:</b> <code>{C}</code>
<b>First Name:</b> <code>{G}</code>
<b>Last Name:</b> <code>{H}</code>
<b>DC ID:</b> <code>{I}</code>
<b>Is Bot:</b> <code>{J}</code>
<b>Language Code:</b> <code>{K}</code>
<b>Last Online Date:</b> <code>{L}</code>
""";await A.reply_text(D)
