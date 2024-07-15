import json

class DataManager:
    def __init__(self):
        self.channel_settings_file = 'data/channel_settings.json'
        self.guild_package_names_file = 'data/guild_package_names.json'

    def load_json(self, file_name):
        try:
            with open(file_name, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_json(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f)

    def get_channel_settings(self):
        return self.load_json(self.channel_settings_file)

    def save_channel_settings(self, data):
        self.save_json(self.channel_settings_file, data)

    def get_guild_packages(self, guild_id):
        guild_package_names = self.load_json(self.guild_package_names_file)
        return guild_package_names.get(str(guild_id), [])

    def save_guild_packages(self, guild_id, packages):
        guild_package_names = self.load_json(self.guild_package_names_file)
        guild_package_names[str(guild_id)] = packages
        self.save_json(self.guild_package_names_file, guild_package_names)
