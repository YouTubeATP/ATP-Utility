from main import getPrefix
import discord
from discord.ext import commands
import json
import requests
from bs4 import BeautifulSoup
import traceback
from decouple import config
import boto3

## Aternos API
class AternosAPI():
    def __init__(self, headers, TOKEN):
        self.headers = {}
        self.TOKEN = TOKEN
        self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
        self.headers['Cookie'] = headers
        self.SEC = self.getSEC()
        self.JavaSoftwares = ['Vanilla', 'Spigot', 'Forge', 'Magma','Snapshot', 'Bukkit', 'Paper', 'Modpacks', 'Glowstone']
        self.BedrockSoftwares = ['Bedrock', 'Pocketmine-MP']

    def getSEC(self):
        headers = self.headers['Cookie'].split(";")
        for sec in headers:
            if sec[:12] == "ATERNOS_SEC_":
                sec = sec.split("_")
                if len(sec) == 3:
                    sec = ":".join(sec[2].split("="))
                    return sec

        print("Invaild SEC")
        exit(1)

    def GetStatus(self):
        webserver = requests.get(url='https://aternos.org/server/', headers=self.headers)
        webdata = BeautifulSoup(webserver.content, 'html.parser')
        status = webdata.find('span', class_='statuslabel-label').get_text()
        status = status.strip()
        return status

    def StartServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Online":
            return "Server Already Running"
        else:
            parameters = {}
            parameters['headstart'] = 0
            parameters['SEC'] = self.SEC
            parameters['TOKEN'] = self.TOKEN
            startserver = requests.get(url=f"https://aternos.org/panel/ajax/start.php", params=parameters, headers=self.headers)
            return "Server Started"

    def StopServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Offline":
            return "Server Already Offline"
        else:
            parameters = {}
            parameters['SEC'] = self.SEC
            parameters['TOKEN'] = self.TOKEN
            stopserver = requests.get(url=f"https://aternos.org/panel/ajax/stop.php", params=parameters, headers=self.headers)
            return "Server Stopped"

    def GetServerInfo(self):
        ServerInfo = requests.get(url='https://aternos.org/server/', headers=self.headers)
        ServerInfo = BeautifulSoup(ServerInfo.content, 'html.parser')

        Software = ServerInfo.find('span', id='software').get_text()
        Software = Software.strip()

        if(Software in self.JavaSoftwares):
            IP = ServerInfo.find('div', class_='server-ip mobile-full-width').get_text()
            IP = IP.strip()

            IP = IP.split(" ")
            IP = IP[0].strip()

            Port = "25565(Optional)"

            return f"{IP},{Port},{Software}"

        elif(Software in self.BedrockSoftwares):
            IP = ServerInfo.find('span', id='ip').get_text()
            IP = IP.strip()

            Port = ServerInfo.find('span', id='port').get_text()
            Port = Port.strip()

            return f"{IP},{Port},{Software}"

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

