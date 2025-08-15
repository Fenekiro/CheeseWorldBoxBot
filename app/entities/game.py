from dataclasses import dataclass
from functools import cached_property
import ujson

from app.entities.game_research import GameResearch


@dataclass
class Game:
    id: int
    name: str
    start_date_timestamp: float
    end_date_timestamp: float | None
    _researches_json_str: str
    researches_image_link: str
    _winners_str: str
    image_link: str | None
    _is_open_for_registration_int: int
    _is_finished_int: int

    @cached_property
    def researches(self) -> list[GameResearch]:
        dict_researches: list[dict] = ujson.loads(self._researches_json_str)

        return [
            GameResearch(
                research["id"],
                research["name"],
                research["minutes_to_complete"],
                research["required_researches"],
                research["mutually_exclusive_researches"]
            ) for research in dict_researches
        ]

    @cached_property
    def winners(self) -> list[int]:
        return ujson.loads(self._winners_str)

    @cached_property
    def is_open_for_registration(self) -> bool:
        return self._is_open_for_registration_int == 1

    @cached_property
    def is_finished(self) -> bool:
        return self._is_finished_int == 1
