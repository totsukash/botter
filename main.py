import os

import discord
from dotenv import load_dotenv

from hello import hello
from gpt import gpt35_chat

load_dotenv('.env')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(hello.prefix):
        await hello.reply_hello(message)
    elif message.content.startswith(gpt35_chat.prefix):
        await gpt35_chat.reply_chat(message)


client.run(os.getenv('DISCORD_BOT_TOKEN'))
