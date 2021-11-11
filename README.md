# Discord Massban Bot

This little bot can ban recently joined users to prevent/cleanup bot spam waves.

## Public Bot

I'm hosting a public instance of this bot. You can invite it using [this link](https://discord.com/oauth2/authorize?client_id=907638667600883795&scope=bot&permissions=4). If you have questions or want to report bugs, use the [issues](https://github.com/muckelba/ValoBattlepassCalcBot/issues) tab.

**Make sure to grant the bot ban rights!**

## Installation

Python 3.6+ required, only tested 3.8!

Install the requirements:
```bash
pip install -r requirements.txt
```

Copy and rename `config.ini.example` to `config.ini` and paste the discord bottoken and configure the list of roles that are allowed to use the bot. The `bantext` option can be used to send users a DM before banning them to give false positives a chance to contact you. Set it to `""` to disable this feature. 

Run the bot:
```bash
python bot.py
```

## Usage

`!botspam !botspam [number of minutes since joined (default is 60)] [number of days since account creation (optional)]`

So if you want to ban every user that joined 120 minutes ago and only accounts that were created 2 weeks ago, use `!botspam 120 14`. You'll get a list of users that got selected. If you want to finally ban that list, click on the reaction. It'll take some time, depending on the amount of users. You'll get a message when the bot is finished.