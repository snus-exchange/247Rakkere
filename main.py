import discord
from discord.ext import commands
import asyncio
import yt_dlp
import os
from dotenv import load_dotenv

load_dotenv()  # Henter verdier fra .env-filen

TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_URL = os.getenv("YOUTUBE_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
}

@bot.event
async def on_ready():
    print(f"✅ Logget inn som {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("🔊 Koblet til voice-kanal!")
    else:
        await ctx.send("Du må være i en voice-kanal først!")

@bot.command()
async def play(ctx):
    vc = ctx.voice_client
    if not vc:
        await ctx.send("Boten må være i en voice-kanal først. Bruk !join")
        return

    await ctx.send("🎶 Starter nonstop Rakkere!")

    while True:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(YOUTUBE_URL, download=False)
            url2 = info['url']
            title = info.get('title', 'ukjent sang')

        vc.stop()
        vc.play(discord.FFmpegPCMAudio(url2, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'))
        await ctx.send(f"🔁 Spiller nå: {title}")

        while vc.is_playing():
            await asyncio.sleep(1)

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Forlot voice-kanalen!")

bot.run(TOKEN)
