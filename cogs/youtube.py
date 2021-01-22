import discord
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from decouple import config
import boto3
import json
import time

## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

## YouTube API setup
ytkey = config("YTKEY") ## YouTube Data API v3 API Key
youtube = build("youtube", "v3", developerKey=ytkey) # Initialize YouTube Data API v3

class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtubeWatch.start()

    def getYoutubers(self):
        return json.loads(client.get_object(Bucket="ansonbotaws", Key="youtube.json")["Body"].read()) # Gets the object from AWS, takes the body, reads it and converts it to dict

    def getVideos(self, channelID: str):
        a = youtube.channels().list(id=channelID, part="contentDetails").execute()
        return youtube.playlistItems().list(playlistId=a['items'][0]['contentDetails']['relatedPlaylists']['uploads'], part="snippet", maxResults=10).execute()

    def youtubeCache(self):
        youtubes = {}
        with open("ytcache.json", "w") as f:
            for channel in self.getYoutubers().keys():
                youtubes.update({f"{channel}": self.getVideos(channel)})
            json.dump(youtubes, f, indent=4)
        print("YouTube videos cached!")

    @commands.command()
    async def register(self, ctx, channelID: str, channel: str):
        channel = channel[2:-1]
        if not channelID.startswith("UC"):
            await ctx.send("Invalid Channel ID!")
            return
        youtubers = self.getYoutubers()
        if channelID not in youtubers:
            youtubers.update({f"{channelID}": [f"{channel}"]})
        else:
            youtubers[channelID].append(str(channel))
        with open("youtube.json", "w") as f:
            json.dump(youtubers, f, indent=4)
        with open("youtube.json", "rb") as f:
            client.upload_fileobj(f, "ansonbotaws", "prefix.json")
        await ctx.send(f"Registered notifications in <#{channel}> for channel ID {channelID}!")

    @commands.command()
    async def deregister(self, ctx, channelID: str, channel: str):
        channel = channel[2:-1]
        if not channelID.startswith("UC"):
            await ctx.send("Invalid Channel ID!")
            return
        youtubers = self.getYoutubers()
        youtubers[channelID].pop(str(channel))
        with open("youtube.json", "w") as f:
            json.dump(youtubers, f, indent=4)
        with open("youtube.json", "rb") as f:
            client.upload_fileobj(f, "ansonbotaws", "prefix.json")
        await ctx.send(f"Deregistered notifications in <#{channel}> for channel ID {channelID}!")

    @tasks.loop(minutes=2)
    async def youtubeWatch(self):
        with open("ytcache.json", "r") as f:
            cache = json.load(f)
            for channelkey, channelvalue in zip(list(self.getYoutubers().keys()), list(self.getYoutubers().values())):
                new = self.getVideos(channelkey)['items']
                try:
                    old = cache[channelkey]['items']
                except KeyError:
                    self.youtubeCache()
                    time.sleep(2)
                    old = cache[channelkey]['items']
                diff = new[0] != old[0]
                if diff:
                    for dc in channelvalue:
                        discordChannel = self.bot.get_channel(int(dc))
                        embed=discord.Embed(title=f"{new[0]['snippet']['channelTitle']} uploaded a video!", color=0xffff00)
                        embed.set_thumbnail(url=new[0]['snippet']['thumbnails']['standard']['url'])
                        embed.add_field(name=new[0]['snippet']['title'], value=f"{new[0]['snippet']['description']}\nhttps://youtube.com/watch?v={new[0]['snippet']['resourceId']['videoId']}", inline=False)
                        await discordChannel.send(embed=embed)
        self.youtubeCache()

    @youtubeWatch.before_loop
    async def before_youtubeWatch(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        self.youtubeCache()

def setup(bot):
    bot.add_cog(YouTube(bot))
