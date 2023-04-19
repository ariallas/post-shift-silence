To run:
1. Install Python
1. Run `pip install telethon`
1. Make an app at https://my.telegram.org/apps and put your *api_id* and *api_hash* in the config file
1. Run the bat files
	- `mute_for_3_days.bat` to mute listed chats for 3 days
	- `unmute_now.bat` to imidiately unmute listed chats
	
CMD Arguments:
- `-d`, `-hr`, `-m`  - how many days/hour/minutes to mute for
- `-f` - mute until exact time of the day
- `-u` - unmute chats instead of muting

Examples:
- `python main.py -d 2 -hr 21` - mute for exactly 2 days and 21 hour
- `python main.py -d 3 -hr 9 -m 0 -f` - mute until 3 days from now, till 9:00

Initial launch will require a login (it creates my.session file), subsequent launches will not.