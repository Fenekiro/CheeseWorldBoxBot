from dataclasses import dataclass

from app.entities.game_research import GameResearch


@dataclass
class Game:
    id: int
    name: str
    start_date_timestamp: float
    end_date_timestamp: float | None
    researches: list[GameResearch]
    researches_image_link: str
    winners: list[int]
    image_link: str | None
    is_open_for_registration: bool
    is_finished: bool
