Touhou Project (東方Project) is a creation by ZUN of Team Shanghai Alice:
http://www16.big.or.jp/~zun/

Uses Touhou fan images created by Dairi:
https://www.pixiv.net/member.php?id=4920496

SEIGATRON created by Robbie Munro (LunaSeikaku):
https://github.com/LunaSeikaku
--------------------------------------------------------------------------------------------------------------------------------------------
SEIGATRON V.0.8
--------------------------------------------------------------------------------------------------------------------------------------------
SEIGATRON is a recreational Bot designed for use on the messaging service Discord. It features a minimal selection of 'standard' Discord bot commands and a selection of mathematical commands,
however the main attraction is the main Touhou Command Base which allows users to engage in a turn-based RPG combat system.

Originally just a Python Command Base added to an existing bot, SEIGATRON has since been reconstructed from scratch as a Bot with a C# front-end engine backed up with the Python back-end processor for Touhou-related commands.
This was done to reduce the memory size of the Bot below a 500Mb application limit on a cloud service, however it has since also provided a boost to overhead due to a complete eradication of 'bloat' from the original Bot.

Features:
- A fully-fleshed out turn-based RPG system inspired by the Touhou Project series of games
	- Currently 145 various Touhou characters each with various Spellcard attacks, inspired by the Touhou Project universe
		- Different 'difficulties' and 'distances' of play alter the loadout and effect of the Spellcards
	- Touhou characters have various rarities
		- If a duplicate Touhou is found by a Player, their original Touhou moves to the next higher rarity
	- Single and team battles, from 1v1, to 6v6, to theoretically XvX
		- Uses numpy and PIL for creation of team images (lineup of your characters) without compromising overhead
	- Status effects, critical hits, misses and more
	- Elemental system
- Battles play out in real time on Discord, as messages provide an ongoing battle feed
- Players can gather Touhou characters, have them go on adventures, and battle them against other Players
	- Players can have a Touhou Secretary that fights most 1 duels for them
	- Players can have a Team of 6 Touhous to fight team duels for them
	- Players have a Backpack that stores any Touhou characters they find for battle later
	- Players have Points they can use to perform cooler commands like PvP
- Customisable Character list, Spellcard list, Element list, etc for the owner of the Bot
	- Tip: use the '!!balance TouhouX TouhouY' command when editing data. It will simulate 10 battles for you on each difficulty, and graph them for your perusal.
--------------------------------------------------------------------------------------------------------------------------------------------
Install:
1: Open _path.txt, enter the path to your Python.exe, save and close.
2.1: Go to https://discordapp.com/developers/applications/ and sign into your Discord account.
2.2: Click 'New Application', enter the name of your Bot and click 'Create'.
2.3: Under 'Settings' on the left, click 'Bot', then 'Add Bot' on the right. 
2.4: Under 'Token', click Copy. Open _token.txt, paste your copy in there, save and close.
2.5: Click 'OAuth2' on the left, then click the 'bot' checkbox under 'Scopes'.
2.6: Copy the newly-generated URL at the bottom of the page, enter it into a browser and invite the Bot to your Discord server.
3: [OPTIONAL] Open _prefix.txt, change '!!' to whatever prefix you wish to use to initiate commands for your Bot to read, save and close.
4: Run Bot!
5: Enter commands for your Bot to run eg '!!help' for a list of commands
--------------------------------------------------------------------------------------------------------------------------------------------
Things still to add:
- Dairi is still working on Touhou 16 sprites! Thus; not all Touhou characters have sprites. Error handling is in place for this, but if you get a file not found error, it's probably from that.
- Spellcards still have to be mostly added and linked to respective Touhou characters. However engine is fully in place, and currently most Touhou characters use a default selection of Spellcard attacks.
- Commands still have to be finalized, run against test cases and made robust and consistent. Unexpected issues may occur.
- Further statistical information for more accurate graphs and after-battle reports.
- Full guide!
--------------------------------------------------------------------------------------------------------------------------------------------
IMAGES OF BOT IN ACTION:
Discord Log of a battle between 2 Touhou character: https://imgur.com/a/G8RjKUS
Graphing of 10 battles between 2 Touhou characters (used for balancing): https://imgur.com/a/af3tn2s
