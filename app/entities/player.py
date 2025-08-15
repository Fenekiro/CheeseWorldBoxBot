from dataclasses import dataclass
from functools import cached_property


@dataclass
class Player:
    game_id: int
    discord_id: int
    _registration_message_discord_id_str: str  # values are too big for SQLite INT type so TEXT is used instead
    country_name: str
    capital_name: str
    race: str
    culture_name: str
    _is_eliminated_int: int

    @cached_property
    def registration_message_discord_id(self) -> int:
        return int(self._registration_message_discord_id_str)

    @cached_property
    def is_eliminated(self) -> bool:
        return self._is_eliminated_int == 1
