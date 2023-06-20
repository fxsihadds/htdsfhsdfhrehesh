import re
import os
from pyrogram import filters


def extract_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}:[^\s]+\b'
    emails = re.findall(pattern, text)
    return emails


def register(app):
    @app.on_message(filters.command('gscraper'))
    async def scraper_command(client, message):
        if message.reply_to_message is not None and message.reply_to_message.document:
            # Scraping from a replied document
            document = message.reply_to_message.document

            if document.file_name.endswith('.txt'):
                # Check if the file is a text file
                file_path = await client.download_media(document)

                with open(file_path, 'r', encoding='utf-8') as file:
                    text_to_scrape = file.read()

                # Remove the temporary file
                os.remove(file_path)
            else:
                await client.send_message(
                    chat_id=message.chat.id,
                    text='Please provide a text file (.txt) to scrape Gmail.'
                )
                return
        else:
            # Scraping from the command message
            command_text = message.text.split(' ', 1)
            if len(command_text) > 1:
                text_to_scrape = command_text[1]
            else:
                await client.send_message(
                    chat_id=message.chat.id,
                    text='Please provide a text file (.txt) or text to scrape Gmail.'
                )
                return

        emails = extract_emails(text_to_scrape)

        if len(emails) > 0:
            # Create a file with the extracted emails
            filename = 'extracted_emails.txt'
            with open(filename, 'w') as file:
                for email in emails:
                    file.write(email + '\n')

            # Reply with the file
            await client.send_document(
                chat_id=message.chat.id,
                document=filename,
                caption=f'Extracted {len(emails)} email(s).'
            )

            # Remove the file after sending
            os.remove(filename)

        else:
            await client.send_message(
                chat_id=message.chat.id,
                text='No email addresses found in the provided text.'
            )