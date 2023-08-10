# discbot
python based discord bot

## SETUP
To run this bot locally, you need to create a file "config.json" within the base directory.
Within this config file you need the following field:
`"Token": "<your discord token>"`
This will allow the bot to run within your discord server.
To then run the bot you need to enter the command:
`./bot.py`
This will run everything and load the cogs.

## Features
The bot runs off of cogs. Think of them as a micro-service that the bot loads when ran from the command line.
On boot, the bot will load the cogs recursivly within the `/cogs` directory. If you want to add new cogs then you add them there.
As of now the bot has the following operational cogs:
- base_commands (check ping of bot)
- wikipedia (view summaries from wikipedia)
- economy (commands to add users to DB and view wallet balance)


