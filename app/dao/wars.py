import asyncio
import time

import aiosqlite

from app.dao.sql_settings import connection
from app.entities.player import Player
from app.entities.war import War


class Wars:
    SETUP_QUERY = """
        CREATE TABLE IF NOT EXISTS wars(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            aggressor_discord_id INTEGER,
            defender_discord_id INTEGER,
            end_date_timestamp REAL,
            war_cooldown REAL, 
            war_cooldown_delay REAL 
        )
    """
    INSERT_WAR_QUERY = "INSERT INTO wars(game_id, aggressor_discord_id, defender_discord_id) VALUES (?, ?, ?)"
    FETCH_WAR_QUERY = "SELECT * FROM wars WHERE id = ?"
    SET_WAR_END_TIMESTAMP_QUERY = """
        UPDATE wars
        SET end_date_timestamp = strftime('%s', 'now'), war_cooldown = strftime('%s', 'now') + 1800
        WHERE id = ?
    """
    PAUSE_ALL_WAR_COOLDOWNS_QUERY = """
        UPDATE wars
        SET cooldown_delay = war_cooldown - strftime('%s', 'now'), war_cooldown = null
        WHERE game_id = ? AND strftime('%s', 'now') < war_cooldown
    """
    CONTINUE_ALL_WAR_COOLDOWNS_QUERY = """
        UPDATE wars
        SET war_cooldown = strftime('%s', 'now') + cooldown_delay, cooldown_delay = null
        WHERE game_id = ? AND cooldown_delay IS NOT NULL
    """

    def __init__(self) -> None:
        asyncio.create_task(self.__setup())

    async def insert_war(self, aggressor: Player, defender: Player) -> War:
        cursor: aiosqlite.Cursor = await connection.execute(
            self.INSERT_WAR_QUERY,
            (aggressor.game_id, aggressor.discord_id, defender.discord_id,)
        )
        await connection.commit()

        return War(cursor.lastrowid, aggressor.game_id, aggressor.discord_id, defender.discord_id, None, None, None)

    async def fetch_war(self, war_id: int) -> War | None:
        db_response: aiosqlite.Cursor = await connection.execute(
            self.FETCH_WAR_QUERY,
            (war_id,)
        )

        war_data = await db_response.fetchone()

        if not war_data:
            return
        else:
            return War(*war_data)

    async def finish_war(self, war_id: int) -> None:
        await connection.execute(
            self.SET_WAR_END_TIMESTAMP_QUERY,
            (war_id,)
        )
        await connection.commit()

    async def pause_all_war_cooldowns(self, game_id: int) -> None:
        await connection.execute(
            self.PAUSE_ALL_WAR_COOLDOWNS_QUERY,
            (game_id,)
        )
        await connection.commit()

    async def continue_all_war_cooldowns(self, game_id: int) -> None:
        await connection.execute(
            self.CONTINUE_ALL_WAR_COOLDOWNS_QUERY,
            (game_id,)
        )
        await connection.commit()

    async def __setup(self) -> None:
        await connection.execute(self.SETUP_QUERY)
        await connection.commit()
