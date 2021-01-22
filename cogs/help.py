import discord
from discord.ext import commands
from disputils import BotEmbedPaginator

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        ## Page 1 - General Commands
        embedGC=discord.Embed(title="ATP Utility Bot Help", description="General Commands", color=0xffffff)
        embedGC.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedGC.add_field(name=f"`{ctx.prefix}ping`", value="Returns the bot's latency in milliseconds.", inline=True)
        embedGC.add_field(name=f"`{ctx.prefix}invite`", value="Sends the invite link of the bot.", inline=True)
        embedGC.add_field(name=f"`{ctx.prefix}source <github | gitlab>`", value="Sends the GitHub and/ or GitLab repository(ies) of the bot.", inline=True)
        embedGC.add_field(name=f"`{ctx.prefix}support`", value="Sends the link to the bot's support server.", inline=True)
        embedGC.add_field(name=f"`{ctx.prefix}help`", value="This command.", inline=True)
        embedGC.set_footer(text="[] Required <> Optional")
        ## Page 2 - Admin
        embedAdmin=discord.Embed(title="ATP Utility Bot Help", description="Admins", color=0xffffff)
        embedAdmin.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedAdmin.add_field(name=f"`{ctx.prefix}cprefix [newPrefix]`", value="Changes the bot's prefix.", inline=True)
        embedAdmin.add_field(name=f"`{ctx.prefix}clear <amount>`", value="Deletes a number of messages specified by the user. If it is not specified, the bot deletes 5 messages.", inline=True)
        embedAdmin.set_footer(text="[] Required <> Optional")
        ## Page 3 - Aternos 1
        embedAternos1=discord.Embed(title="ATP Utility Bot Help", description="Aternos 1", color=0xffffff)
        embedAternos1.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedAternos1.set_footer(text="[] Required <> Optional")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            embedAternos1.add_field(name=f"`{ctx.prefix}gaf [token] [headerCookie]`", value="Generates an authentication file for Aternos commands.\n[How to obtain the token and headerCookie?](https://streamable.com/0tomau)", inline=False)
        elif isinstance(ctx.channel, discord.channel.TextChannel):
            embedAternos1.add_field(name=f"`{ctx.prefix}auth [token] [headerCookie]`", value="Sets the credentials for Aternos commands.\n[How to obtain the token and headerCookie?](https://streamable.com/0tomau)", inline=False)
            embedAternos1.add_field(name=f"`{ctx.prefix}delauth`", value="Deletes the credentials for Aternos commands.", inline=False)
        ## Page 4 - Aternos 2
        embedAternos2=discord.Embed(title="ATP Utility Bot Help", description="Aternos 2", color=0xffffff)
        embedAternos2.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            embedAternos2.add_field(name=":warning: Caution", value="You will need to **attach** the generated `auth.json` file, or the commands won't work!", inline=False)
        embedAternos2.add_field(name=f"`{ctx.prefix}start`", value="Starts the Aternos Server.", inline=True)
        embedAternos2.add_field(name=f"`{ctx.prefix}stop`", value="Stops the Aternos Server.", inline=True)
        embedAternos2.set_footer(text="[] Required <> Optional")
        ## Page 5 - COVID-19 Hong Kong
        embedC19HK=discord.Embed(title="ATP Utility Bot Help", description="COVID-19 Hong Kong Stat Commands", color=0xffffff)
        embedC19HK.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedC19HK.add_field(name=f"`{ctx.prefix}c19hkd <DD/MM/YYYY>`", value="Sends data regarding Hong Kong's COVID-19 status as of a date. If no date is inserted, the bot will return data as of yesterday.", inline=False)
        embedC19HK.add_field(name=f"`{ctx.prefix}c19hkcd [caseno]`", value="Sends data regarding a COVID-19 case in Hong Kong, given the case number.", inline=False)
        embedC19HK.add_field(name=f"`{ctx.prefix}c19hklist [dataType] [operator | sortType] [val1] [val2]`", value="Returns a list regarding multiple days of Hong Kong's COVID-19 status, given the parameters. See [here](https://i.imgur.com/qnpcx83.png) for details.\nNote: this command does not show properly for some Discord clients.", inline=False)
        embedC19HK.add_field(name=f"`{ctx.prefix}c19hkclist [dataType] [operator | sortType] [val1] [val2]`", value="Returns a list regarding multiple Hong Kong's COVID-19 cases, given the parameters. See [here](https://i.imgur.com/mfccw5P.png) for details.\nNote: this command does not show properly for some Discord clients.", inline=False)
        embedC19HK.set_footer(text="[] Required <> Optional")
        ## Page 6 - Fun Commands
        embedFun=discord.Embed(title="ATP Utility Bot Help", description="Fun Commands", color=0xffffff)
        embedFun.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedFun.add_field(name=f"`{ctx.prefix}8ball [question]`", value="Asks the Magic 8-Ball a question.", inline=True)
        embedFun.add_field(name=f"`{ctx.prefix}fortune`", value="Gives you a fortune cookie. Yum!", inline=True)
        embedFun.add_field(name=f"`{ctx.prefix}da <mentionUser>`", value="Tells you the color of the default avatar for a user!", inline=False)
        embedFun.add_field(name=f"`{ctx.prefix}rate`", value="Let the bot rate something.", inline=True)
        embedFun.set_footer(text="[] Required <> Optional")
        ## Page 7 - Invite Manager Commands
        embedInv=discord.Embed(title="ATP Utility Bot Help", description="Invite Manager Commands", color=0xffffff)
        embedInv.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedInv.add_field(name=f"`{ctx.prefix}invleader`", value="Gives you the invite leaderboard. Who invited the most users?", inline=False)
        embedInv.add_field(name=f"`{ctx.prefix}inviteChannel [mentionChannel]`", value="Configure the channel used for logging user join activity. (Inviter and link used to join)", inline=False)
        embedInv.add_field(name=f"`{ctx.prefix}inviteRemove`", value=f"Removes the channel set up in `{ctx.prefix}inviteChannel`. Hence disables the user join logger.", inline=False)
        embedInv.set_footer(text="[] Required <> Optional")
        ## Page 8 - NetherGames Commands
        embedNG=discord.Embed(title="ATP Utility Bot Help", description="NetherGames Commands", color=0xffffff)
        embedNG.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedNG.add_field(name=f"`{ctx.prefix}ngp [gamertag]`", value="Displays statistics of a given player for the Minecraft server NetherGames.", inline=False)
        embedNG.add_field(name=f"`{ctx.prefix}ngfl [gamertag]`", value="Displays the friend list of a given player in the Minecraft server NetherGames.", inline=False)
        embedNG.set_footer(text="[] Required <> Optional")
        ## Page 9 - YouTube Commands
        embedYT=discord.Embed(title="ATP Utility Bot Help", description="YouTube Commands", color=0xffffff)
        embedYT.set_thumbnail(url="https://i.imgur.com/YUFIrJJ.png")
        embedYT.add_field(name=f"`{ctx.prefix}register [youtubeChannelID] [discordChannel]`", value="Registers a YouTube channel and a discord channel for video upload notifications.", inline=False)
        embedYT.add_field(name=f"`{ctx.prefix}deregister [youtubeChannelID] [discordChannel]`", value="Deregisters a YouTube channel and the corresponding discord channel from video upload notifications.", inline=False)
        embedYT.set_footer(text="[] Required <> Optional")
        ## Main code here
        embeds = [embedGC, embedAdmin, embedAternos1, embedAternos2, embedC19HK, embedFun, embedInv, embedNG, embedYT]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

def setup(bot):
    bot.add_cog(Help(bot))
