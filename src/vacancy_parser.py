from abc import ABC, abstractmethod


class VacancyParser(ABC):
    """Абстрактный класс для создания классов подключающихся к различным API"""

    url: str  # url адрес платформы с которой загружаются данные
    headers: dict  # заголовок запроса
    params: dict  # параметры запроса

    @abstractmethod
    def load_vacancies(self):
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass
