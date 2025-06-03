import discord
from discord.ext import commands
import logging

class DiscordBot:
    def __init__(self, token, channel_id):
        self.bot = commands.Bot(command_prefix="/")
        self.channel_id = channel_id
        self.bot.command()(self.topgainers)
        self.bot.event(self.on_ready)

    async def on_ready(self):
        logging.info(f"Discord bot logged in as {self.bot.user}")

    async def send_message(self, message, image_path=None):
        """Send a message and optional image to the Discord channel."""
        try:
            channel = self.bot.get_channel(int(self.channel_id))
            if channel:
                await channel.send(message)
                if image_path:
                    await channel.send(file=discord.File(image_path))
            else:
                logging.error("Discord channel not found")
        except Exception as e:
            logging.error(f"Error sending Discord message: {e}")

    async def topgainers(self, ctx):
        """Handle /topgainers command (for testing)."""
        await ctx.send("Fetching top gainers... Check the channel for updates!")

    def start(self):
        """Start the Discord bot."""
        self.bot.run(self.bot.token)
