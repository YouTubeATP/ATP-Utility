## Imports 
import discord
from discord.ext import commands
from decouple import config, UndefinedValueError # A better way to access .env files
import boto3 # Package for AWS
import json
import os
import sys
import io
import traceback

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

@bot.command(aliases=["environ", "env"])
async def environment(ctx):
    try:
        env = config("ENV")
    except UndefinedValueError:
        await ctx.send("Environment undefined!")
    else:
        if env == "LOCAL":
            await ctx.send(f"LOCAL\nI am running locally!\n**{round(bot.latency * 1000)}ms**")
        elif env == "HEROKU":
            await ctx.send(f"HEROKU\nI am running on Heroku!\n**{round(bot.latency * 1000)}ms**")
        elif env == "REPL":
            await ctx.send(f"REPL\nI am running on repl.it!\n**{round(bot.latency * 1000)}ms**")
        else:
            await ctx.send(f"Value undefined: {env}")

@bot.command(name='exec')
async def exec_command(ctx, *, arg1):
    if str(ctx.author.id) == owner:
        arg1 = arg1[6:-4]
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            exec(arg1)
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
        except:
            x = traceback.format_exc()
            embed=discord.Embed(title=f'Execution Failed!', color=0xff0000)
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed = embed)
        else:
            embed=discord.Embed(title=f'Execution Success!', color=0x00ff00)
            embed.set_author(name="ATP City Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
            await ctx.send(embed = embed)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

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