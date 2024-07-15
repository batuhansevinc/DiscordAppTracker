import discord
from discord.ext import commands
from package_checker import PackageChecker
from channel_manager import ChannelManager
from data_manager import DataManager
import json

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['TOKEN']
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, data_manager):
        super().__init__(command_prefix='!', intents=intents)
        self.channel_manager = ChannelManager(data_manager)
        self.package_checker = PackageChecker(data_manager)
        self.data_manager = data_manager

    async def setup_hook(self):

        self.tree.clear_commands(guild=None)
        self.tree.add_command(set_channel)
        self.tree.add_command(add_package)
        self.tree.add_command(remove_package)
        self.tree.add_command(list_packages)
        self.tree.add_command(check_status)
        await self.tree.sync()

        self.package_checker.start_checking(self)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        for guild in self.guilds:
            channel_id = self.channel_manager.get_channel_id(guild.id)
            if channel_id:
                channel = self.get_channel(channel_id)
                if channel:
                    await channel.send("Bot is online and ready!")

data_manager = DataManager()
bot = MyBot(data_manager)

@discord.app_commands.command(name="set_channel", description="Sets the notification channel for this server.")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    bot.channel_manager.set_channel(interaction.guild.id, channel.id)
    await interaction.response.send_message(f"Notification channel set to {channel.mention}", ephemeral=True)

@discord.app_commands.command(name="add_package", description="Adds a package name to the list.")
async def add_package(interaction: discord.Interaction, package_name: str):
    if bot.package_checker.add_package(interaction.guild.id, package_name):
        await interaction.response.send_message(f"Package name **{package_name}** added.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Package name **{package_name}** is already in the list.", ephemeral=True)

@discord.app_commands.command(name="remove_package", description="Removes a package name from the list.")
async def remove_package(interaction: discord.Interaction, package_name: str):
    if bot.package_checker.remove_package(interaction.guild.id, package_name):
        await interaction.response.send_message(f"Package name **{package_name}** removed.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Package name **{package_name}** not found in the list.", ephemeral=True)

@discord.app_commands.command(name="list_packages", description="Lists all package names in the list.")
async def list_packages(interaction: discord.Interaction):
    package_list = bot.package_checker.list_packages(interaction.guild.id)
    if package_list:
        await interaction.response.send_message(f"Current package names:\n{package_list}", ephemeral=True)
    else:
        await interaction.response.send_message("No package names in the list.", ephemeral=True)

@discord.app_commands.command(name="check_status", description="Checks the status of all package names in the list.")
async def check_status(interaction: discord.Interaction):
    await bot.package_checker.check_status(interaction)

bot.run(TOKEN)
