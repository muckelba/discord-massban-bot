import discord
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import *
import logging
import asyncio
import json
import configparser
import random 
from string import ascii_uppercase
import os
from datetime import datetime, date

from dateutil.relativedelta import relativedelta, FR, TU
from dateutil.easter import easter
from dateutil.parser import parse
from dateutil import rrule

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents=intents)

config = configparser.ConfigParser()
config.read('config.ini')

token = config['main']['token']
admins = json.loads(config['main']['admins'])

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

@client.command()
@commands.has_any_role(*admins)
async def botspam(ctx, joined="60", created=None):
    usage = "Usage: `!botspam [number of minutes since joined (default is 60)] [number of days since account creation (optional)]`"
    try:
        joined = int(joined)
    except ValueError:
        await ctx.send(f":x: The first parameter is not a real number.\n{usage}")
        return
    if created:
        try:
            created = int(created)
        except ValueError:
            await ctx.send(f":x: The second parameter is not a real number.\n{usage}")
            return

    recentlyJoined = []

    for member in ctx.guild.members:
        if member.joined_at > datetime.now(timezone.utc) - timedelta(minutes=joined) and member != client.user:
            if (not created) or (created and member.created_at > datetime.now(timezone.utc) - timedelta(days=created)):
                recentlyJoined.append(member)

    if not recentlyJoined:
        await ctx.send("No users were selected with that filter.")
        return

    randomid = ''.join(random.choice(ascii_uppercase) for i in range(12))
    filename = f"banlist_{randomid}.txt"    

    with open(filename, "w") as text_file:
        accounts = []
        for account in recentlyJoined:
            accountjoined = datetime.now(timezone.utc) - account.joined_at
            accountcreated = datetime.now(timezone.utc) - account.created_at
            accounts.append(f"{account.name}#{account.discriminator}, joined {int(accountjoined.seconds / 60)} minutes ago, created {int(accountcreated.days)} days ago.") 

        text_file.write('\n'.join(str(line) for line in accounts))

    with open(filename, "rb") as file:
        message = await ctx.send("**The following list of users will be banned, do you want to continue?**\n*You have 2 minutes to click on the reaction emote.*", file=discord.File(file, filename))

    os.remove(filename)
    await message.add_reaction('🚫')

    def check(reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) == "🚫" and user == ctx.author

    try:
        await client.wait_for("reaction_add", check=check, timeout=120.0)
    except asyncio.TimeoutError:
        await ctx.send("Command timed out")
        return

    async with ctx.channel.typing():
        await ctx.send(f"Banning {len(recentlyJoined)} users...")
        for member in recentlyJoined:
            try:
                await member.ban(reason="Bot spam. Automatically banned by massban bot")
            except Exception as e:
                await ctx.send(f"User could not be banned, error:\n ```{str(e)}```")
                continue
            logging.info(f"{member} banned")
            await asyncio.sleep(3)

        await ctx.send("Members banned successfully!")

# Boot confirmation
@client.event
async def on_ready():
    logging.info("Bot is ready")

client.run(token)
