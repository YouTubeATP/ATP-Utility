import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from decouple import config
import boto3
import json

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

class Admins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cprefix"])
    @commands.has_permissions(administrator=True)
    async def changePrefix(self, ctx, *, newPrefix):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send("Changing prefix is unavailable in DMs! We are sorry for any inconvenience caused.")
        elif isinstance(ctx.channel, discord.channel.TextChannel):
            prefixes = json.loads(client.get_object(Bucket="ansonbotaws", Key="prefix.json")["Body"].read()) # Gets the object from AWS, takes the body, reads it and converts it to dict
            prefixes.update({f"{ctx.message.guild.id}": f"{newPrefix}"})
            with open("prefix.json", "w") as f:
                json.dump(prefixes, f, indent=4)
            with open("prefix.json", "rb") as f:
                client.upload_fileobj(f, "ansonbotaws", "prefix.json")
            await ctx.send(f"My prefix has been changed to `{newPrefix}`\nPlease remember it!")
        else:
            return

    @changePrefix.error
    async def changePrefix_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Sorry, but you do not have the permissions to do that.")

    @commands.command()
    async def clear(self, ctx, amount):
        if not await has_permissions(manage_channels=True).predicate(ctx):
            raise MissingPermissions(["manage_channels"])
        await ctx.channel.purge(limit = int(amount) + 1)
        await ctx.send(f'**{amount}** message(s) had been deleted!')

def setup(bot):
    bot.add_cog(Admins(bot))
