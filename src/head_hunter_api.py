import requests

from src.employer_info import EmployerInfo
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

    def get_items(self, end_url:str, params:dict, key_items:bool=True):
        """ Метод для загрузки информации по вакансиям или компаниям """

        url = self.__base_url + end_url

        if not key_items:
            response = requests.get(url, headers=self.__headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise ConnectionError(f"Ошибка запроса: {response.status_code}")

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


    def get_list_employers(self, employer_name:str) -> list[Employers]:
        """ Метод для получения списка работодателей по слову в названии """
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

    def get_employer_info(self, employer_id:int) -> EmployerInfo:
        """ Метод для получения информации о работодателе по ID"""
        params = {}
        employer = self.get_items(f'employers/{employer_id}/', params, False)
        employer_dict = {
            "employer_id": employer["id"],
            "name": employer["name"],
            "employer_url": employer["site_url"],
            "employer_city": employer["area"]["name"],
            "url": employer["alternate_url"]
        }
        return EmployerInfo.add_employer(employer_dict)


    def get_vacancies(self, employer_ids:list, only_with_salary:bool, keyword: str = "python") -> list[Vacancy]:
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