## Aternos commands
class Aternos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gaf"])
    async def generateAuthFile(self, ctx, token: str, *, headerCookie: str):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            auth = {}
            auth.update({"token": token, "headerCookie": headerCookie})
            with open("auth.json", "w") as f:
                json.dump(auth, f, indent=4)
            await ctx.send("Your Authentication File has been generated. Please avoid sharing or using the file in public servers.\nAternos commands are available in DMs only.", file=discord.File(fp="auth.json", filename="auth.json"))
            del auth # Resetting the auth file
            with open("auth.json", "w") as f:
                json.dump({}, f, indent=4)
        else:
            await ctx.send("Please only use this command in a DM!")
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                pass

    @commands.command(aliases=["auth"])
    async def serverAuth(self, ctx, token: str, *, headerCookie: str):
        if isinstance(ctx.channel, discord.channel.TextChannel): # Checks if the message is sent in a server
            auth = {}
            auth.update({"token": token, "headerCookie": headerCookie})
            cookies = json.loads(client.get_object(Bucket="ansonbotaws", Key="cookies.json")["Body"].read()) # Gets the object from AWS, takes the body, reads it and converts it to dict
            cookies.update({f"{ctx.guild.id}": auth})
            ## Upload to AWS
            with open("cookies.json", "w") as f:
                json.dump(cookies, f, indent=4)
            with open("cookies.json", "rb") as f:
                client.upload_fileobj(f, "ansonbotaws", "cookies.json")
            ## Clean up local storage
            with open("cookies.json", "w") as f:
                json.dump({}, f, indent=4)
            del auth, cookies
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden: # Can't delete message due to missing permissions
                pass
            await ctx.send(f"Your cookies have been stored securely in our remote AWS S3 database.\nUse {ctx.prefix}delAuth in case you want to remove it from our database.")
        else:
            await ctx.send("Please only use this command in a server!")
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden: # Can't delete message due to missing permissions
                pass

    @commands.command(aliases=["delauth"])
    async def delServerAuth(self, ctx):
        if isinstance(ctx.channel, discord.channel.TextChannel): # Checks if the message is sent in a server
            auth = {}
            cookies = json.loads(client.get_object(Bucket="ansonbotaws", Key="cookies.json")["Body"].read()) # Gets the object from AWS, takes the body, reads it and converts it to dict
            cookies.update({f"{ctx.guild.id}": auth})
            ## Upload to AWS
            with open("cookies.json", "w") as f:
                json.dump(cookies, f, indent=4)
            with open("cookies.json", "rb") as f:
                client.upload_fileobj(f, "ansonbotaws", "cookies.json")
            ## Clean up local storage
            with open("cookies.json", "w") as f:
                json.dump({}, f, indent=4)
            del auth, cookies
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden: # Can't delete message due to missing permissions
                pass
            await ctx.send(f"Your cookies have been stored securely in our remote AWS S3 database.\nUse {ctx.prefix}delAuth in case you want to remove it from our database.")
        else:
            await ctx.send("Please only use this command in a server!")
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden: # Can't delete message due to missing permissions
                pass

    @commands.command(aliases=["open"])
    async def start(self, ctx):
        ## Checking:
        ## 1. Whether there is only 1 attachment
        ## 2. Whether that attachment is auth.json
        ## 3. Whether the command is used in a DM
        try:
            if len(ctx.message.attachments) == 1 and ctx.message.attachments[0].filename == "auth.json" and isinstance(ctx.channel, discord.channel.DMChannel):
                ## Taking the credentials
                await ctx.message.attachments[0].save("cookie.json")
                with open("cookie.json", "r") as f:
                    cookies = json.load(f) 
                ## Reset cookie.json
                with open("cookie.json", "w") as f:
                    json.dump({}, f, indent=4)
            elif isinstance(ctx.channel, discord.channel.TextChannel):
                cookies = json.loads(client.get_object(Bucket="ansonbotaws", Key="cookies.json")["Body"].read()) # Gets the object from AWS, takes the body, reads it and converts it to dict
                try:
                    cookies = cookies[str(ctx.message.guild.id)]
                except KeyError:
                    await ctx.send("Your server owner has not registered the server cookies yet! Sorry, but we may not open the server.")
                    return
            try:
                server = AternosAPI(headers=cookies["headerCookie"], TOKEN=cookies["token"])
            except KeyError:
                await ctx.send("Your server owner has not registered the server cookies yet! Sorry, but we may not open the server.")
                return
            await ctx.send("Starting the server now...")
            await ctx.send(server.StartServer())
            del cookies, server
        except:
            await ctx.send("Please check your input and attachments and try again!")
            traceback.print_exc()
        
    @commands.command()
    async def stop(self, ctx):
        ## Checking:
        ## 1. Whether there is only 1 attachment
        ## 2. Whether that attachment is auth.json
        ## 3. Whether the command is used in a DM
        try:
            if len(ctx.message.attachments) == 1 and ctx.message.attachments[0].filename == "auth.json" and isinstance(ctx.channel, discord.channel.DMChannel):
                ## Taking the credentials
                await ctx.message.attachments[0].save("cookie.json")
                with open("cookie.json", "r") as f:
                    cookies = json.load(f) 
                ## Reset cookie.json
                with open("cookie.json", "w") as f:
                    json.dump({}, f, indent=4)
            elif isinstance(ctx.channel, discord.channel.TextChannel):
                cookies = json.loads(client.get_object(Bucket="ansonbotaws", Key="cookies.json")["Body"].read()) # Gets the object from AWS, takes the body, reads it and converts it to dict
                try:
                    cookies = cookies[str(ctx.message.guild.id)]
                except KeyError:
                    await ctx.send("Your server owner has not registered the server cookies yet! Sorry, but we may not open the server.")
                    return
            try:
                server = AternosAPI(headers=cookies["headerCookie"], TOKEN=cookies["token"])
            except KeyError:
                await ctx.send("Your server owner has not registered the server cookies yet! Sorry, but we may not open the server.")
                return
            await ctx.send("Stopping the server now...")
            await ctx.send(server.StopServer())
            del cookies, server
        except:
            await ctx.send("Please check your input and attachments and try again!")
            traceback.print_exc()

def setup(bot):
    bot.add_cog(Aternos(bot))
