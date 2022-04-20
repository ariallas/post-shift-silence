import asyncio
import datetime
import configparser
from argparse import ArgumentParser
from zoneinfo import ZoneInfo
from telethon import TelegramClient, functions, types

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    api_id = config.getint('api', 'api_id')
    api_hash = config['api']['api_hash']
    chats_to_mute = config['settings']['channels'].replace('\n', '').split(',')

    return api_id, api_hash, chats_to_mute

def read_arguments():
    parser = ArgumentParser()
    parser.add_argument('-u', '--unmute', default=False, action='store_true', help='unmute all chats')
    parser.add_argument('-d', '--days', default=0, type=int, help='how many days to mute for')
    parser.add_argument('-hr', '--hours', default=0, type=int, help='how many hours to mute for')
    parser.add_argument('-m', '--minutes', default=1, type=int, help='how many minutes to mute for')
    args = parser.parse_args()
    return args.unmute, args.days, args.hours, args.minutes

def get_mute_until(mute_for):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    delta = datetime.timedelta(days=mute_for['days'], hours=mute_for['hours'], minutes=mute_for['minutes'])
    return current_time + delta

async def main():
    # If mute_until is not None, mute chats until that date. Else unmute the chats.
    async def process_chats(chats, mute_until):
        if mute_until:
            print('Muting until %s' % (mute_until + datetime.timedelta(hours=3)).strftime("%b %d %Y %H:%M"))
        else:
            print('Unmuting chats')

        for chat in chats:
            result = await client(functions.account.UpdateNotifySettingsRequest(
                peer=chat,
                settings=types.InputPeerNotifySettings(
                    mute_until=mute_until,
            )))
            print('Succesfully processed %s' % chat)

    api_id, api_hash, chats_to_mute = read_config()
    unmute, days, hours, minutes = read_arguments()
    mute_for = { 'days': days, 'hours': hours, 'minutes': minutes }
    mute_until = None
    if not unmute:
        mute_until = get_mute_until(mute_for)

    async with TelegramClient('my', api_id, api_hash) as client:
        await client.get_dialogs()
        await process_chats(chats_to_mute, mute_until)

asyncio.run(main())