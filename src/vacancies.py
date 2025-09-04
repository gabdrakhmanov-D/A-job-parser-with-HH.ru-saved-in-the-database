class Vacancy:
    """Класс для создания объектов вакансий"""

    job_title: str  # название вакансии
    job_link: str  # ссылка на вакансию
    salary_from: int  # зарплата от
    salary_to: int
    requirements: str  # требования
    responsibility: str  # обязанности
    employer_name:str # название компании
    experience:str # требуемый опыт

    __slots__ = ("job_title",
                 "job_link",
                 "salary_from",
                 "salary_to",
                 "requirements",
                 "responsibility",
                 "employer_name",
                 "experience")

    def __init__(self,
                 job_title: str,
                 requirements: str,
                 responsibility: str,
                 salary_from: int,
                 salary_to:int,
                 job_link: str,
                 employer_name: str,
                 experience: str
                 ):

        self.job_title = job_title
        self.requirements = requirements
        self.responsibility = responsibility
        self.salary_from = self.__validation_salary(salary_from)
        self.salary_to = self.__validation_salary(salary_to)
        self.employer_name = employer_name
        self.experience = experience
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
        return other if isinstance(other, int) else other.salary_to

    def __eq__(self, other):
        salary = self.__verify_data(other)
        return self.salary_to == salary

    def __gt__(self, other):
        salary = self.__verify_data(other)
        return self.salary_to > salary

    def __ge__(self, other):
        salary = self.__verify_data(other)
        return self.salary_to >= salary

    def __lt__(self, other):
        salary = self.__verify_data(other)
        return self.salary_to < salary

    def __le__(self, other):
        salary = self.__verify_data(other)
        return self.salary_to <= salary

    @classmethod
    def add_vacancy(cls, vacancy_dict: dict):
        """Метод для создания объектов класса из словаря"""
        return cls(**vacancy_dict)
