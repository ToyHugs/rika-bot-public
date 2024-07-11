# ===================================================================================
# =================================== IMPORTS =======================================
# ===================================================================================

import discord
import os
import plugins.artificial as artificial


# ===================================================================================
# =================================== CONSTANTS =====================================
# ===================================================================================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


# ===================================================================================
# =================================== FUNCTIONS =====================================
# ===================================================================================

# Create the bot
bot = discord.Bot()

# ===================================================================================
# =================================== COMMANDS ======================================
# ===================================================================================

guild_ids_tab = [361923022178746370, 903296382952157234]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Hello command
@bot.slash_command(name="sylvain", description="Crie comme un débile, Sylvain DURIF", guild_ids=guild_ids_tab)
async def crie(ctx: discord.ApplicationContext):
    print("Crie")
    await ctx.respond("https://cdn.discordapp.com/attachments/903352959486804058/1221199849962340552/Sylvain_Durif_crie.mp4?ex=662d657d&is=661af07d&hm=58f8d9c9f552194b078e9ddaa82153c30f21ad70d3b4810ebc877966c9803ac2&")

@bot.slash_command(name="booba", description="Say hello to the bot")
async def booba(ctx: discord.ApplicationContext):
    print("Booba")
    await ctx.respond("Hello!")


# Retrieve the id of the guilds where the commands is used
@bot.slash_command(name="guilds", description="Retourne les identifiants des guilds où la commande est utilisée", guild_ids=guild_ids_tab)
async def guilds(ctx: discord.ApplicationContext):
    guild_ids = ctx.guild_id
    await ctx.respond(f"Guilds ids: {guild_ids}")


# Talk with the bot
@bot.slash_command(name="talk", description="Talk with the bot")
async def talk(ctx: discord.ApplicationContext, message: str):
    # Envoie le message de l'utilisateur
    await ctx.respond(f"{ctx.user.name} : {message}")

    # Récupère le message de l'IA
    response = artificial.run(ctx.guild_id, message)

    # Envoie le message de l'IA
    for message_out in response:
        await ctx.respond(f"{message_out}")



# Run the bot

bot.run(DISCORD_TOKEN)
