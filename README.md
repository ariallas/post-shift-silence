To run:
1. Install Python
1. Run `pip install telethon`
1. Make an app at https://my.telegram.org/apps and put your *api_id* and *api_hash* in the config file
1. Run the bat files
	- `mute_for_3_days.bat` to mute listed chats for 3 days
	- `unmute_now.bat` to imidiately unmute listed chats
	
CMD Arguments:
- `-d`, `-hr`, `-m`  - how many days/hour/minutes to mute for
- `-u` - unmute chats instead of muting

Initial launch will require a login (it creates my.session file), subsequent launches will not.