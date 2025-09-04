from config import PATH_TO_DB_INI
from src.create_DB import CreateDB
from src.head_hunter_api import HeadHunterAPI


def user_interaction():
    """Основная функция для запуска приложения"""
    # hh_api = HeadHunterAPI()
    # hh_vacancies = hh_api.get_vacancies()
    # if not hh_vacancies:
    #     print('Не удалось получить вакансии с платформы.')
    #     return None
    # k=0
    # for vacancy in hh_vacancies:
    #     if k==5:
    #         break
    #     print(vacancy.employer_name)
    #     k+=1
    new_db = CreateDB('vacancies')
    new_db.create_new_db()
if __name__ == '__main__':
    user_interaction()
