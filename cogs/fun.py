import discord
from discord.ext import commands
import json
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question):
        choice = random.randint(0, 19)
        if choice in range(0, 10):
            color = 0x00ff00 # Green
        elif choice in range(10, 15):
            color = 0xffff00 # Yellow
        elif choice in range(15, 20):
            color = 0xff0000 # Red
        else:
            raise IndexError("Choice is out of range.")
        with open("assets/8ball.json", "r") as f:
            answers = json.load(f)
        embed=discord.Embed(title="Magic 8 Ball", color=color)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/71FfSFVzXJL._AC_SL1500_.jpg")
        embed.add_field(name="Question", value=question, inline=True)
        embed.add_field(name="Answer", value=answers[choice], inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def fortune(self, ctx):
        with open("assets/fortunes.json", "r") as f:
            answers = json.load(f)
        embed=discord.Embed(title="Fortune Cookie", description=random.choice(answers))
        embed.set_thumbnail(url="https://cdn.shopify.com/s/files/1/0836/4641/products/FORTUNE-COOKIE.jpg?v=1527554178")
        await ctx.send(embed=embed)

    @commands.command(aliases=['da'])
    async def defaultAvatar(self, ctx, *, user: discord.Member=None):
        if user:
            remainder = int(user.discriminator) % 5
            pronoun = f"{user.name} has"
        else:
            remainder = int(ctx.author.discriminator) % 5 
            pronoun = "You have"
        if remainder == 0:
            color = "blurple"
            colorh = 0x7289DA # Blurple
            link = "https://cdn.discordapp.com/embed/avatars/0.png"
        elif remainder == 1:
            color = "gray"
            colorh = 0x747F8D # Gray
            link = "https://cdn.discordapp.com/embed/avatars/1.png"
        elif remainder == 2:
            color = "green"
            colorh = 0x43B581 # Green
            link = "https://cdn.discordapp.com/embed/avatars/2.png"
        elif remainder == 3:
            color = "yellow"
            colorh = 0xFAA61A # Yellow
            link = "https://cdn.discordapp.com/embed/avatars/3.png"
        elif remainder == 4:
            color = "red"
            colorh = 0xF04747 # Red
            link = "https://cdn.discordapp.com/embed/avatars/4.png"
        else:
            raise IndexError("Remainder is out of range.")
        embed=discord.Embed(title="Default avatar color", color=colorh)
        embed.set_thumbnail(url=link)
        embed.add_field(name=f"{pronoun} a {color}-colored default avatar!", value="[Want to know how this works?](http://gg.gg/nv7ek)", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rate(self, ctx):
        await ctx.send(f"{str(random.randint(0, 100) / 10)}/10")

def setup(bot):
    bot.add_cog(Fun(bot))
