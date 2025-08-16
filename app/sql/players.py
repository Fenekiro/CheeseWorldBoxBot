import asyncio
import aiosqlite

from app.entities.player import Player
from app.sql.sql_settings import connection


class PlayersSql:
    SETUP_QUERY = """
        CREATE TABLE IF NOT EXISTS players (
            game_id INTEGER,
            discord_id INTEGER,
            registration_message_discord_id TEXT, 
            country_name TEXT,
            capital_name TEXT,
            race TEXT,
            culture_name TEXT,
            is_eliminated SMALLINT
        )
    """
    FETCH_ALL_PLAYERS_QUERY = """
        SELECT * FROM players
        WHERE game_id = ?
    """
    FETCH_PLAYER_QUERY = """
        SELECT * FROM players
        WHERE game_id = ? AND discord_id = ?
    """
    INSERT_PLAYER_QUERY = """
        INSERT INTO players (
            game_id,
            discord_id,
            registration_message_discord_id, 
            country_name,
            capital_name,
            race,
            culture_name,
            is_eliminated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    ELIMINATE_PLAYER_QUERY = """
        UPDATE players
        SET is_eliminated = 1
        WHERE game_id = ? AND discord_id = ?
    """
    REVIVE_PLAYER_QUERY = """
        UPDATE players
        SET is_eliminated = 0
        WHERE game_id = ? AND discord_id = ?
    """
    DELETE_ALL_PLAYERS_QUERY = """
        DELETE FROM players 
        WHERE game_id = ?
    """
    DELETE_PLAYER_QUERY = """
        DELETE FROM players
        WHERE game_id = ? AND discord_id = ?
    """

    def __init__(self) -> None:
        asyncio.create_task(self.__setup())

    async def fetch_all_players(self, game_id: int) -> list[Player]:
        db_response: aiosqlite.Cursor = await connection.execute(
            self.FETCH_ALL_PLAYERS_QUERY,
            (game_id,)
        )

        return [Player(*player_data) for player_data in await db_response.fetchall()]

    async def fetch_player(self, game_id: int, player_discord_id: int) -> Player | None:
        db_response: aiosqlite.Cursor = await connection.execute(
            self.FETCH_PLAYER_QUERY,
            (game_id, player_discord_id,)
        )

        player_data = await db_response.fetchone()

        if not player_data:
            return
        else:
            return Player(*player_data)

    async def insert_player(self, player: Player) -> Player:
        await connection.execute(
            self.INSERT_PLAYER_QUERY,
            *player.__dict__.values(),
        )

        return player

    async def eliminate_player(self, player: Player) -> None:
        await connection.execute(
            self.ELIMINATE_PLAYER_QUERY,
            (player.game_id, player.discord_id,)
        )

    async def revive_player(self, player: Player) -> None:
        await connection.execute(
            self.REVIVE_PLAYER_QUERY,
            (player.game_id, player.discord_id,)
        )

    async def delete_all_players(self, game_id: int) -> None:
        await connection.execute(
            self.DELETE_ALL_PLAYERS_QUERY,
            (game_id,)
        )

    async def delete_player(self, player: Player) -> None:
        await connection.execute(
            self.DELETE_PLAYER_QUERY,
            (player.game_id, player.discord_id,)
        )

    async def __setup(self) -> None:
        await connection.execute(self.SETUP_QUERY)
        await connection.commit()
