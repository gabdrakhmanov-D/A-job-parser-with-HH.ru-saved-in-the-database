import requests

from src.employers import Employers
from src.vacancies import Vacancy
from src.vacancy_parser import VacancyParser


class HeadHunterAPI(VacancyParser):
    """Класс для получения вакансий и списка работодателей с сайта HH.ru"""

    def __init__(self):
        self.keyword = ""
        self.__base_url = "https://api.hh.ru/"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def get_items(self, end_url:str, params:dict):
        """ Метод для загрузки информации по вакансиям или компаниям """

        url = self.__base_url + end_url
        items = []

        while params["page"] < 20:
            response = requests.get(
                url, headers=self.__headers, params=params            )

            if response.status_code == 200:
                current_vacancies = response.json().get("items", [])
                items.extend(current_vacancies)
                params["page"] += 1
            else:
                raise ConnectionError(f"Ошибка запроса: {response.status_code}")

        return items


    def get_list_employers(self, employer_name):
        list_employers = []
        params = {"text": employer_name,
                  "only_with_vacancies": True,
                  "page": self.__params["page"],
                  "per_page": self.__params["per_page"]}
        employers = self.get_items('employers/', params)

        for employer in employers:
            employer_dict = {
                "id": employer["id"],
                "name": employer["name"],
                "url": employer["alternate_url"],
                "open_vacancies": employer["open_vacancies"]
            }
            list_employers.append(Employers.add_employer(employer_dict))

        return list_employers


    def get_vacancies(self, employer_ids:list, only_with_salary:bool, keyword: str = "") -> list[Vacancy]:
        """ Метод для получения списка словарей вакансий по ключевому слову.
            По умолчанию вакансии загружаются по слову 'python'. """

        self.keyword = keyword
        list_employers_and_vacancies = []
        try:
            for employer_id in employer_ids:
                params = {"employer_id": employer_id,
                          "only_with_salary": only_with_salary,
                          "currency": 'RUR',
                          "page": self.__params["page"],
                          "per_page": self.__params["per_page"],
                          "text": self.keyword
                        }

                list_vacancies = []
                vacancies = self.get_items('vacancies/', params)
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

                list_employers_and_vacancies.append({employer_id: list_vacancies})
            return list_employers_and_vacancies

        except ConnectionError:
            return list_employers_and_vacancies
