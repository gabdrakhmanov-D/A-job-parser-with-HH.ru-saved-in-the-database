class Employers:
    employer_id: int
    name: str
    open_vacancies: str
    url: str

    __slots__ = ('employer_id', 'name', 'open_vacancies', 'url')

    def __init__(self, employer_id, name, open_vacancies, url):
        self.employer_id = employer_id
        self.name = name
        self.url = url
        self.open_vacancies = open_vacancies

    @classmethod
    def add_employer(cls, employer_dict: dict):
        """Метод для создания объектов класса из словаря"""
        return cls(**employer_dict)

    @staticmethod
    def __verify_data(other):
        """Метод для проверки принадлежности объекта к классу int или Employers"""
        if not isinstance(other, (int, Employers)):
            raise TypeError("Сравнивать можно только с типом int или Employers")
        return other if isinstance(other, int) else other.open_vacancies

    def __eq__(self, other):
        open_vacancies = self.__verify_data(other)
        return self.open_vacancies == open_vacancies

    def __gt__(self, other):
        open_vacancies = self.__verify_data(other)
        return self.open_vacancies > open_vacancies

    def __ge__(self, other):
        open_vacancies = self.__verify_data(other)
        return self.open_vacancies >= open_vacancies

    def __lt__(self, other):
        open_vacancies = self.__verify_data(other)
        return self.open_vacancies < open_vacancies

    def __le__(self, other):
        open_vacancies = self.__verify_data(other)
        return self.open_vacancies <= open_vacancies
