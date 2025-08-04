from dataclasses import dataclass


@dataclass
class War:
    id: int
    game_id: int
    aggressor_discord_id: int
    defender_discord_id: int
    end_date_timestamp: float | None
