import boto3
import discord
import os

prefix = "!claude-kb"

region = "us-east-1"
modelId = "anthropic.claude-3-haiku-20240307-v1:0"
knowledgebaseId = "D3WROLAHX0"
modelArn = f'arn:aws:bedrock:{region}::foundation-model/{modelId}'


async def reply_chat(message: discord.Message):
    content = message.content.removeprefix(prefix + " ")

    # AWS アクセスキー ID とシークレットアクセスキーを環境変数から取得
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    client = session.client(service_name='bedrock-agent-runtime')

    response = client.retrieve_and_generate(
        input={
            'text': content
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': knowledgebaseId,
                'modelArn': modelArn,
            },
        },
    )
    await message.channel.send(response['output']['text'])
