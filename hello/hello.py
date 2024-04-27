import discord

prefix = '!hello'


async def reply_hello(message: discord.Message):
    await message.channel.send('Hello!')
