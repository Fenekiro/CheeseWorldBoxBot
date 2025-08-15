from dataclasses import dataclass

from app.entities.game_research import GameResearch


@dataclass
class PlayerResearch:
    game_research: GameResearch
    item_count: int
    researching_until_timestamp: float
    producing_item_until_timestamp: float | None
