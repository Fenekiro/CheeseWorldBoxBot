class WarCooldownNotFinishedError(Exception):
    def __init__(self):
        self.message = "Вы не можете объявить войну другому государству до окончания 30-минутного кулдауна на войну"
        super().__init__(self.message)


class PlayerWarLimitError(Exception):
    def __init__(self):
        self.message = "Это государство уже состоит в 3 войнах - государство не может участвовать более чем в 3 войнах"
        super().__init__(self.message)


class AlreadyInWarError(Exception):
    def __init__(self):
        self.message = "Вы не можете объявить новую войну до окончания текущей"
        super().__init__(self.message)


class InvalidWarError(Exception):
    def __init__(self):
        self.message = "Этой войны не существует"
        super().__init__(self.message)


class PlayerIsNotEliminatedError(Exception):
    def __init__(self):
        self.message = "Это государство не выбыло из игры и не может быть возрождено"
        super().__init__(self.message)
