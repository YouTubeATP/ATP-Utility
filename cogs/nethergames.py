import discord
from discord.ext import commands
import urllib.parse
import urllib.request
from urllib.error import HTTPError
import json

class NetherGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['ngp', 'ngplayer', 'nethergamesp'])
    async def nethergamesplayer(self, ctx, *, arg):
        try:
            if len(arg) >= 1: ## Checks whether argument 1 (gamertag) exists
                ngstats1 = urllib.parse.quote(arg)
                ngstats2 = urllib.request.Request("https://api.nethergames.org/?action=stats&player=" + str(ngstats1), headers={'User-Agent': 'Mozilla/5.0'}) ## Contrusts the API link and urllib request
                print('Requesting data now from: ' + "https://api.nethergames.org/?action=stats&player=" + str(ngstats1))
                ngstats3 = urllib.request.urlopen(ngstats2) ## Stores info from API to var ngstats2
                for line in ngstats3: ## Code that decodes the API data into json we can use
                    ngstats4 = line.decode("utf-8") ## Stores json into var ngstats3
                    ngstats = json.loads(ngstats4) ## Converts json into python dictionary, which we can use
                    kills1 = ngstats['kills']
                    deaths1 = ngstats['deaths']
                    kills2 = int(ngstats['kills'])
                    deaths2 = int(ngstats['deaths'])
                    try:
                        kdr = round(kills2 / deaths2, 2)
                    except ZeroDivisionError:
                        kdr = '-'
                    wins1 = ngstats['wins']
                    level1 = ngstats['level']
                    credits1 = ngstats['statusCredits']
                    lastjoin1 = ngstats['lastJoin']
                    firstjoin1 = ngstats['firstJoin']
                    tier1 = ngstats['tier']
                    guild1 = ngstats['guild']
                    voted1 = ngstats['voted']
                    bio1 = ngstats['bio']
                    lastserver1 = ngstats['lastServer']
                    lastseen1 = ngstats['lastSeen']
                    discorddata1 = ngstats['discordData']
                    ## For FinalKillsData, only extract Duels, MM, SW, BW, since they are the only ones that are really useful
                    duels1 = ngstats['winsData']['Duels']
                    mm1 = ngstats['winsData']['MM']
                    sw1 = ngstats['winsData']['SW']
                    bw1 = ngstats['winsData']['BW']
                    ## Changing var values from computer gibberish to human readable language
                    if ngstats['ranks'][0]:
                        rank = str(ngstats['ranks'])
                        rank = rank.replace("[", "")
                        rank = rank.replace("]", "")
                        rank = rank.replace("'", "")
                    else:
                        rank = "N/A"
                    if not credits1:
                        credits1 = 0
                    else:
                        credits1 = ngstats['statusCredits']
                    if not tier1:
                        tier1 = 'N/A'
                    else:
                        tier1 = ngstats['tier']
                    if not bio1:
                        bio1 = 'N/A'
                    else:
                        bio1 = ngstats['bio']
                    if not guild1:
                        guild1 = 'N/A'
                    else:
                        guild1 = ngstats['guild']
                    if voted1 == 0:
                        voted1 = 'Did not vote'
                    elif voted1 == 1:
                        voted1 = 'Voted but unclaimed'
                    elif voted1 == 2:
                        voted1 = 'Voted & claimed'
                    ## Finally, the part that makes the actual embed message
                    ngstatsembed=discord.Embed(title=f'{arg} - Player Statistics', url="https://account.nethergames.org/player/" + str(ngstats1), color=0xff8c00)
                    ngstatsembed.set_author(name="NetherGames Network", url="https://nethergames.org", icon_url="https://cdn.nethergames.org/img/logo/discord-icon-nobg.png")
                    ngstatsembed.set_thumbnail(url="https://player.nethergames.org/avatar/" + str(ngstats1))
                    ngstatsembed.add_field(name="Kills", value=f'{kills1}', inline=True)
                    ngstatsembed.add_field(name="Deaths", value=f'{deaths1}', inline=True)
                    ngstatsembed.add_field(name="K/DR", value=f'{kdr}', inline=True)
                    ngstatsembed.add_field(name="Wins", value=f'{wins1}', inline=True)
                    ngstatsembed.add_field(name="Level", value=f'{level1}', inline=True)
                    ngstatsembed.add_field(name="Credits", value=f'{credits1}', inline=True)
                    ngstatsembed.add_field(name="Rank", value=f'{rank}', inline=True)
                    ngstatsembed.add_field(name="Tier", value=f'{tier1}', inline=True)
                    ngstatsembed.add_field(name="Guild", value=f'{guild1}', inline=True)
                    ngstatsembed.add_field(name="First seen", value=f'{firstjoin1}', inline=True)
                    ngstatsembed.add_field(name="Last seen", value=f'{lastjoin1}', inline=True)
                    ngstatsembed.add_field(name="Vote Status", value=f'{voted1}', inline=True)
                    ngstatsembed.add_field(name="Biography", value=f'{bio1}', inline=True)
                    ## Hiding that field in FinalKillsData if the player has 0 FinalKills in that gamemode
                    winsData1 = r'''ngstatsembed.add_field(name="Wins Summary", value=f'Duels: {duels1}\nMurder Mystery: {mm1}\nSkyWars: {sw1}\nBedwars: {bw1}', inline=True)'''
                    if duels1 == 0:
                        winsData1 = winsData1.replace(r"Duels: {duels1}\n", "")
                    if mm1 == 0:
                        winsData1 = winsData1.replace(r"Murder Mystery: {mm1}\n", "")
                    if sw1 == 0:
                        winsData1 = winsData1.replace(r"SkyWars: {sw1}\n", "")
                    if bw1 == 0:
                        winsData1 = winsData1.replace(r"Bedwars: {bw1}", "")
                    exec(winsData1)
                    ## Online / Offline status
                    if int(ngstats["online"]) == 1:
                        ngstatsembed.set_footer(text=f'Online - playing on {lastserver1}', icon_url="https://cdn.nethergames.org/img/green.png")
                    else:
                        ngstatsembed.set_footer(text=f'Offline - last seen {lastseen1} ago on {lastserver1}', icon_url="https://cdn.nethergames.org/img/red.png")
                    ## Linked Discord Account (from API discordData)
                    if not discorddata1:
                        ngstatsembed.add_field(name="Linked Discord Account", value=f'N/A', inline=True)
                    else:
                        linkeddiscordid = ngstats['discordData']['claim']
                        user = await self.bot.fetch_user(linkeddiscordid)
                        ngstatsembed.add_field(name="Linked Discord Account", value=f'{user.name}#{user.discriminator}', inline=True)
                    await ctx.send(embed = ngstatsembed)
        except HTTPError:
            await ctx.send('This is not a valid player name! Please verify your input and try again.')

    @commands.command(aliases = ['ngfl', 'ngf', 'nethergamesfl', 'nethergamesf', "ngfriend", 'ngfriendlist'])
    async def NetherGamesFriendList(self, ctx, *, arg):
        try:
            if len(arg) >= 1: ## Checks whether argument 1 (gamertag) exists
                ngstats1 = urllib.parse.quote(arg)
                ngstats2 = urllib.request.Request("https://api.nethergames.org/?action=stats&player=" + str(ngstats1), headers={'User-Agent': 'Mozilla/5.0'}) ## Contrusts the API link and urllib request
                print('Requesting data now from: ' + "https://api.nethergames.org/?action=stats&player=" + str(ngstats1))
                ngstats3 = urllib.request.urlopen(ngstats2) ## Stores info from API to var ngstats2
                for line in ngstats3: ## Code that decodes the API data into json we can use
                    ngstats4 = line.decode("utf-8") ## Stores json into var ngstats3
                    ngstats = json.loads(ngstats4) ## Converts json into python dictionary, which we can use
                    ## Storing the friend list into a variable
                    ngfriendlist = ngstats['friends']
                    ## Magic that turns a python list into a numbered human readable list
                    message = f"Friend list of player {arg}\n```"
                    for i, friend in enumerate(ngfriendlist, start = 1):
                        message += f"\n{i}. {friend}"
                    message += "\n```"
                    await ctx.send(message)
        except HTTPError:
            await ctx.send('This is not a valid player name! Please verify your input and try again.')

def setup(bot):
    bot.add_cog(NetherGames(bot))