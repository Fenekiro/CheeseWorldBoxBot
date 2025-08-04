from app.entities.player import Player
from app.dao.sql_settings import connection


class Players:
    FETCH_ALL_PLAYERS_QUERY = "SELECT * FROM players WHERE game_id = ?"
    FETCH_PLAYER_QUERY = "SELECT * FROM players WHERE game_id = ? AND discord_id = ?"
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
    DELETE_ALL_PLAYERS_QUERY = "DELETE FROM players WHERE game_id = ?"
    DELETE_PLAYER_QUERY = "DELETE FROM players WHERE game_id = ? AND discord_id = ?"
    ELIMINATE_PLAYER_QUERY = "UPDATE players SET is_eliminated = 1 WHERE game_id = ? AND discord_id = ?"
    REVIVE_PLAYER_QUERY = "UPDATE players SET is_eliminated = 0 WHERE game_id = ? AND discord_id = ?"

    async def fetch_all_players(self, game_id: int) -> list[Player]:
        db_response = await connection.execute(
            self.FETCH_ALL_PLAYERS_QUERY,
            (game_id,)
        )