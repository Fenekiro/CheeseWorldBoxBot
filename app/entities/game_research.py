from dataclasses import dataclass


@dataclass
class GameResearch:
    id: int
    name: str
    minutes_to_complete: int
    required_researches: list[int]
    mutually_exclusive_researches: list[int]
