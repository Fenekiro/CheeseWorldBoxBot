from dataclasses import dataclass


@dataclass
class PlayerResearch:
    game_id: int
    player_discord_id: int
    game_research_id: int
    item_count: int
    researching_until_timestamp: float | None
    researching_delay: float | None
    producing_item_until_timestamp: float | None
    production_delay: float | None
