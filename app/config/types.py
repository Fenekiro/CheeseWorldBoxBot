from dataclasses import dataclass
import ujson


@dataclass
class ConfigData:
    discord: "DiscordConfigData"
    service: "ServiceConfigData"

    def to_json(self) -> str:
        config_dict = {
            "discord": self.discord.__dict__,
            "service": self.service.__dict__
        }

        return ujson.dumps(config_dict, indent=2)


@dataclass
class DiscordConfigData:
    bot_token: str
    commands_channel_id: int
    events_channel_id: int
    registration_for_game_channel_id: int
    admin_ids: list[int]
    debug_channel_id: int
    game_role_id: int


@dataclass
class ServiceConfigData:
    current_game_id: int | None
    game_session_is_open: bool
