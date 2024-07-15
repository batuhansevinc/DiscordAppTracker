import discord
from discord.ext import tasks
import requests

class PackageChecker:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def add_package(self, guild_id, package_name):
        guild_packages = self.data_manager.get_guild_packages(guild_id)
        if package_name not in guild_packages:
            guild_packages.append(package_name)
            self.data_manager.save_guild_packages(guild_id, guild_packages)
            return True
        return False

    def remove_package(self, guild_id, package_name):
        guild_packages = self.data_manager.get_guild_packages(guild_id)
        if package_name in guild_packages:
            guild_packages.remove(package_name)
            self.data_manager.save_guild_packages(guild_id, guild_packages)
            return True
        return False

    def list_packages(self, guild_id):
        return "\n".join(self.data_manager.get_guild_packages(guild_id))

    async def check_status(self, interaction):
        guild_id = interaction.guild.id
        guild_packages = self.data_manager.get_guild_packages(guild_id)
        if not guild_packages:
            await interaction.response.send_message("No package names in the list to check.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        for package_name in guild_packages:
            store_url = f"https://play.google.com/store/apps/details?id={package_name}"
            try:
                response = requests.get(store_url)
                if response.status_code == 200:
                    current_status = "Published"
                elif response.status_code == 404:
                    current_status = "In Review or Rejected"
                else:
                    current_status = f"Unexpected status code: {response.status_code}"

                status_message = f"**Package Name:** {package_name}\n**Google Play Store Status:** {current_status}"
                await interaction.followup.send(status_message)
            except Exception as e:
                await interaction.followup.send(f"An unexpected error occurred while checking {package_name}: {e}")

    def start_checking(self, bot):
        @tasks.loop(minutes=5)
        async def check_app_status():
            await bot.wait_until_ready()
            for guild in bot.guilds:
                channel_id = bot.channel_manager.get_channel_id(guild.id)
                if not channel_id:
                    continue

                channel = bot.get_channel(channel_id)
                if not channel:
                    continue

                guild_packages = self.data_manager.get_guild_packages(guild.id)
                if not guild_packages:
                    continue

                updated_packages = guild_packages.copy()
                for package_name in guild_packages:
                    store_url = f"https://play.google.com/store/apps/details?id={package_name}"
                    try:
                        response = requests.get(store_url)
                        if response.status_code == 200:
                            current_status = "Published"
                        elif response.status_code == 404:
                            current_status = "In Review or Rejected"
                        else:
                            current_status = f"Unexpected status code: {response.status_code}"

                        if current_status == "Published":
                            await channel.send(f"**Package Name:** {package_name}\n**Google Play Store Status:** {current_status}")
                            updated_packages.remove(package_name)
                    except Exception as e:
                        await channel.send(f"An unexpected error occurred while checking {package_name}: {e}")

                self.data_manager.save_guild_packages(guild.id, updated_packages)

        check_app_status.start()
