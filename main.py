import discord
from discord.ext import commands
import requests
import os
import webserver

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def test(ctx, *arg):
    restpuesta = ' '.join(arg)
    await ctx.send(restpuesta)

@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ", 1)[0].lower()
        result = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        if result.text == "Not Found":
             await ctx.send("Pokemon no encontrado")
        else:
            imagen_url = result.json()['sprites']['front_default']
            print(imagen_url)
            await ctx.send(imagen_url)
    except Exception as e:
        print("Error: ", e)
    
@poke.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Debes ingresar el nombre de un pokemon")

@bot.command()
async def limpiar(ctx):
    await ctx.channel.purge()
    await ctx.send("Mensajes eliminados", delete_after=3)

webserver.keep_alive()
print("Bot is running")
bot.run(str(DISCORD_TOKEN))