import asyncio
import datetime
import configparser
from zoneinfo import ZoneInfo
from telethon import TelegramClient, functions, types

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    api_id = config['api']['api_id']
    api_hash = config['api']['api_hash']
    chats_to_mute = config['settings']['channels'].replace('\n', '').split(',')
    mute_for = { 'days': config.getint('mute_for', 'days'), 'hours': config.getint('mute_for', 'hours'), 'minutes': config.getint('mute_for', 'minutes') }
    return api_id, api_hash, chats_to_mute, mute_for

def get_mute_until(mute_for):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    delta = datetime.timedelta(days=mute_for['days'], hours=mute_for['hours'], minutes=mute_for['minutes'])
    return current_time + delta

async def main():
    api_id, api_hash, chats_to_mute, mute_for = read_config()
    mute_until = get_mute_until(mute_for)
    print('Muting until %s' % (mute_until + datetime.timedelta(hours=3)).strftime("%b %d %Y %H:%M"))

    async with TelegramClient('anon', api_id, api_hash) as client:
        await client.get_dialogs()

        for chat in chats_to_mute:
            result = await client(functions.account.UpdateNotifySettingsRequest(
                peer=chat,
                settings=types.InputPeerNotifySettings(
                    mute_until=mute_until,
            )))
            if result:
                print('Succesfully muted %s' % chat)

asyncio.run(main())