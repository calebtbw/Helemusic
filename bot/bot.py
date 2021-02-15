from datetime import datetime
from pathlib import Path

import discord
from discord import Embed, File
from discord.ext import commands


class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(
            command_prefix=self.prefix, 
            case_insensitive=True, 
            intents=discord.Intents.all(),
        )

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded '{cog}' cog.")

        print("Setup complete.")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

   # async def on_error(self, err, *args, **kwargs):
   #     raise 
   
   # async def on_command_error(self, ctx, exc):
   #     raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        self.guild = self.get_guild(808533625016156220)
        self.stdout = self.get_channel(808620454122225674)

        embed = Embed(title="Now Online!", description="Beta Release", 
                          colour=0xFF0000, timestamp=datetime.utcnow())
        fields = [("HELEMUSIC", "0.0.1", True),
                  ("Made by:", "Caleb T.", True),
                  ("For:", "JR Discord Bot Developer Pitch", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name="HELEMUSIC", icon_url=self.guild.me.avatar_url)
        embed.set_footer(text="Made with Python")    
        embed.set_thumbnail(url=self.guild.icon_url)
    
        await self.stdout.send(embed=embed)

        await self.stdout.send(file=File("./images/music.png"))

        await self.stdout.send("Now Online!")
        print("Bot Ready!")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("!")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)