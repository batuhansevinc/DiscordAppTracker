class ChannelManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_channel_id(self, guild_id):
        return self.data_manager.get_channel_settings().get(str(guild_id))

    def set_channel(self, guild_id, channel_id):
        channel_settings = self.data_manager.get_channel_settings()
        channel_settings[str(guild_id)] = channel_id
        self.data_manager.save_channel_settings(channel_settings)
