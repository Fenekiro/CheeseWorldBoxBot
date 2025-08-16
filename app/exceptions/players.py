class PlayerNotFoundError(Exception):
    def __init__(self):
        self.message = "Игрок не был найден в базе данных. Убедитесь, что верно указали ID игры и дискорд ID игрока"
        super().__init__(self.message)


class PlayerIsEliminatedError(Exception):
    def __init__(self):
        self.message = "Это государство уничтожено и потому больше не может участвовать в игре, если его не возродят"
        super().__init__(self.message)


class PlayerAlreadyRegisteredError(Exception):
    def __init__(self):
        self.message = "Вы не можете дважды зарегистрироваться на одну и ту же игру"
        super().__init__(self.message)


class GameRegistrationIsClosedError(Exception):
    def __init__(self):
        self.message = "Вы не можете зарегистрироваться или отменить регистрацию на игру, если регистрация уже закрыта"
        super().__init__(self.message)

