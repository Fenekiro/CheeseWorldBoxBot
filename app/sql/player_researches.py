import asyncio
import time
import aiosqlite

from app.sql.sql_settings import connection
from app.entities.game_research import GameResearch
from app.entities.player import Player
from app.entities.player_research import PlayerResearch


class PlayerResearchesSql:
    SETUP_QUERY = """
        CREATE TABLE IF NOT EXISTS player_researches(
            game_id INTEGER,
            player_discord_id INTEGER,
            game_research_id INTEGER,
            item_count INTEGER,
            researching_until_timestamp REAL,
            researching_delay REAL,
            producing_item_until_timestamp REAL,
            production_delay REAL
        )
    """
    FETCH_ALL_PLAYER_RESEARCHES_QUERY = """
        SELECT * FROM player_researches
        WHERE game_id = ?
    """
    FETCH_PLAYER_RESEARCHES_QUERY = """
        SELECT * FROM player_researches
        WHERE game_id = ? AND player_discord_id = ?
    """
    INSERT_PLAYER_RESEARCH_QUERY = """
        INSERT INTO player_researches(
            game_id,
            player_discord_id,
            game_research_id,
            item_count,
            researching_until_timestamp,
            researching_delay,
            producing_item_until_timestamp,
            production_delay
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    REMOVE_PLAYER_ONGOING_RESEARCH_QUERY = """
        DELETE FROM player_researches
        WHERE game_id = ? AND player_discord_id = ? AND strftime('%s', 'now') < researching_until_timestamp
    """
    INSERT_PLAYER_ITEM_PRODUCTION_QUERY = """
        UPDATE player_researches
        SET producing_item_until_timestamp = ?
        WHERE game_id = ? AND player_discord_id = ? AND game_research_id = ?
    """
    UPDATE_PLAYER_RESEARCH_ITEM_COUNT_QUERY = """
        UPDATE player_researches
        SET item_count = ?
        WHERE game_id = ? AND player_discord_id = ?
    """
    PAUSE_ALL_PLAYER_ONGOING_RESEARCHES_QUERY = """
        UPDATE player_researches
        SET researching_delay = researching_until_timestamp - strftime('%s', 'now'), researching_until_timestamp = null
        WHERE game_id = ? AND strftime('%s', 'now') < researching_until_timestamp
    """
    CONTINUE_ALL_PLAYER_ONGOING_RESEARCHES_QUERY = """
        UPDATE player_researches
        SET researching_until_timestamp = strftime('%s', 'now') + researching_delay, researching_delay = null
        WHERE game_id = ? AND researching_until_timestamp IS NULL
    """
    PAUSE_ALL_PLAYER_ONGOING_ITEM_PRODUCTIONS_QUERY = """
        UPDATE player_researches
        SET production_delay = producing_item_until_timestamp - strftime('%s', 'now'), producing_item_until_timestamp = null
        WHERE game_id = ? AND strftime('%s', 'now') < producing_item_until_timestamp
    """
    CONTINUE_ALL_PLAYER_ONGOING_ITEM_PRODUCTIONS_QUERY = """
        UPDATE player_researches
        SET producing_item_until_timestamp = strftime('%s', 'now') + production_delay, production_delay = null
        WHERE game_id = ? AND producing_item_until_timestamp IS NULL
    """

    def __init__(self) -> None:
        asyncio.create_task(self.__setup())

    async def fetch_player_researches(self, player: Player) -> list[PlayerResearch]:
        db_response: aiosqlite.Cursor = await connection.execute(
            self.FETCH_PLAYER_RESEARCHES_QUERY,
            (player.game_id, player.discord_id,)
        )

        return [PlayerResearch(*player_research_data) for player_research_data in await db_response.fetchall()]

    async def insert_player_research(self, player: Player, game_research: GameResearch) -> PlayerResearch:
        researching_until_timestamp = time.time() + game_research.minutes_to_complete * 60

        await connection.execute(
            self.INSERT_PLAYER_RESEARCH_QUERY,
            (player.game_id, player.discord_id, game_research.id, 0, researching_until_timestamp, None, None, None,)
        )
        await connection.commit()

        return PlayerResearch(
            player.game_id,
            player.discord_id,
            game_research.id,
            0,
            researching_until_timestamp,
            None,
            None,
            None
        )

    async def remove_player_ongoing_research(self, player: Player) -> None:
        await connection.execute(
            self.REMOVE_PLAYER_ONGOING_RESEARCH_QUERY,
            (player.game_id, player.discord_id,)
        )
        await connection.commit()

    async def insert_player_item_production(self, player: Player, game_research: GameResearch) -> None:
        producing_item_until_timestamp = time.time() + game_research.minutes_to_complete * 60

        await connection.execute(
            self.INSERT_PLAYER_ITEM_PRODUCTION_QUERY,
            (producing_item_until_timestamp, player.game_id, player.discord_id, game_research.id,)
        )
        await connection.commit()

    async def update_player_research_item_count(self, player_research: PlayerResearch, **kwargs) -> None:
        if kwargs["task"] == "reduce":
            await connection.execute(
                self.UPDATE_PLAYER_RESEARCH_ITEM_COUNT_QUERY,
                (player_research.item_count - 1, player_research.game_id, player_research.player_discord_id,)
            )
        elif kwargs["task"] == "produce":
            await connection.execute(
                self.UPDATE_PLAYER_RESEARCH_ITEM_COUNT_QUERY,
                (player_research.item_count + 1, player_research.game_id, player_research.player_discord_id,)
            )

        await connection.commit()

    async def pause_all_player_ongoing_researches(self, game_id: int) -> None:
        await connection.execute(
            self.PAUSE_ALL_PLAYER_ONGOING_RESEARCHES_QUERY,
            (game_id,)
        )
        await connection.commit()

    async def continue_all_player_ongoing_researches(self, game_id: int) -> None:
        await connection.execute(
            self.CONTINUE_ALL_PLAYER_ONGOING_RESEARCHES_QUERY,
            (game_id,)
        )
        await connection.commit()

    async def pause_all_player_ongoing_item_productions(self, game_id: int) -> None:
        await connection.execute(
            self.PAUSE_ALL_PLAYER_ONGOING_ITEM_PRODUCTIONS_QUERY,
            (game_id,)
        )
        await connection.commit()

    async def continue_all_player_ongoing_item_productions(self, game_id: int) -> None:
        await connection.execute(
            self.CONTINUE_ALL_PLAYER_ONGOING_ITEM_PRODUCTIONS_QUERY,
            (game_id,)
        )
        await connection.commit()

    async def __setup(self) -> None:
        await connection.execute(self.SETUP_QUERY)
        await connection.commit()
