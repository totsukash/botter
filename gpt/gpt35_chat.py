import discord
import os
from openai import OpenAI

prefix = "!chat"


async def reply_chat(message: discord.Message):
    content = message.content.removeprefix(prefix + " ")

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
    )

    await message.channel.send(chat_completion.choices[0].message.content)
