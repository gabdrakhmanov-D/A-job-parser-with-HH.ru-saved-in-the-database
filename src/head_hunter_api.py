import requests
from src.vacancies import Vacancy
from src.vacancy_parser import VacancyParser


class HeadHunterAPI(VacancyParser):
    """Класс для получения вакансий с сайта HH.ru"""

    def __init__(self):
        self.keyword = ""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def load_vacancies(self) -> list:
        """Метод для получения списка вакансий с сервера"""
        all_vacancies = []
        self.__params["text"] = self.keyword
        while self.__params["page"] < 20:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )

            if response.status_code == 200:
                current_vacancies = response.json().get("items", [])
                all_vacancies.extend(current_vacancies)
                self.__params["page"] += 1
            else:
                raise ConnectionError(f"Ошибка запроса: {response.status_code}")
        return all_vacancies

    def get_vacancies(self, keyword: str = "python") -> list[Vacancy]:
        """Метод для получения списка словарей вакансий по ключевому слову.
        По умолчанию вакансии загружаются по слову 'python'."""
        list_vacancies = []
        self.keyword = keyword
        try:
            vacancies = self.load_vacancies()
            for vacancy in vacancies:
                vacancy_dict = {
                    "job_title": vacancy.get("name"),
                    "requirements": vacancy["snippet"]["requirement"],
                    "responsibility": vacancy["snippet"]["responsibility"],
                    "salary_from": vacancy["salary"]["from"] if vacancy["salary"] else "-",
                    "salary_to": vacancy["salary"]["to"] if vacancy["salary"] else "-",
                    "job_link": vacancy.get("alternate_url"),
                    "employer_name": vacancy["employer"]["name"],
                    "experience": vacancy["experience"]["name"]

                }

                list_vacancies.append(Vacancy.add_vacancy(vacancy_dict))
            return list_vacancies
        except ConnectionError:
            return list_vacancies

a= HeadHunterAPI()
print(a.load_vacancies())