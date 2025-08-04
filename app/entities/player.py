from dataclasses import dataclass


@dataclass
class Player:
    game_id: int
    discord_id: int
    registration_message_discord_id: str
    country_name: str
    capital_name: str
    race: str
    culture_name: str
    is_eliminated: bool
