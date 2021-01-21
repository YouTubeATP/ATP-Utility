import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
import traceback
import json
from decouple import config
import boto3

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getInvs(self, id):
        try:
            return json.loads(client.get_object(Bucket="ansonbotaws", Key="invites.json")["Body"].read())[str(id)]
        except KeyError:
            return {}

    async def updateInvs(self, dict, id):
        invites = json.loads(client.get_object(Bucket="ansonbotaws", Key="invites.json")["Body"].read())
        invites.update({f"{str(id)}": dict})
        with open("invites.json", "w") as f:
            json.dump(invites, f, indent=4)
        with open("invites.json", "rb") as f:
            client.upload_fileobj(f, "ansonbotaws", "invites.json")

    @commands.Cog.listener()
    async def on_ready(self):
        global invites
        invites = {}
        for guild in self.bot.guilds:
            try:
                invites[guild.id] = await guild.invites()
            except discord.errors.Forbidden as exception:
                continue
        print("Invites cached!")

    def code2inv(self, list, code):
        for invite in list:
            if invite.code == code:
                return invite
        else:
            return False

    def diff(self, li1: list, li2: list):
        return list(set(li2)-set(li1))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global invites
        if not member.bot:
            old_inv = invites[member.guild.id]
            new_inv = await member.guild.invites()
            for invite in old_inv:
                try:
                    if invite.uses < int(self.code2inv(new_inv, invite.code).uses):
                        invites[member.guild.id] = new_inv
                        with open('invitechannel.json', 'r') as f:
                            invc = json.load(f)
                            channel = self.bot.get_channel(int(invc[str(member.guild.id)]))
                            embed=discord.Embed(title=f'{member.name} Joined!', color=0xff9000)
                            embed.add_field(name="Joined", value=f"<@{member.id}>", inline=True)
                            embed.add_field(name="Invited by", value=f"<@{invite.inviter.id}>", inline=True)
                            embed.add_field(name="Joined with link", value=f"https://discord.gg/{invite.code}", inline=False)
                        await channel.send(embed=embed)
                        invsJson = await self.getInvs(member.guild.id)
                        if str(invite.inviter.id) in invsJson:
                            invNo = int(invsJson[str(invite.inviter.id)])
                            invsJson[str(invite.inviter.id)] = int(invNo + 1)
                        else:
                            invsJson.update({f"{str(invite.inviter.id)}": 1})
                        await self.updateInvs(invsJson, member.guild.id)
                    elif not self.code2inv(new_inv, invite.code):
                        continue
                except AttributeError:
                    continue
            if len(self.diff(li1=old_inv, li2=new_inv)) > 0:
                invite = (self.diff(old_inv, new_inv))[0]
                invites[member.guild.id] = new_inv
                with open('invitechannel.json', 'r') as f:
                    invc = json.load(f)
                    channel = self.bot.get_channel(int(invc[str(member.guild.id)]))
                    embed=discord.Embed(title=f'{member.name} Joined!', color=0xff9000)
                    embed.add_field(name="Joined", value=f"<@{member.id}>", inline=True)
                    embed.add_field(name="Invited by", value=f"<@{invite.inviter.id}>", inline=True)
                    embed.add_field(name="Joined with link", value=f"https://discord.gg/{invite.code}", inline=False)
                await channel.send(embed=embed)
                invsJson = await self.getInvs(member.guild.id)
                if str(invite.inviter.id) in invsJson:
                    invNo = int(invsJson[str(invite.inviter.id)])
                    invsJson[str(invite.inviter.id)] = int(invNo + 1)
                else:
                    invsJson.update({f"{str(invite.inviter.id)}": 1})
                await self.updateInvs(invsJson, member.guild.id)

    @commands.command(aliases=["invleader"])
    async def inviteleaderboard(self, ctx):
        invs = await self.getInvs(ctx.guild.id)
        leaders = dict(sorted(invs.items(), key=lambda x: x[1], reverse=True))
        leaderv = list(leaders.values())
        leaderk = list(leaders.keys())
        msg = "**__Invites Leaderboard__**"
        rank = int(leaderv[0])
        place = 1
        usersDone = 0
        for name, inve in zip(leaderk, leaderv):
            for users in ctx.guild.members:
                if str(users.id) == str(name):
                    user = users
                else:
                    continue
                if rank > int(inve):
                    place += 1
                    rank = int(leaderv[usersDone])
                msg += f"\n{str(place)}. {user.name}#{user.discriminator} - {rank} Invite"
                if int(inve) > 1:
                    msg += "s"
                usersDone += 1
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        global invites
        try:
            invites[member.guild.id] = await member.guild.invites()
        except discord.errors.Forbidden:
            traceback.print_exc()

    @commands.command()
    async def inviteChannel(self, ctx, *, channel: str):
        if ('administrator', True) in iter(ctx.author.permissions_in(ctx.channel)):
            invc = json.loads(client.get_object(Bucket="ansonbotaws", Key="invitechannel.json")["Body"].read())
            channel = channel[2:-1]
            invc[ctx.guild.id] = channel
            with open('invitechannel.json', 'w') as f:
                json.dump(invc, f, indent=4)
            with open("invitechannel.json", "rb") as f:
                client.upload_fileobj(f, "ansonbotaws", "invitechannel.json")
            await ctx.send(f"Invite manager channel has been set to <#{channel}>!")
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

    @commands.command()
    async def inviteRemove(self, ctx):
        if ('administrator', True) in iter(ctx.author.permissions_in(ctx.channel)):
            invc = json.loads(client.get_object(Bucket="ansonbotaws", Key="invitechannel.json")["Body"].read())
            invc.pop(ctx.guild.id)
            with open('invitechannel.json', 'w') as f:
                json.dump(invc, f, indent=4)
            with open("invitechannel.json", "rb") as f:
                client.upload_fileobj(f, "ansonbotaws", "invitechannel.json")
            await ctx.send('Removed invite manager channel!')
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

def setup(bot):
    bot.add_cog(Invite(bot))