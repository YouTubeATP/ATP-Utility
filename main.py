## Imports 
import discord
from discord.ext import commands
from decouple import config # A better way to access .env files
import boto3 # Package for AWS
import json
import os

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

def getPrefix(bot, message):
    prefixes = json.loads(client.get_object(Bucket="ansonbotaws", Key="prefix.json")["Body"].read()) # Gets the object from AWS, takes the body, reads it and converts it to dict
    try:
        return prefixes[str(message.guild.id)]
    except KeyError: # No prefix set up yet, likely a new guild
        ## Update remote database
        prefixes.update({f"{message.guild.id}": "a!"})
        with open("prefix.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        with open("prefix.json", "rb") as f:
            client.upload_fileobj(f, "ansonbotaws", "prefix.json")
        ## Return default prefix
        return "a!"
    except AttributeError: # Likely a DM
        return "a!" # Return default prefix

## Bot setup
bot = commands.Bot(command_prefix=getPrefix)
bot.remove_command("help") # Remove built-in help command for custom help command

owner = config("OWNER") # User ID of the bot owner

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}!\nBot is ready.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="mentions for prefix"))
    print('Bot status changed!')

## Load extensions
for i in os.listdir('./cogs'):
    if i.endswith('.py'):
        bot.load_extension(f'cogs.{i[:-3]}')
print('Extensions loaded!')

## Mention for prefix
@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await message.channel.send(f"My prefix is `{getPrefix(bot=bot, message=message)}`")
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! The latency is **{round(bot.latency * 1000)}ms**.')

@bot.command(aliases=["github"])
async def source(ctx):
    await ctx.send("Here is the GitHub repository for the bot:\nhttps://github.com/YouTubeATP/ATP-Utility")

@bot.command()
async def support(ctx):
    await ctx.send("Here is the bot's support server:\nhttps://discord.gg/dJn7mBJxyS")

@bot.command()
async def invite(ctx):
    await ctx.send("Here is the invite link for the bot:\nhttps://bit.ly/3bSPBmh")

## Extension control commands
@bot.command()
async def extload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def extunload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def extreload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Reloaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def extlist(ctx):
    if str(ctx.author.id) == str(owner):
        exts = []
        for i in os.listdir('./cogs'):
            if i.endswith('.py'):
                exts.append(i[:-3])
        message1 = ''
        for j in exts:
            message1 += f'''`{j}`\n'''
        await ctx.send(message1)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

bot.run(config("TOKEN"))