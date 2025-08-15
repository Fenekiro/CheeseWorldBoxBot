import asyncio
import time

import aiosqlite
import ujson

from app.dao.sql_settings import connection
from app.entities.game import Game


class Games:
    SETUP_QUERY = """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            start_date_timestamp REAL,
            end_date_timestamp REAL,
            researches TEXT,
            researches_image_link TEXT, 
            winners TEXT,
            image_link TEXT,
            is_open_for_registration SMALLINT,
            is_finished SMALLINT
        )
    """
    FETCH_ALL_GAMES_QUERY = "SELECT * FROM games"
    FETCH_GAME_QUERY = "SELECT * FROM games WHERE id = ?"
    INSERT_NEW_GAME_QUERY = """
        INSERT INTO games(
            name,
            start_date_timestamp,
            end_date_timestamp,
            researches,
            researches_image_link,
            winners,
            image_link,
            is_open_for_registration,
            is_finished
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    TOGGLE_GAME_REGISTRATION_STATUS_QUERY = "UPDATE games SET is_open_for_registration = ? WHERE id = ?"
    FINISH_GAME_QUERY = "UPDATE games SET end_date_timestamp = ?, winners = ?, image_link = ?, is_finished = ? WHERE id = ?"
    DELETE_GAME_QUERY = "DELETE FROM games WHERE id = ?"

    def __init__(self) -> None:
        asyncio.create_task(self.__setup())

    async def fetch_all_games(self) -> list[Game]:
        db_response: aiosqlite.Cursor = await connection.execute(self.FETCH_ALL_GAMES_QUERY)

        return [Game(*game_data) for game_data in await db_response.fetchall()]

    async def fetch_game(self, game_id: int) -> Game | None:
        db_response: aiosqlite.Cursor = await connection.execute(
            self.FETCH_GAME_QUERY,
            (game_id,)
        )

        game_data = await db_response.fetchone()

        if not game_data:
            return
        else:
            return Game(*game_data)

    async def insert_new_game(self, name: str, researches: list[dict], researches_image_link: str) -> Game | None:
        db_response: aiosqlite.Cursor = await connection.execute(
            self.INSERT_NEW_GAME_QUERY,
            (name, time.time(), None, ujson.dumps(researches), researches_image_link, "[]", "", 1, 0,)
        )
        await connection.commit()

        return await self.fetch_game(db_response.lastrowid)

    async def toggle_game_registration_status(self, game_id: int, **kwargs) -> None:
        if kwargs["task"] == "open":
            await connection.execute(
                self.TOGGLE_GAME_REGISTRATION_STATUS_QUERY,
                (1, game_id,)
            )
        elif kwargs["task"] == "close":
            await connection.execute(
                self.TOGGLE_GAME_REGISTRATION_STATUS_QUERY,
                (0, game_id,)
            )

        await connection.commit()

    async def finish_game(self, game_id: int, winners: list[int], image_link: str) -> Game | None:
        await connection.execute(
            self.FINISH_GAME_QUERY,
            (time.time(), ujson.dumps(winners), image_link, 1, game_id,)
        )
        await connection.commit()

        return await self.fetch_game(game_id)

    async def delete_game(self, game_id: int) -> None:
        await connection.execute(
            self.DELETE_GAME_QUERY,
            (game_id,)
        )
        await connection.commit()

    async def __setup(self) -> None:
        await connection.execute(self.SETUP_QUERY)
        await connection.commit()
