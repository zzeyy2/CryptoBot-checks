from telethon import TelegramClient, types, functions, events
import asyncio
from telethon.tl.functions.messages import AddChatUserRequest, GetBotCallbackAnswerRequest
import configparser
config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')
chats = config['SYS']['chats'].split(',')


async def func():
    session = config['SYS']['session']
    client = TelegramClient(fr'{session}', api_hash=config['SYS']['API_HASH'], api_id=int(config['SYS']['API_ID']))
    await client.connect()
    if await client.is_user_authorized():
        print("client connected")
    chats_ent =[]
    for chat in chats:
        ent = await client.get_entity(int(chat))
        

        @client.on(events.NewMessage(chats=int(ent.id)))
        async def check(event):
            #print(event)
            if not event.entities == None:
                for entity in event.entities:
                    if isinstance(entity, types.MessageEntityUrl):
                        message = event.message.text
                        url = message[entity.offset:][:entity.length]
                        print(f'Новая ссылка: {url}')
                        code = url.split('start=')[-1]
                        await client.send_message('https://t.me/CryptoBot', message=f'/start {code}')





    await client.run_until_disconnected()
async def main():
    task = asyncio.create_task(func())
    await task



if __name__=='__main__':
    asyncio.run(main())