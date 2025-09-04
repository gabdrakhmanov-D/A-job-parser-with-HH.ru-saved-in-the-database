class Vacancy:
    """Класс для создания объектов вакансий"""

    job_title: str  # название вакансии
    job_link: str  # ссылка на вакансию
    salary: int  # зарплата
    requirements: str  # требования
    responsibility: str  # обязанности
    __slots__ = ("job_title", "job_link", "salary", "requirements", "responsibility")

    def __init__(self,
                 job_title: str,
                 requirements: str,
                 responsibility: str,
                 salary: int,
                 job_link: str):

        self.job_title = job_title
        self.requirements = requirements
        self.responsibility = responsibility
        self.salary = self.__validation_salary(salary)
        self.job_link = job_link

    @staticmethod
    def __validation_salary(salary: int | str | None) -> int:
        """Метод для валидации зарплаты"""
        if not isinstance(salary, int) or not salary:
            return 0
        return salary

    @staticmethod
    def __verify_data(other):
        """Метод для проверки принадлежности объекта к классу int или Vacancy"""
        if not isinstance(other, (int, Vacancy)):
            raise TypeError("Сравнивать можно только с типом int или Vacancy")
        return other if isinstance(other, int) else other.salary

    def __eq__(self, other):
        salary = self.__verify_data(other)
        return self.salary == salary

    def __gt__(self, other):
        salary = self.__verify_data(other)
        return self.salary > salary

    def __ge__(self, other):
        salary = self.__verify_data(other)
        return self.salary >= salary

    def __lt__(self, other):
        salary = self.__verify_data(other)
        return self.salary < salary

    def __le__(self, other):
        salary = self.__verify_data(other)
        return self.salary <= salary

    @classmethod
    def add_vacancy(cls, vacancy_dict: dict):
        """Метод для создания объектов класса из словаря"""
        return cls(**vacancy_dict)
