import ujson

from app.config.types import ConfigData, DiscordConfigData, ServiceConfigData

CONFIG_PATH = __file__.replace(r"config.py", "config.json")


class Config:
    def __init__(self, data: ConfigData) -> None:
        self.data: ConfigData = data

    def update_json_file(self) -> None:
        with open(CONFIG_PATH, "w") as file:
            file.write(self.data.to_json())


def get_config() -> Config:
    with open(CONFIG_PATH, "r") as file:
        config_dict: dict = ujson.loads(file.read())
        config_data = ConfigData(
            DiscordConfigData(
                config_dict["discord"]["bot_token"],
                config_dict["discord"]["commands_channel_id"],
                config_dict["discord"]["events_channel_id"],
                config_dict["discord"]["registration_for_game_channel_id"],
                config_dict["discord"]["admin_ids"],
                config_dict["discord"]["debug_channel_id"],
                config_dict["discord"]["game_role_id"]
            ),
            ServiceConfigData(
                config_dict["service"]["current_game_id"],
                config_dict["service"]["game_session_is_open"]
            )
        )

        return Config(config_data)


config = get_config()
