from abc import ABC, abstractmethod


class VacancyParser(ABC):
    """Абстрактный класс для создания классов подключающихся к различным API"""

    url: str  # url адрес платформы с которой загружаются данные
    headers: dict  # заголовок запроса
    params: dict  # параметры запроса

    @abstractmethod
    def get_list_employers(self, employer_name):
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, employer_id: int, only_with_salary: bool):
        pass
