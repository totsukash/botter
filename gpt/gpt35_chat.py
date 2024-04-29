import discord
import os
from openai import OpenAI

prefix = "!gpt"
conversation_history = {}  # user_id: [{role: "user", content: "hello"}]


def add_conversation_history(user_id: str, role: str, content: str):
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": role, "content": content})


def get_conversation_history(user_id: str) -> []:
    return conversation_history.get(user_id, [])


def remove_conversation_history(user_id: str, length: int):
    if user_id in conversation_history:
        del conversation_history[user_id][0:length]


async def reply_chat(message: discord.Message):
    content = message.content.removeprefix(prefix + " ")
    user_id = str(message.author.id)

    # 会話履歴を追加(ユーザー)
    add_conversation_history(user_id, "user", content)
    history = get_conversation_history(user_id)

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "あなたは親切なAIアシスタントです。userの入力に対して自然な日本語で回答して下さい",
            },
            *history,
        ],
        model="gpt-3.5-turbo",
    )
    ai_message = chat_completion.choices[0].message.content

    # 会話履歴を追加(AI)
    add_conversation_history(user_id, "assistant", ai_message)

    # 会話履歴が10より多い場合、古い履歴を削除
    if len(history) > 10:
        remove_conversation_history(user_id, 2)

    await message.channel.send(ai_message)
