class GameNotFoundError(Exception):
    def __init__(self):
        self.message = "Игра не была найдена в базе данных. Убедитесь, что указали верный ID игры"
        super().__init__(self.message)


class GameSessionIsClosedError(Exception):
    def __init__(self):
        self.message = "Игровая сессия уже закрыта. Также после её закрытия нельзя совершать игровые действия"
        super().__init__(self.message)


class GameSessionIsNotClosedError(Exception):
    def __init__(self):
        self.message = "Игровая сессия уже открыта. Также после её открытия нельзя сменить игру"
        super().__init__(self.message)
