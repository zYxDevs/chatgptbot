import openai
import os
import telethon
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
openai_api_key = os.environ.get("OPENAI_API_KEY")
GROUP_ID = os.environ.get("GROUP_ID")
OWNER_ID = os.environ.get("OWNER_ID")

client = TelegramClient(session='session_name', api_id=api_id, api_hash=api_hash)
client.start(bot_token=bot_token)

openai.api_key = openai_api_key

# /start command
@client.on(telethon.events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond("Hello! I am a Telegram bot powered by the OpenAI ChatGPT model.\nCreated by @HYBRID_Bots.\nTo use me Join @HYBRID_Chat and send your questions along with /ask command")

# Handle all other messages
@client.on(telethon.events.NewMessage)
async def message_handler(event):
    if event.message.to_id.channel_id == GROUP_ID and event.message.message.strip().startswith("/ask"):
        # Get the message text
        message_text = event.message.message.strip().replace("/ask","",1).strip()

        # Use the OpenAI API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{message_text}\n",
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5
        )

        # Send the response to the user
        await event.respond(response.choices[0].text)
    elif event.message.to_id.user_id != OWNER_ID and event.message.to_id.chat_id is None:
        await event.respond("I am a group only bot. Please join @HYBRID_Chat to use")

# Run the bot
client.run_until_disconnected()