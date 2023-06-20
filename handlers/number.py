from twilio.rest import Client as TwilioClient
from pyrogram import filters


def register(app):
    @app.on_message(filters.command('sms'))
    def number_command(client, message):
        command_text = message.text.split(' ', 2)
        if len(command_text) > 2:
            phone_number = command_text[1]
            text_to_send = command_text[2]

            # Send custom message using Twilio API
            response = send_custom_message(phone_number, text_to_send, client, message)
            if response:
                client.send_message(
                    chat_id=message.chat.id,
                    text=f"Message sent to {phone_number} successfully."
                )
            else:
                client.send_message(
                    chat_id=message.chat.id,
                    text=f"Failed to send message to {phone_number}."
                )
        else:
            client.send_message(
                chat_id=message.chat.id,
                text="Please provide a phone number and message."
            )

    def send_custom_message(phone_number, text, client, message):
        account_sid = 'ACe8585c651ee047c2f22b045055390819'
        auth_token = 'aa70de1755daf48cf19a8cbb2fdf811d'
        twilio_phone_number = '+13613924650'

        try:
            from twilio.rest import Client as TwilioClient

            client = TwilioClient(account_sid, auth_token)

            message = client.messages.create(
                body=text,
                from_=twilio_phone_number,
                to=phone_number
            )

            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
