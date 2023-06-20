import openai
from pyrogram import filters

openai.api_key = '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'


def generate_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50  # Set the maximum number of tokens for the response
    )
    return response.choices[0].message.content


def register(app):
    @app.on_message(filters.command('gpt'))
    def gpt_command(client, message):
        if len(message.text.split(' ', 1)) > 1:
            prompt = message.text.split(' ', 1)[1]
            response = generate_gpt_response(prompt)

            # Reply with the initial response
            client.send_message(
                chat_id=message.chat.id,
                text=response
            )

            # Prepare a future reply
            future_reply = generate_gpt_response('Tell me more about it.')

            # Delayed reply using scheduled message
            client.send_message(
                chat_id=message.chat.id,
                text=future_reply,
                scheduled=True,
                delay=10  # Delay the reply by 10 seconds (adjust as needed)
            )
        else:
            client.send_message(
                chat_id=message.chat.id,
                text='Please provide a text for the GPT command.'
            )
