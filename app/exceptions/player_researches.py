class AlreadyResearchingError(Exception):
    def __init__(self):
        self.message = "У вас уже есть текущее исследование и до его окончания вы не можете начать новое"
        super().__init__(self.message)


class AlreadyResearchedError(Exception):
    def __init__(self):
        self.message = "Вы уже завершили это исследование и не можете исследовать его повторно"
        super().__init__(self.message)


class MutuallyExclusiveResearchError(Exception):
    def __init__(self):
        self.message = "Вы не можете провести это исследование, поскольку уже провели взаимоисключающее исследование"
        super().__init__(self.message)


class RequiredResearchesNotCompletedError(Exception):
    def __init__(self):
        self.message = "Вы не можете начать данное исследование, поскольку не завершили предшествующие ему исследования"
        super().__init__(self.message)


class ProducingTwoSameItemsAtTheSameTimeError(Exception):
    def __init__(self):
        self.message = "Вы не можете производить две технологии от одного исследования одновременно"
        super().__init__(self.message)


class ProducingTooManyItemsError(Exception):
    def __init__(self):
        self.message = "У вас уже производятся 3 технологии, вы не можете производить больше 3"
        super().__init__(self.message)


class ItemsPerResearchLimitError(Exception):
    def __init__(self):
        self.message = "Вы не можете создать суммарно более 3 единиц технологии от одного исследования"
        super().__init__(self.message)


class ResearchNotFoundInPlayerDataError(Exception):
    def __init__(self):
        self.message = "Данное исследование не было найдено в вашем списке завершённых исследований"
        super().__init__(self.message)


class ResearchNotFinishedError(Exception):
    def __init__(self):
        self.message = "Вы ещё не завершили данное исследование и не можете производить от него технологии"
        super().__init__(self.message)


class ResearchNotFoundError(Exception):
    def __init__(self):
        self.message = "Это исследование не было найдено в базе данных"
        super().__init__(self.message)


# Pretty sure it won't be used; if so then I'll remove it
# class ItemProductionNotFinishedError(Exception):
#     def __init__(self):
#         self.message = "Your item production is not finished yet, you cannot produce another item"
#         super().__init__(self.message)


#
class ItemCountBelowZeroError(Exception):
    def __init__(self):
        self.message = "У вас закончились единицы технологии данного исследования"
        super().__init__(self.message)
