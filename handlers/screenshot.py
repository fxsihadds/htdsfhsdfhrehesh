import os
from pyrogram import filters
from pyppeteer import launch


def register(app):
    @app.on_message(filters.command('screenshot'))
    async def screenshot_command(client, message):
        command_text = message.text.split(' ', 1)
        if len(command_text) > 1:
            url = command_text[1]

            # Declare the screenshot file variable
            screenshot_file = 'screenshot.jpg'

            # Launch a headless Chrome browser
            browser = await launch()
            page = await browser.newPage()

            try:
                # Set the viewport size to capture the full page
                await page.setViewport({'width': 1920, 'height': 1080})

                # Navigate to the specified URL with an increased timeout value
                await page.goto(url, {'timeout': 60000})  # Increased timeout to 60 seconds

                # Take a screenshot of the full page and compress it as a JPG file
                await page.screenshot({'path': screenshot_file, 'type': 'jpeg', 'quality': 50, 'fullPage': True})

                # Send the screenshot file as a document
                await client.send_document(
                    chat_id=message.chat.id,
                    document=screenshot_file,
                    caption='Screenshot of the webpage.'
                )

            finally:
                # Close the browser
                await browser.close()

                # Check if the file exists before removing it
                if os.path.exists(screenshot_file):
                    # Delete the screenshot file
                    os.remove(screenshot_file)

        else:
            await client.send_message(
                chat_id=message.chat.id,
                text='Please provide a URL to take a screenshot of.'
            )
