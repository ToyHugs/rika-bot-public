import discord
import logging

# Import Token from token.txt
with open('token.txt', 'r') as f:
    token = f.read()

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[361923022178746370])
async def hello(ctx):
    print("Hello!")
    await ctx.respond("Hello!")

@bot.slash_command(guild_ids=[361923022178746370])
async def coucou(ctx):
    await ctx.send("Coucou!")
    await ctx.respond()

bot.run(token)